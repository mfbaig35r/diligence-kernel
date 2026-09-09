"""Durable execution of a review table.

A run is a row in `run` and a set of cells. It survives a crash: every cell is committed as
it is filled, so resuming skips what is already done. Nothing is filled twice unless asked.

Order matters twice over. Within a unit, columns run in topological stage order, because a
stage-2 prompt consumes the stage-1 answers as established results — filling them out of
order would feed a prompt an empty upstream. Across units, iteration is unit-major so the
unit's documents stay in the cached prefix.

**Concurrency runs inside a stage, never across one.** Every column of a stage is independent
by construction — that is what a topological stage means — so they are filled together and
the run waits at the stage boundary. 338 of the corpus's 591 columns are stage 1, so this is
most of the work.

Two details the naive version gets wrong:

- **The first cell of a unit runs alone.** Firing a whole stage at once means every request
  misses the prompt cache simultaneously, because nothing has populated it yet. One serial
  call writes the unit's prefix into cache; the rest of the stage then reads it.
- **Only the model calls are concurrent.** Every database write happens on the calling
  thread after a stage completes, so SQLite sees one writer and cell ordering stays
  deterministic.

The engine never decides which document controls, never computes, and never overwrites a
locked or human-corrected cell.
"""

from __future__ import annotations

import itertools
import json
import os
import sqlite3
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any

from .. import binding
from ..constants import SPAN_EXACT_TYPES
from ..db import now
from ..findings import Finding, KernelError
from ..vault import search
from .llm import CellFiller, CellRequest
from .providers import Usage
from .validate import validate_cell, validate_provenance, validate_verbatim

#: A unit whose documents fit in this many characters goes into the cached prefix whole.
#: Above it, the engine retrieves per column instead and gives up the cache benefit.
WHOLE_UNIT_CHAR_BUDGET = 240_000

#: Passages retrieved per column when a unit is too large to send whole.
RETRIEVAL_LIMIT = 12

#: Model calls in flight at once, within a stage. Raise for throughput, lower for rate limits.
DEFAULT_CONCURRENCY = 6


def configured_concurrency() -> int:
    raw = os.environ.get("DILIGENCE_KERNEL_CONCURRENCY")
    try:
        return max(1, int(raw)) if raw else DEFAULT_CONCURRENCY
    except ValueError:
        return DEFAULT_CONCURRENCY


@dataclass(slots=True)
class _Prepared:
    """One cell's work, assembled on the calling thread before any call is made."""

    column: sqlite3.Row
    request: CellRequest
    system: Any
    sources: list[str]
    existing: sqlite3.Row | None
    answer: Any = None
    usage: Any = field(default=None)
    error: Exception | None = None


@dataclass(slots=True)
class RunScope:
    unit_ids: list[int] | None = None
    column_names: list[str] | None = None
    reason: str | None = None
    refill: bool = False  # re-fill cells that already have a value

    def to_json(self) -> str:
        return json.dumps(
            {
                "unit_ids": self.unit_ids,
                "column_names": self.column_names,
                "reason": self.reason,
                "refill": self.refill,
            }
        )


def create_run(conn: sqlite3.Connection, table_number: str, scope: RunScope, *, model: str) -> int:
    table = conn.execute("SELECT id FROM review_table WHERE number = ?", (table_number,)).fetchone()
    if table is None:
        raise KernelError(f"Table {table_number} is not loaded in this matter.")
    units, columns = _plan(conn, int(table["id"]), scope)
    cur = conn.execute(
        """INSERT INTO run (table_id, status, scope, model, cells_total, created_at)
           VALUES (?, 'pending', ?, ?, ?, ?)""",
        (int(table["id"]), scope.to_json(), model, len(units) * len(columns), now()),
    )
    conn.commit()
    return int(cur.lastrowid)


