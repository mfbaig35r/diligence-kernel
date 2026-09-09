"""Cost must be knowable before it is paid. These cover the free estimate path."""

from __future__ import annotations

import pytest

from diligence_kernel.engine.llm import (
    CACHE_READ_MULTIPLIER,
    count_request_tokens,
    estimate_cost,
    price_of,
)
from diligence_kernel.engine.runner import RunScope, create_run, execute_run, preview_run
from diligence_kernel.vault.ingest import ingest_path
from diligence_kernel.vault.units import assemble_units

from .stub import StubFiller
from .test_pipeline import _classify


class CountingClient:
    """Stands in for the SDK's free token-counting endpoint."""

    def __init__(self) -> None:
        self.calls: list[dict] = []
        self.messages = self

    def count_tokens(self, *, model, system, messages):
        self.calls.append({"model": model, "system": system, "messages": messages})
        chars = sum(len(b["text"]) for b in system) + len(messages[0]["content"])
        return type("Counted", (), {"input_tokens": chars // 4})()


def test_pricing_is_known_for_the_default_model():
    assert price_of("claude-opus-5") == (5.00, 25.00)
    assert price_of("no-such-model") is None
    assert estimate_cost("no-such-model", input_tokens=1000, output_tokens=100) is None


def test_cost_is_linear_in_tokens():
    one = estimate_cost("claude-opus-5", input_tokens=1_000_000, output_tokens=0)
    assert one == pytest.approx(5.00)
    two = estimate_cost("claude-opus-5", input_tokens=0, output_tokens=1_000_000)
    assert two == pytest.approx(25.00)


def test_cached_reads_are_cheaper_than_fresh_input():
    fresh = estimate_cost("claude-opus-5", input_tokens=1_000_000, output_tokens=0)
    cached = estimate_cost(
        "claude-opus-5", input_tokens=0, output_tokens=0, cache_read_tokens=1_000_000
    )
    assert cached == pytest.approx(fresh * CACHE_READ_MULTIPLIER)


def test_count_request_tokens_sends_system_and_user(loaded):
    client = CountingClient()
    n = count_request_tokens(
        client, "claude-opus-5", [{"type": "text", "text": "abcd" * 10}], "x" * 40
    )
    assert n > 0
    assert client.calls[0]["model"] == "claude-opus-5"
    assert client.calls[0]["messages"][0]["role"] == "user"


def test_preview_builds_the_requests_a_run_would_send(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")

    requests = preview_run(loaded, "01", RunScope())
    assert len(requests) == 2 * 27, "two rows, twenty-seven columns"
    assert all(r["system"] and r["user"] for r in requests)
    assert "## Task" in requests[0]["user"]

    # Stage order is preserved, so an estimate reflects the run that would happen.
    stages = [r["stage"] for r in requests if r["unit_id"] == requests[0]["unit_id"]]
    assert stages == sorted(stages)


def test_preview_marks_one_cache_write_per_unit(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")
    requests = preview_run(loaded, "01", RunScope())

    for unit_id in {r["unit_id"] for r in requests}:
        roles = [r["cache_role"] for r in requests if r["unit_id"] == unit_id]
        assert roles[0] == "write"
        assert set(roles[1:]) == {"read"}, "every later column of a unit reads the prefix"


def test_preview_costs_nothing_and_writes_nothing(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")
    before = loaded.execute("SELECT COUNT(*) AS n FROM cell").fetchone()["n"]
    preview_run(loaded, "01", RunScope())
    after = loaded.execute("SELECT COUNT(*) AS n FROM cell").fetchone()["n"]
    assert before == after == 0
    assert loaded.execute("SELECT COUNT(*) AS n FROM run").fetchone()["n"] == 0


def test_preview_skips_what_a_run_would_skip(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")
    run_id = create_run(loaded, "01", RunScope(), model="stub")
    execute_run(loaded, run_id, filler=StubFiller())

    assert preview_run(loaded, "01", RunScope()) == [], "filled cells cost nothing to skip"
    assert len(preview_run(loaded, "01", RunScope(refill=True))) == 54

    loaded.execute("UPDATE cell SET locked = 1")
    loaded.commit()
    assert preview_run(loaded, "01", RunScope(refill=True)) == []


def test_preview_scope_narrows_the_estimate(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")
    unit_id = loaded.execute("SELECT id FROM review_unit LIMIT 1").fetchone()["id"]
    requests = preview_run(
        loaded, "01", RunScope(unit_ids=[unit_id], column_names=["Governing Law"])
    )
    assert len(requests) == 1
    assert requests[0]["column"] == "Governing Law"


def test_preview_on_an_unknown_table_is_an_error(loaded):
    from diligence_kernel.findings import KernelError

    with pytest.raises(KernelError):
        preview_run(loaded, "99", RunScope())


def test_run_estimate_tool_reports_cost_without_spending(loaded, dataroom, monkeypatch):
    from diligence_kernel import server

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    server.set_conn(loaded)
    try:
        ingest_path(loaded, dataroom)
        _classify(loaded)
        assemble_units(loaded, "01")

        out = server.run_estimate("01")
        assert out["cells"] == 54
        assert out["rows"] == 2
        assert out["input_tokens"] > 0
        assert out["estimated_cost_usd"] is not None
        assert out["estimated_cost_without_caching_usd"] >= out["estimated_cost_usd"]
        assert loaded.execute("SELECT COUNT(*) AS n FROM run").fetchone()["n"] == 0

        # With no credentials the figures are approximate, and it says so rather than failing.
        assert out["token_counts_exact"] is False
        assert any(f["code"] == "TOKENS_ESTIMATED_NOT_COUNTED" for f in out["findings"])
    finally:
        server.set_conn(None)


def test_run_estimate_reports_when_there_is_nothing_to_run(loaded, dataroom):
    from diligence_kernel import server

    server.set_conn(loaded)
    try:
        ingest_path(loaded, dataroom)
        _classify(loaded)
        assemble_units(loaded, "01")
        run_id = create_run(loaded, "01", RunScope(), model="stub")
        execute_run(loaded, run_id, filler=StubFiller())

        out = server.run_estimate("01")
        assert out["cells"] == 0
        assert any(f["code"] == "NOTHING_TO_RUN" for f in out["findings"])
    finally:
        server.set_conn(None)
