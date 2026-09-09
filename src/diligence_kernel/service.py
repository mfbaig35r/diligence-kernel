"""Tool implementations. The server module is transport; this is the behaviour."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from .constants import BUILD_ORDER, PAIRED_TABLES
from .corpus.loader import load_corpus
from .db import now
from .derive import artifacts as artifacts_mod
from .engine.runner import RunScope, create_run, execute_run
from .findings import Finding, KernelError, dump
from .vault import classify as classify_mod
from .vault import search as search_mod
from .vault import units as units_mod
from .vault.ingest import ingest_path

CORPUS_ENV = "DILIGENCE_KERNEL_CORPUS"

#: Output tokens a cell costs, for estimation. Measured at ~1,145 over 50 cells of Table 05
#: on gpt-5 at medium effort — a reasoning model spends far more than the visible answer
#: suggests, and the spend tracks how ambiguous the document is rather than how long it is.
#: Re-measure when the default model or effort changes.
OUTPUT_TOKENS_PER_CELL = 1100


def corpus_root() -> Path:
    raw = os.environ.get(CORPUS_ENV)
    if raw:
        return Path(raw).expanduser()
    return Path(__file__).resolve().parents[2] / "review-table-prompts"


def result(findings: list[Finding] | None = None, **payload: Any) -> dict[str, Any]:
    fs = findings or []
    return {**payload, "findings": dump(fs), "finding_count": len(fs)}


# --- matter -----------------------------------------------------------------------------


def matter_open(
    conn: sqlite3.Connection,
    name: str,
    *,
    side: str | None = None,
    as_of_date: str | None = None,
    objective: str | None = None,
    load: bool = True,
) -> dict[str, Any]:
    existing = conn.execute("SELECT * FROM matter WHERE id = 1").fetchone()
    findings: list[Finding] = []
    if existing and existing["name"] != name:
        raise KernelError(
            f"This database already holds the matter {existing['name']!r}. One matter is one "
            "database file; point DILIGENCE_KERNEL_DB at a new path for a new matter."
        )
    root = corpus_root()
    if not existing:
        conn.execute(
            """INSERT INTO matter (id, name, side, as_of_date, objective, corpus_root, created_at)
               VALUES (1,?,?,?,?,?,?)""",
            (name, side, as_of_date, objective, str(root), now()),
        )
    else:
        conn.execute(
            "UPDATE matter SET side=COALESCE(?,side), as_of_date=COALESCE(?,as_of_date), "
            "objective=COALESCE(?,objective) WHERE id=1",
            (side, as_of_date, objective),
        )
    conn.commit()

    counts = {}
    if load:
        if not root.exists():
            raise KernelError(
                f"The prompt corpus is not at {root}. Set {CORPUS_ENV} to its directory."
            )
        counts, findings = load_corpus(conn, root)
    return result(
        findings, matter=name, as_of_date=as_of_date, corpus=str(root), corpus_load=counts
    )


def corpus_check(conn: sqlite3.Connection, *, table: str | None = None) -> dict[str, Any]:
    """Audit the loaded prompts against the standards 00a sets for them."""
    from .corpus.lint import lint_corpus

    findings = lint_corpus(conn)
    if table:
        findings = [f for f in findings if str(f.subject_name).startswith(f"{table} ")]
    counts: dict[str, int] = {}
    for f in findings:
        counts[f.code] = counts.get(f.code, 0) + 1
    total = conn.execute("SELECT COUNT(*) AS n FROM column_def").fetchone()["n"]
    return result(
        findings,
        columns_checked=total,
        columns_with_findings=len({f.subject_name for f in findings}),
        by_code=counts,
    )


def matter_parameters_set(
    conn: sqlite3.Connection, entities: list[dict[str, Any]], *, replace: bool = False
) -> dict[str, Any]:
    """Record the entities the Table Instructions name, so their placeholders can be bound."""
    from . import binding

    if replace:
        conn.execute("DELETE FROM entity")
    stored = 0
    for record in entities:
        name = (record.get("name") or "").strip()
        if not name:
            continue
        conn.execute(
            """INSERT INTO entity (name, jurisdiction, role, is_subject, created_at)
               VALUES (?,?,?,?,?)
               ON CONFLICT(name) DO UPDATE SET
                 jurisdiction=excluded.jurisdiction, role=excluded.role,
                 is_subject=excluded.is_subject""",
            (
                name,
                record.get("jurisdiction"),
                record.get("role"),
                int(bool(record.get("is_subject", True))),
                now(),
            ),
        )
        stored += 1
    conn.commit()

    matter = conn.execute("SELECT * FROM matter WHERE id = 1").fetchone()
    known = binding.entities_of(conn)
    findings: list[Finding] = []
    remaining: dict[str, list[str]] = {}
    for row in conn.execute("SELECT number, table_instructions FROM review_table ORDER BY number"):
        left = binding.unbound(
            binding.bind(row["table_instructions"] or "", matter=matter, entities=known)
        )
        if left:
            remaining[row["number"]] = left
    if remaining:
        every = sorted({p for v in remaining.values() for p in v})
        findings.append(
            Finding(
                code="UNBOUND_PARAMETERS",
                subject_type="matter",
                subject_id=1,
                subject_name=matter["name"] if matter else "matter",
                observation=(
                    f"{len(remaining)} tables still carry unbound placeholders: {', '.join(every)}. "
                    "A prompt that reaches the model with these cannot answer questions about them."
                ),
                evidence={"tables": remaining},
            )
        )
    return result(
        findings,
        entities=stored,
        subjects=sum(1 for e in known if e.is_subject),
        tables_fully_bound=len(conn.execute("SELECT id FROM review_table").fetchall())
        - len(remaining),
    )


def matter_status(conn: sqlite3.Connection) -> dict[str, Any]:
    matter = conn.execute("SELECT * FROM matter WHERE id = 1").fetchone()
    if matter is None:
        raise KernelError("No matter is open in this database. Call matter_open first.")
    docs = conn.execute(
        """SELECT COUNT(*) AS total,
                  SUM(extract_status='extracted') AS extracted,
                  SUM(extract_status='failed') AS failed FROM document"""
    ).fetchone()
    classified = conn.execute(
        "SELECT COUNT(*) AS n FROM classification WHERE workstream IS NOT NULL"
    ).fetchone()["n"]
    unrouted = len(units_mod.unrouted_documents(conn))
    tables = conn.execute(
        """SELECT t.number, t.title,
                  (SELECT COUNT(*) FROM column_def c WHERE c.table_id = t.id) AS columns,
                  (SELECT COUNT(*) FROM review_unit u WHERE u.table_id = t.id) AS units,
                  (SELECT COUNT(*) FROM cell cl JOIN column_def c2 ON c2.id = cl.column_id
                   WHERE c2.table_id = t.id AND cl.value IS NOT NULL) AS filled
           FROM review_table t ORDER BY t.number"""
    ).fetchall()
    findings: list[Finding] = []
    if unrouted:
        findings.append(
            Finding(
                code="DOCUMENTS_UNROUTED",
                subject_type="matter",
                subject_id=1,
                subject_name=matter["name"],
                observation=(
                    f"{unrouted} extracted documents carry no classification, so no table can see "
                    "them."
                ),
                evidence={"count": unrouted},
            )
        )
    return result(
        findings,
        matter=matter["name"],
        as_of_date=matter["as_of_date"],
        documents={
            "total": docs["total"] or 0,
            "extracted": docs["extracted"] or 0,
            "failed": docs["failed"] or 0,
            "classified": classified,
        },
        tables=[
            {
                "number": t["number"],
                "title": t["title"],
                "columns": t["columns"],
                "units": t["units"],
                "cells_filled": t["filled"],
            }
            for t in tables
            if t["units"] or t["filled"]
        ],
        build_order=list(BUILD_ORDER),
    )


# --- vault --------------------------------------------------------------------------------


def vault_ingest(
    conn: sqlite3.Connection,
    path: str,
    *,
    recursive: bool = True,
    force: bool = False,
    ocr: str | None = None,
) -> dict[str, Any]:
    root = Path(path).expanduser()
    if not root.exists():
        raise KernelError(f"{root} does not exist.")
    if not root.is_dir():
        raise KernelError(f"{root} is not a directory; point vault_ingest at the data room.")
    counts, findings = ingest_path(conn, root, recursive=recursive, force=force, ocr=ocr)
    return result(findings, path=str(root), **counts)


def vault_search(
    conn: sqlite3.Connection, query: str, *, unit_id: int | None = None, limit: int = 10
) -> dict[str, Any]:
    if unit_id is not None:
        passages = search_mod.search_unit(conn, unit_id, query, limit=limit)
        return result(passages=[p.to_dict() for p in passages], scope=f"unit {unit_id}")
    expr = search_mod.fts_query(query)
    rows = (
        conn.execute(
            """SELECT c.id, c.document_id, d.filename, c.text, c.char_start, c.char_end,
                  c.page_start, c.page_end
           FROM chunk_fts f JOIN chunk c ON c.id = f.rowid
           JOIN document d ON d.id = c.document_id
           WHERE chunk_fts MATCH ? ORDER BY bm25(chunk_fts) LIMIT ?""",
            (expr, limit),
        ).fetchall()
        if expr
        else []
    )
    return result(
        passages=[
            {
                "chunk_id": r["id"],
                "document_id": r["document_id"],
                "filename": r["filename"],
                "text": r["text"],
                "char_start": r["char_start"],
                "char_end": r["char_end"],
                "page_start": r["page_start"],
                "page_end": r["page_end"],
            }
            for r in rows
        ],
        scope="whole vault",
    )


def classification_record(
    conn: sqlite3.Connection, records: list[dict[str, Any]]
) -> dict[str, Any]:
    """Store Table 05 output for files, whether the engine or Claude produced it."""
    fields = (
        "workstream",
        "secondary_workstream",
        "document_type",
        "document_role",
        "subject_entity",
        "counterparty",
        "document_date",
        "operative_date",
        "amends_or_issued_under",
        "compilation_flag",
        "completeness",
        "language",
        "routing_disposition",
    )
    findings: list[Finding] = []
    stored = 0
    for record in records:
        filename = record.get("filename")
        row = conn.execute(
            "SELECT id FROM document WHERE filename = ? OR source_path = ?",
            (filename, filename),
        ).fetchone()
        if row is None:
            findings.append(
                Finding(
                    code="DOCUMENT_NOT_IN_VAULT",
                    subject_type="document",
                    subject_id=None,
                    subject_name=str(filename),
                    observation="No ingested document carries that filename; the record was skipped.",
                    evidence={"filename": filename},
                )
            )
            continue
        values = [record.get(f) for f in fields]
        conn.execute(
            f"""INSERT INTO classification (document_id, {", ".join(fields)}, classified_at)
                VALUES (?{", ?" * len(fields)}, ?)
                ON CONFLICT(document_id) DO UPDATE SET
                {", ".join(f"{f}=excluded.{f}" for f in fields)}, classified_at=excluded.classified_at""",
            (int(row["id"]), *values, now()),
        )
        stored += 1
    conn.commit()
    return result(findings, stored=stored, submitted=len(records))


# --- units ----------------------------------------------------------------------------------


def units_propose(conn: sqlite3.Connection, table: str) -> dict[str, Any]:
    proposed, findings = units_mod.propose_units(conn, table)
    return result(
        findings,
        table=table,
        units=[
            {"label": u.label, "unit_key": u.unit_key, "documents": len(u.document_ids)}
            for u in proposed
        ],
    )


def units_assemble(
    conn: sqlite3.Connection, table: str, *, replace: bool = False
) -> dict[str, Any]:
    counts, findings = units_mod.assemble_units(conn, table, replace=replace)
    return result(findings, table=table, **counts)


# --- runs -------------------------------------------------------------------------------------


def run_table(
    conn: sqlite3.Connection,
    table: str,
    *,
    unit_ids: list[int] | None = None,
    columns: list[str] | None = None,
    refill: bool = False,
    reason: str | None = None,
    model: str | None = None,
    provider: str | None = None,
    concurrency: int | None = None,
    filler: Any = None,
) -> dict[str, Any]:
    from .engine.llm import CellFiller
    from .engine.providers import ProviderUnavailable

    if concurrency:
        os.environ["DILIGENCE_KERNEL_CONCURRENCY"] = str(int(concurrency))
    scope = RunScope(unit_ids=unit_ids, column_names=columns, reason=reason, refill=refill)
    if filler is None:
        try:
            filler = CellFiller(provider=provider, model=model)
        except ProviderUnavailable as exc:
            raise KernelError(str(exc)) from exc
    chosen = getattr(filler, "model", model or "unknown")
    run_id = create_run(conn, table, scope, model=chosen)
    summary, findings = execute_run(conn, run_id, filler=filler)
    if table == classify_mod.INTAKE_TABLE and summary["status"] == "complete":
        counts, projected = classify_mod.project_intake(conn, run_id=run_id)
        summary = {**summary, **counts}
        findings.extend(projected)
    return result(findings, **summary)


def run_estimate(
    conn: sqlite3.Connection,
    table: str,
    *,
    unit_ids: list[int] | None = None,
    columns: list[str] | None = None,
    refill: bool = False,
    model: str | None = None,
    provider: str | None = None,
) -> dict[str, Any]:
    """What a run would cost, without running it."""
    from .engine.llm import CellFiller
    from .engine.providers import ProviderUnavailable, estimate_cost
    from .engine.runner import preview_run

    findings: list[Finding] = []
    try:
        filler = CellFiller(provider=provider, model=model)
    except ProviderUnavailable as exc:
        raise KernelError(str(exc)) from exc

    scope = RunScope(unit_ids=unit_ids, column_names=columns, refill=refill)
    requests = preview_run(conn, table, scope, filler=filler)
    if not requests:
        findings.append(
            Finding(
                code="NOTHING_TO_RUN",
                subject_type="table",
                subject_id=None,
                subject_name=f"Table {table}",
                observation=(
                    "No cell is in scope: the table has no rows, or every cell in scope is "
                    "already filled, locked, or reviewed."
                ),
                evidence={"table": table},
            )
        )
        return result(findings, table=table, cells=0)

    counted: list[int] = []
    exact = True
    try:
        for r in requests:
            n, is_exact = filler.count(r["request"], system=r["system"])
            counted.append(n)
            exact = exact and is_exact
    except Exception as exc:
        exact = False
        counted = [(len(r["user"]) + len(r["system"])) // 4 for r in requests]
        findings.append(
            Finding(
                code="TOKENS_ESTIMATED_NOT_COUNTED",
                subject_type="table",
                subject_id=None,
                subject_name=f"Table {table}",
                observation=(
                    "Tokens could not be counted, so the figures are a character-based "
                    f"approximation: {exc}"
                ),
                evidence={"model": filler.model, "provider": filler.provider.name},
            )
        )

    write = sum(c for c, r in zip(counted, requests, strict=True) if r["cache_role"] == "write")
    read = sum(c for c, r in zip(counted, requests, strict=True) if r["cache_role"] == "read")
    plain = sum(c for c, r in zip(counted, requests, strict=True) if r["cache_role"] == "none")
    est_out = OUTPUT_TOKENS_PER_CELL * len(requests)

    # A prefix below the provider's minimum is never cached, so do not price it as if it were.
    per_unit = {}
    for c, r in zip(counted, requests, strict=True):
        if r["cache_role"] == "write":
            per_unit[r["unit_id"]] = c
    too_small = [u for u, n in per_unit.items() if n < filler.provider.min_cacheable_tokens]
    if too_small:
        findings.append(
            Finding(
                code="PREFIX_BELOW_CACHE_MINIMUM",
                subject_type="table",
                subject_id=None,
                subject_name=f"Table {table}",
                observation=(
                    f"{len(too_small)} of {len(per_unit)} rows have a prefix shorter than "
                    f"{filler.provider.min_cacheable_tokens} tokens, which {filler.provider.name} "
                    "does not cache; those rows are priced without the discount."
                ),
                evidence={"rows_below_minimum": len(too_small)},
            )
        )
        moved = sum(
            c
            for c, r in zip(counted, requests, strict=True)
            if r["unit_id"] in too_small and r["cache_role"] in {"read", "write"}
        )
        plain += moved
        read -= sum(
            c
            for c, r in zip(counted, requests, strict=True)
            if r["unit_id"] in too_small and r["cache_role"] == "read"
        )
        write -= sum(
            c
            for c, r in zip(counted, requests, strict=True)
            if r["unit_id"] in too_small and r["cache_role"] == "write"
        )

    cost = estimate_cost(
        filler.provider,
        filler.model,
        input_tokens=plain,
        output_tokens=est_out,
        cache_read_tokens=max(0, read),
        cache_write_tokens=max(0, write),
    )
    uncached = estimate_cost(
        filler.provider, filler.model, input_tokens=sum(counted), output_tokens=est_out
    )
    if cost is None:
        findings.append(
            Finding(
                code="MODEL_PRICE_UNKNOWN",
                subject_type="table",
                subject_id=None,
                subject_name=filler.model,
                observation=(
                    f"No price is recorded for {filler.model!r}; set DILIGENCE_KERNEL_PRICE_IN and "
                    "DILIGENCE_KERNEL_PRICE_OUT (USD per million tokens) to price it."
                ),
                evidence={"provider": filler.provider.name, "model": filler.model},
            )
        )
    return result(
        findings,
        table=table,
        provider=filler.provider.name,
        model=filler.model,
        cells=len(requests),
        rows=len({r["unit_id"] for r in requests}),
        input_tokens=sum(counted),
        estimated_output_tokens=est_out,
        cached_input_tokens=max(0, read),
        token_counts_exact=exact,
        estimated_cost_usd=None if cost is None else round(cost, 4),
        estimated_cost_without_caching_usd=None if uncached is None else round(uncached, 4),
    )


def run_status(conn: sqlite3.Connection, run_id: int | None = None) -> dict[str, Any]:
    if run_id is not None:
        row = conn.execute(
            """SELECT r.*, t.number, t.title FROM run r JOIN review_table t ON t.id=r.table_id
               WHERE r.id = ?""",
            (run_id,),
        ).fetchone()
        if row is None:
            raise KernelError(f"Run {run_id} does not exist.")
        return result(run=_run_dict(row))
    rows = conn.execute(
        """SELECT r.*, t.number, t.title FROM run r JOIN review_table t ON t.id=r.table_id
           ORDER BY r.created_at DESC LIMIT 20"""
    ).fetchall()
    return result(runs=[_run_dict(r) for r in rows])


def _run_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "run_id": row["id"],
        "table": f"{row['number']} {row['title']}",
        "status": row["status"],
        "cells_total": row["cells_total"],
        "cells_done": row["cells_done"],
        "cells_failed": row["cells_failed"],
        "input_tokens": row["input_tokens"],
        "output_tokens": row["output_tokens"],
        "model": row["model"],
        "error": row["error"],
        "scope": json.loads(row["scope"] or "{}"),
    }


# --- reading the table ------------------------------------------------------------------------


def table_read(
    conn: sqlite3.Connection,
    table: str,
    *,
    columns: list[str] | None = None,
    only_flagged: bool = False,
    limit: int = 50,
) -> dict[str, Any]:
    tbl = conn.execute(
        "SELECT id, number, title FROM review_table WHERE number = ?", (table,)
    ).fetchone()
    if tbl is None:
        raise KernelError(f"Table {table} is not loaded in this matter.")
    units = conn.execute(
        "SELECT id, label FROM review_unit WHERE table_id = ? ORDER BY position LIMIT ?",
        (int(tbl["id"]), limit),
    ).fetchall()
    col_sql = "SELECT id, name, native_type, position FROM column_def WHERE table_id = ?"
    params: list[Any] = [int(tbl["id"])]
    if columns:
        col_sql += f" AND name COLLATE NOCASE IN ({','.join('?' * len(columns))})"
        params.extend(columns)
    cols = conn.execute(col_sql + " ORDER BY position", params).fetchall()

    rows = []
    for unit in units:
        cells: dict[str, Any] = {}
        for col in cols:
            cell = conn.execute(
                """SELECT value, review_status, materiality, validation, is_fallback
                   FROM cell WHERE unit_id = ? AND column_id = ?""",
                (int(unit["id"]), int(col["id"])),
            ).fetchone()
            if cell is None:
                continue
            violations = json.loads(cell["validation"] or "[]")
            if only_flagged and not violations:
                continue
            cells[col["name"]] = {
                "value": cell["value"],
                "review_status": cell["review_status"],
                "materiality": cell["materiality"],
                "validation": violations,
            }
        if cells or not only_flagged:
            rows.append({"unit_id": int(unit["id"]), "unit": unit["label"], "cells": cells})
    return result(table=f"{tbl['number']} {tbl['title']}", rows=rows, row_count=len(rows))


def cell_evidence(conn: sqlite3.Connection, unit_id: int, column: str) -> dict[str, Any]:
    row = conn.execute(
        """SELECT cell.id, cell.value, cell.validation, c.name, c.native_type
           FROM cell JOIN column_def c ON c.id = cell.column_id
           WHERE cell.unit_id = ? AND c.name COLLATE NOCASE = ?""",
        (unit_id, column),
    ).fetchone()
    if row is None:
        raise KernelError(f"No cell for column {column!r} in unit {unit_id}.")
    evidence = conn.execute(
        """SELECT e.quote, e.char_start, e.char_end, d.filename,
                  d.text_source, d.ocr_engine, d.ocr_confidence
           FROM cell_evidence e JOIN document d ON d.id = e.document_id
           WHERE e.cell_id = ? ORDER BY e.rank""",
        (int(row["id"]),),
    ).fetchall()
    return result(
        column=row["name"],
        native_type=row["native_type"],
        value=row["value"],
        validation=json.loads(row["validation"] or "[]"),
        evidence=[
            {
                "filename": e["filename"],
                "quote": e["quote"],
                "char_start": e["char_start"],
                "char_end": e["char_end"],
                "text_source": e["text_source"] or "extracted",
                "ocr_engine": e["ocr_engine"],
                "ocr_confidence": e["ocr_confidence"],
            }
            for e in evidence
        ],
    )


def cell_review(
    conn: sqlite3.Connection,
    unit_id: int,
    column: str,
    *,
    review_status: str | None = None,
    value: str | None = None,
    materiality: str | None = None,
    deal_consequence: str | None = None,
    reviewed_by: str | None = None,
    lock: bool | None = None,
) -> dict[str, Any]:
    """Record a human's judgment on a cell. 00a: a cell Harvey filled is a candidate."""
    row = conn.execute(
        """SELECT cell.id, cell.value FROM cell JOIN column_def c ON c.id = cell.column_id
           WHERE cell.unit_id = ? AND c.name COLLATE NOCASE = ?""",
        (unit_id, column),
    ).fetchone()
    if row is None:
        raise KernelError(f"No cell for column {column!r} in unit {unit_id}.")
    cell_id = int(row["id"])
    if value is not None and value != row["value"]:
        conn.execute(
            """INSERT INTO cell_history
               (cell_id, previous_value, new_value, reason, actor, changed_at)
               VALUES (?,?,?, 'human review', ?, ?)""",
            (cell_id, row["value"], value, reviewed_by or "unknown", now()),
        )
    conn.execute(
        """UPDATE cell SET
             value = COALESCE(?, value),
             review_status = COALESCE(?, review_status),
             materiality = COALESCE(?, materiality),
             deal_consequence = COALESCE(?, deal_consequence),
             reviewed_by = COALESCE(?, reviewed_by),
             locked = COALESCE(?, locked)
           WHERE id = ?""",
        (
            value,
            review_status,
            materiality,
            deal_consequence,
            reviewed_by,
            None if lock is None else int(lock),
            cell_id,
        ),
    )
    conn.commit()
    return result(unit_id=unit_id, column=column, review_status=review_status, locked=lock)


