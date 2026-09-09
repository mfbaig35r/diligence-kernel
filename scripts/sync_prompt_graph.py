#!/usr/bin/env python
"""Rebuild prompt-graph's record of the corpus from the markdown.

    python scripts/sync_prompt_graph.py --matter "Diligence Corpus Library"

**The markdown is the source of truth.** It is what git tracks, what a partner redlines, and
what `00a` section 11 calls "the history and the reasons". prompt-graph holds versions, the
cross-table dependency graph and the evaluation log — derived, and rebuilt from here.

So a prompt is edited in `review-table-prompts/`, and this replays the change into
prompt-graph, where `table_ingest` versions it: an unchanged prompt is left alone, a changed
one gets a new minor version, and a column missing from the submission is reported rather
than retired silently. That keeps prompt-graph's history honest without letting it become a
second place prompts are written.

This calls `prompt_graph.service.table_ingest` directly, which is exactly what the MCP tool
of that name calls. Going through the conversation instead would risk 1.19M characters
drifting in transcription, for no gain.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROMPT_GRAPH = Path("/Users/fbaig/Projects/prompt-graph")
sys.path.insert(0, str(REPO / "src"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matter", default="Diligence Corpus Library")
    parser.add_argument("--corpus", default=str(REPO / "review-table-prompts"))
    parser.add_argument("--tables", nargs="*", help="Table numbers; all by default.")
    parser.add_argument("--change-note", default="Sync from the markdown corpus.")
    parser.add_argument("--actor", default="diligence-kernel sync")
    parser.add_argument("--dry-run", action="store_true", help="Parse and report; write nothing.")
    args = parser.parse_args()

    from diligence_kernel import db as kernel_db
    from diligence_kernel.corpus.loader import load_corpus
    from diligence_kernel.export import table_payload

    # Parse the markdown into a scratch database: prompt-graph is fed from the corpus, never
    # from a matter's working state.
    scratch = Path(tempfile.mkdtemp()) / "corpus.db"
    conn = kernel_db.connect(scratch)
    counts, parse_findings = load_corpus(conn, Path(args.corpus).expanduser())
    print(f"parsed {counts['tables']} tables, {counts['columns']} columns from {args.corpus}")
    for f in parse_findings:
        print(f"  ! {f.code}: {f.subject_name} — {f.observation[:100]}")

    numbers = args.tables or [
        r["number"] for r in conn.execute("SELECT number FROM review_table ORDER BY number")
    ]
    payloads = [table_payload(conn, n) for n in numbers]
    if args.dry_run:
        chars = sum(len(c["prompt_text"]) for p in payloads for c in p["columns"])
        print(f"\ndry run: {len(payloads)} tables, {chars:,} prompt characters. Nothing written.")
        return 0

    sys.path.insert(0, str(PROMPT_GRAPH / "src"))
    from prompt_graph import db as pg_db
    from prompt_graph import service
    from prompt_graph.models import ColumnRecord, TableMeta

    pg = pg_db.connect()
    print(f"\nprompt-graph db: {pg_db.db_path()}")

    codes: Counter[str] = Counter()
    created = revised = unchanged = 0
    for p in payloads:
        out = service.table_ingest(
            pg,
            args.matter,
            p["table"],
            [ColumnRecord(**c) for c in p["columns"]],
            TableMeta(**p["table_meta"]) if p.get("table_meta") else None,
            p.get("table_instructions"),
            "drafted",
            args.actor,
            args.change_note,
        )
        created += len(out.get("created", []))
        revised += len(out.get("new_versions", []))
        unchanged += len(out.get("unchanged", []))
        for f in out.get("findings", []):
            codes[f["code"] if isinstance(f, dict) else f.code] += 1
    pg.commit()

    print(f"\ncreated {created}, revised {revised}, unchanged {unchanged}")
    if codes:
        print("findings by code:")
        for code, n in codes.most_common():
            print(f"  {code:34s} {n}")
    print("\nRun suite_check in prompt-graph for the graph, parameter and consistency families.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
