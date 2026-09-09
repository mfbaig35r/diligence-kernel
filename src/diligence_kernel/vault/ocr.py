"""Reading pages that have no text layer.

A recorded deed, a stamped filing, an old lease exhibit: a real data room is full of them,
and without OCR they are invisible to every table.

**What OCR text is.** It is a transcription, not the document. Two consequences the rest of
the system has to respect:

- A Verbatim column checked against OCR text is checking one reading against another, not
  against the page. That is worth doing — it still catches paraphrase — but it does not
  prove the words are the document's, so a cell drawn from OCR is marked.
- The two engines fail differently. Tesseract garbles, which is visible. A vision model
  produces fluent plausible text, which is not. That asymmetry is why tesseract is the
  default for legal work even though a vision model reads harder scans.

Nothing here silently substitutes OCR for extraction: a document whose text came from OCR
records that fact, its engine, and its confidence.
"""

from __future__ import annotations

import os
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

#: Below this mean confidence, a transcription is reported as unreliable.
LOW_CONFIDENCE = 0.70
#: A page with fewer extracted characters than this is treated as having no text layer.
TEXT_LAYER_MIN_CHARS = 40
DEFAULT_DPI = 300


@dataclass(slots=True)
class OCRPage:
    page_number: int
    text: str
    confidence: float | None = None


@dataclass(slots=True)
class OCRResult:
    engine: str
    pages: list[OCRPage] = field(default_factory=list)
    error: str | None = None

    @property
    def confidence(self) -> float | None:
        scored = [p.confidence for p in self.pages if p.confidence is not None]
        return sum(scored) / len(scored) if scored else None

    @property
    def text(self) -> str:
        return "\n\n".join(p.text for p in self.pages)

    @property
    def usable(self) -> bool:
        return bool(self.text.strip()) and self.error is None


class OCREngine(ABC):
    name: str

    @abstractmethod
    def available(self) -> tuple[bool, str]:
        """Whether this engine can run here, and why not when it cannot."""

    @abstractmethod
    def transcribe(self, path: Path, page_numbers: list[int], *, dpi: int) -> OCRResult:
        """Read the named pages. Never raises for a page it cannot read."""


class TesseractOCR(OCREngine):
    """Local, free, offline, and deterministic. The default.

    Its errors are garbled characters rather than invented sentences, which is the right
    failure mode when a human will be checking the result against the page.
    """

    name = "tesseract"

    def available(self) -> tuple[bool, str]:
        try:
            import pytesseract  # noqa: F401
        except ImportError:
            return False, "pytesseract is not installed (pip install 'diligence-kernel[ocr]')"
        try:
            import pdf2image  # noqa: F401
        except ImportError:
            return False, "pdf2image is not installed"
        if shutil.which("tesseract") is None:
            return False, "the tesseract binary is not on PATH (brew install tesseract)"
        if shutil.which("pdftoppm") is None:
            return False, "poppler is not on PATH (brew install poppler)"
        return True, ""

    def transcribe(self, path: Path, page_numbers: list[int], *, dpi: int) -> OCRResult:
        import pdf2image
        import pytesseract

        result = OCRResult(engine=self.name)
        for number in page_numbers:
            try:
                images = pdf2image.convert_from_path(
                    str(path), dpi=dpi, first_page=number, last_page=number
                )
                if not images:
                    continue
                data = pytesseract.image_to_data(images[0], output_type=pytesseract.Output.DICT)
                text = pytesseract.image_to_string(images[0])
                scores = [
                    int(c)
                    for c, w in zip(data["conf"], data["text"], strict=False)
                    if str(c).lstrip("-").isdigit() and int(c) >= 0 and w.strip()
                ]
                confidence = (sum(scores) / len(scores) / 100) if scores else None
                result.pages.append(OCRPage(number, text, confidence))
            except Exception as exc:
                result.error = str(exc)[:300]
                break
        return result


class VisionOCR(OCREngine):
    """A vision model reads the page. Better on hard scans; opt in deliberately.

    It transcribes fluently, which means a misreading looks like ordinary text rather than
    like an error. Documents also leave the machine. Both are why it is not the default.
    """

    name = "vision"

    def __init__(self, model: str | None = None, client: object | None = None) -> None:
        self.model = model or os.environ.get("DILIGENCE_KERNEL_OCR_MODEL", "gpt-5-mini")
        self._client = client

    def available(self) -> tuple[bool, str]:
        try:
            import pdf2image  # noqa: F401
        except ImportError:
            return False, "pdf2image is not installed"
        try:
            import openai  # noqa: F401
        except ImportError:
            return False, "the openai SDK is not installed"
        if shutil.which("pdftoppm") is None:
            return False, "poppler is not on PATH (brew install poppler)"
        return True, ""

    PROMPT = (
        "Transcribe all text from this scanned page exactly as printed. Preserve line and "
        "paragraph breaks. Do not summarize, interpret, paraphrase, correct, or complete "
        "anything. Where a word is illegible write [illegible]. Return only the transcription."
    )

    def transcribe(self, path: Path, page_numbers: list[int], *, dpi: int) -> OCRResult:
        import base64
        import io

        import pdf2image

        if self._client is None:
            import openai

            self._client = openai.OpenAI()

        result = OCRResult(engine=self.name)
        for number in page_numbers:
            try:
                images = pdf2image.convert_from_path(
                    str(path), dpi=dpi, first_page=number, last_page=number
                )
                if not images:
                    continue
                buf = io.BytesIO()
                images[0].save(buf, format="PNG")
                encoded = base64.b64encode(buf.getvalue()).decode()
                response = self._client.responses.create(
                    model=self.model,
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "input_text", "text": self.PROMPT},
                                {
                                    "type": "input_image",
                                    "image_url": f"data:image/png;base64,{encoded}",
                                },
                            ],
                        }
                    ],
                )
                # A vision model reports no confidence; the absence is recorded honestly.
                result.pages.append(OCRPage(number, response.output_text or "", None))
            except Exception as exc:
                result.error = str(exc)[:300]
                break
        return result


ENGINES: dict[str, type[OCREngine]] = {"tesseract": TesseractOCR, "vision": VisionOCR}
DEFAULT_ORDER = ("tesseract",)


def configured_mode() -> str:
    """`auto` (default), `tesseract`, `vision`, or `off`."""
    return (os.environ.get("DILIGENCE_KERNEL_OCR") or "auto").strip().lower()


def configured_dpi() -> int:
    raw = os.environ.get("DILIGENCE_KERNEL_OCR_DPI")
    try:
        return max(72, int(raw)) if raw else DEFAULT_DPI
    except ValueError:
        return DEFAULT_DPI


def select_engine(mode: str | None = None) -> tuple[OCREngine | None, str]:
    """Pick an engine, or explain why there is none."""
    mode = (mode or configured_mode()).lower()
    if mode == "off":
        return None, "OCR is off (DILIGENCE_KERNEL_OCR=off)"
    names = DEFAULT_ORDER if mode == "auto" else (mode,)
    reasons: list[str] = []
    for name in names:
        cls = ENGINES.get(name)
        if cls is None:
            reasons.append(f"{name!r} is not a known OCR engine")
            continue
        engine = cls()
        ok, why = engine.available()
        if ok:
            return engine, ""
        reasons.append(f"{name}: {why}")
    return None, "; ".join(reasons)


def pages_needing_ocr(page_texts: list[str]) -> list[int]:
    """1-indexed pages whose extracted text is too thin to be a text layer."""
    return [
        number
        for number, text in enumerate(page_texts, start=1)
        if len((text or "").strip()) < TEXT_LAYER_MIN_CHARS
    ]