# --- corpus ---------------------------------------------------------------------------------------


def table_describe(conn: sqlite3.Connection, table: str) -> dict[str, Any]:
    tbl = conn.execute("SELECT * FROM review_table WHERE number = ?", (table,)).fetchone()
    if tbl is None:
        raise KernelError(f"Table {table} is not loaded in this matter.")
    cols = conn.execute(
        """SELECT position, name, native_type, type_caveat, configured_options, purpose, stage,
                  prompt_chars
           FROM column_def WHERE table_id = ? ORDER BY position""",
        (int(tbl["id"]),),
    ).fetchall()
    pairs = [p for p in PAIRED_TABLES if table in p]
    findings: list[Finding] = []
    for pair in pairs:
        other = pair[1] if pair[0] == table else pair[0]
        findings.append(
            Finding(
                code="TABLE_MUST_PAIR",
                subject_type="table",
                subject_id=int(tbl["id"]),
                subject_name=f"Table {table}",
                observation=(
                    f"00a pairs Table {pair[0]} with Table {pair[1]}: the first returns "
                    f"`Incorporated terms` that only the second resolves."
                ),
                evidence={"pair": list(pair), "other": other},
            )
        )
    return result(
        findings,
        table=f"{tbl['number']} {tbl['title']}",
        review_unit=tbl["review_unit"],
        grouping_enabled=bool(tbl["grouping_enabled"]),
        max_docs_per_unit=tbl["max_docs_per_unit"],
        vault_project=tbl["vault_project"],
        table_instructions=tbl["table_instructions"],
        columns=[
            {
                "position": c["position"],
                "name": c["name"],
                "native_type": c["native_type"],
                "type_caveat": c["type_caveat"],
                "stage": c["stage"],
                "configured_options": json.loads(c["configured_options"] or "null"),
                "purpose": c["purpose"],
                "prompt_chars": c["prompt_chars"],
            }
            for c in cols
        ],
    )


