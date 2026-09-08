"""Standards enforcement on a filled cell, before it persists.

00a states its rules as prompt instructions. A prompt instruction is a request; these are
checks. A cell that violates one is recorded with the violation attached rather than
silently accepted, because a wrong cell that looks right is the failure mode the whole
system exists to avoid.

Every function here is pure: text in, violation codes out. No database, no model.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..constants import (
    ARITHMETIC_MARKERS,
    BANNED_FALLBACKS,
    FALLBACK_VOCABULARY,
    NOT_STATED_TYPES,
    POSITIVE_NULL_FINDINGS,
)

DATE_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
MARKDOWN_RE = re.compile(r"(\*\*|__|^#{1,6}\s|^\s*[-*+]\s|^\s*\d+\.\s|`)", re.MULTILINE)
CITATION_RE = re.compile(r"(§+\s*\d|\bSection\s+\d+(\.\d+)*\b|\[\d+\]|\bp\.\s*\d+)")


@dataclass(slots=True)
class Violation:
    code: str
    detail: str


def _normalized(value: str) -> str:
    return value.strip().strip(".").strip()


def is_fallback(value: str) -> bool:
    return _normalized(value).lower() in {f.lower() for f in FALLBACK_VOCABULARY}


def is_positive_null(value: str) -> bool:
    return _normalized(value).lower() in {p.lower() for p in POSITIVE_NULL_FINDINGS}


def validate_cell(
    value: str,
    *,
    native_type: str,
    configured_options: list[str] | None = None,
    column_name: str = "",
) -> list[Violation]:
    """Check one filled cell against the 00a standards. Returns every violation found."""
    violations: list[Violation] = []
    raw = value or ""
    text = _normalized(raw)

    if not text:
        return [
            Violation(
                "CELL_EMPTY",
                "The cell is empty; every cell must state a value or a fallback state.",
            )
        ]

    # --- 00a section 5: banned fallback synonyms ------------------------------------
    lowered = text.lower()
    for banned in BANNED_FALLBACKS:
        if lowered == banned.lower():
            violations.append(
                Violation(
                    "BANNED_FALLBACK",
                    f"{text!r} is a banned synonym; 00a section 5 permits only "
                    f"{', '.join(FALLBACK_VOCABULARY)}.",
                )
            )
            break

    fallback = is_fallback(text)

    # `Not stated` belongs to typed columns only.
    if fallback and lowered == "not stated" and native_type not in NOT_STATED_TYPES:
        violations.append(
            Violation(
                "NOT_STATED_ON_UNTYPED_COLUMN",
                f"`Not stated` is reserved for {', '.join(sorted(NOT_STATED_TYPES))} columns; "
                f"{column_name or 'this column'} is {native_type}.",
            )
        )

    # --- Classify: the answer must be a configured option or a permitted fallback -----
    if native_type == "Classify" and configured_options:
        options_lower = {o.strip().lower() for o in configured_options}
        if lowered not in options_lower and not fallback:
            violations.append(
                Violation(
                    "OPTION_NOT_CONFIGURED",
                    f"{text!r} is not one of the configured options for {column_name or 'this column'}.",
                )
            )
        if len(text.splitlines()) > 1:
            violations.append(
                Violation(
                    "CLASSIFY_MULTILINE",
                    "A Classify cell must contain the option alone, on one line.",
                )
            )

    # --- typed columns ----------------------------------------------------------------
    if native_type == "Date" and not fallback and not DATE_RE.match(text):
        violations.append(
            Violation(
                "DATE_FORMAT",
                f"{text!r} is not `YYYY-MM-DD` or a permitted partial date; 00a requires ISO dates "
                "with partial precision preserved.",
            )
        )

    # --- 00a section 6: markdown organises the prompt, not the cell --------------------
    if native_type != "Verbatim" and MARKDOWN_RE.search(raw):
        violations.append(
            Violation(
                "MARKDOWN_IN_CELL",
                "The cell contains markdown; 00a section 6 does not authorise markdown in a "
                "returned cell.",
            )
        )

    # --- 00a section 7: report, never compute ------------------------------------------
    if any(marker in lowered for marker in ARITHMETIC_MARKERS):
        violations.append(
            Violation(
                "ARITHMETIC_IN_CELL",
                "The cell appears to state a computed figure; 00a section 7 requires every figure "
                "to be reported as stated, with arithmetic done outside the table.",
            )
        )

    # --- reasoning and citations belong in evidence fields, not the cell ---------------
    if (
        not fallback
        and native_type not in {"Verbatim", "Free Response"}
        and CITATION_RE.search(text)
    ):
        violations.append(
            Violation(
                "CITATION_IN_CELL",
                "The cell carries a section or page citation; those belong in the evidence fields.",
            )
        )

    return violations


def validate_verbatim(value: str, sources: list[str]) -> list[Violation]:
    """Confirm a Verbatim cell reproduces text that actually appears in its sources.

    00a: "The entire spot-check design rests on this." A Verbatim column that paraphrases
    is worse than one that returns a fallback, because it reads as quotable.
    """
    text = _normalized(value)
    if not text or is_fallback(text):
        return []
    needle = _collapse(text)
    if any(needle in _collapse(s) for s in sources):
        return []
    return [
        Violation(
            "VERBATIM_NOT_IN_SOURCE",
            "The quoted text does not appear in the documents in this review unit; a Verbatim "
            "column must reproduce source text exactly.",
        )
    ]


def _collapse(s: str) -> str:
    """Whitespace- and quote-insensitive comparison, so line wrapping is not a mismatch."""
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip().lower()
