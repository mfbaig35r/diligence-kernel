"""The tool surface, exercised as a client would reach it."""

from __future__ import annotations

import pytest

from diligence_kernel import server
from diligence_kernel.engine import runner

from .conftest import INGESTED
from .stub import StubFiller
from .test_pipeline import _classify


@pytest.fixture
def wired(conn, corpus_root, monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_CORPUS", str(corpus_root))
    server.set_conn(conn)
    yield conn
    server.set_conn(None)


def test_matter_open_loads_the_corpus(wired):
    out = server.matter_open("Project Cedar", side="buy", as_of_date="2026-09-01")
    assert out["matter"] == "Project Cedar"
    assert out["corpus_load"]["tables"] == 24
    assert out["corpus_load"]["columns"] == 591
    assert out["finding_count"] == 0


def test_matter_open_refuses_a_second_matter_in_one_file(wired):
    server.matter_open("Project Cedar")
    out = server.matter_open("Project Birch")
    assert "error" in out
    assert "one database file" in out["error"]


def test_unknown_table_returns_an_error_not_a_traceback(wired):
    server.matter_open("Project Cedar")
    out = server.table_describe("99")
    assert out["error"].startswith("Table 99 is not loaded")


def test_table_describe_reports_stages_options_and_caveats(wired):
    server.matter_open("Project Cedar")
    out = server.table_describe("01")
    assert out["grouping_enabled"] is True
    assert out["max_docs_per_unit"] == 25
    assert len(out["columns"]) == 27
    chain = next(c for c in out["columns"] if c["name"] == "Chain Completeness")
    assert chain["native_type"] == "Classify"
    assert chain["stage"] == 2
    assert "Sequence gap" in chain["configured_options"]
    verbatim = next(c for c in out["columns"] if c["name"] == "Assignment Language")
    assert verbatim["type_caveat"], "the untested-Verbatim caveat is surfaced, not dropped"


def test_paired_tables_are_reported(wired):
    server.matter_open("Project Cedar")
    out = server.table_describe("03")
    assert any(f["code"] == "TABLE_MUST_PAIR" for f in out["findings"])


def test_columns_find_searches_the_whole_corpus(wired):
    server.matter_open("Project Cedar")
    out = server.columns_find("change of control")
    tables = {c["table"][:2] for c in out["columns"]}
    assert len(tables) > 1, "the concept appears in more than one table"

    typed = server.columns_find("date", native_type="Verbatim")
    assert all(c["native_type"] == "Verbatim" for c in typed["columns"])


def test_column_prompt_returns_text_and_edges(wired):
    server.matter_open("Project Cedar")
    out = server.column_prompt("01", "chain completeness")
    assert "## Task" in out["prompt_text"]
    assert out["upstream"] == ["Documents in Unit"]


def test_ingest_search_and_review_round_trip(wired, dataroom, monkeypatch):
    server.matter_open("Project Cedar", as_of_date="2026-09-01")
    ing = server.vault_ingest(str(dataroom))
    assert ing["ingested"] == INGESTED

    status = server.matter_status()
    assert status["documents"]["extracted"] == INGESTED
    assert any(f["code"] == "DOCUMENTS_UNROUTED" for f in status["findings"])

    _classify(wired)
    assert server.units_assemble("01")["created"] == 2

    # Fill with the stub rather than the model.
    real = runner.execute_run
    monkeypatch.setattr(
        runner,
        "execute_run",
        lambda c, rid, filler=None, progress=None: real(c, rid, filler=StubFiller()),
    )
    monkeypatch.setattr("diligence_kernel.service.execute_run", runner.execute_run)
    run = server.run_table("01", reason="first pass")
    assert run["status"] == "complete"
    assert run["cells_done"] == 54

    read = server.table_read("01", columns=["Governing Law", "Chain Completeness"])
    assert read["row_count"] == 2
    unit_id = read["rows"][0]["unit_id"]
    assert read["rows"][0]["cells"]["Governing Law"]["value"] == "New York"

    ev = server.cell_evidence(unit_id, "Governing Law")
    assert ev["evidence"], "the cell names the sentence it came from"
    assert ev["evidence"][0]["char_start"] is not None

    server.cell_review(
        unit_id,
        "Governing Law",
        review_status="Verified",
        materiality="Material",
        reviewed_by="FB",
        lock=True,
    )
    after = server.table_read("01", columns=["Governing Law"])
    cell = after["rows"][0]["cells"]["Governing Law"]
    assert cell["review_status"] == "Verified" and cell["materiality"] == "Material"

    issues = server.artifact_build("issues_list")
    assert issues["row_count"] == 1
    assert issues["rows"][0]["column"] == "Governing Law"


def test_artifacts_report_unreviewed_rows(wired, dataroom, monkeypatch):
    server.matter_open("Project Cedar")
    server.vault_ingest(str(dataroom))
    _classify(wired)
    server.units_assemble("01")
    real = runner.execute_run
    monkeypatch.setattr(
        "diligence_kernel.service.execute_run",
        lambda c, rid, filler=None, progress=None: real(c, rid, filler=StubFiller()),
    )
    server.run_table("01")

    out = server.artifact_build("chain_gaps")
    assert out["row_count"] == 2, "both units were scripted with a referenced-but-absent amendment"
    assert any(f["code"] == "ARTIFACT_CARRIES_UNREVIEWED_CELLS" for f in out["findings"])


def test_artifact_list_names_every_artifact(wired):
    server.matter_open("Project Cedar")
    keys = {a["key"] for a in server.artifact_list()["artifacts"]}
    assert {"consent_schedule", "coverage_register", "issues_list", "chain_gaps"} <= keys
