#!/usr/bin/env python
"""Compare two runs of the same table cell by cell.

    python scripts/compare_runs.py --a matters/fixture.db --b matters/luna.db --table 05

Same documents, same prompts, same ground truth — so every difference is the model. Reports
where they agree, where they differ, and which of them the ground truth backs.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))

from expected_intake import EXPECTED, LOAD_BEARING  # noqa: E402
from score_intake import matches  # noqa: E402

from diligence_kernel import db  # noqa: E402
from diligence_kernel.engine.providers import OpenAIProvider, estimate_cost  # noqa: E402
from diligence_kernel.engine.validate import is_fallback  # noqa: E402

GREEN, RED, YELLOW, DIM, BOLD, RESET = (
    "\033[32m",
    "\033[31m",
    "\033[33m",
    "\033[2m",
    "\033[1m",
    "\033[0m",
)


def cells(path: Path, table: str) -> dict[tuple[str, str], tuple[str, list[str]]]:
    conn = db.connect(path)
    rows = conn.execute(
        """SELECT d.filename, c.name, cell.value, cell.validation
           FROM cell
           JOIN column_def c ON c.id = cell.column_id
           JOIN review_table t ON t.id = c.table_id
           JOIN review_unit u ON u.id = cell.unit_id
           JOIN unit_document ud ON ud.unit_id = u.id
           JOIN document d ON d.id = ud.document_id
           WHERE t.number = ? AND d.parent_document_id IS NULL""",
        (table,),
    ).fetchall()
    return {
        (r["filename"], r["name"]): (
            (r["value"] or "").strip(),
            json.loads(r["validation"] or "[]"),
        )
        for r in rows
    }


def summary(path: Path) -> dict:
    conn = db.connect(path)
    r = conn.execute("SELECT * FROM run ORDER BY id DESC LIMIT 1").fetchone()
    p = OpenAIProvider()
    cost = estimate_cost(
        p,
        r["model"],
        input_tokens=r["input_tokens"],
        output_tokens=r["output_tokens"],
        cache_read_tokens=r["cache_read_tokens"],
        cache_write_tokens=r["cache_write_tokens"],
    )
    done = r["cells_done"] or 1
    return {
        "model": r["model"],
        "status": r["status"],
        "done": r["cells_done"],
        "failed": r["cells_failed"],
        "out_per_cell": r["output_tokens"] // done,
        "fresh_in": r["input_tokens"],
        "cached_in": r["cache_read_tokens"],
        "out": r["output_tokens"],
        "cost": cost,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", required=True)
    parser.add_argument("--b", required=True)
    parser.add_argument("--table", default="05")
    args = parser.parse_args()

    a_path, b_path = Path(args.a), Path(args.b)
    a, b = cells(a_path, args.table), cells(b_path, args.table)
    sa, sb = summary(a_path), summary(b_path)

    print(f"{BOLD}Run comparison — Table {args.table}{RESET}\n")
    print(f"  {'':22s} {sa['model']:>18s} {sb['model']:>18s}")
    for label, key, fmt in (
        ("cells filled", "done", "{:,}"),
        ("failed", "failed", "{:,}"),
        ("output tokens/cell", "out_per_cell", "{:,}"),
        ("fresh input", "fresh_in", "{:,}"),
        ("cached input", "cached_in", "{:,}"),
        ("output tokens", "out", "{:,}"),
    ):
        print(f"  {label:22s} {fmt.format(sa[key]):>18s} {fmt.format(sb[key]):>18s}")
    ca, cb = sa["cost"], sb["cost"]
    show_a = f"${ca:.4f}" if ca else "?"
    show_b = f"${cb:.4f}" if cb else "?"
    print(f"  {'cost':22s} {show_a:>18s} {show_b:>18s}")
    if ca and cb and cb:
        print(f"  {DIM}{ca / cb:.0f}x cheaper{RESET}")

    shared = sorted(set(a) & set(b))
    agree = [k for k in shared if a[k][0].lower() == b[k][0].lower()]
    print(f"\n{BOLD}Agreement{RESET}")
    print(
        f"  identical values: {len(agree)}/{len(shared)} ({len(agree) / max(1, len(shared)):.0%})"
    )

    print(f"\n{BOLD}Where they differ{RESET}")
    scored = Counter()
    for key in shared:
        va, vb = a[key][0], b[key][0]
        if va.lower() == vb.lower():
            continue
        filename, column = key
        accepted = EXPECTED.get(filename, {}).get(column)
        verdict = ""
        if accepted:
            ok_a, ok_b = matches(va, accepted), matches(vb, accepted)
            if ok_a and not ok_b:
                verdict, colour = "A right", GREEN
                scored["a"] += 1
            elif ok_b and not ok_a:
                verdict, colour = "B right", YELLOW
                scored["b"] += 1
            elif ok_a and ok_b:
                verdict, colour = "both ok", DIM
                scored["both"] += 1
            else:
                verdict, colour = "both wrong", RED
                scored["neither"] += 1
        else:
            colour = DIM
            scored["unscored"] += 1
        star = "*" if column in LOAD_BEARING else " "
        print(f" {star}{filename[:30]:32s} {column[:24]:26s}")
        print(f"    A: {va[:58]!r}")
        print(f"    B: {vb[:58]!r}   {colour}{verdict}{RESET}")

    print(f"\n{BOLD}Disagreements judged against ground truth{RESET}")
    for label, key in (
        ("A right", "a"),
        ("B right", "b"),
        ("both acceptable", "both"),
        ("both wrong", "neither"),
        ("no ground truth", "unscored"),
    ):
        print(f"  {label:20s} {scored[key]}")

    print(f"\n{BOLD}Fallback and violation rates{RESET}")
    for name, data in (("A", a), ("B", b)):
        fb = sum(1 for v, _ in data.values() if is_fallback(v))
        viol = sum(len(codes) for _, codes in data.values())
        print(
            f"  {name}: {fb}/{len(data)} fallbacks ({fb / max(1, len(data)):.0%}), "
            f"{viol} standards violations"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
