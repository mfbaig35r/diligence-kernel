"""The corpus is the schema. If it does not parse cleanly, nothing downstream is trustworthy."""

from __future__ import annotations

import json

from diligence_kernel.corpus.loader import compute_stages, load_corpus
from diligence_kernel.corpus.parser import (
    ColumnSpec,
    parse_corpus,
    parse_inventory,
    resolve_at_refs,
)

EXPECTED_TABLES = 24
EXPECTED_COLUMNS = 591


def test_every_inventory_parses_without_a_finding(corpus_root):
    specs, findings = parse_corpus(corpus_root)
    tables = [s for s in specs if s.is_table]
    assert len(tables) == EXPECTED_TABLES
    assert sum(len(s.columns) for s in tables) == EXPECTED_COLUMNS
    assert findings == [], [f.observation for f in findings]


def test_every_column_carries_a_prompt_and_a_type(corpus_root):
    specs, _ = parse_corpus(corpus_root)
    for spec in (s for s in specs if s.is_table):
        for col in spec.columns:
            assert col.prompt_text, f"{spec.number} {col.name}"
            assert col.native_type, f"{spec.number} {col.name}"
            assert "## Task" in col.prompt_text
            assert "## Output format" in col.prompt_text


def test_classify_columns_declare_their_options(corpus_root):
    specs, _ = parse_corpus(corpus_root)
    classify = [c for s in specs if s.is_table for c in s.columns if c.native_type == "Classify"]
    assert len(classify) == 152
    assert all(c.configured_options for c in classify)


def test_type_caveats_are_kept_not_discarded(corpus_root):
    """00a section 8 calls the untested-fallback notes load-bearing."""
    specs, _ = parse_corpus(corpus_root)
    caveats = [c for s in specs if s.is_table for c in s.columns if c.type_caveat]
    assert len(caveats) == 57
    assert all(c.native_type in {"Date", "Duration", "Verbatim", "Free Response"} for c in caveats)


def test_table_instructions_and_dependency_maps_survive_the_fence(corpus_root):
    specs, _ = parse_corpus(corpus_root)
    for spec in (s for s in specs if s.is_table):
        assert spec.table_instructions, spec.number
        assert spec.dependency_map, spec.number
        assert "```" not in spec.table_instructions


def test_contracts_core_shape(corpus_root):
    spec, findings = parse_inventory(corpus_root / "01-contracts-core-prompt-inventory.md")
    assert findings == []
    assert spec.number == "01"
    assert spec.grouping_enabled is True
    assert spec.max_docs_per_unit == 25
    assert len(spec.columns) == 27
    chain = next(c for c in spec.columns if c.name == "Chain Completeness")
    assert chain.native_type == "Classify"
    assert chain.upstream == ["Documents in Unit"]
    assert "Complete on its face" in chain.configured_options


def test_intake_is_per_file_and_ungrouped(corpus_root):
    spec, _ = parse_inventory(corpus_root / "05-intake-classification-prompt-inventory.md")
    assert spec.grouping_enabled is False
    assert len(spec.columns) == 20


def test_at_refs_resolve_through_em_dashes():
    names = ["Termination for Convenience — Holder", "Documents in Unit"]
    resolved, unresolved = resolve_at_refs(
        "Use @Termination for Convenience — Holder and @Documents in Unit.", names
    )
    assert set(resolved) == set(names)
    assert unresolved == []


def test_stage_order_follows_the_dependency_graph():
    columns = [
        ColumnSpec(1, "A", "Free Response"),
        ColumnSpec(2, "B", "Classify", upstream=["A"]),
        ColumnSpec(3, "C", "Classify", upstream=["B"]),
        ColumnSpec(4, "D", "Free Response"),
    ]
    stages, cycles = compute_stages(columns)
    assert stages == {"A": 1, "D": 1, "B": 2, "C": 3}
    assert cycles == []


def test_a_cycle_is_reported_not_silently_ordered():
    columns = [
        ColumnSpec(1, "A", "Classify", upstream=["B"]),
        ColumnSpec(2, "B", "Classify", upstream=["A"]),
    ]
    stages, cycles = compute_stages(columns)
    assert stages == {}
    assert cycles == [["A", "B"]]


def test_load_is_idempotent_and_no_table_has_a_cycle(conn, corpus_root):
    counts, findings = load_corpus(conn, corpus_root)
    assert counts["tables"] == EXPECTED_TABLES
    assert counts["columns"] == EXPECTED_COLUMNS
    assert findings == []

    again, _ = load_corpus(conn, corpus_root)
    assert again["tables"] == 0 and again["skipped"] == EXPECTED_TABLES

    unstaged = conn.execute("SELECT COUNT(*) AS n FROM column_def WHERE stage IS NULL").fetchone()
    assert unstaged["n"] == 0


def test_stage_one_columns_have_no_upstream(loaded):
    rows = loaded.execute(
        """SELECT c.name FROM column_def c
           WHERE c.stage = 1 AND EXISTS (SELECT 1 FROM column_dep d WHERE d.downstream_id = c.id)"""
    ).fetchall()
    assert rows == []


def test_options_round_trip_through_the_database(loaded):
    row = loaded.execute(
        """SELECT configured_options FROM column_def c JOIN review_table t ON t.id = c.table_id
           WHERE t.number = '01' AND c.name = 'Chain Completeness'"""
    ).fetchone()
    assert "Sequence gap" in json.loads(row["configured_options"])