def column_prompt(conn: sqlite3.Connection, table: str, column: str) -> dict[str, Any]:
    row = conn.execute(
        """SELECT c.*, t.number, t.table_instructions FROM column_def c
           JOIN review_table t ON t.id = c.table_id
           WHERE t.number = ? AND c.name COLLATE NOCASE = ?""",
        (table, column),
    ).fetchone()
    if row is None:
        raise KernelError(f"Table {table} has no column named {column!r}.")
    upstream = conn.execute(
        """SELECT c.name FROM column_dep d JOIN column_def c ON c.id = d.upstream_id
           WHERE d.downstream_id = ? ORDER BY c.position""",
        (int(row["id"]),),
    ).fetchall()
    downstream = conn.execute(
        """SELECT c.name FROM column_dep d JOIN column_def c ON c.id = d.downstream_id
           WHERE d.upstream_id = ? ORDER BY c.position""",
        (int(row["id"]),),
    ).fetchall()
    return result(
        table=table,
        column=row["name"],
        native_type=row["native_type"],
        type_caveat=row["type_caveat"],
        stage=row["stage"],
        configured_options=json.loads(row["configured_options"] or "null"),
        prompt_text=row["prompt_text"],
        prompt_chars=row["prompt_chars"],
        upstream=[u["name"] for u in upstream],
        downstream=[d["name"] for d in downstream],
    )


