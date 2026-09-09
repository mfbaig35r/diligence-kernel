"""Cost must be knowable before it is paid. These cover the free estimate path."""

from __future__ import annotations

import pytest

from diligence_kernel.engine.llm import CellFiller
from diligence_kernel.engine.providers import (
    AnthropicProvider,
    OpenAIProvider,
    PromptPrefix,
    ProviderUnavailable,
    estimate_cost,
    get_provider,
)
from diligence_kernel.engine.runner import RunScope, create_run, execute_run, preview_run
from diligence_kernel.vault.ingest import ingest_path
from diligence_kernel.vault.units import assemble_units

from .stub import StubFiller
from .test_pipeline import _classify


def test_openai_is_the_default_provider(monkeypatch):
    monkeypatch.delenv("DILIGENCE_KERNEL_PROVIDER", raising=False)
    assert get_provider().name == "openai"
    assert get_provider("anthropic").name == "anthropic"


def test_provider_comes_from_the_environment(monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_PROVIDER", "anthropic")
    assert get_provider().name == "anthropic"


def test_unknown_provider_is_refused():
    with pytest.raises(ProviderUnavailable):
        get_provider("bedrock")


def test_pricing_is_per_provider():
    openai, anthropic = OpenAIProvider(), AnthropicProvider()
    assert openai.pricing("gpt-5.4").input == 2.50
    assert openai.pricing("gpt-5.4").output == 15.00
    assert anthropic.pricing("claude-opus-5").input == 5.00
    # A model the table does not carry reports unknown rather than a stale guess.
    assert openai.pricing("gpt-7-imaginary") is None
    assert estimate_cost(openai, "gpt-7-imaginary", input_tokens=1000, output_tokens=100) is None


def test_cached_input_and_cache_writes_are_per_model():
    """The published rates differ; a single provider-wide multiplier would be wrong."""
    openai = OpenAIProvider()
    # gpt-5.4 does not charge separately for a cache write; gpt-5.6-terra does.
    assert openai.pricing("gpt-5.4").cache_write is None
    assert openai.pricing("gpt-5.6-terra").cache_write == 2.50
    assert openai.pricing("gpt-5.6-terra").cached_input == 0.20

    free_write = estimate_cost(
        openai, "gpt-5.4", input_tokens=0, output_tokens=0, cache_write_tokens=10_000
    )
    paid_write = estimate_cost(
        openai, "gpt-5.6-terra", input_tokens=0, output_tokens=0, cache_write_tokens=10_000
    )
    assert free_write == 0.0
    assert paid_write == pytest.approx(0.025)


def test_long_context_is_priced_at_its_own_rate():
    from diligence_kernel.engine.providers import LONG_CONTEXT_THRESHOLD

    openai = OpenAIProvider()
    short = estimate_cost(openai, "gpt-5.4", input_tokens=1_000, output_tokens=0)
    long = estimate_cost(
        openai, "gpt-5.4", input_tokens=LONG_CONTEXT_THRESHOLD + 1_000, output_tokens=0
    )
    assert short == pytest.approx(1_000 * 2.50 / 1e6), "short-context input rate"
    assert long == pytest.approx((LONG_CONTEXT_THRESHOLD + 1_000) * 5.00 / 1e6), "double, above"

    # A model with no long-context rates keeps its single rate at any size.
    flat = AnthropicProvider()
    a = estimate_cost(flat, "claude-opus-5", input_tokens=1_000, output_tokens=0)
    b = estimate_cost(flat, "claude-opus-5", input_tokens=1_000_000, output_tokens=0)
    assert b == pytest.approx(a * 1000)


def test_an_operator_can_price_an_unlisted_model(monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_PRICE_IN", "3.0")
    monkeypatch.setenv("DILIGENCE_KERNEL_PRICE_OUT", "12.0")
    cost = estimate_cost(
        OpenAIProvider(), "gpt-6-astra", input_tokens=1_000_000, output_tokens=1_000_000
    )
    assert cost == pytest.approx(15.0)


def test_cost_is_linear_in_tokens():
    """Below the long-context threshold, where ordinary review units live."""
    p = OpenAIProvider()
    assert estimate_cost(p, "gpt-5.4", input_tokens=10_000, output_tokens=0) == pytest.approx(0.025)
    assert estimate_cost(p, "gpt-5.4", input_tokens=0, output_tokens=10_000) == pytest.approx(0.15)


def test_cached_reads_are_cheaper_than_fresh_input():
    for provider, model in (
        (OpenAIProvider(), "gpt-5.4"),
        (AnthropicProvider(), "claude-opus-5"),
    ):
        fresh = estimate_cost(provider, model, input_tokens=1_000_000, output_tokens=0)
        cached = estimate_cost(
            provider, model, input_tokens=0, output_tokens=0, cache_read_tokens=1_000_000
        )
        assert cached == pytest.approx(fresh * 0.1), "cached input is a tenth of fresh"


def test_anthropic_cache_writes_cost_a_premium():
    a = AnthropicProvider()
    fresh = estimate_cost(a, "claude-opus-5", input_tokens=1_000_000, output_tokens=0)
    written = estimate_cost(
        a, "claude-opus-5", input_tokens=0, output_tokens=0, cache_write_tokens=1_000_000
    )
    assert written > fresh


def test_openai_counts_tokens_locally_without_credentials():
    """tiktoken means an OpenAI estimate needs no network and no key."""
    p = OpenAIProvider()
    n, exact = p.count_tokens(
        "gpt-5.4", PromptPrefix(text="The quick brown fox. " * 50, cache_key="k"), "x " * 20
    )
    assert n > 100
    assert exact is False, "local counting excludes request scaffolding, so it is approximate"


def test_filler_defaults_follow_the_provider(monkeypatch):
    monkeypatch.delenv("DILIGENCE_KERNEL_MODEL", raising=False)
    monkeypatch.delenv("DILIGENCE_KERNEL_EFFORT", raising=False)
    f = CellFiller(provider="openai")
    assert f.provider.name == "openai"
    assert f.model == OpenAIProvider.default_model
    assert f.effort == OpenAIProvider.default_effort

    a = CellFiller(provider="anthropic")
    assert a.model == AnthropicProvider.default_model
    assert a.effort == AnthropicProvider.default_effort


def test_preview_builds_the_requests_a_run_would_send(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")

    requests = preview_run(loaded, "01", RunScope(), filler=StubFiller())
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
    requests = preview_run(loaded, "01", RunScope(), filler=StubFiller())

    for unit_id in {r["unit_id"] for r in requests}:
        roles = [r["cache_role"] for r in requests if r["unit_id"] == unit_id]
        assert roles[0] == "write"
        assert set(roles[1:]) == {"read"}, "every later column of a unit reads the prefix"


def test_preview_costs_nothing_and_writes_nothing(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")
    before = loaded.execute("SELECT COUNT(*) AS n FROM cell").fetchone()["n"]
    preview_run(loaded, "01", RunScope(), filler=StubFiller())
    after = loaded.execute("SELECT COUNT(*) AS n FROM cell").fetchone()["n"]
    assert before == after == 0
    assert loaded.execute("SELECT COUNT(*) AS n FROM run").fetchone()["n"] == 0


def test_preview_skips_what_a_run_would_skip(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")
    run_id = create_run(loaded, "01", RunScope(), model="stub")
    execute_run(loaded, run_id, filler=StubFiller())

    assert preview_run(loaded, "01", RunScope(), filler=StubFiller()) == [], (
        "filled cells cost nothing to skip"
    )
    assert len(preview_run(loaded, "01", RunScope(refill=True), filler=StubFiller())) == 54

    loaded.execute("UPDATE cell SET locked = 1")
    loaded.commit()
    assert preview_run(loaded, "01", RunScope(refill=True), filler=StubFiller()) == []


def test_preview_scope_narrows_the_estimate(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")
    unit_id = loaded.execute("SELECT id FROM review_unit LIMIT 1").fetchone()["id"]
    requests = preview_run(
        loaded,
        "01",
        RunScope(unit_ids=[unit_id], column_names=["Governing Law"]),
        filler=StubFiller(),
    )
    assert len(requests) == 1
    assert requests[0]["column"] == "Governing Law"


def test_preview_on_an_unknown_table_is_an_error(loaded):
    from diligence_kernel.findings import KernelError

    with pytest.raises(KernelError):
        preview_run(loaded, "99", RunScope(), filler=StubFiller())


def test_run_estimate_tool_reports_cost_without_spending(loaded, dataroom, monkeypatch):
    from diligence_kernel import server

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    server.set_conn(loaded)
    try:
        ingest_path(loaded, dataroom)
        _classify(loaded)
        assemble_units(loaded, "01")

        out = server.run_estimate("01", model="gpt-5.4")
        assert out["provider"] == "openai"
        assert out["cells"] == 54
        assert out["rows"] == 2
        assert out["input_tokens"] > 0
        assert out["estimated_cost_usd"] is not None
        assert out["estimated_cost_without_caching_usd"] >= out["estimated_cost_usd"]
        assert loaded.execute("SELECT COUNT(*) AS n FROM run").fetchone()["n"] == 0

        # OpenAI counts locally, so an estimate works with no key and no network.
        assert out["token_counts_exact"] is False
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

        out = server.run_estimate("01", model="gpt-5.4")
        assert out["cells"] == 0
        assert any(f["code"] == "NOTHING_TO_RUN" for f in out["findings"])
    finally:
        server.set_conn(None)
