"""Data-room ingestion: extract, chunk, locate, embed, store.

distillcore does the extraction and chunking. What it does not do, and what legal evidence
needs, is offsets: a cell that quotes a document must be able to point at the exact
characters and page it came from. So every chunk is located back into the full text and
given a char span and a page range.

Ingestion is idempotent by content hash: re-ingesting an unchanged file is a no-op.
"""

from __future__ import annotations

import hashlib
import sqlite3
import struct
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path

from ..db import now
from ..findings import Finding
from . import ocr as ocr_mod
from . import tabular
from .cleaning import strip_running_lines

#: Read as prose: extracted, cleaned, chunked by paragraph.
PROSE_SUFFIXES = frozenset({".txt", ".md", ".pdf", ".docx", ".html", ".htm"})
#: Read as tables: chunked by rows, header repeated. See `tabular.py`.
TABULAR_SUFFIXES = tabular.TABULAR_SUFFIXES
SUPPORTED = PROSE_SUFFIXES | TABULAR_SUFFIXES

#: File types a data room contains that this vault cannot read yet. They are reported
#: rather than skipped in silence: a produced document nobody can see is exactly what the
#: coverage register exists to catch, and an unread file must not look like an absent one.
KNOWN_UNREADABLE: dict[str, str] = {
    ".xls": "the legacy Excel format; re-save it as .xlsx",
    ".doc": "the legacy Word format; re-save it as .docx",
    ".ppt": "PowerPoint is not supported",
    ".pptx": "PowerPoint is not supported",
    ".msg": "Outlook mail is not supported; export the message as .pdf or .txt",
    ".eml": "email is not supported; export the message as .pdf or .txt",
    ".rtf": "RTF is not supported; re-save it as .docx",
    ".zip": "archives are not opened; expand it into the data room first",
    ".7z": "archives are not opened; expand it into the data room first",
    ".rar": "archives are not opened; expand it into the data room first",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def pack_embedding(vector: Sequence[float]) -> bytes:
    return struct.pack(f"<{len(vector)}f", *vector)


def unpack_embedding(blob: bytes | None) -> list[float]:
    if not blob:
        return []
    return list(struct.unpack(f"<{len(blob) // 4}f", blob))


def locate_chunks(full_text: str, chunks: list[str]) -> list[tuple[int, int]]:
    """Find each chunk's character span in the full text.

    Chunks are contiguous slices in order, possibly overlapping, so the search advances a
    cursor and only falls back to a global search when a chunk cannot be found ahead of it
    (which happens when a chunker normalises whitespace).
    """
    spans: list[tuple[int, int]] = []
    cursor = 0
    for piece in chunks:
        probe = piece.strip()
        if not probe:
            spans.append((cursor, cursor))
            continue
        idx = full_text.find(probe, cursor)
        if idx == -1:
            idx = full_text.find(probe)
        if idx == -1:
            head = probe[:80]
            idx = full_text.find(head, cursor)
            if idx == -1:
                idx = full_text.find(head)
        if idx == -1:
            spans.append((cursor, min(cursor + len(probe), len(full_text))))
            continue
        end = idx + len(probe)
        spans.append((idx, end))
        cursor = max(cursor, idx + max(1, len(probe) // 2))
    return spans


def page_boundaries_from_text(pages: Iterable[str]) -> list[tuple[int, int, int]]:
    """(page_number, char_start, char_end) for pages joined by a blank line.

    The full text is rebuilt from these same strings, so the offsets are exact by
    construction rather than by agreement with the extractor.
    """
    out: list[tuple[int, int, int]] = []
    cursor = 0
    for number, text in enumerate(pages, start=1):
        out.append((number, cursor, cursor + len(text)))
        cursor += len(text) + 2  # pages are joined with "\n\n"
    return out


def pages_for_span(
    bounds: list[tuple[int, int, int]], start: int, end: int
) -> tuple[int | None, int | None]:
    hits = [num for num, s, e in bounds if start < e and end > s]
    return (min(hits), max(hits)) if hits else (None, None)


def ingest_path(
    conn: sqlite3.Connection,
    root: Path,
    *,
    recursive: bool = True,
    embedder: Callable[[list[str]], list[list[float]]] | None = None,
    target_tokens: int = 500,
    max_tokens: int = 1000,
    overlap_tokens: int = 50,
    force: bool = False,
    ocr: str | None = None,
) -> tuple[dict[str, int], list[Finding]]:
    """Ingest every supported file under `root` into the vault."""
    from distillcore import chunk as dc_chunk
    from distillcore.extractors import extract as dc_extract

    counts = {
        "ingested": 0,
        "unchanged": 0,
        "failed": 0,
        "unsupported": 0,
        "chunks": 0,
        "header_lines_removed": 0,
        "ocred": 0,
    }
    findings: list[Finding] = []

    paths = sorted(p for p in (root.rglob("*") if recursive else root.glob("*")) if p.is_file())
    for path in paths:
        suffix = path.suffix.lower()
        if suffix not in SUPPORTED:
            counts["unsupported"] += 1
            if (reason := KNOWN_UNREADABLE.get(suffix)) is not None:
                findings.append(
                    Finding(
                        code="DOCUMENT_FORMAT_UNREADABLE",
                        subject_type="document",
                        subject_id=None,
                        subject_name=path.name,
                        observation=f"The file was produced but cannot be read: {reason}.",
                        evidence={"path": str(path), "suffix": suffix},
                    )
                )
            continue

        digest = sha256_file(path)
        existing = conn.execute(
            "SELECT id, sha256, extract_status FROM document WHERE source_path = ?", (str(path),)
        ).fetchone()
        if (
            existing
            and existing["sha256"] == digest
            and existing["extract_status"] == "extracted"
            and not force
        ):
            counts["unchanged"] += 1
            continue
        if existing:
            conn.execute("DELETE FROM document WHERE id = ?", (existing["id"],))

        is_tabular = suffix in TABULAR_SUFFIXES
        try:
            if is_tabular:
                sheets = tabular.read_sheets(path)
                result = None
            else:
                result = dc_extract(path)
        except Exception as exc:
            counts["failed"] += 1
            conn.execute(
                """INSERT INTO document
                   (source_path, filename, sha256, bytes, extract_status, extract_error, ingested_at)
                   VALUES (?,?,?,?,'failed',?,?)""",
                (str(path), path.name, digest, path.stat().st_size, str(exc)[:500], now()),
            )
            findings.append(
                Finding(
                    code="EXTRACT_FAILED",
                    subject_type="document",
                    subject_id=None,
                    subject_name=path.name,
                    observation=f"The file could not be extracted: {exc}",
                    evidence={"path": str(path), "suffix": suffix},
                )
            )
            continue

        # A spreadsheet is chunked by rows with its header repeated, not by paragraph.
        # `tabular.render` builds the stored text and the chunks together, so each chunk is
        # an exact slice and offsets need no searching.
        if is_tabular:
            full_text, prechunked = tabular.render(sheets)
            page_count = len(sheets)
            doc_id = _insert_document(
                conn, path, digest, page_count, full_text, "extracted", None, None
            )
            counts["ingested"] += 1
            # Report what the workbook holds before deciding whether it holds anything, so
            # an empty sheet is named rather than lost behind a single DOCUMENT_EMPTY.
            findings.extend(_sheet_findings(doc_id, path, sheets))
            if not full_text.strip():
                findings.append(
                    Finding(
                        code="DOCUMENT_EMPTY",
                        subject_type="document",
                        subject_id=doc_id,
                        subject_name=path.name,
                        observation="The workbook holds no rows and no table can see it.",
                        evidence={"path": str(path)},
                    )
                )
                continue
            spans = tabular.spans_for(full_text, prechunked)
            _insert_chunks(conn, doc_id, prechunked, spans, [], embedder, findings, path)
            counts["chunks"] += len(prechunked)
            continue

        # Remove running headers and footers before anything reads the text. They land
        # mid-sentence at every page break, and everything downstream suffers for it.
        page_texts = [p.text for p in (result.pages or [])]

        # A page with no text layer is a scan. OCR reads it, and the document records that
        # its text is a transcription rather than the document's own.
        text_source, engine_name, confidence = "extracted", None, None
        needs = ocr_mod.pages_needing_ocr(page_texts) if suffix == ".pdf" else []
        if needs:
            engine, why = ocr_mod.select_engine(ocr)
            if engine is None:
                findings.append(
                    Finding(
                        code="OCR_UNAVAILABLE",
                        subject_type="document",
                        subject_id=None,
                        subject_name=path.name,
                        observation=(
                            f"{len(needs)} of {len(page_texts) or 1} pages have no text layer and "
                            f"could not be read: {why}."
                        ),
                        evidence={"path": str(path), "pages": needs},
                    )
                )
            else:
                transcribed = engine.transcribe(path, needs, dpi=ocr_mod.configured_dpi())
                if transcribed.usable:
                    by_page = {p.page_number: p.text for p in transcribed.pages}
                    page_texts = [
                        by_page.get(n, t) for n, t in enumerate(page_texts or [""], start=1)
                    ] or [transcribed.text]
                    text_source = "ocr"
                    engine_name = transcribed.engine
                    confidence = transcribed.confidence
                    counts["ocred"] += 1
                else:
                    findings.append(
                        Finding(
                            code="OCR_FAILED",
                            subject_type="document",
                            subject_id=None,
                            subject_name=path.name,
                            observation=(
                                "OCR produced no usable text"
                                + (f": {transcribed.error}" if transcribed.error else ".")
                            ),
                            evidence={"path": str(path), "engine": transcribed.engine},
                        )
                    )

        cleaned = strip_running_lines(page_texts)
        full_text = cleaned.full_text if cleaned.pages else (result.full_text or "")
        counts["header_lines_removed"] += cleaned.lines_removed
        doc_id = _insert_document(
            conn,
            path,
            digest,
            result.page_count,
            full_text,
            text_source,
            engine_name,
            confidence,
        )
        counts["ingested"] += 1

        if text_source == "ocr":
            shown = "unreported" if confidence is None else f"{confidence:.0%}"
            findings.append(
                Finding(
                    code="DOCUMENT_OCRED",
                    subject_type="document",
                    subject_id=doc_id,
                    subject_name=path.name,
                    observation=(
                        f"{len(needs)} pages had no text layer and were transcribed by "
                        f"{engine_name} at {shown} mean confidence; the text is a reading of "
                        "the document, not the document."
                    ),
                    evidence={"engine": engine_name, "confidence": confidence, "pages": needs},
                )
            )
            if confidence is not None and confidence < ocr_mod.LOW_CONFIDENCE:
                findings.append(
                    Finding(
                        code="OCR_LOW_CONFIDENCE",
                        subject_type="document",
                        subject_id=doc_id,
                        subject_name=path.name,
                        observation=(
                            f"The transcription averaged {confidence:.0%} confidence, below "
                            f"the {ocr_mod.LOW_CONFIDENCE:.0%} threshold; treat every cell "
                            "drawn from it as unverified."
                        ),
                        evidence={"engine": engine_name, "confidence": confidence},
                    )
                )

        if not full_text.strip():
            findings.append(
                Finding(
                    code="DOCUMENT_EMPTY",
                    subject_type="document",
                    subject_id=doc_id,
                    subject_name=path.name,
                    observation="The file yielded no text and no table can see it.",
                    evidence={"path": str(path), "page_count": result.page_count},
                )
            )
            continue

        pieces = dc_chunk(
            full_text,
            strategy="paragraph",
            target_tokens=target_tokens,
            max_tokens=max_tokens,
            overlap_tokens=overlap_tokens,
        )
        spans = locate_chunks(full_text, pieces)
        bounds = page_boundaries_from_text(cleaned.pages)
        _insert_chunks(conn, doc_id, pieces, spans, bounds, embedder, findings, path)
        counts["chunks"] += len(pieces)

    conn.commit()
    return counts, findings


def _insert_document(
    conn: sqlite3.Connection,
    path: Path,
    digest: str,
    page_count: int | None,
    full_text: str,
    text_source: str,
    engine_name: str | None,
    confidence: float | None,
) -> int:
    cur = conn.execute(
        """INSERT INTO document
           (source_path, filename, sha256, bytes, page_count, full_text,
            extract_status, text_source, ocr_engine, ocr_confidence, ingested_at)
           VALUES (?,?,?,?,?,?, 'extracted', ?,?,?,?)""",
        (
            str(path),
            path.name,
            digest,
            path.stat().st_size,
            page_count,
            full_text,
            text_source,
            engine_name,
            confidence,
            now(),
        ),
    )
    return int(cur.lastrowid)


def _insert_chunks(
    conn: sqlite3.Connection,
    doc_id: int,
    pieces: list[str],
    spans: list[tuple[int, int]],
    bounds: list[tuple[int, int, int]],
    embedder: Callable[[list[str]], list[list[float]]] | None,
    findings: list[Finding],
    path: Path,
) -> None:
    vectors: list[list[float]] = []
    if embedder is not None and pieces:
        try:
            vectors = embedder(pieces)
        except Exception as exc:
            findings.append(
                Finding(
                    code="EMBEDDING_FAILED",
                    subject_type="document",
                    subject_id=doc_id,
                    subject_name=path.name,
                    observation=f"Chunks were stored without embeddings: {exc}",
                    evidence={"path": str(path)},
                )
            )
    for i, (piece, (start, end)) in enumerate(zip(pieces, spans, strict=False)):
        p_start, p_end = pages_for_span(bounds, start, end) if bounds else (None, None)
        vec = vectors[i] if i < len(vectors) else None
        conn.execute(
            """INSERT INTO chunk
               (document_id, chunk_index, text, char_start, char_end, page_start, page_end,
                token_estimate, embedding, embedding_dim)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                doc_id,
                i,
                piece,
                start,
                end,
                p_start,
                p_end,
                max(1, len(piece) // 4),
                pack_embedding(vec) if vec else None,
                len(vec) if vec else None,
            ),
        )


def _sheet_findings(doc_id: int, path: Path, sheets: list[tabular.Sheet]) -> list[Finding]:
    """Report what a workbook holds, and any sheet whose header could not be found.

    A sheet with no header is a grid of unlabelled columns. It is still stored, because a
    produced document must not disappear, but nothing downstream can name its fields.
    """
    out = [
        Finding(
            code="WORKBOOK_READ",
            subject_type="document",
            subject_id=doc_id,
            subject_name=path.name,
            observation=(
                f"{len(sheets)} sheets were read as tables: "
                + "; ".join(f"{s.name} ({s.row_count} rows)" for s in sheets)
                + "."
            ),
            evidence={"sheets": [{"name": s.name, "rows": s.row_count} for s in sheets]},
        )
    ]
    empty = [s.name for s in sheets if not s.rows and not s.header]
    if empty:
        out.append(
            Finding(
                code="SHEET_EMPTY",
                subject_type="document",
                subject_id=doc_id,
                subject_name=path.name,
                observation=f"{', '.join(empty)} holds no rows.",
                evidence={"sheets": empty},
            )
        )
    headerless = [s.name for s in sheets if not s.header and s.rows]
    if headerless:
        out.append(
            Finding(
                code="SHEET_WITHOUT_HEADER",
                subject_type="document",
                subject_id=doc_id,
                subject_name=path.name,
                observation=(
                    f"No header row could be identified in {', '.join(headerless)}; its columns "
                    "are unlabelled and cannot be relied on."
                ),
                evidence={"sheets": headerless},
            )
        )
    return out
