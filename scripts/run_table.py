#!/usr/bin/env python
"""Run a review table against a matter, with progress and a cost gate.

    python scripts/run_table.py 05 --db matters/fixture.db --room tests/fixtures/dataroom
    python scripts/run_table.py 05 --db matters/fixture.db --run

Estimates first and stops, unless `--run` is given. Progress is written as it goes, so a
long run can be watched or resumed after an interruption.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from diligence_kernel import db, env, service  # noqa: E402
from diligence_kernel.engine import runner as runner_mod  # noqa: E402
from diligence_kernel.engine.llm import CellFiller  # noqa: E402
from diligence_kernel.engine.providers import estimate_cost  # noqa: E402
from diligence_kernel.engine.runner import RunScope, create_run, execute_run  # noqa: E402
from diligence_kernel.vault.ingest import ingest_path  # noqa: E402
from diligence_kernel.vault.units import assemble_units  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("table")
    parser.add_argument("--db", required=True)
    parser.add_argument("--room", help="Ingest this data room first.")
    parser.add_argument("--run", action="store_true", help="Spend. Without it, estimate only.")
    parser.add_argument("--model", default=None)
    parser.add_argument("--provider", default=None)
    parser.add_argument("--effort", default=None)
    parser.add_argument("--concurrency", type=int, default=None)
    args = parser.parse_args()

    env.load()
    if args.concurrency:
        os.environ["DILIGENCE_KERNEL_CONCURRENCY"] = str(args.concurrency)
    path = Path(args.db).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = db.connect(path)

    service.matter_open(conn, "Fixture data room", as_of_date="2026-09-08")
    if args.room:
        counts, findings = ingest_path(conn, Path(args.room).expanduser())
        print(f"ingest: { ({k: v for k, v in counts.items() if v}) }", flush=True)
        for f in findings:
            print(f"  ! {f.code}: {f.subject_name}", flush=True)

    assembled, _ = assemble_units(conn, args.table)
    print(f"units: {assembled}", flush=True)

    filler = CellFiller(provider=args.provider, model=args.model, effort=args.effort)
    estimate = service.run_estimate(conn, args.table, model=filler.model, provider=args.provider)
    print(
        f"\nplan: {estimate['cells']} cells over {estimate['rows']} rows on "
        f"{estimate['provider']}/{estimate['model']} (effort {filler.effort}, "
        f"concurrency {runner_mod.configured_concurrency()})",
        flush=True,
    )
    print(
        f"estimate: {estimate['input_tokens']:,} in, "
        f"{estimate['estimated_output_tokens']:,} out, "
        f"${estimate['estimated_cost_usd']}",
        flush=True,
    )
    if not args.run:
        print("\nNothing spent. Re-run with --run.", flush=True)
        return 0

    started = time.time()

    def progress(done: int, count: int) -> None:
        if done % 10 == 0 or done == count:
            rate = done / max(1e-6, time.time() - started)
            left = (count - done) / rate if rate else 0
            print(
                f"  {done}/{count} cells  {rate * 60:.1f}/min  ~{left / 60:.0f} min left",
                flush=True,
            )

    run_id = create_run(conn, args.table, RunScope(reason="full table"), model=filler.model)
    summary, findings = execute_run(conn, run_id, filler=filler, progress=progress)

    elapsed = time.time() - started
    actual = estimate_cost(
        filler.provider,
        filler.model,
        input_tokens=summary["input_tokens"],
        output_tokens=summary["output_tokens"],
    )
    print(
        f"\n{summary['status']}: {summary['cells_done']}/{summary['cells_total']} filled, "
        f"{summary['cells_failed']} failed in {elapsed / 60:.1f} min",
        flush=True,
    )
    cached = summary.get("cache_read_tokens", 0)
    total_in = summary["input_tokens"] + cached
    print(
        f"tokens: {summary['input_tokens']:,} fresh in / {cached:,} cached in "
        f"({cached / max(1, total_in):.0%}) / {summary['output_tokens']:,} out"
        + (f"  ≈ ${actual:.2f}" if actual else ""),
        flush=True,
    )

    from collections import Counter

    counted = Counter(f.code for f in findings)
    if counted:
        print("\nfindings:", flush=True)
        for code, n in counted.most_common():
            print(f"  {code}: {n}", flush=True)
    if args.table == "05":
        counts, projected = service.classify_mod.project_intake(conn, run_id=run_id)
        print(f"\nclassification projected: {counts}", flush=True)
        for f in projected:
            print(f"  ! {f.code}: {f.subject_name}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
