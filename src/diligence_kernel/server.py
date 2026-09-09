"""diligence-kernel MCP server: stdio transport, findings not verdicts.

Every tool docstring is written for the model calling it. The server never decides which
document controls, never computes, and never makes a legal determination.
"""

from __future__ import annotations

import argparse
import functools
import sqlite3
import sys
from collections.abc import Callable
from typing import Annotated, Any

from mcp.server.mcpserver import MCPServer
from pydantic import Field

from . import db, service
from .findings import KernelError

INSTRUCTIONS = """diligence-kernel ingests an M&A data room, classifies and groups its files, and
runs the review-table prompt corpus against them, persisting every cell with the evidence it
was drawn from.

The corpus is the schema: 24 tables, 591 columns, each with a prompt the server does not
author. The server never drafts prompts, never decides which document is operative, never
decides materiality, and does no arithmetic. Those stay with a human, and the human-review
columns are where their answers live.

Tools return findings: {code, subject_type, subject_id, subject_name, observation, evidence}.
An observation is one factual sentence; interpret it for the user. Ids in results exist so
you can pass them back to tools; do not show them unless asked.

A typical matter: matter_open -> vault_ingest -> run_table('05') to classify -> units_assemble
for each workstream table -> run_table(that table) -> table_read / cell_evidence to review ->
cell_review to record judgments -> artifact_build for the schedules.

A cell the engine filled is a candidate, not a finding. It does not go in a memo and is not
told to a client until its review status says otherwise."""

mcp = MCPServer("diligence-kernel", instructions=INSTRUCTIONS)

_conn: sqlite3.Connection | None = None


def get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = db.connect()
    return _conn


def set_conn(conn: sqlite3.Connection | None) -> None:
    """Used by tests to point the tools at a temporary database."""
    global _conn
    _conn = conn


def _tool(fn: Callable[..., dict[str, Any]]) -> Callable[..., dict[str, Any]]:
    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> dict[str, Any]:
        try:
            return fn(*args, **kwargs)
        except KernelError as exc:
            return {"error": str(exc), "findings": [], "finding_count": 0}
        except (ValueError, KeyError) as exc:
            return {"error": str(exc), "findings": [], "finding_count": 0}

    return wrapper


Table = Annotated[
    str, Field(description="Table number as the corpus defines it, e.g. '01' or '13'.")
]


# --- matter -------------------------------------------------------------------------------


@mcp.tool()
@_tool
def matter_open(
    name: Annotated[str, Field(description="The matter's name, as the deal team calls it.")],
    side: Annotated[str | None, Field(description="'buy' or 'sell'.")] = None,
    as_of_date: Annotated[
        str | None,
        Field(description="The diligence as-of date, YYYY-MM-DD. Prompts compare dates to it."),
    ] = None,
    objective: Annotated[
        str | None, Field(description="What the deal team is trying to learn.")
    ] = None,
) -> dict[str, Any]:
    """Open the matter in this database and load the review-table prompt corpus.

    One matter is one database file. Loading the corpus is idempotent: unchanged inventories
    are skipped, a changed one is re-parsed. Call this before anything else.
    """
    return service.matter_open(
        get_conn(), name, side=side, as_of_date=as_of_date, objective=objective
    )


@mcp.tool()
@_tool
def matter_status() -> dict[str, Any]:
    """Report what the matter holds: documents, classification, units, and cells filled per table.

    Reports documents that carry no classification, because no table can see those.
    """
    return service.matter_status(get_conn())


# --- vault --------------------------------------------------------------------------------


@mcp.tool()
@_tool
def vault_ingest(
    path: Annotated[str, Field(description="Directory holding the data room.")],
    recursive: bool = True,
    force: Annotated[
        bool, Field(description="Re-extract files whose content is unchanged.")
    ] = False,
    ocr: Annotated[
        str | None,
        Field(description="auto (default, local tesseract) | tesseract | vision | off."),
    ] = None,
) -> dict[str, Any]:
    """Extract, chunk, and store every supported file under a directory.

    Idempotent by content hash: an unchanged file is skipped. A PDF page with no text layer
    is a scan, and is read by OCR — locally with tesseract by default, so nothing leaves the
    machine. A document read that way records that its text is a transcription rather than
    the document's own, reports the engine and its confidence, and any Verbatim cell drawn
    from it is flagged: the quotation was checked against a reading of the page, not the page.

    `vision` sends page images to the model instead. It reads harder scans, but it
    transcribes fluently, so a misreading looks like ordinary text — opt in deliberately.
    """
    return service.vault_ingest(get_conn(), path, recursive=recursive, force=force, ocr=ocr)


@mcp.tool()
@_tool
def vault_search(
    query: Annotated[str, Field(description="What to look for, in the documents' own words.")],
    unit_id: Annotated[int | None, Field(description="Restrict to one review unit.")] = None,
    limit: int = 10,
) -> dict[str, Any]:
    """Search the vault's text and return passages with their document, page, and offsets."""
    return service.vault_search(get_conn(), query, unit_id=unit_id, limit=limit)


