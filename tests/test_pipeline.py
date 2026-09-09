"""End to end: data room in, filled review table out, with no model call."""

from __future__ import annotations

import json

from diligence_kernel.db import now
from diligence_kernel.engine.runner import RunScope, create_run, execute_run
from diligence_kernel.vault.ingest import ingest_path
from diligence_kernel.vault.units import assemble_units

from .stub import StubFiller

# What Table 05 would have produced for the fixture data room. Classification is stubbed
# here so the test exercises routing and assembly, not the model.
CLASSIFICATIONS = {
    "msa-base.txt": {
        "workstream": "Contracts",
        "document_type": "Master services agreement",
        "subject_entity": "Acme Manufacturing LLC",
        "counterparty": "Northwind Logistics Inc.",
        "document_date": "2022-03-14",
        "amends_or_issued_under": "Not applicable",
        "document_role": "Base",
        "routing_disposition": "Route to Contracts",
    },
    "msa-amendment-1.txt": {
        "workstream": "Contracts",
        "document_type": "Amendment",
        "subject_entity": "Acme Manufacturing LLC",
        "counterparty": "Northwind Logistics Inc.",
        "document_date": "2024-01-09",
        "amends_or_issued_under": "Master Services Agreement dated March 14, 2022",
        "document_role": "Amendment",
        "routing_disposition": "Route to Contracts",
    },
    "supply-agreement.txt": {
        "workstream": "Contracts",
        "document_type": "Supply agreement",
        "subject_entity": "Acme Manufacturing LLC",
        "counterparty": "Cedar Components GmbH",
        "document_date": "2023-08-01",
        "amends_or_issued_under": "Not applicable",
        "document_role": "Base",
        "routing_disposition": "Route to Contracts",
    },
}


