"""Concurrency inside a stage, never across one.

The speedup is not the interesting part; the guarantees are. A stage-2 prompt consumes
stage-1 answers, so if concurrency ever crossed a stage boundary a prompt would be fed an
empty upstream and nobody would notice.
"""

from __future__ import annotations

import threading
import time

import pytest

from diligence_kernel.engine.llm import CellAnswer, CellRequest
from diligence_kernel.engine.providers import PromptPrefix, Usage
from diligence_kernel.engine.runner import (
    DEFAULT_CONCURRENCY,
    RunScope,
    configured_concurrency,
    create_run,
    execute_run,
)
from diligence_kernel.vault.ingest import ingest_path
from diligence_kernel.vault.units import assemble_units

from .stub import SCRIPT, StubFiller
from .test_pipeline import _classify


class RecordingFiller(StubFiller):
    """Records when each call starts and ends, so overlap can be measured."""

    def __init__(self, delay: float = 0.02, script=None) -> None:
        super().__init__(script if script is not None else SCRIPT)
        self.delay = delay
        self.lock = threading.Lock()
        # (column, unit cache key, thread, start, end)
        self.spans: list[tuple[str, str, int, float, float]] = []
        self.threads: set[int] = set()
        self.peak = 0
        self._live = 0

    def fill(self, request: CellRequest, *, system: PromptPrefix):
        with self.lock:
            self._live += 1
            self.peak = max(self.peak, self._live)
            self.threads.add(threading.get_ident())
        start = time.perf_counter()
        time.sleep(self.delay)
        value, evidence = self.script.get(request.column_name, ("Not addressed", []))
        answer = CellAnswer(value=value, evidence=evidence, source_document=None)
        with self.lock:
            self._live -= 1
            self.spans.append(
                (
                    request.column_name,
                    system.cache_key,
                    threading.get_ident(),
                    start,
                    time.perf_counter(),
                )
            )
            self.calls.append(request)
            self.systems.append(system)
        return answer, Usage(input_tokens=100, output_tokens=10, cache_read_tokens=50)


