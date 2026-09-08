"""Table 05 routes the whole vault. This is the loop from raw files to a routed data room."""

from __future__ import annotations

from diligence_kernel import server
from diligence_kernel.engine import runner
from diligence_kernel.vault.ingest import ingest_path
from diligence_kernel.vault.units import assemble_units, documents_in_scope

from .stub import StubFiller

# What Table 05 would return for the fixture data room, keyed by column name. The stub
# returns the same values for every row, so the per-file assertions below use the columns
# that do not vary.
INTAKE_SCRIPT = {
    "Workstream": ("Contracts", []),
    "Document Type": ("Master services agreement", []),
    "Document Role": ("Operative instrument", []),
    "Subject Entity": ("Acme Manufacturing LLC", []),
    "Counterparty": ("Northwind Logistics Inc.", []),
    "Document Date": ("2022-03-14", []),
    "Amends or Issued Under": ("Not applicable", []),
    "Routing Disposition": ("Route to workstream table", []),
    "Language": ("English", []),
}


def test_intake_runs_over_every_file_before_any_classification_exists(loaded, dataroom):
    ingest_path(loaded, dataroom)
    scope = documents_in_scope(loaded, "05")
    assert len(scope) == 3, "intake sees every extracted file, classified or not"

    counts, findings = assemble_units(loaded, "05")
    assert counts["created"] == 3, "intake is per file, one row each"
    assert findings == []


def test_running_intake_populates_the_classification_routing_table(loaded, dataroom, monkeypatch):
    server.set_conn(loaded)
    try:
        ingest_path(loaded, dataroom)
        assemble_units(loaded, "05")

        real = runner.execute_run
        monkeypatch.setattr(
            "diligence_kernel.service.execute_run",
            lambda c, rid, filler=None, progress=None: real(
                c, rid, filler=StubFiller(INTAKE_SCRIPT)
            ),
        )
        out = server.run_table("05")
        assert out["status"] == "complete"
        assert out["cells_done"] == 3 * 20
        assert out["classified"] == 3

        rows = loaded.execute(
            "SELECT workstream, document_type, routing_disposition FROM classification"
        ).fetchall()
        assert len(rows) == 3
        assert {r["workstream"] for r in rows} == {"Contracts"}

        # Routing now works: the contracts tables can see the files.
        assert len(documents_in_scope(loaded, "01")) == 3
        assert len(documents_in_scope(loaded, "24")) == 0, "tax sees nothing"
    finally:
        server.set_conn(None)


def test_fallback_states_do_not_project_as_values(loaded, dataroom, monkeypatch):
    server.set_conn(loaded)
    try:
        ingest_path(loaded, dataroom)
        assemble_units(loaded, "05")
        script = dict(INTAKE_SCRIPT)
        script["Workstream"] = ("Unable to determine", [])
        real = runner.execute_run
        monkeypatch.setattr(
            "diligence_kernel.service.execute_run",
            lambda c, rid, filler=None, progress=None: real(c, rid, filler=StubFiller(script)),
        )
        out = server.run_table("05")

        assert any(f["code"] == "DOCUMENT_WITHOUT_WORKSTREAM" for f in out["findings"])
        row = loaded.execute("SELECT workstream FROM classification LIMIT 1").fetchone()
        assert row["workstream"] is None, "`Unable to determine` is not a workstream"
        assert documents_in_scope(loaded, "01") == []
    finally:
        server.set_conn(None)
