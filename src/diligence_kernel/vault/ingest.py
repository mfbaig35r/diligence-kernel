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
from typing import Any

from ..db import now
from ..findings import Finding

#: Extensions distillcore can extract without optional extras installed.
ALWAYS_AVAILABLE = {".txt", ".md", ".csv", ".json"}
OPTIONAL = {
    ".pdf": "distillcore[pdf]",
    ".docx": "distillcore[docx]",
    ".html": "distillcore[html]",
    ".htm": "distillcore[html]",
    ".xlsx": "distillcore[excel]",
}
SUPPORTED = ALWAYS_AVAILABLE | set(OPTIONAL)


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


def page_boundaries(pages: Iterable[Any]) -> list[tuple[int, int, int]]:
    """(page_number, char_start, char_end) for each page, as distillcore joins them."""
    out: list[tuple[int, int, int]] = []
    cursor = 0
    for page in pages:
        text = getattr(page, "text", "") or ""
        number = getattr(page, "page_number", len(out) + 1)
        out.append((number, cursor, cursor + len(text)))
        cursor += len(text) + 2  # distillcore joins pages with a blank line
    return out


def pages_for_span(bounds: list[tuple[int, int, int]], start: int, end: int) -> tuple[int | None, int | None]:
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
) -> tuple[dict[str, int], list[Finding]]:
    """Ingest every supported file under `root` into the vault."""
    from distillcore import chunk as dc_chunk
    from distillcore.extractors import extract as dc_extract

    counts = {"ingested": 0, "unchanged": 0, "failed": 0, "unsupported": 0, "chunks": 0}
    findings: list[Finding] = []

    paths = sorted(p for p in (root.rglob("*") if recursive else root.glob("*")) if p.is_file())
    for path in paths:
        suffix = path.suffix.lower()
        if suffix not in SUPPORTED:
            counts["unsupported"] += 1
            continue

        digest = sha256_file(path)
        existing = conn.execute(
            "SELECT id, sha256, extract_status FROM document WHERE source_path = ?", (str(path),)
        ).fetchone()
        if existing and existing["sha256"] == digest and existing["extract_status"] == "extracted" and not force:
            counts["unchanged"] += 1
            continue
        if existing:
            conn.execute("DELETE FROM document WHERE id = ?", (existing["id"],))

        try:
            result = dc_extract(path)
        except Exception as exc:
            counts["failed"] += 1
            conn.execute(
                """INSERT INTO document
                   (source_path, filename, sha256, bytes, extract_status, extract_error, ingested_at)
                   VALUES (?,?,?,?,'failed',?,?)""",
                (str(path), path.name, digest, path.stat().st_size, str(exc)[:500], now()),
            )
            hint = OPTIONAL.get(suffix)
            findings.append(Finding(
                code="EXTRACT_FAILED", subject_type="document", subject_id=None,
                subject_name=path.name,
                observation=f"The file could not be extracted: {exc}",
                evidence={"path": str(path)} | ({"install": hint} if hint else {}),
            ))
            continue

        full_text = result.full_text or ""
        cur = conn.execute(
            """INSERT INTO document
               (source_path, filename, sha256, bytes, page_count, full_text,
                extract_status, ingested_at)
               VALUES (?,?,?,?,?,?, 'extracted', ?)""",
            (str(path), path.name, digest, path.stat().st_size,
             result.page_count, full_text, now()),
        )
        doc_id = int(cur.lastrowid)
        counts["ingested"] += 1

        if not full_text.strip():
            findings.append(Finding(
                code="DOCUMENT_EMPTY", subject_type="document", subject_id=doc_id,
                subject_name=path.name,
                observation="The file extracted to no text; it may be a scan needing OCR.",
                evidence={"path": str(path), "page_count": result.page_count},
            ))
            continue

        pieces = dc_chunk(
            full_text, strategy="paragraph", target_tokens=target_tokens,
            max_tokens=max_tokens, overlap_tokens=overlap_tokens,
        )
        spans = locate_chunks(full_text, pieces)
        bounds = page_boundaries(result.pages or [])
        vectors: list[list[float]] = []
        if embedder is not None and pieces:
            try:
                vectors = embedder(pieces)
            except Exception as exc:
                findings.append(Finding(
                    code="EMBEDDING_FAILED", subject_type="document", subject_id=doc_id,
                    subject_name=path.name,
                    observation=f"Chunks were stored without embeddings: {exc}",
                    evidence={"path": str(path)},
                ))

        for i, (piece, (start, end)) in enumerate(zip(pieces, spans, strict=False)):
            p_start, p_end = pages_for_span(bounds, start, end)
            vec = vectors[i] if i < len(vectors) else None
            conn.execute(
                """INSERT INTO chunk
                   (document_id, chunk_index, text, char_start, char_end, page_start, page_end,
                    token_estimate, embedding, embedding_dim)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (doc_id, i, piece, start, end, p_start, p_end,
                 max(1, len(piece) // 4),
                 pack_embedding(vec) if vec else None, len(vec) if vec else None),
            )
        counts["chunks"] += len(pieces)

    conn.commit()
    return counts, findings