@pytest.fixture
def ready(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")
    return loaded


def _stage_of(conn, name: str) -> int:
    return conn.execute(
        """SELECT c.stage FROM column_def c JOIN review_table t ON t.id = c.table_id
           WHERE t.number = '01' AND c.name = ?""",
        (name,),
    ).fetchone()["stage"]


# --- the guarantees ---------------------------------------------------------------------


def test_no_cell_starts_before_its_stage_is_reachable(ready, monkeypatch):
    """The load-bearing invariant: within a unit, a stage never overlaps the one before it.

    Across units it may and should — unit two's stage 1 runs after unit one has finished,
    which is why this is measured per unit rather than globally.
    """
    monkeypatch.setenv("DILIGENCE_KERNEL_CONCURRENCY", "6")
    filler = RecordingFiller()
    run_id = create_run(ready, "01", RunScope(), model="stub")
    execute_run(ready, run_id, filler=filler)

    per_unit: dict[str, dict[int, list[tuple[float, float]]]] = {}
    for name, unit_key, _, start, end in filler.spans:
        stage = _stage_of(ready, name)
        per_unit.setdefault(unit_key, {}).setdefault(stage, []).append((start, end))

    assert len(per_unit) == 2, "both rows ran"
    for unit_key, by_stage in per_unit.items():
        stages = sorted(by_stage)
        assert len(stages) > 1, "the table has more than one stage"
        for stage, nxt in zip(stages, stages[1:], strict=False):
            latest_end = max(e for _, e in by_stage[stage])
            earliest_start = min(s for s, _ in by_stage[nxt])
            assert earliest_start >= latest_end, (
                f"in {unit_key}, stage {nxt} began before stage {stage} finished"
            )


def test_upstream_answers_are_present_for_every_downstream_prompt(ready, monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_CONCURRENCY", "8")
    filler = RecordingFiller()
    run_id = create_run(ready, "01", RunScope(), model="stub")
    execute_run(ready, run_id, filler=filler)

    chain = [c for c in filler.calls if c.column_name == "Chain Completeness"]
    assert chain, "the column ran"
    for call in chain:
        assert "Documents in Unit" in call.established
        assert call.established["Documents in Unit"], "the upstream value was not empty"


def test_calls_actually_overlap(ready, monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_CONCURRENCY", "6")
    filler = RecordingFiller(delay=0.05)
    run_id = create_run(ready, "01", RunScope(), model="stub")
    execute_run(ready, run_id, filler=filler)
    assert filler.peak > 1, "more than one call was in flight"
    assert len(filler.threads) > 1


def test_concurrency_one_is_fully_serial(ready, monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_CONCURRENCY", "1")
    filler = RecordingFiller()
    run_id = create_run(ready, "01", RunScope(), model="stub")
    execute_run(ready, run_id, filler=filler)
    assert filler.peak == 1


def test_the_first_call_of_a_unit_runs_alone(ready, monkeypatch):
    """It populates the prompt cache; firing the whole stage at once would miss it."""
    monkeypatch.setenv("DILIGENCE_KERNEL_CONCURRENCY", "6")
    filler = RecordingFiller(delay=0.05)
    run_id = create_run(ready, "01", RunScope(), model="stub")
    execute_run(ready, run_id, filler=filler)

    ordered = sorted(filler.spans, key=lambda s: s[3])
    first_end = ordered[0][4]
    second_start = ordered[1][3]
    assert second_start >= first_end, "the opening call did not run alone"


# --- results are unchanged by concurrency ------------------------------------------------


def test_the_same_cells_are_produced_as_when_serial(loaded, dataroom, monkeypatch):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")

    def fill_all(concurrency: str) -> dict[tuple[int, str], str]:
        monkeypatch.setenv("DILIGENCE_KERNEL_CONCURRENCY", concurrency)
        loaded.execute("DELETE FROM cell")
        loaded.commit()
        run_id = create_run(loaded, "01", RunScope(refill=True), model="stub")
        execute_run(loaded, run_id, filler=StubFiller())
        return {
            (r["unit_id"], r["name"]): r["value"]
            for r in loaded.execute(
                """SELECT cell.unit_id, c.name, cell.value FROM cell
                   JOIN column_def c ON c.id = cell.column_id"""
            )
        }

    assert fill_all("1") == fill_all("8")


def test_a_failure_in_a_stage_does_not_stop_the_rest(ready, monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_CONCURRENCY", "4")

    class Flaky(RecordingFiller):
        def fill(self, request, *, system):
            if request.column_name == "Governing Law":
                raise RuntimeError("provider said no")
            return super().fill(request, system=system)

    run_id = create_run(ready, "01", RunScope(), model="stub")
    summary, findings = execute_run(ready, run_id, filler=Flaky())

    assert summary["cells_failed"] == 2, "one per unit"
    assert summary["cells_done"] == summary["cells_total"] - 2
    assert any(f.code == "CELL_FILL_FAILED" for f in findings)


def test_cache_tokens_are_recorded(ready, monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_CONCURRENCY", "4")
    run_id = create_run(ready, "01", RunScope(), model="stub")
    summary, _ = execute_run(ready, run_id, filler=RecordingFiller())
    assert summary["cache_read_tokens"] > 0, "cached input is measured, not inferred"
    assert summary["concurrency"] == 4
    per_cell = ready.execute("SELECT SUM(cache_read_tokens) AS n FROM cell").fetchone()["n"]
    assert per_cell == summary["cache_read_tokens"]


# --- configuration ---------------------------------------------------------------------------


def test_concurrency_is_configurable(monkeypatch):
    monkeypatch.delenv("DILIGENCE_KERNEL_CONCURRENCY", raising=False)
    assert configured_concurrency() == DEFAULT_CONCURRENCY
    monkeypatch.setenv("DILIGENCE_KERNEL_CONCURRENCY", "12")
    assert configured_concurrency() == 12
    monkeypatch.setenv("DILIGENCE_KERNEL_CONCURRENCY", "0")
    assert configured_concurrency() == 1, "never zero"
    monkeypatch.setenv("DILIGENCE_KERNEL_CONCURRENCY", "nonsense")
    assert configured_concurrency() == DEFAULT_CONCURRENCY
