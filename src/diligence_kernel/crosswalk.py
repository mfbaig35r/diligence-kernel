"""Matching playbook fields to corpus columns by meaning rather than shared words.

Term overlap was tried first and is not fit for this. It resolved about 42% of the playbook's
fields while 95% of their distinct terms appear somewhere in the corpus, and hand-checking the
fields it called gaps found the concepts present with columns of their own — `Drag-Along`,
`Anti-Dilution Protection`, `Liquidation Preference`, `Preemptive Rights`. A scorer that
mislabels covered concepts as gaps is worse than none, because a gap report is read as a list
of things to build.

Embeddings compare what a field and a column are *about*. The scores here still propose
candidates for a human to confirm — a crosswalk between two unvalidated syntheses cannot be
authoritative — but the absence signal becomes worth acting on.

Embeddings are cached by content hash, so re-running costs nothing until the text changes.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path  # noqa: F401  (re-exported for tests)

DEFAULT_MODEL = "text-embedding-3-small"
#: Cosine similarity above which a column is a candidate answer for a field. Calibrated in
#: `scripts/crosswalk.py --calibrate` against pairs confirmed by hand.
DEFAULT_THRESHOLD = 0.42
#: A field is treated as answered when its best candidate reaches this. Set below the
#: lowest score observed on a pair confirmed by hand (0.48 — "board composition, quorum and
#: voting requirements" against `02 Governing Body Composition`), so a covered concept is not
#: reported as a gap. Re-derive with `scripts/crosswalk.py --calibrate` if the model changes.
COVERED_AT = 0.45


@dataclass(slots=True)
class Match:
    table: str
    column: str
    score: float


@dataclass(slots=True)
class FieldResult:
    prompt_id: str
    field: str
    layer: str
    matches: list[Match] = field(default_factory=list)

    @property
    def best(self) -> float:
        return self.matches[0].score if self.matches else 0.0

    @property
    def covered(self) -> bool:
        return self.layer != "extraction" or self.best >= COVERED_AT


def cache_path() -> Path:
    raw = os.environ.get("DILIGENCE_KERNEL_EMBED_CACHE")
    return Path(raw).expanduser() if raw else Path.home() / ".diligence-kernel" / "embeddings.json"


def _key(text: str, model: str) -> str:
    return hashlib.sha256(f"{model}\x00{text}".encode()).hexdigest()[:24]


def embed_all(
    texts: Sequence[str],
    *,
    model: str = DEFAULT_MODEL,
    embedder: Callable[[list[str]], list[list[float]]] | None = None,
    batch: int = 128,
) -> dict[str, list[float]]:
    """Embed every text, reading and writing a content-hash cache.

    Returns a mapping from text to vector, so callers need not track order.
    """
    path = cache_path()
    cache: dict[str, list[float]] = {}
    if path.is_file():
        try:
            cache = json.loads(path.read_text())
        except (OSError, ValueError):
            cache = {}

    unique = list(dict.fromkeys(texts))
    missing = [t for t in unique if _key(t, model) not in cache]
    if missing:
        if embedder is None:
            from distillcore.embedding.openai import openai_embedder

            embedder = openai_embedder(model=model)
        for start in range(0, len(missing), batch):
            chunk = missing[start : start + batch]
            for text, vector in zip(chunk, embedder(chunk), strict=True):
                cache[_key(text, model)] = vector
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cache))

    return {t: cache[_key(t, model)] for t in unique if _key(t, model) in cache}


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


def rank(
    field_vector: Sequence[float],
    columns: list[dict],
    vectors: dict[str, list[float]],
    *,
    top: int = 3,
    threshold: float = DEFAULT_THRESHOLD,
) -> list[Match]:
    """The columns most likely to answer a field, best first."""
    scored: list[Match] = []
    for column in columns:
        vector = vectors.get(column["text"])
        if vector is None:
            continue
        score = cosine(field_vector, vector)
        if score >= threshold:
            scored.append(Match(column["table"], column["name"], score))
    scored.sort(key=lambda m: -m.score)
    return scored[:top]


def column_text(name: str, purpose: str | None, table_title: str) -> str:
    """What a column is embedded as: its name, its table, and its stated purpose.

    The purpose sentence carries most of the meaning — a name like `Evidence Basis` says
    little on its own, and the corpus writes one attorney-readable sentence per column.
    """
    parts = [name, f"in {table_title}"]
    if purpose:
        parts.append(purpose)
    return " — ".join(parts)
