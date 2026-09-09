#!/usr/bin/env python
"""Verify the live model path on the smallest possible run.

Safe by default: with no flags it estimates cost using the free token-counting endpoint and
spends nothing. `--run` is what actually fills cells.

    python scripts/smoke_test.py                 # free: credentials + cost estimate
    python scripts/smoke_test.py --run           # spends: fills 4 cells on one row

It works on a throwaway database in a temp directory, never a real matter, and it caps the
number of cells so a typo cannot start a batch.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from diligence_kernel import db, env, service  # noqa: E402
from diligence_kernel.engine.llm import CellFiller  # noqa: E402
from diligence_kernel.engine.providers import ProviderUnavailable, estimate_cost  # noqa: E402
from diligence_kernel.engine.runner import RunScope, preview_run  # noqa: E402
from diligence_kernel.vault.ingest import ingest_path  # noqa: E402
from diligence_kernel.vault.units import assemble_units  # noqa: E402

#: A smoke test that can fill more than this is not a smoke test.
MAX_CELLS = 12

DIM, BOLD, GREEN, RED, YELLOW, RESET = (
    "\033[2m",
    "\033[1m",
    "\033[32m",
    "\033[31m",
    "\033[33m",
    "\033[0m",
)


def say(text: str = "") -> None:
    print(text, flush=True)


def rule(title: str) -> None:
    say(f"\n{BOLD}{title}{RESET}\n{DIM}{'─' * len(title)}{RESET}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Actually call the model. Without this, nothing is spent.",
    )
    parser.add_argument("--table", default="05", help="Table number (default 05, the classifier).")
    parser.add_argument(
        "--columns",
        type=int,
        default=4,
        help="How many columns to fill, in stage order (default 4).",
    )
    parser.add_argument(
        "--dataroom",
        default=str(REPO / "tests" / "fixtures" / "dataroom"),
        help="Directory to ingest (default: the three fixture agreements).",
    )
    parser.add_argument("--provider", default=None, help="openai (default) or anthropic.")
    parser.add_argument("--model", default=None, help="Override the model.")
    parser.add_argument("--effort", default=None, help="low | medium | high | xhigh | max.")
    parser.add_argument("--keep", action="store_true", help="Keep the temporary database.")
    args = parser.parse_args()

    loaded_from_env = env.load()
    workdir = Path(tempfile.mkdtemp(prefix="dk-smoke-"))
    conn = db.connect(workdir / "smoke.db")
    try:
        filler = CellFiller(provider=args.provider, model=args.model, effort=args.effort)
    except ProviderUnavailable as exc:
        say(f"{RED}✗{RESET} {exc}")
        return 2
    model = filler.model

    try:
        # -- 1. corpus ------------------------------------------------------------------
        rule("0. Credentials")
        if loaded_from_env:
            say(f"  {GREEN}✓{RESET} loaded {', '.join(sorted(set(loaded_from_env)))} from .env")
        elif os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY"):
            say(f"  {GREEN}✓{RESET} a key is set in the environment")
        else:
            say(f"  {YELLOW}!{RESET} no key found in the environment or a .env file")

        rule("1. Corpus")
        loaded = service.matter_open(conn, "Smoke Test", as_of_date="2026-09-08")
        say(
            f"  {GREEN}✓{RESET} {loaded['corpus_load']['tables']} tables, "
            f"{loaded['corpus_load']['columns']} columns from {loaded['corpus']}"
        )
        if loaded["finding_count"]:
            say(f"  {RED}✗{RESET} corpus parsed with {loaded['finding_count']} findings")
            return 1

        # -- 2. vault -------------------------------------------------------------------
        rule("2. Vault")
        counts, findings = ingest_path(conn, Path(args.dataroom).expanduser())
        say(f"  {GREEN}✓{RESET} {counts['ingested']} documents, {counts['chunks']} chunks")
        for f in findings:
            say(f"  {YELLOW}!{RESET} {f.code}: {f.observation}")
        if not counts["ingested"]:
            say(f"  {RED}✗{RESET} nothing ingested; check --dataroom")
            return 1

        assemble_units(conn, args.table)

        # -- 3. plan --------------------------------------------------------------------
        rule("3. Plan")
        all_requests = preview_run(conn, args.table, RunScope(), filler=filler)
        if not all_requests:
            say(f"  {RED}✗{RESET} Table {args.table} has no rows in scope")
            if args.table != "05":
                say(
                    f"\n  {DIM}Every workstream table is routed by Table 05. Until intake has{RESET}"
                )
                say(f"  {DIM}classified the data room, no other table can see a document.{RESET}")
                say(f"  {DIM}Smoke-test Table 05 first:{RESET}")
                say("      python scripts/smoke_test.py --run")
            return 1

        first_unit = all_requests[0]["unit_id"]
        columns = [r["column"] for r in all_requests if r["unit_id"] == first_unit][: args.columns]
        scope = RunScope(unit_ids=[first_unit], column_names=columns, reason="smoke test")
        requests = preview_run(conn, args.table, scope, filler=filler)

        if len(requests) > MAX_CELLS:
            say(f"  {RED}✗{RESET} {len(requests)} cells exceeds the smoke-test cap of {MAX_CELLS}")
            return 1
        say(f"  Table {args.table}, one row: {DIM}{all_requests[0]['unit']}{RESET}")
        say(f"  {len(requests)} cells — {', '.join(columns)}")
        say(
            f"  provider {BOLD}{filler.provider.name}{RESET}, model {BOLD}{model}{RESET}, "
            f"effort {filler.effort}"
        )

        # -- 4. estimate (free) -----------------------------------------------------------
        rule("4. Cost estimate")
        try:
            counted, exact = [], True
            for r in requests:
                n, is_exact = filler.count(r["request"], system=r["system"])
                counted.append(n)
                exact = exact and is_exact
        except Exception as exc:
            say(f"  {RED}✗{RESET} could not count tokens: {exc}")
            say(
                f"\n  {DIM}For openai set OPENAI_API_KEY; for anthropic set ANTHROPIC_API_KEY{RESET}"
            )
            say(f"  {DIM}(or ANTHROPIC_AUTH_TOKEN, or an `ant auth login` profile).{RESET}")
            return 2

        say(
            f"  {GREEN}✓{RESET} {len(counted)} requests counted"
            f"{'' if exact else DIM + ' (locally, so approximate)' + RESET}"
        )

        prefix_tokens = next(
            (c for c, r in zip(counted, requests, strict=True) if r["cache_role"] == "write"), 0
        )
        cacheable = prefix_tokens >= filler.provider.min_cacheable_tokens
        cached = (
            sum(c for c, r in zip(counted, requests, strict=True) if r["cache_role"] == "read")
            if cacheable
            else 0
        )
        fresh = sum(counted) - cached
        est_out = service.OUTPUT_TOKENS_PER_CELL * len(requests)
        cost = estimate_cost(
            filler.provider,
            model,
            input_tokens=fresh,
            output_tokens=est_out,
            cache_read_tokens=cached,
        )
        say(f"  input:  {sum(counted):,} tokens across {len(requests)} cells")
        if cacheable:
            say(f"  {DIM}of which {cached:,} served from the cached unit prefix{RESET}")
        else:
            say(
                f"  {YELLOW}!{RESET} the unit prefix is {prefix_tokens:,} tokens, below the "
                f"{filler.provider.min_cacheable_tokens:,}-token minimum,"
            )
            say(
                f"      {DIM}so {filler.provider.name} will not cache it. These fixture documents{RESET}"
            )
            say(f"      {DIM}are too small to show the caching win; real ones will.{RESET}")
        say(f"  output: ~{est_out:,} tokens estimated")
        say(
            f"  {BOLD}cost:   {f'${cost:.4f}' if cost is not None else 'unknown for this model'}{RESET}"
        )
        if cost is None:
            say(
                f"  {DIM}Set DILIGENCE_KERNEL_PRICE_IN / _OUT (USD per million) to price it.{RESET}"
            )

        if not args.run:
            say(
                f"\n  {YELLOW}Nothing was spent.{RESET} Re-run with {BOLD}--run{RESET} to fill these cells."
            )
            return 0

        # -- 5. run (spends) ---------------------------------------------------------------
        rule("5. Run")
        out = service.run_table(
            conn,
            args.table,
            unit_ids=[first_unit],
            columns=columns,
            reason="smoke test",
            model=model,
        )
        if out.get("error"):
            say(f"  {RED}✗{RESET} {out['error']}")
            return 1
        say(
            f"  status {out['status']}, {out['cells_done']}/{out['cells_total']} filled, "
            f"{out['cells_failed']} failed"
        )
        say(f"  tokens in {out['input_tokens']:,} / out {out['output_tokens']:,}")
        actual = estimate_cost(
            filler.provider,
            model,
            input_tokens=out["input_tokens"],
            output_tokens=out["output_tokens"],
        )
        if actual is not None:
            say(f"  {DIM}billed roughly ${actual:.4f} (excludes the cache discount){RESET}")

        # -- 6. what came back --------------------------------------------------------------
        rule("6. Cells")
        ok = True
        for column in columns:
            cell = service.cell_evidence(conn, first_unit, column)
            violations = cell["validation"]
            mark = f"{GREEN}✓{RESET}" if not violations else f"{RED}✗{RESET}"
            say(f"\n  {mark} {BOLD}{column}{RESET} {DIM}({cell['native_type']}){RESET}")
            say(f"      value: {cell['value']}")
            if violations:
                ok = False
                say(f"      {RED}violations: {', '.join(violations)}{RESET}")
            for e in cell["evidence"][:2]:
                located = "" if e["char_start"] is None else f" @{e['char_start']}"
                say(f"      {DIM}evidence [{e['filename']}{located}]: {e['quote'][:110]}{RESET}")
            if not cell["evidence"]:
                say(f"      {YELLOW}no evidence quoted{RESET}")

        rule("Result")
        for f in out["findings"]:
            say(f"  {YELLOW}!{RESET} {f['code']}: {f['observation']}")
        if ok and out["cells_failed"] == 0:
            say(f"  {GREEN}The live model path works end to end.{RESET}")
            return 0
        say(f"  {YELLOW}Cells were filled, but some breached the 00a standards (above).{RESET}")
        say(f"  {DIM}That is a prompt or model finding, not a plumbing failure.{RESET}")
        return 0

    finally:
        conn.close()
        if args.keep:
            say(f"\n{DIM}database kept at {workdir / 'smoke.db'}{RESET}")
        else:
            shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