def _plan(
    conn: sqlite3.Connection, table_id: int, scope: RunScope
) -> tuple[list[sqlite3.Row], list[sqlite3.Row]]:
    unit_sql = "SELECT id, label FROM review_unit WHERE table_id = ?"
    params: list[Any] = [table_id]
    if scope.unit_ids:
        unit_sql += f" AND id IN ({','.join('?' * len(scope.unit_ids))})"
        params.extend(scope.unit_ids)
    units = conn.execute(unit_sql + " ORDER BY position", params).fetchall()

    col_sql = """SELECT id, name, native_type, configured_options, prompt_text, stage, position
                 FROM column_def WHERE table_id = ?"""
    col_params: list[Any] = [table_id]
    if scope.column_names:
        placeholders = ",".join("?" * len(scope.column_names))
        col_sql += f" AND name COLLATE NOCASE IN ({placeholders})"
        col_params.extend(scope.column_names)
    columns = conn.execute(
        col_sql + " ORDER BY COALESCE(stage, 99), position", col_params
    ).fetchall()
    return units, columns


def execute_run(
    conn: sqlite3.Connection,
    run_id: int,
    *,
    filler: CellFiller | None = None,
    progress: Callable[[int, int], None] | None = None,
) -> tuple[dict[str, Any], list[Finding]]:
    """Run to completion, committing each cell. Safe to call again after a failure."""
    run = conn.execute("SELECT * FROM run WHERE id = ?", (run_id,)).fetchone()
    if run is None:
        raise KernelError(f"Run {run_id} does not exist.")
    if run["status"] in {"complete", "cancelled"}:
        return _summary(conn, run_id), []

    table = conn.execute("SELECT * FROM review_table WHERE id = ?", (run["table_id"],)).fetchone()
    scope_raw = json.loads(run["scope"] or "{}")
    scope = RunScope(
        unit_ids=scope_raw.get("unit_ids"),
        column_names=scope_raw.get("column_names"),
        reason=scope_raw.get("reason"),
        refill=bool(scope_raw.get("refill")),
    )
    filler = filler or CellFiller(model=run["model"])
    findings: list[Finding] = []

    conn.execute(
        "UPDATE run SET status='running', started_at=COALESCE(started_at, ?) WHERE id=?",
        (now(), run_id),
    )
    conn.commit()

    units, columns = _plan(conn, int(run["table_id"]), scope)

    # Bind the matter's parameters into the Table Instructions before anything reads them.
    # Unbound, they ask the model to identify a "review subject" against square brackets.
    matter = conn.execute("SELECT * FROM matter WHERE id = 1").fetchone()
    instructions = binding.bind(
        table["table_instructions"] or "",
        matter=matter,
        entities=binding.entities_of(conn),
    )
    if still := binding.unbound(instructions):
        findings.append(
            Finding(
                code="UNBOUND_PARAMETERS",
                subject_type="table",
                subject_id=int(run["table_id"]),
                subject_name=f"Table {table['number']}",
                observation=(
                    f"{len(still)} parameters in the Table Instructions were not bound and "
                    f"reach the model as placeholders: {', '.join(still)}. Answers that depend "
                    "on them cannot be right."
                ),
                evidence={"placeholders": still},
            )
        )

    workers = configured_concurrency()
    conn.execute("UPDATE run SET concurrency = ? WHERE id = ?", (workers, run_id))
    conn.commit()

    total = len(units) * len(columns)
    done = 0
    usage_total = Usage()

    try:
        for unit in units:
            unit_id = int(unit["id"])
            blocks, whole = _unit_context(conn, unit_id)
            ocr_documents = {
                int(r["id"])
                for r in conn.execute(
                    """SELECT d.id FROM unit_document ud JOIN document d ON d.id = ud.document_id
                       WHERE ud.unit_id = ? AND d.text_source = 'ocr'""",
                    (unit_id,),
                )
            }
            if not blocks:
                findings.append(
                    Finding(
                        code="UNIT_HAS_NO_TEXT",
                        subject_type="unit",
                        subject_id=unit_id,
                        subject_name=unit["label"],
                        observation=(
                            "The review unit holds no extracted text; its cells were skipped."
                        ),
                        evidence={"unit_id": unit_id},
                    )
                )
                done += len(columns)
                if progress:
                    progress(done, total)
                continue

            system = filler.build_system(
                table_instructions=instructions,
                unit_label=unit["label"],
                evidence_blocks=blocks,
                cache_key=f"{table['number']}:{unit_id}",
            )
            sources = [str(b.get("text", "")) for b in blocks]
            unit_has_ocr = bool(ocr_documents)
            first_of_unit = True

            # Stage by stage. Columns are already ordered by stage, so grouping is a scan.
            for _, group in itertools.groupby(columns, key=lambda c: c["stage"]):
                stage_columns = list(group)
                prepared: list[_Prepared] = []
                for column in stage_columns:
                    item = _prepare(
                        conn,
                        unit,
                        unit_id,
                        column,
                        filler,
                        table,
                        system,
                        sources,
                        whole,
                        scope,
                        findings,
                        instructions,
                    )
                    if item is None:
                        done += 1
                        continue
                    prepared.append(item)
                if not prepared:
                    if progress:
                        progress(done, total)
                    continue

                # The first call of a unit runs alone so it populates the prompt cache; the
                # rest of the stage then reads the prefix instead of re-paying for it.
                if first_of_unit:
                    _call(filler, prepared[0])
                    head, tail = prepared[:1], prepared[1:]
                    first_of_unit = False
                else:
                    head, tail = [], prepared

                if tail:
                    with ThreadPoolExecutor(max_workers=min(workers, len(tail))) as pool:
                        list(pool.map(lambda item: _call(filler, item), tail))

                # Everything below runs on this thread: one writer, deterministic order.
                for item in head + tail:
                    done += 1
                    if item.error is not None:
                        conn.execute(
                            "UPDATE run SET cells_failed = cells_failed + 1 WHERE id = ?",
                            (run_id,),
                        )
                        findings.append(
                            Finding(
                                code="CELL_FILL_FAILED",
                                subject_type="cell",
                                subject_id=None,
                                subject_name=f"{unit['label']} / {item.column['name']}",
                                observation=f"The cell could not be filled: {item.error}",
                                evidence={
                                    "unit_id": unit_id,
                                    "column": item.column["name"],
                                },
                            )
                        )
                        continue

                    usage_total.add(item.usage)
                    options = json.loads(item.column["configured_options"] or "null") or []
                    violations = validate_cell(
                        item.answer.value,
                        native_type=item.column["native_type"],
                        configured_options=options,
                        column_name=item.column["name"],
                    )
                    if item.column["native_type"] in SPAN_EXACT_TYPES:
                        violations += validate_verbatim(item.answer.value, item.sources)
                    violations += validate_provenance(
                        item.column["native_type"], unit_has_ocr=unit_has_ocr
                    )

                    _persist_cell(
                        conn,
                        unit_id=unit_id,
                        column_id=int(item.column["id"]),
                        run_id=run_id,
                        answer=item.answer,
                        violations=[v.code for v in violations],
                        usage=item.usage,
                        previous=item.existing,
                    )
                    for v in violations:
                        findings.append(
                            Finding(
                                code=v.code,
                                subject_type="cell",
                                subject_id=None,
                                subject_name=f"{unit['label']} / {item.column['name']}",
                                observation=v.detail,
                                evidence={
                                    "value": item.answer.value[:300],
                                    "column": item.column["name"],
                                },
                            )
                        )
                    conn.execute(
                        """UPDATE run SET cells_done = cells_done + 1,
                           input_tokens = input_tokens + ?, output_tokens = output_tokens + ?,
                           cache_read_tokens = cache_read_tokens + ?,
                           cache_write_tokens = cache_write_tokens + ?
                           WHERE id = ?""",
                        (
                            item.usage.input_tokens,
                            item.usage.output_tokens,
                            item.usage.cache_read_tokens,
                            item.usage.cache_write_tokens,
                            run_id,
                        ),
                    )
                conn.commit()
                if progress:
                    progress(done, total)

        conn.execute("UPDATE run SET status='complete', finished_at=? WHERE id=?", (now(), run_id))
        conn.commit()
    except Exception as exc:
        conn.execute(
            "UPDATE run SET status='failed', error=?, finished_at=? WHERE id=?",
            (str(exc)[:1000], now(), run_id),
        )
        conn.commit()
        raise

    return _summary(conn, run_id), findings