@mcp.tool()
@_tool
def classification_record(
    records: Annotated[
        list[dict[str, Any]],
        Field(
            description="One record per file, each with 'filename' plus any of: workstream, "
            "secondary_workstream, document_type, document_role, subject_entity, counterparty, "
            "document_date, operative_date, amends_or_issued_under, compilation_flag, "
            "completeness, language, routing_disposition."
        ),
    ],
) -> dict[str, Any]:
    """Store Table 05 classification for files, which is what routes them to every other table.

    Use this when you have classified files yourself. Running Table 05 through run_table
    writes the same records. A file with no workstream is invisible to every workstream table.
    """
    return service.classification_record(get_conn(), records)


# --- units ---------------------------------------------------------------------------------


@mcp.tool()
@_tool
def units_propose(table: Table) -> dict[str, Any]:
    """Show the rows a table would run over, without writing them.

    Grouped tables assemble a family from a base document plus everything issued under it.
    Reports dependents whose base is absent or ambiguous: 00a warns that a family missing an
    amendment produces a confidently wrong row and nothing else detects it.
    """
    return service.units_propose(get_conn(), table)


@mcp.tool()
@_tool
def units_assemble(
    table: Table,
    replace: Annotated[
        bool, Field(description="Discard existing auto-assembled units first.")
    ] = False,
) -> dict[str, Any]:
    """Write the review units for a table. Units a human assembled are never replaced."""
    return service.units_assemble(get_conn(), table, replace=replace)


# --- runs ------------------------------------------------------------------------------------


@mcp.tool()
@_tool
def run_table(
    table: Table,
    unit_ids: Annotated[list[int] | None, Field(description="Restrict to these rows.")] = None,
    columns: Annotated[
        list[str] | None, Field(description="Restrict to these column names.")
    ] = None,
    refill: Annotated[bool, Field(description="Re-fill cells that already carry a value.")] = False,
    reason: Annotated[str | None, Field(description="Why this run exists, for the record.")] = None,
    model: Annotated[str | None, Field(description="Override the model for this run.")] = None,
    provider: Annotated[
        str | None,
        Field(description="'openai' or 'anthropic'. Defaults to DILIGENCE_KERNEL_PROVIDER."),
    ] = None,
) -> dict[str, Any]:
    """Fill a review table's cells, in dependency order, from the documents in each row.

    The run is durable: every cell commits as it is filled, so calling again after a failure
    resumes rather than restarting. Already-filled cells are skipped unless refill is set, and
    a locked or human-corrected cell is never overwritten.

    Each cell is checked against the 00a standards before it persists: the fallback
    vocabulary, Classify options, ISO dates, no markdown, no arithmetic, and for Verbatim
    columns that the quoted text actually appears in the row's documents. Violations are
    recorded on the cell and returned as findings.

    This spends money. A 27-column table over 40 rows is roughly 1,080 model calls.
    """
    return service.run_table(
        get_conn(),
        table,
        unit_ids=unit_ids,
        columns=columns,
        refill=refill,
        reason=reason,
        model=model,
    )


@mcp.tool()
@_tool
def run_estimate(
    table: Table,
    unit_ids: Annotated[list[int] | None, Field(description="Restrict to these rows.")] = None,
    columns: Annotated[
        list[str] | None, Field(description="Restrict to these column names.")
    ] = None,
    refill: Annotated[bool, Field(description="Include cells that already carry a value.")] = False,
    model: Annotated[str | None, Field(description="Price against this model instead.")] = None,
    provider: Annotated[str | None, Field(description="'openai' or 'anthropic'.")] = None,
) -> dict[str, Any]:
    """Report what run_table would cost, without running it or spending anything.

    Counts the exact requests the run would send. Cells that are already filled, locked, or
    reviewed are excluded, because a run would skip them. Reports the cost both with and
    without the cached unit prefix, so the saving from that design is visible.

    Call this before any run over more than a handful of rows.
    """
    return service.run_estimate(
        get_conn(),
        table,
        unit_ids=unit_ids,
        columns=columns,
        refill=refill,
        model=model,
        provider=provider,
    )


@mcp.tool()
@_tool
def run_status(
    run_id: Annotated[int | None, Field(description="One run; omit for the last twenty.")] = None,
) -> dict[str, Any]:
    """Report a run's progress, token spend, and any error that stopped it."""
    return service.run_status(get_conn(), run_id)


# --- reading ------------------------------------------------------------------------------------


@mcp.tool()
@_tool
def table_read(
    table: Table,
    columns: Annotated[list[str] | None, Field(description="Only these columns.")] = None,
    only_flagged: Annotated[
        bool, Field(description="Only cells carrying a standards violation.")
    ] = False,
    limit: int = 50,
) -> dict[str, Any]:
    """Read a filled table: one entry per row, with each cell's value, review status, and violations."""
    return service.table_read(
        get_conn(), table, columns=columns, only_flagged=only_flagged, limit=limit
    )


