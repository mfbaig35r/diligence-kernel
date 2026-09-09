#!/usr/bin/env python
"""Score a Table 05 run against the fixture ground truth.

    python scripts/score_intake.py --db matters/fixture.db

Separates two kinds of wrong, because they cost differently:

- a **miss** is a wrong value a reviewer will catch;
- an **overconfident** answer is a single definite value where the document genuinely admits
  more than one, or none. That is worse: it routes a file somewhere plausible and nothing
  downstream detects what was lost.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from expected_intake import EXPECTED, LOAD_BEARING  # noqa: E402

from diligence_kernel import db  # noqa: E402
from diligence_kernel.engine.validate import is_fallback  # noqa: E402

GREEN, RED, YELLOW, DIM, BOLD, RESET = (
    "\033[32m",
    "\033[31m",
    "\033[33m",
    "\033[2m",
    "\033[1m",
    "\033[0m",
)


def matches(value: str, accepted: set) -> bool | None:
    """True if right, False if wrong, None if the check needs a human eye."""
    normalized = value.strip()
    if None in accepted and is_fallback(normalized):
        return True
    if "NAMES_THE_MSA" in accepted:
        return "master services" in normalized.lower() or "2022" in normalized
    if "NAMES_THE_LEASE" in accepted:
        return "lease" in normalized.lower() or "2021" in normalized
    if "COMPILATION" in accepted:
        low = normalized.lower()
        return "single" not in low
    return any(a is not None and a.lower() == normalized.lower() for a in accepted)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    args = parser.parse_args()
    conn = db.connect(Path(args.db).expanduser())

    right = wrong = overconfident = 0
    rows: list[tuple[str, str, str, str, str]] = []

    for filename, columns in EXPECTED.items():
        for column, accepted in columns.items():
            cell = conn.execute(
                """SELECT cell.value FROM cell
                   JOIN column_def c ON c.id = cell.column_id
                   JOIN review_unit u ON u.id = cell.unit_id
                   JOIN unit_document ud ON ud.unit_id = u.id
                   JOIN document d ON d.id = ud.document_id
                   JOIN review_table t ON t.id = c.table_id
                   WHERE t.number = '05' AND c.name = ? AND d.filename = ?
                     AND d.parent_document_id IS NULL
                   LIMIT 1""",
                (column, filename),
            ).fetchone()
            if cell is None:
                rows.append((filename, column, "—", "not filled", YELLOW))
                continue
            value = (cell["value"] or "").strip()
            ok = matches(value, accepted)
            ambiguous = None in accepted or len(accepted) > 1
            if ok:
                right += 1
                mark, colour = "ok", GREEN
            elif ambiguous and not is_fallback(value):
                overconfident += 1
                wrong += 1
                mark, colour = "OVERCONFIDENT", RED
            else:
                wrong += 1
                mark, colour = "wrong", RED
            rows.append((filename, column, value[:40], mark, colour))

    current = ""
    for filename, column, value, mark, colour in rows:
        if filename != current:
            print(f"\n{BOLD}{filename}{RESET}")
            current = filename
        star = " *" if column in LOAD_BEARING else "  "
        print(f" {star}{column[:26]:28s} {value[:40]:42s} {colour}{mark}{RESET}")

    total = right + wrong
    print(f"\n{BOLD}Score{RESET}")
    print(f"  correct: {right}/{total} ({right / max(1, total):.0%})")
    print(f"  wrong:   {wrong}")
    print(f"  of which overconfident on an ambiguous document: {overconfident}")
    print(f"  {DIM}* marks a column something downstream depends on{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