def preview_run(
    conn: sqlite3.Connection,
    table_number: str,
    scope: RunScope,
    *,
    filler: CellFiller | None = None,
) -> list[dict[str, Any]]:
    """Build the exact requests a run would send, without sending any of them.

    This is what makes a run's cost knowable before it is paid for. The requests are built
    through the same helpers `execute_run` uses, so an estimate drawn from them describes
    the run that would actually happen.
    """
    table = conn.execute("SELECT * FROM review_table WHERE number = ?", (table_number,)).fetchone()
    if table is None:
        raise KernelError(f"Table {table_number} is not loaded in this matter.")
    filler = filler or CellFiller()
    units, columns = _plan(conn, int(table["id"]), scope)
    matter = conn.execute("SELECT * FROM matter WHERE id = 1").fetchone()
    instructions = binding.bind(
        table["table_instructions"] or "", matter=matter, entities=binding.entities_of(conn)
    )

    out: list[dict[str, Any]] = []
    for unit in units:
        unit_id = int(unit["id"])
        blocks, whole = _unit_context(conn, unit_id)
        if not blocks:
            continue
        system = filler.build_system(
            table_instructions=instructions,
            unit_label=unit["label"],
            evidence_blocks=blocks,
            cache_key=f"{table['number']}:{unit_id}",
        )
        for index, column in enumerate(columns):
            column_id = int(column["id"])
            existing = conn.execute(
                "SELECT value, locked, review_status FROM cell WHERE unit_id=? AND column_id=?",
                (unit_id, column_id),
            ).fetchone()
            if existing and not scope.refill and existing["value"]:
                continue
            if existing and (
                existing["locked"] or existing["review_status"] in {"Verified", "Corrected"}
            ):
                continue
            request = CellRequest(
                column_name=column["name"],
                prompt_text=column["prompt_text"],
                native_type=column["native_type"],
                configured_options=json.loads(column["configured_options"] or "null") or [],
                established=_established(conn, unit_id, column_id),
            )
            out.append(
                {
                    "unit_id": unit_id,
                    "unit": unit["label"],
                    "column": column["name"],
                    "native_type": column["native_type"],
                    "stage": column["stage"],
                    "system": system,
                    "request": request,
                    "user": filler.build_user(request),
                    # Only the first column of a unit pays to write the prefix into cache;
                    # the rest read it. `whole` says the unit's documents are in that prefix.
                    "cache_role": ("write" if index == 0 else "read") if whole else "none",
                }
            )
    return out


