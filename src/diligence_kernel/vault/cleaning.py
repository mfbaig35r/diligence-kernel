"""Removing what a page has but a document does not.

Every legal PDF carries a running header and footer. A PDF extractor emits them in reading
order, so they land in the middle of the text — and a clause that spans a page break comes
out with `Confidential Page 1 of 3` wedged into the middle of a sentence.

That breaks three things at once: the Verbatim check rejects a correct quotation, retrieval
scores a passage on boilerplate, and the model reads a sentence interrupted by noise. So the
running lines are removed before anything else sees the text.

Only lines that actually repeat across pages are removed. A one-page document is left
untouched, because nothing can be shown to repeat.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

#: How many lines at each end of a page can be a running header or footer.
BAND = 3
#: A line must appear in at least this share of pages to count as running.
THRESHOLD = 0.6

_DIGITS = re.compile(r"\d+")
_WS = re.compile(r"\s+")


@dataclass(slots=True)
class CleanResult:
    pages: list[str]
    full_text: str
    lines_removed: int
    patterns: list[str]


def _signature(line: str) -> str:
    """Compare lines ignoring page numbers, so `Page 1 of 3` matches `Page 2 of 3`."""
    return _DIGITS.sub("#", _WS.sub(" ", line).strip().casefold())


def strip_running_lines(pages: list[str]) -> CleanResult:
    """Drop repeated head and foot lines from every page, and rebuild the full text."""
    if len(pages) < 2:
        text = pages[0] if pages else ""
        return CleanResult(pages=list(pages), full_text=text, lines_removed=0, patterns=[])

    split = [p.splitlines() for p in pages]
    needed = max(2, math.ceil(THRESHOLD * len(pages)))

    counts: dict[tuple[str, str], set[int]] = {}
    for index, lines in enumerate(split):
        for line in lines[:BAND]:
            if line.strip():
                counts.setdefault(("head", _signature(line)), set()).add(index)
        for line in lines[-BAND:]:
            if line.strip():
                counts.setdefault(("foot", _signature(line)), set()).add(index)

    running = {key for key, seen in counts.items() if len(seen) >= needed}
    if not running:
        return CleanResult(
            pages=list(pages), full_text="\n\n".join(pages), lines_removed=0, patterns=[]
        )

    removed = 0
    cleaned: list[str] = []
    for lines in split:
        keep: list[str] = []
        last = len(lines) - 1
        for position, line in enumerate(lines):
            band = "head" if position < BAND else ("foot" if position > last - BAND else None)
            if band and (band, _signature(line)) in running:
                removed += 1
                continue
            keep.append(line)
        cleaned.append("\n".join(keep).strip("\n"))

    return CleanResult(
        pages=cleaned,
        full_text="\n\n".join(cleaned),
        lines_removed=removed,
        patterns=sorted({sig for _, sig in running}),
    )
