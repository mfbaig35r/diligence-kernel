"""Evidence retrieval over the vault.

Two paths, because two kinds of column need different things:

- **Chunk retrieval** for classification and extraction columns: FTS5 keyword matching,
  optionally fused with cosine similarity over stored embeddings.
- **Whole-unit context** for Verbatim columns and for small review units: the documents go
  in intact, because a clause split across a chunk boundary cannot be quoted exactly, and
  00a says the entire spot-check design rests on Verbatim returning true source text.

Retrieval is always scoped to a review unit. A cell may never see a document outside its
own unit: 00a's shared rule is "analyze only the documents in the current review unit".
"""

from __future__ import annotations

import math
import re
import sqlite3
from dataclasses import dataclass

from .ingest import unpack_embedding

FTS_SAFE_RE = re.compile(r"[^\w\s]+")
STOPWORDS = frozenset(
    [
        "the",
        "a",
        "an",
        "and",
        "or",
        "of",
        "to",
        "in",
        "for",
        "on",
        "with",
        "is",
        "are",
        "be",
        "as",
        "by",
        "at",
        "from",
        "that",
        "this",
        "it",
        "its",
        "any",
        "all",
        "each",
        "every",
        "not",
        "no",
        "if",
        "then",
        "than",
        "which",
        "who",
        "whom",
        "whose",
        "what",
        "when",
        "where",
    ]
)


@dataclass(slots=True)
class Passage:
    chunk_id: int
    document_id: int
    filename: str
    text: str
    char_start: int
    char_end: int
    page_start: int | None
    page_end: int | None
    score: float

    def to_dict(self) -> dict[str, object]:
        return {
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "filename": self.filename,
            "text": self.text,
            "char_start": self.char_start,
            "char_end": self.char_end,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "score": round(self.score, 4),
        }


def unit_document_ids(conn: sqlite3.Connection, unit_id: int) -> list[int]:
    return [
        int(r["document_id"])
        for r in conn.execute(
            "SELECT document_id FROM unit_document WHERE unit_id = ? ORDER BY document_id",
            (unit_id,),
        )
    ]


def fts_query(text: str, *, limit_terms: int = 24) -> str:
    """Turn prompt text into an FTS5 OR query, dropping punctuation and stopwords."""
    cleaned = FTS_SAFE_RE.sub(" ", text.lower())
    seen: dict[str, None] = {}
    for word in cleaned.split():
        if len(word) < 3 or word in STOPWORDS or word.isdigit():
            continue
        seen.setdefault(word, None)
        if len(seen) >= limit_terms:
            break
    return " OR ".join(f'"{w}"' for w in seen)


def _cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


def search_unit(
    conn: sqlite3.Connection,
    unit_id: int,
    query: str,
    *,
    limit: int = 12,
    query_vector: list[float] | None = None,
) -> list[Passage]:
    """Retrieve the passages in a review unit most likely to answer `query`.

    Keyword and vector scores are fused by reciprocal rank, which needs no calibration
    between two scales that are not comparable.
    """
    doc_ids = unit_document_ids(conn, unit_id)
    if not doc_ids:
        return []
    placeholders = ",".join("?" * len(doc_ids))

    keyword_rank: dict[int, int] = {}
    expr = fts_query(query)
    if expr:
        rows = conn.execute(
            f"""SELECT c.id FROM chunk_fts f
                JOIN chunk c ON c.id = f.rowid
                WHERE chunk_fts MATCH ? AND c.document_id IN ({placeholders})
                ORDER BY bm25(chunk_fts) LIMIT ?""",
            (expr, *doc_ids, limit * 4),
        ).fetchall()
        for rank, row in enumerate(rows):
            keyword_rank[int(row["id"])] = rank

    vector_rank: dict[int, int] = {}
    if query_vector:
        scored: list[tuple[float, int]] = []
        for row in conn.execute(
            f"SELECT id, embedding FROM chunk WHERE document_id IN ({placeholders}) AND embedding IS NOT NULL",
            doc_ids,
        ):
            scored.append(
                (_cosine(query_vector, unpack_embedding(row["embedding"])), int(row["id"]))
            )
        scored.sort(reverse=True)
        for rank, (_, cid) in enumerate(scored[: limit * 4]):
            vector_rank[cid] = rank

    fused: dict[int, float] = {}
    for cid, rank in keyword_rank.items():
        fused[cid] = fused.get(cid, 0.0) + 1.0 / (60 + rank)
    for cid, rank in vector_rank.items():
        fused[cid] = fused.get(cid, 0.0) + 1.0 / (60 + rank)

    if not fused:  # nothing matched; fall back to the unit's opening passages
        return unit_passages(conn, unit_id, limit=limit)

    top = sorted(fused.items(), key=lambda kv: kv[1], reverse=True)[:limit]
    ids = [cid for cid, _ in top]
    by_id = _load_passages(conn, ids)
    out = []
    for cid, score in top:
        if (p := by_id.get(cid)) is not None:
            p.score = score
            out.append(p)
    return out