def _unit_context(conn: sqlite3.Connection, unit_id: int) -> tuple[list[dict[str, object]], bool]:
    """The unit's documents whole when they fit, else its opening passages.

    The boolean says whether the whole unit is present, which decides whether per-column
    retrieval is needed.
    """
    blocks = [
        b
        for b in search.unit_full_text(conn, unit_id, max_chars=WHOLE_UNIT_CHAR_BUDGET)
        if str(b.get("text", "")).strip()
    ]
    # A document that extracted to nothing — a scan without OCR — contributes no evidence.
    # Dropping it here is what makes the caller report the unit rather than ask the model to
    # answer from an empty page.
    size = sum(len(str(b.get("text", ""))) for b in blocks)
    whole = (
        bool(blocks)
        and size <= WHOLE_UNIT_CHAR_BUDGET
        and not any(b.get("truncated") for b in blocks)
    )
    if whole:
        return blocks, True
    passages = search.unit_passages(conn, unit_id, limit=RETRIEVAL_LIMIT)
    return (
        [
            {"filename": p.filename, "role": None, "text": p.text, "truncated": False}
            for p in passages
        ],
        False,
    )


def _established(conn: sqlite3.Connection, unit_id: int, column_id: int) -> dict[str, str]:
    """Upstream answers already recorded for this row, in the prompt's own terms."""
    rows = conn.execute(
        """SELECT c.name AS name, cell.value AS value
           FROM column_dep d
           JOIN column_def c ON c.id = d.upstream_id
           LEFT JOIN cell ON cell.column_id = d.upstream_id AND cell.unit_id = ?
           WHERE d.downstream_id = ?
           ORDER BY c.position""",
        (unit_id, column_id),
    ).fetchall()
    return {r["name"]: r["value"] for r in rows if r["value"]}


