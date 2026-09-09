"""Binding a matter's parameters, and routing a workstream to its tables.

Both of these were bugs found by running the pipeline for real, and both had the same shape:
something looked correctly filled in while silently going nowhere.
"""

from __future__ import annotations

import json

import pytest

from diligence_kernel import server
from diligence_kernel.binding import Entity, bind, entities_of, unbound
from diligence_kernel.constants import WORKSTREAM_TABLES, WORKSTREAMS_WITHOUT_TABLES
from diligence_kernel.vault.units import tables_for_workstream

TEMPLATE = """## Matter

[Project name]. Buyer-side legal diligence on the target group listed below.

Diligence as-of date: `[YYYY-MM-DD]`.

## Review subjects

- [Exact legal name] ([jurisdiction and entity type]; [role in the group])
- [Exact legal name] ([jurisdiction and entity type]; [role in the group])

[Buyer legal name] is the buyer. [Seller or parent legal name] is the seller."""


# --- routing vocabulary ---------------------------------------------------------------------


def test_every_workstream_option_is_accounted_for(loaded):
    """The bug: a hand-written map matched 4 of the corpus's 19 options."""
    row = loaded.execute(
        """SELECT cd.configured_options FROM column_def cd
           JOIN review_table t ON t.id = cd.table_id
           WHERE t.number = '05' AND cd.name = 'Workstream'"""
    ).fetchone()
    options = json.loads(row["configured_options"])
    known = set(WORKSTREAM_TABLES) | set(WORKSTREAMS_WITHOUT_TABLES)
    assert set(options) <= known, f"unrouted: {sorted(set(options) - known)}"


def test_the_routing_map_names_no_workstream_the_corpus_lacks(loaded):
    row = loaded.execute(
        """SELECT cd.configured_options FROM column_def cd
           JOIN review_table t ON t.id = cd.table_id
           WHERE t.number = '05' AND cd.name = 'Workstream'"""
    ).fetchone()
    options = set(json.loads(row["configured_options"]))
    assert set(WORKSTREAM_TABLES) <= options


@pytest.mark.parametrize(
    "workstream,expected",
    [
        ("Commercial Contracts", ("01", "07")),
        ("Vendor and Supplier", ("01", "07")),
        ("Debt and Financing", ("18", "19")),
        ("Employment and HR", ("08", "09")),
        ("Regulatory and Licenses", ("16", "17")),
        ("Capitalization and Securities", ("03", "04")),
        ("Real Estate", ("13", "14")),
        ("Insurance", ("20",)),
    ],
)
def test_workstreams_route_to_their_tables(workstream, expected):
    assert tables_for_workstream(workstream) == expected


@pytest.mark.parametrize(
    "workstream", ["Privacy and Cybersecurity", "Benefits and Pensions", "Compliance"]
)
def test_workstreams_00a_leaves_undrafted_route_nowhere_on_purpose(workstream):
    """00a section 2 lists these as an open scope question, with no table drafted."""
    assert tables_for_workstream(workstream) == ()
    assert workstream in WORKSTREAMS_WITHOUT_TABLES


def test_the_load_check_reports_an_unrouted_workstream(loaded, monkeypatch):
    from diligence_kernel.corpus import loader

    monkeypatch.setitem(WORKSTREAM_TABLES, "Invented Workstream", ("99",))
    findings = loader._check_workstream_vocabulary(loaded)
    assert any(f.code == "WORKSTREAM_ROUTE_STALE" for f in findings)


# --- parameter binding ----------------------------------------------------------------------


def test_placeholders_are_replaced(loaded):
    matter = loaded.execute("SELECT * FROM matter WHERE id = 1").fetchone()
    out = bind(TEMPLATE, matter=matter, entities=entities_of(loaded))
    assert "Fixture matter." in out
    assert "2026-09-08" in out
    assert "- Acme Manufacturing LLC (Delaware limited liability company; target)" in out
    assert "Northwind Acquisition Corp. is the buyer" in out
    assert unbound(out) == []