def unit_passages(conn: sqlite3.Connection, unit_id: int, *, limit: int = 12) -> list[Passage]:
    """The unit's passages in document order, for when retrieval finds nothing to rank."""
    doc_ids = unit_document_ids(conn, unit_id)
    if not doc_ids:
        return []
    placeholders = ",".join("?" * len(doc_ids))
    rows = conn.execute(
        f"""SELECT c.id, c.document_id, d.filename, c.text, c.char_start, c.char_end,
                   c.page_start, c.page_end
            FROM chunk c JOIN document d ON d.id = c.document_id
            WHERE c.document_id IN ({placeholders})
            ORDER BY c.document_id, c.chunk_index LIMIT ?""",
        (*doc_ids, limit),
    ).fetchall()
    return [_row_to_passage(r, 0.0) for r in rows]


def unit_full_text(
    conn: sqlite3.Connection, unit_id: int, *, max_chars: int = 400_000
) -> list[dict[str, object]]:
    """Every document in the unit, whole, in date order where a date is known.

    This is the Verbatim path and the small-unit path. Truncation is reported rather than
    silent, because a Verbatim answer drawn from a truncated document is not verifiable.
    """
    rows = conn.execute(
        """SELECT d.id, d.filename, d.full_text, d.page_count,
                  COALESCE(cl.document_date, '') AS document_date, ud.role
           FROM unit_document ud
           JOIN document d ON d.id = ud.document_id
           LEFT JOIN classification cl ON cl.document_id = d.id
           WHERE ud.unit_id = ?
           ORDER BY document_date, d.filename""",
        (unit_id,),
    ).fetchall()
    out: list[dict[str, object]] = []
    budget = max_chars
    for row in rows:
        text = row["full_text"] or ""
        truncated = len(text) > budget
        if truncated:
            text = text[: max(0, budget)]
        budget -= len(text)
        out.append(
            {
                "document_id": int(row["id"]),
                "filename": row["filename"],
                "role": row["role"],
                "document_date": row["document_date"] or None,
                "text": text,
                "truncated": truncated,
            }
        )
        if budget <= 0:
            break
    return out


def _load_passages(conn: sqlite3.Connection, ids: list[int]) -> dict[int, Passage]:
    if not ids:
        return {}
    placeholders = ",".join("?" * len(ids))
    rows = conn.execute(
        f"""SELECT c.id, c.document_id, d.filename, c.text, c.char_start, c.char_end,
                   c.page_start, c.page_end
            FROM chunk c JOIN document d ON d.id = c.document_id
            WHERE c.id IN ({placeholders})""",
        ids,
    ).fetchall()
    return {int(r["id"]): _row_to_passage(r, 0.0) for r in rows}


def _row_to_passage(row: sqlite3.Row, score: float) -> Passage:
    return Passage(
        chunk_id=int(row["id"]),
        document_id=int(row["document_id"]),
        filename=row["filename"],
        text=row["text"],
        char_start=row["char_start"] or 0,
        char_end=row["char_end"] or 0,
        page_start=row["page_start"],
        page_end=row["page_end"],
        score=score,
    )