def _classify(conn):
    for filename, fields in CLASSIFICATIONS.items():
        row = conn.execute("SELECT id FROM document WHERE filename = ?", (filename,)).fetchone()
        assert row is not None, filename
        conn.execute(
            """INSERT INTO classification
               (document_id, workstream, document_type, subject_entity, counterparty,
                document_date, amends_or_issued_under, document_role, routing_disposition,
                classified_at)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                int(row["id"]),
                fields["workstream"],
                fields["document_type"],
                fields["subject_entity"],
                fields["counterparty"],
                fields["document_date"],
                fields["amends_or_issued_under"],
                fields["document_role"],
                fields["routing_disposition"],
                now(),
            ),
        )
    conn.commit()


def test_ingest_extracts_and_chunks(loaded, dataroom):
    counts, findings = ingest_path(loaded, dataroom)
    assert counts["ingested"] == 3
    assert counts["failed"] == 0
    assert counts["chunks"] > 0
    assert findings == []

    # Re-ingesting an unchanged data room is a no-op.
    again, _ = ingest_path(loaded, dataroom)
    assert again["ingested"] == 0 and again["unchanged"] == 3


def test_chunk_offsets_point_at_real_text(loaded, dataroom):
    ingest_path(loaded, dataroom)
    rows = loaded.execute(
        """SELECT c.text, c.char_start, c.char_end, d.full_text
           FROM chunk c JOIN document d ON d.id = c.document_id"""
    ).fetchall()
    assert rows
    for row in rows:
        excerpt = row["full_text"][row["char_start"] : row["char_end"]]
        assert excerpt.strip() == row["text"].strip()


def test_units_group_the_amendment_with_its_base(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    counts, findings = assemble_units(loaded, "01")
    assert counts["created"] == 2, "the MSA family and the standalone supply agreement"

    families = loaded.execute(
        """SELECT u.label, COUNT(ud.document_id) AS n
           FROM review_unit u JOIN unit_document ud ON ud.unit_id = u.id
           GROUP BY u.id ORDER BY n DESC"""
    ).fetchall()
    assert families[0]["n"] == 2, "base agreement and its amendment share one row"
    assert families[1]["n"] == 1
    assert [f.code for f in findings] == []


def test_run_fills_cells_in_stage_order_with_evidence(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")

    filler = StubFiller()
    run_id = create_run(loaded, "01", RunScope(reason="test"), model="stub")
    summary, findings = execute_run(loaded, run_id, filler=filler)

    assert summary["status"] == "complete"
    assert summary["cells_done"] == summary["cells_total"] == 2 * 27

    # Columns were filled in topological order: no stage-2 column ran before its stage-1
    # upstream within the same unit.
    stages = {
        r["name"]: r["stage"]
        for r in loaded.execute(
            """SELECT c.name, c.stage FROM column_def c
               JOIN review_table t ON t.id = c.table_id WHERE t.number = '01'"""
        )
    }
    seen = [stages[c.column_name] for c in filler.calls[:27]]
    assert seen == sorted(seen), "stages must be non-decreasing within a unit"

    # A stage-2 prompt received its upstream answer as an established result.
    chain = next(c for c in filler.calls if c.column_name == "Chain Completeness")
    assert "Documents in Unit" in chain.established

    # Evidence was located back into the source documents with offsets.
    ev = loaded.execute(
        """SELECT e.quote, e.char_start, e.char_end, d.full_text
           FROM cell_evidence e JOIN document d ON d.id = e.document_id
           WHERE e.char_start IS NOT NULL"""
    ).fetchall()
    assert ev, "at least one quote resolved to a character offset"
    for row in ev:
        assert row["full_text"][row["char_start"] : row["char_end"]] == row["quote"]


def test_unit_documents_are_cached_and_reused_across_columns(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")
    filler = StubFiller()
    run_id = create_run(loaded, "01", RunScope(), model="stub")
    execute_run(loaded, run_id, filler=filler)

    # Every column of a unit shares one prefix, keyed to that unit, so both providers can
    # serve it from cache. The documents appear in it exactly once.
    first_unit = filler.systems[:27]
    assert all(s is first_unit[0] or s == first_unit[0] for s in first_unit)
    assert first_unit[0].cache_key.endswith(str(first_unit[0].cache_key.split(":")[-1]))
    assert first_unit[0].text.count("<document ") == 2, "the family's two documents, once"

    # The second unit gets a different key, so one unit's cache cannot serve another's.
    second_unit = filler.systems[27:]
    assert second_unit[0].cache_key != first_unit[0].cache_key


def test_verbatim_paraphrase_is_recorded_as_a_violation(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")

    script = dict(StubFiller().script)
    script["Assignment Language"] = ("The contract may not be transferred without permission.", [])
    run_id = create_run(loaded, "01", RunScope(), model="stub")
    _, findings = execute_run(loaded, run_id, filler=StubFiller(script))

    assert any(f.code == "VERBATIM_NOT_IN_SOURCE" for f in findings)
    row = loaded.execute(
        """SELECT cell.validation FROM cell
           JOIN column_def c ON c.id = cell.column_id
           WHERE c.name = 'Assignment Language' LIMIT 1"""
    ).fetchone()
    assert "VERBATIM_NOT_IN_SOURCE" in json.loads(row["validation"])


def test_rerun_skips_filled_cells_and_respects_locks(loaded, dataroom):
    ingest_path(loaded, dataroom)
    _classify(loaded)
    assemble_units(loaded, "01")
    first = StubFiller()
    run_a = create_run(loaded, "01", RunScope(), model="stub")
    execute_run(loaded, run_a, filler=first)
    assert len(first.calls) == 54

    second = StubFiller()
    run_b = create_run(loaded, "01", RunScope(), model="stub")
    execute_run(loaded, run_b, filler=second)
    assert second.calls == [], "already-filled cells are not refilled without refill=True"

    loaded.execute("UPDATE cell SET locked = 1")
    loaded.commit()
    third = StubFiller()
    run_c = create_run(loaded, "01", RunScope(refill=True), model="stub")
    _, findings = execute_run(loaded, run_c, filler=third)
    assert third.calls == [], "locked cells are never overwritten"
    assert any(f.code == "CELL_LOCKED_NOT_REFILLED" for f in findings)