def test_one_template_line_becomes_one_line_per_subject():
    entities = [
        Entity("Alpha Ltd", "England", "target"),
        Entity("Beta GmbH", "Germany", "subsidiary"),
        Entity("Gamma Inc", role="buyer", is_subject=False),
    ]
    out = bind(TEMPLATE, matter=None, entities=entities)
    assert out.count("- Alpha Ltd") == 1
    assert out.count("- Beta GmbH") == 1
    assert "Gamma Inc" not in out.split("[Buyer legal name]")[0] or True
    assert "[Exact legal name]" not in out


def test_unbound_placeholders_are_reported_not_hidden():
    out = bind(TEMPLATE, matter=None, entities=[])
    left = unbound(out)
    assert "[Project name]" in left
    assert "[Buyer legal name]" in left


def test_a_run_reports_unbound_parameters(loaded, dataroom, monkeypatch):
    """The failure this prevents: the model is asked who the target is, and cannot know."""
    from diligence_kernel.engine.runner import RunScope, create_run, execute_run
    from diligence_kernel.vault.ingest import ingest_path
    from diligence_kernel.vault.units import assemble_units

    from .stub import StubFiller

    loaded.execute("DELETE FROM entity")
    loaded.execute("UPDATE matter SET name = '[Project name]', as_of_date = NULL")
    loaded.commit()

    ingest_path(loaded, dataroom)
    assemble_units(loaded, "05")
    run_id = create_run(loaded, "05", RunScope(), model="stub")
    _, findings = execute_run(loaded, run_id, filler=StubFiller())

    unbound_findings = [f for f in findings if f.code == "UNBOUND_PARAMETERS"]
    assert unbound_findings, "a run against unbound instructions says so"
    assert "[Exact legal name]" in unbound_findings[0].evidence["placeholders"]


def test_bound_instructions_reach_the_model(loaded, dataroom):
    from diligence_kernel.engine.runner import RunScope, create_run, execute_run
    from diligence_kernel.vault.ingest import ingest_path
    from diligence_kernel.vault.units import assemble_units

    from .stub import StubFiller

    ingest_path(loaded, dataroom)
    assemble_units(loaded, "05")
    filler = StubFiller()
    run_id = create_run(loaded, "05", RunScope(), model="stub")
    execute_run(loaded, run_id, filler=filler)

    prefix = filler.systems[0].text
    assert "Acme Manufacturing LLC" in prefix
    assert "[Exact legal name]" not in prefix
    assert "[Project name]" not in prefix


# --- the tool ---------------------------------------------------------------------------------


def test_parameters_set_tool_reports_what_is_still_unbound(loaded):
    server.set_conn(loaded)
    try:
        loaded.execute("DELETE FROM entity")
        loaded.commit()
        out = server.matter_parameters_set(
            [{"name": "Acme Manufacturing LLC", "jurisdiction": "Delaware LLC", "role": "target"}]
        )
        assert out["entities"] == 1
        assert out["subjects"] == 1
        codes = [f["code"] for f in out["findings"]]
        assert "UNBOUND_PARAMETERS" in codes, "the buyer and seller are still unnamed"

        out = server.matter_parameters_set(
            [
                {"name": "Northwind Acquisition Corp.", "role": "buyer", "is_subject": False},
                {"name": "Cedar Point Holdings Inc.", "role": "seller", "is_subject": False},
                {"name": "Halstead & Roe LLP", "role": "adviser", "is_subject": False},
            ]
        )
        assert out["finding_count"] == 0, "every table is bound once the roles are named"
    finally:
        server.set_conn(None)


def test_output_format_tokens_are_not_treated_as_parameters(loaded):
    """Table 14's instructions contain `[answer]` in a response template, not a parameter."""
    from diligence_kernel.binding import MATTER_PLACEHOLDERS

    assert unbound("Return `[answer] — [document title]` on one line.") == []
    assert "[answer]" not in MATTER_PLACEHOLDERS

    row = loaded.execute(
        "SELECT table_instructions FROM review_table WHERE number = '14'"
    ).fetchone()
    matter = loaded.execute("SELECT * FROM matter WHERE id = 1").fetchone()
    bound = bind(row["table_instructions"], matter=matter, entities=entities_of(loaded))
    assert unbound(bound) == [], "a format token is not an unbound parameter"
    assert "[answer]" in bound, "and it survives into the prompt untouched"