def _persist_cell(
    conn: sqlite3.Connection,
    *,
    unit_id: int,
    column_id: int,
    run_id: int,
    answer: Any,
    violations: list[str],
    usage: Usage,
    previous: sqlite3.Row | None,
) -> int:
    from .validate import is_fallback

    payload = (
        answer.value,
        int(is_fallback(answer.value)),
        json.dumps(violations),
        run_id,
        usage.input_tokens,
        usage.output_tokens,
        usage.cache_read_tokens,
        usage.cache_write_tokens,
        now(),
    )
    if previous:
        cell_id = int(previous["id"])
        conn.execute(
            """UPDATE cell SET value=?, is_fallback=?, validation=?, run_id=?,
               input_tokens=?, output_tokens=?, cache_read_tokens=?, cache_write_tokens=?,
               filled_at=?, stale=0 WHERE id=?""",
            (*payload, cell_id),
        )
        if previous["value"] != answer.value:
            conn.execute(
                """INSERT INTO cell_history
                   (cell_id, run_id, previous_value, new_value, reason, actor, changed_at)
                   VALUES (?,?,?,?, 'run', 'engine', ?)""",
                (cell_id, run_id, previous["value"], answer.value, now()),
            )
    else:
        cur = conn.execute(
            """INSERT INTO cell (unit_id, column_id, value, is_fallback, validation, run_id,
                                 input_tokens, output_tokens, cache_read_tokens,
                                 cache_write_tokens, filled_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (unit_id, column_id, *payload),
        )
        cell_id = int(cur.lastrowid)

    conn.execute("DELETE FROM cell_evidence WHERE cell_id = ?", (cell_id,))
    for rank, quote in enumerate(getattr(answer, "evidence", []) or []):
        located = _locate_quote(conn, unit_id, quote)
        if located is None:
            continue
        doc_id, chunk_id, start, end = located
        conn.execute(
            """INSERT INTO cell_evidence
               (cell_id, chunk_id, document_id, quote, char_start, char_end, rank)
               VALUES (?,?,?,?,?,?,?)""",
            (cell_id, chunk_id, doc_id, quote[:2000], start, end, rank),
        )
    return cell_id


def _locate_quote(
    conn: sqlite3.Connection, unit_id: int, quote: str
) -> tuple[int, int | None, int | None, int | None] | None:
    """Find a quoted sentence in the unit's documents so evidence carries an offset.

    A quote the engine cannot locate is dropped rather than stored with a false offset; the
    Verbatim validator is what reports a value that is not in the source.
    """
    probe = " ".join(quote.split())[:300]
    if not probe:
        return None
    for row in conn.execute(
        """SELECT d.id, d.full_text FROM unit_document ud
           JOIN document d ON d.id = ud.document_id WHERE ud.unit_id = ?""",
        (unit_id,),
    ):
        text = row["full_text"] or ""
        idx = text.find(probe)
        if idx == -1:
            collapsed = " ".join(text.split())
            j = collapsed.find(probe)
            if j == -1:
                continue
            return int(row["id"]), None, None, None
        chunk = conn.execute(
            """SELECT id FROM chunk WHERE document_id = ? AND char_start <= ? AND char_end >= ?
               ORDER BY chunk_index LIMIT 1""",
            (int(row["id"]), idx, idx),
        ).fetchone()
        return int(row["id"]), (int(chunk["id"]) if chunk else None), idx, idx + len(probe)
    return None


def _summary(conn: sqlite3.Connection, run_id: int) -> dict[str, Any]:
    row = conn.execute(
        """SELECT r.*, t.number AS table_number, t.title AS table_title
           FROM run r JOIN review_table t ON t.id = r.table_id WHERE r.id = ?""",
        (run_id,),
    ).fetchone()
    return {
        "run_id": run_id,
        "table": f"{row['table_number']} {row['table_title']}",
        "status": row["status"],
        "cells_total": row["cells_total"],
        "cells_done": row["cells_done"],
        "cells_failed": row["cells_failed"],
        "input_tokens": row["input_tokens"],
        "output_tokens": row["output_tokens"],
        "cache_read_tokens": row["cache_read_tokens"],
        "cache_write_tokens": row["cache_write_tokens"],
        "concurrency": row["concurrency"],
        "error": row["error"],
    }


def _prepare(
    conn: sqlite3.Connection,
    unit: sqlite3.Row,
    unit_id: int,
    column: sqlite3.Row,
    filler: CellFiller,
    table: sqlite3.Row,
    system: Any,
    sources: list[str],
    whole: bool,
    scope: RunScope,
    findings: list[Finding],
    instructions: str,
) -> _Prepared | None:
    """Assemble one cell's work on the calling thread, or None if it should be skipped.

    Every database read happens here — the skip checks, the established results, and the
    per-column retrieval — so that a worker thread only makes a network call.
    """
    column_id = int(column["id"])
    existing = conn.execute(
        "SELECT id, value, locked, review_status FROM cell WHERE unit_id=? AND column_id=?",
        (unit_id, column_id),
    ).fetchone()
    if existing and not scope.refill and existing["value"]:
        return None
    if existing and (existing["locked"] or existing["review_status"] in {"Verified", "Corrected"}):
        findings.append(
            Finding(
                code="CELL_LOCKED_NOT_REFILLED",
                subject_type="cell",
                subject_id=int(existing["id"]),
                subject_name=column["name"],
                observation=(
                    "The cell was left as it stands because it is "
                    f"{'locked' if existing['locked'] else existing['review_status'].lower()}."
                ),
                evidence={"unit": unit["label"], "column": column["name"]},
            )
        )
        return None

    per_column_system, per_column_sources = system, sources
    if not whole:
        passages = search.search_unit(conn, unit_id, column["prompt_text"], limit=RETRIEVAL_LIMIT)
        retrieved = [
            {
                "filename": p.filename,
                "role": None,
                "text": p.text,
                "truncated": False,
                "text_source": "extracted",
            }
            for p in passages
        ]
        per_column_system = filler.build_system(
            table_instructions=instructions,
            unit_label=unit["label"],
            evidence_blocks=retrieved,
            cache_key=f"{table['number']}:{unit_id}:{column['name']}",
        )
        per_column_sources = [p.text for p in passages]

    request = CellRequest(
        column_name=column["name"],
        prompt_text=column["prompt_text"],
        native_type=column["native_type"],
        configured_options=json.loads(column["configured_options"] or "null") or [],
        established=_established(conn, unit_id, column_id),
    )
    return _Prepared(
        column=column,
        request=request,
        system=per_column_system,
        sources=per_column_sources,
        existing=existing,
    )


def _call(filler: CellFiller, item: _Prepared) -> _Prepared:
    """The only work that runs off the calling thread. Never raises."""
    try:
        item.answer, item.usage = filler.fill(item.request, system=item.system)
    except Exception as exc:  # recorded per cell; one failure must not stop a stage
        item.error = exc
    return item