@mcp.tool()
@_tool
def cell_evidence(
    unit_id: Annotated[int, Field(description="The row, from table_read or units_assemble.")],
    column: Annotated[str, Field(description="Exact column name.")],
) -> dict[str, Any]:
    """Show a cell's value and the sentences it was drawn from, with document and offsets.

    This is how a reviewer checks a cell without opening the whole document. A cell whose
    evidence list is empty was filled from no quoted text.
    """
    return service.cell_evidence(get_conn(), unit_id, column)


@mcp.tool()
@_tool
def cell_review(
    unit_id: int,
    column: str,
    review_status: Annotated[
        str | None, Field(description="Unreviewed | Verified | Corrected | Disputed.")
    ] = None,
    value: Annotated[
        str | None, Field(description="A corrected value. The old one is kept in history.")
    ] = None,
    materiality: Annotated[
        str | None, Field(description="Critical | Material | Monitor | Immaterial.")
    ] = None,
    deal_consequence: Annotated[
        str | None, Field(description="What it means for the deal.")
    ] = None,
    reviewed_by: Annotated[str | None, Field(description="Reviewer's initials.")] = None,
    lock: Annotated[bool | None, Field(description="Lock the cell against re-runs.")] = None,
) -> dict[str, Any]:
    """Record a human's judgment on a cell: verification, correction, materiality, consequence.

    Materiality and deal consequence are human columns by design; the engine never fills them.
    A verified or locked cell is not overwritten by a later run.
    """
    return service.cell_review(
        get_conn(),
        unit_id,
        column,
        review_status=review_status,
        value=value,
        materiality=materiality,
        deal_consequence=deal_consequence,
        reviewed_by=reviewed_by,
        lock=lock,
    )


# --- corpus ---------------------------------------------------------------------------------------


@mcp.tool()
@_tool
def table_describe(table: Table) -> dict[str, Any]:
    """Describe a table: its review unit, grouping, Table Instructions, and every column.

    Each column reports its native type, execution stage, configured options, and any
    pre-run verification caveat the inventory recorded against its type.
    """
    return service.table_describe(get_conn(), table)


@mcp.tool()
@_tool
def column_prompt(table: Table, column: str) -> dict[str, Any]:
    """Return one column's full prompt text, with its upstream and downstream columns."""
    return service.column_prompt(get_conn(), table, column)


@mcp.tool()
@_tool
def columns_find(
    query: Annotated[
        str, Field(description="Words to match in a column name, purpose, or prompt.")
    ],
    native_type: Annotated[
        str | None, Field(description="Classify | Date | Verbatim | Free Response | Duration.")
    ] = None,
    limit: int = 25,
) -> dict[str, Any]:
    """Find columns across all 24 tables by name, purpose, or prompt text."""
    return service.columns_find(get_conn(), query, native_type=native_type, limit=limit)


# --- artifacts -------------------------------------------------------------------------------------


@mcp.tool()
@_tool
def artifact_list() -> dict[str, Any]:
    """List the derived artifacts and what each is built from."""
    return service.artifact_list()


@mcp.tool()
@_tool
def artifact_build(
    artifact: Annotated[
        str,
        Field(
            description="consent_schedule | coverage_register | closing_conditions | "
            "transaction_payments | chain_gaps | issues_list"
        ),
    ],
    min_review_status: Annotated[
        str | None, Field(description="Only carry cells at this review status, e.g. 'Verified'.")
    ] = None,
) -> dict[str, Any]:
    """Build a derived artifact by filtering cells that already exist.

    00a: never re-derive a schedule by asking a fresh question, so that the schedule and its
    sources cannot disagree. Each artifact reports how many of its rows are still unreviewed
    or carry a standards violation.
    """
    return service.artifact_build(get_conn(), artifact, min_review_status=min_review_status)


def main() -> None:
    parser = argparse.ArgumentParser(prog="diligence-kernel")
    parser.add_argument("--migrate", action="store_true", help="Apply migrations and exit.")
    parser.add_argument("--corpus-check", action="store_true", help="Parse the corpus and exit.")
    args = parser.parse_args()

    if args.migrate:
        conn = db.connect()
        print(f"schema version {db.schema_version(conn)} at {db.db_path()}")
        return
    if args.corpus_check:
        from .corpus.parser import parse_corpus

        specs, findings = parse_corpus(service.corpus_root())
        tables = [s for s in specs if s.is_table]
        print(f"{len(tables)} tables, {sum(len(s.columns) for s in tables)} columns")
        for f in findings:
            print(f"  {f.code}: {f.subject_name} — {f.observation}", file=sys.stderr)
        sys.exit(1 if findings else 0)

    mcp.run()


if __name__ == "__main__":
    main()