def columns_find(
    conn: sqlite3.Connection, query: str, *, native_type: str | None = None, limit: int = 25
) -> dict[str, Any]:
    """Find columns across the corpus by name, purpose, or prompt text."""
    like = f"%{query.lower()}%"
    sql = """SELECT t.number, t.title, c.name, c.native_type, c.purpose, c.stage
             FROM column_def c JOIN review_table t ON t.id = c.table_id
             WHERE (LOWER(c.name) LIKE ? OR LOWER(c.purpose) LIKE ? OR LOWER(c.prompt_text) LIKE ?)"""
    params: list[Any] = [like, like, like]
    if native_type:
        sql += " AND c.native_type = ?"
        params.append(native_type)
    rows = conn.execute(sql + " ORDER BY t.number, c.position LIMIT ?", [*params, limit]).fetchall()
    return result(
        query=query,
        columns=[
            {
                "table": f"{r['number']} {r['title']}",
                "column": r["name"],
                "native_type": r["native_type"],
                "stage": r["stage"],
                "purpose": r["purpose"],
            }
            for r in rows
        ],
    )


# --- artifacts -------------------------------------------------------------------------------------


def artifact_build(
    conn: sqlite3.Connection, artifact: str, *, min_review_status: str | None = None
) -> dict[str, Any]:
    if artifact == "issues_list":
        rows, findings = artifacts_mod.issues_list(conn)
        spec_title = "Issues list"
        description = "Every cell a reviewer has marked Critical or Material."
    else:
        rows, findings = artifacts_mod.build_artifact(
            conn, artifact, min_review_status=min_review_status
        )
        spec = artifacts_mod.ARTIFACTS[artifact]
        spec_title, description = spec.title, spec.description
    return result(
        findings,
        artifact=artifact,
        title=spec_title,
        description=description,
        row_count=len(rows),
        rows=[
            {
                "table": r.table,
                "unit": r.unit,
                "column": r.column,
                "value": r.value,
                "review_status": r.review_status,
                "materiality": r.materiality,
                "validation": r.validation,
                "carried": r.carried,
            }
            for r in rows
        ],
    )


def artifact_list() -> dict[str, Any]:
    return result(
        artifacts=[
            {"key": s.key, "title": s.title, "description": s.description}
            for s in artifacts_mod.ARTIFACTS.values()
        ]
        + [
            {
                "key": "issues_list",
                "title": "Issues list",
                "description": "Every cell a reviewer has marked Critical or Material.",
            }
        ]
    )
