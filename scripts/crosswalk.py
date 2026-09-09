#!/usr/bin/env python
"""Crosswalk the playbook's diligence prompts against the review-table corpus.

    python scripts/crosswalk.py --playbook playbook/corporate-ma-3.4.json

Two directions, and the second is the one nobody runs:

- **Playbook to corpus** — which fields the practice asks for that no column answers. A gap
  in the tables.
- **Corpus to playbook** — which columns answer nothing the playbook asks and feed no derived
  artifact. Those are columns being filled on every row of every matter for no reader.

**What a match is worth — read this before quoting a number.** Matching is lexical: shared
terms between a playbook field and a column's name and purpose. It is **not good enough to
produce a coverage figure**, and the figures it prints should be read as "how many fields this
crude method could resolve", not as how much of the playbook the corpus answers.

Measured: 95% of the playbook's distinct field terms appear somewhere in the corpus, while
this matcher resolves ~42% of fields. Hand-checking the fields it called gaps found the
concepts present — `drag-along`, `anti-dilution`, `liquidation preference` and `preemptive
rights` all have their own columns. The absence signal is therefore also unreliable, and every
flagged gap needs reading before it is believed.

The lasting value here is the *structure*: which layer answers each field, which tables a
prompt spans, and the field inventory itself. Replacing the scorer with embeddings would make
the numbers mean something; term overlap will not.

And per the playbook's own provenance: it was substantially model-generated rather than
written from observed practice, so agreement is evidence that two syntheses agree, not that
either is right.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from diligence_kernel import db  # noqa: E402
from diligence_kernel.corpus.loader import load_corpus  # noqa: E402
from diligence_kernel.derive.artifacts import ARTIFACTS  # noqa: E402

STOP = set(
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
        "please",
        "provide",
        "including",
        "include",
        "any",
        "such",
        "other",
        "their",
        "there",
        "been",
        "were",
        "was",
        "will",
        "would",
        "shall",
        "may",
        "can",
        "identify",
        "summarize",
        "summarise",
        "assess",
        "flag",
        "list",
        "state",
        "report",
        "review",
        "document",
        "documents",
        "agreement",
        "agreements",
        "target",
        "buyer",
        "seller",
        "company",
        "entity",
        "relevant",
        "material",
        "key",
        "across",
    ]
)
WORD = re.compile(r"[a-z][a-z0-9-]{2,}")

#: Which corpus tables answer each playbook prompt.
#:
#: **The playbook's prompt boundaries are not the corpus's table boundaries.** 3.4.1 is titled
#: "Summarize a Corporate Organizational Document" and asks for capital structure, liquidation
#: preferences and anti-dilution — which the corpus puts in Capitalization (03), not Corporate
#: (02). Scoping a prompt to one workstream reports that mismatch as missing coverage.
TABLES_OF_PROMPT: dict[str, tuple[str, ...]] = {
    "3.4.1": ("02", "03"),
    "3.4.2": ("02", "03"),
    "3.4.3": ("02", "03"),
    "3.4.4": ("02", "03"),
    "3.4.5": ("01", "07"),
    "3.4.6": ("01", "07"),
    "3.4.7": ("01", "07"),
    "3.4.8": ("10", "11", "12"),
    "3.4.9": ("10", "11", "12"),
    "3.4.10": ("08", "09", "04"),
    "3.4.11": ("08", "09"),
    "3.4.12": ("13", "14"),
    "3.4.13": ("15", "17"),
    "3.4.14": ("16", "17"),
    "3.4.15": ("24", "25"),
    "3.4.16": (),  # financial statements: 00a places these out of scope
}

#: A field answered by a human column, not an extraction column. 00a section 10 reserves
#: rating, materiality and consequence for a person, so scoring these against Harvey columns
#: reports a deliberate design choice as a gap.
HUMAN = re.compile(
    r"\brate\b|\brating\b|high,? medium|likelihood|mitigat|recommend|prioriti|materiality|"
    r"deal consequence|significance|severity|assess the risk",
    re.I,
)
#: A field answered by a derived artifact or the memo, not by any single cell.
SYNTHESIS = re.compile(
    r"synthesi[sz]|memo\b|across (?:all|the) |portfolio-level|aggregate|overall summary|"
    r"executive summary|prepare a summary|organi[sz]ed by",
    re.I,
)
#: A field answered by the coverage register and the missing-document tests.
MISSING = re.compile(r"missing|not produced|absent|checklist|request list|follow-up request", re.I)


def answered_by(field: str) -> str:
    """Which layer of the system is supposed to answer a field."""
    if HUMAN.search(field):
        return "human"
    if MISSING.search(field):
        return "missing"
    if SYNTHESIS.search(field):
        return "synthesis"
    return "extraction"


def terms(text: str) -> set[str]:
    return {w for w in WORD.findall((text or "").lower()) if w not in STOP}


def cover(field: set[str], pool: list[dict], limit: int = 4) -> tuple[list[dict], set[str]]:
    """Greedily choose the columns that between them cover a field's terms.

    A playbook field is compound — "authorized and outstanding capital structure (classes of
    stock, voting rights, liquidation preferences, anti-dilution)" — and the corpus decomposes
    exactly that into separate columns by design. Asking whether any *single* column covers
    the field therefore measures the decomposition, not the coverage. What matters is whether
    the columns collectively answer it, and which terms none of them reach.
    """
    remaining = set(field)
    chosen: list[dict] = []
    while remaining and len(chosen) < limit:
        best, gain = None, set()
        for c in pool:
            if c in chosen:
                continue
            g = remaining & c["terms"]
            if len(g) > len(gain):
                best, gain = c, g
        if best is None or not gain:
            break
        chosen.append(best)
        remaining -= gain
    return chosen, remaining


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--playbook", default="playbook/corporate-ma-3.4.json")
    parser.add_argument("--threshold", type=float, default=0.34)
    parser.add_argument("--show", type=int, default=2, help="Candidate columns per field.")
    args = parser.parse_args()

    book = json.loads(Path(args.playbook).read_text())
    conn = db.connect(Path(tempfile.mkdtemp()) / "corpus.db")
    load_corpus(conn, REPO / "review-table-prompts")

    columns = [
        {
            "table": r["number"],
            "name": r["name"],
            "terms": terms(f"{r['name']} {r['purpose'] or ''}"),
        }
        for r in conn.execute(
            """SELECT t.number, cd.name, cd.purpose FROM column_def cd
               JOIN review_table t ON t.id = cd.table_id ORDER BY t.number, cd.position"""
        )
    ]
    matched_columns: set[tuple[str, str]] = set()

    print("=" * 78)
    print("PLAYBOOK → CORPUS   does a column answer what the practice asks?")
    print("=" * 78)
    uncovered: list[tuple[str, str]] = []
    for prompt in book["prompts"]:
        scope = set(TABLES_OF_PROMPT.get(prompt["id"], ()))
        pool = [c for c in columns if c["table"] in scope]
        hits = 0
        by_layer: dict[str, int] = defaultdict(int)
        print(f"\n{prompt['id']}  {prompt['title'][:66]}")
        print(f"        tables {sorted(scope) or '— outside the corpus —'}; {len(pool)} columns")
        if not pool:
            for field in prompt["fields"]:
                uncovered.append((prompt["id"], field, ["outside the corpus"]))
            print(f"        0/{len(prompt['fields'])} — the corpus does not cover this prompt")
            continue
        for field in prompt["fields"]:
            layer = answered_by(field)
            by_layer[layer] += 1
            if layer != "extraction":
                # 00a answers these outside the extraction columns by design: rating and
                # consequence are human columns, synthesis is a derived artifact, and missing
                # items are the coverage register.
                hits += 1
                print(f"    {layer[:4]:4s} {field[:52]:54s}  answered by the {layer} layer")
                continue
            ft = terms(field)
            chosen, missed = cover(ft, pool, limit=args.show + 2)
            covered = (len(ft) - len(missed)) / len(ft) if ft else 0.0
            for c in chosen:
                matched_columns.add((c["table"], c["name"]))
            shown = "; ".join(f"{c['table']} {c['name']}" for c in chosen[: args.show]) or "—"
            if covered >= args.threshold:
                hits += 1
                mark = "ok  "
            else:
                uncovered.append((prompt["id"], field, sorted(missed)))
                mark = "GAP "
            note = f"  [{', '.join(sorted(missed)[:4])}]" if missed else ""
            print(f"    {mark} {field[:52]:54s} {covered:>4.0%} {shown[:44]}{note[:46]}")
        shape = ", ".join(f"{n} {k}" for k, n in sorted(by_layer.items()))
        print(f"        {hits}/{len(prompt['fields'])} fields answered  ({shape})")

    print("\n" + "=" * 78)
    print("CORPUS → PLAYBOOK   which columns answer nothing the playbook asks?")
    print("=" * 78)
    artifact_terms = {
        t for spec in ARTIFACTS.values() for p in spec.column_patterns for t in terms(p)
    }
    unread: dict[str, list[str]] = defaultdict(list)
    for c in columns:
        if (c["table"], c["name"]) in matched_columns:
            continue
        if c["terms"] & artifact_terms:
            continue  # feeds a derived artifact even if no playbook prompt asks for it
        unread[c["table"]].append(c["name"])

    total_unread = sum(len(v) for v in unread.values())
    print(
        f"\n{total_unread} of {len(columns)} columns match no playbook field and feed no artifact"
    )
    for table in sorted(unread):
        print(
            f"  {table}: {len(unread[table]):2d}  {', '.join(unread[table][:6])}"
            + (" …" if len(unread[table]) > 6 else "")
        )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    fields = sum(len(p["fields"]) for p in book["prompts"])
    print(f"  playbook fields              {fields}")
    print(
        f"  with a candidate column      {fields - len(uncovered)} ({(fields - len(uncovered)) / fields:.0%})"
    )
    print(f"  with none                    {len(uncovered)}")
    print(f"  corpus columns               {len(columns)}")
    print(f"  matched to a playbook field  {len(matched_columns)}")
    print(f"  answering nothing read       {total_unread}")
    print(f"\n  {book['provenance']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
