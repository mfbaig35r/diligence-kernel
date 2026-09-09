#!/usr/bin/env python
"""Read a filled table back: values, fallbacks, violations, and what routing it produced.

    python scripts/inspect_table.py 05 --db matters/fixture.db

Written for reviewing a run rather than for the MCP surface: it prints the grid a person
would look at, and the questions worth asking of it.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from diligence_kernel import db  # noqa: E402
from diligence_kernel.engine.validate import is_fallback  # noqa: E402

DIM, BOLD, RESET = "\033[2m", "\033[1m", "\033[0m"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("table")
    parser.add_argument("--db", required=True)
    parser.add_argument("--columns", nargs="*", help="Only these columns.")
    parser.add_argument("--width", type=int, default=34)
    args = parser.parse_args()

    conn = db.connect(Path(args.db).expanduser())
    table = conn.execute(
        "SELECT id, number, title FROM review_table WHERE number = ?", (args.table,)
    ).fetchone()
    if table is None:
        print(f"Table {args.table} is not loaded.")
        return 1

    cols = conn.execute(
        "SELECT id, name, native_type, stage FROM column_def WHERE table_id = ? ORDER BY position",
        (int(table["id"]),),
    ).fetchall()
    if args.columns:
        wanted = {c.lower() for c in args.columns}
        cols = [c for c in cols if c["name"].lower() in wanted]

    units = conn.execute(
        "SELECT id, label FROM review_unit WHERE table_id = ? ORDER BY position",
        (int(table["id"]),),
    ).fetchall()

    print(f"{BOLD}Table {table['number']} — {table['title']}{RESET}")
    print(f"{len(units)} rows x {len(cols)} columns\n")

    fallbacks: Counter[str] = Counter()
    violations: Counter[str] = Counter()
    empty = 0
    values_by_column: dict[str, Counter[str]] = {}

    for unit in units:
        print(f"{BOLD}{unit['label'][:70]}{RESET}")
        for col in cols:
            cell = conn.execute(
                "SELECT value, validation FROM cell WHERE unit_id = ? AND column_id = ?",
                (int(unit["id"]), int(col["id"])),
            ).fetchone()
            if cell is None:
                empty += 1
                print(f"  {col['name'][:28]:30s} {DIM}— not filled —{RESET}")
                continue
            value = (cell["value"] or "").strip()
            codes = json.loads(cell["validation"] or "[]")
            for code in codes:
                violations[code] += 1
            if is_fallback(value):
                fallbacks[value] += 1
            values_by_column.setdefault(col["name"], Counter())[value[: args.width]] += 1
            flag = f"  {' '.join(codes)}" if codes else ""
            shown = value.replace("\n", " ⏎ ")[: args.width]
            print(f"  {col['name'][:28]:30s} {shown}{flag}")
        print()

    print(f"{BOLD}Summary{RESET}")
    filled = len(units) * len(cols) - empty
    print(f"  cells filled: {filled}/{len(units) * len(cols)}")
    print(
        f"  fallback states: {sum(fallbacks.values())} ({sum(fallbacks.values()) / max(1, filled):.0%})"
    )
    for value, n in fallbacks.most_common():
        print(f"    {value}: {n}")
    print(f"  standards violations: {sum(violations.values())}")
    for code, n in violations.most_common():
        print(f"    {code}: {n}")

    print(f"\n{BOLD}Routing produced{RESET}")
    rows = conn.execute(
        """SELECT d.filename, c.workstream, c.document_type, c.document_date,
                  c.amends_or_issued_under
           FROM document d LEFT JOIN classification c ON c.document_id = d.id
           ORDER BY d.filename"""
    ).fetchall()
    for r in rows:
        print(
            f"  {r['filename'][:38]:40s} {str(r['workstream'])[:16]:18s} "
            f"{str(r['document_type'])[:30]}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
