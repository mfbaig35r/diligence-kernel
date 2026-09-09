"""Load the parsed corpus into the matter database and compute execution order.

The markdown is the source of truth; these rows are derived and can be rebuilt at any
time. Reloading is idempotent: a table whose source file is unchanged is skipped unless
forced, and a changed file replaces its own rows only.

The engine needs one thing the markdown states only in prose: the order to fill columns
in. Every column's upstream set gives a DAG, and the topological stage of a column is the
length of the longest upstream chain reaching it. Stage 1 columns have no upstream and can
run concurrently; a stage N column may not run until every stage below it is filled.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

from ..constants import WORKSTREAM_TABLES, WORKSTREAMS_WITHOUT_TABLES
from ..db import now
from ..findings import Finding
from .parser import ColumnSpec, TableSpec, parse_corpus, resolve_at_refs


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compute_stages(columns: list[ColumnSpec]) -> tuple[dict[str, int], list[list[str]]]:
    """Return each column's stage and the cycles that prevented one being assigned.

    Upstream names are resolved case-insensitively against the table's own columns, which
    is what `@Column` means in Harvey: a reference within a table only.
    """
    by_lower = {c.name.lower(): c.name for c in columns}
    names = [c.name for c in columns]
    upstream: dict[str, set[str]] = {}
    for col in columns:
        detected, _ = resolve_at_refs(col.prompt_text, names)
        refs = {*(u.lower() for u in col.upstream), *(d.lower() for d in detected)}
        upstream[col.name] = {
            by_lower[r] for r in refs if r in by_lower and by_lower[r] != col.name
        }

    stages: dict[str, int] = {}
    remaining = dict(upstream)
    stage = 1
    while remaining:
        ready = [n for n, ups in remaining.items() if all(u in stages for u in ups)]
        if not ready:
            break  # everything left sits on a cycle
        for name in ready:
            stages[name] = stage
            del remaining[name]
        stage += 1

    cycles = [sorted(remaining)] if remaining else []
    return stages, cycles


def load_corpus(
    conn: sqlite3.Connection, root: Path, *, force: bool = False
) -> tuple[dict[str, int], list[Finding]]:
    """Parse `root` and persist every table inventory. Returns counts and findings."""
    specs, findings = parse_corpus(root)
    counts = {"tables": 0, "columns": 0, "skipped": 0, "dependencies": 0, "test_cases": 0}

    for spec in specs:
        if not spec.is_table:
            continue
        path = Path(spec.source_path)
        digest = _sha256(path)
        existing = conn.execute(
            "SELECT id, source_sha256 FROM review_table WHERE number = ?", (spec.number,)
        ).fetchone()
        if existing and existing["source_sha256"] == digest and not force:
            counts["skipped"] += 1
            continue
        if existing:
            conn.execute("DELETE FROM review_table WHERE id = ?", (existing["id"],))

        table_id = _insert_table(conn, spec, digest)
        column_ids = _insert_columns(conn, table_id, spec, findings)
        counts["dependencies"] += _insert_dependencies(conn, table_id, spec, column_ids, findings)
        for pos, text in enumerate(spec.test_set, start=1):
            conn.execute(
                "INSERT INTO test_case (table_id, position, text) VALUES (?, ?, ?)",
                (table_id, pos, text),
            )
        counts["test_cases"] += len(spec.test_set)
        counts["tables"] += 1
        counts["columns"] += len(spec.columns)

    findings.extend(_check_workstream_vocabulary(conn))
    conn.commit()
    return counts, findings


def _check_workstream_vocabulary(conn: sqlite3.Connection) -> list[Finding]:
    """Confirm every workstream Table 05 can return is accounted for.

    Routing matches a classification against `WORKSTREAM_TABLES`. If the corpus offers an
    option that map does not know, documents classified into it route to nothing and
    disappear from every table while looking correctly classified. This catches that at load
    time rather than letting it be discovered in a run's results.
    """
    row = conn.execute(
        """SELECT cd.configured_options FROM column_def cd
           JOIN review_table t ON t.id = cd.table_id
           WHERE t.number = '05' AND cd.name = 'Workstream'"""
    ).fetchone()
    if row is None or not row["configured_options"]:
        return []
    options = json.loads(row["configured_options"])
    known = set(WORKSTREAM_TABLES) | set(WORKSTREAMS_WITHOUT_TABLES)
    unknown = [o for o in options if o not in known]
    stale = [k for k in WORKSTREAM_TABLES if k not in options]

    findings: list[Finding] = []
    if unknown:
        findings.append(
            Finding(
                code="WORKSTREAM_NOT_ROUTED",
                subject_type="corpus",
                subject_id=None,
                subject_name="Table 05 Workstream",
                observation=(
                    f"{len(unknown)} workstream options have no routing entry, so a document "
                    f"classified into one would reach no table: {', '.join(unknown)}."
                ),
                evidence={"options": unknown},
            )
        )
    if stale:
        findings.append(
            Finding(
                code="WORKSTREAM_ROUTE_STALE",
                subject_type="corpus",
                subject_id=None,
                subject_name="Table 05 Workstream",
                observation=(
                    f"{len(stale)} routing entries name a workstream the corpus no longer offers: "
                    f"{', '.join(stale)}."
                ),
                evidence={"entries": stale},
            )
        )
    return findings


def _insert_table(conn: sqlite3.Connection, spec: TableSpec, digest: str) -> int:
    cur = conn.execute(
        """INSERT INTO review_table
           (number, slug, title, review_unit, grouping_enabled, max_docs_per_unit,
            vault_project, inventory_version, table_instructions, dependency_map,
            source_path, source_sha256, ingested_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            spec.number,
            spec.slug,
            spec.title,
            spec.review_unit,
            int(spec.grouping_enabled),
            spec.max_docs_per_unit,
            spec.vault_project,
            spec.inventory_version,
            spec.table_instructions,
            spec.dependency_map,
            spec.source_path,
            digest,
            now(),
        ),
    )
    return int(cur.lastrowid)


def _insert_columns(
    conn: sqlite3.Connection, table_id: int, spec: TableSpec, findings: list[Finding]
) -> dict[str, int]:
    stages, cycles = compute_stages(spec.columns)
    for cycle in cycles:
        findings.append(
            Finding(
                code="DEPENDENCY_CYCLE",
                subject_type="table",
                subject_id=table_id,
                subject_name=f"Table {spec.number}",
                observation=(
                    f"{len(cycle)} columns could not be assigned an execution stage because their "
                    "upstream references form a cycle."
                ),
                evidence={"columns": cycle},
            )
        )
    ids: dict[str, int] = {}
    for col in spec.columns:
        cur = conn.execute(
            """INSERT INTO column_def
               (table_id, position, name, native_type, type_caveat, configured_options,
                purpose, prompt_text, prompt_chars, prompt_sections, stage)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                table_id,
                col.position,
                col.name,
                col.native_type or "Free Response",
                col.type_caveat,
                json.dumps(col.configured_options) if col.configured_options else None,
                col.purpose,
                col.prompt_text,
                len(col.prompt_text),
                json.dumps(col.prompt_sections),
                stages.get(col.name),
            ),
        )
        ids[col.name.lower()] = int(cur.lastrowid)
    return ids


def _insert_dependencies(
    conn: sqlite3.Connection,
    table_id: int,
    spec: TableSpec,
    ids: dict[str, int],
    findings: list[Finding],
) -> int:
    """Record every edge, and report an @ref that names no column in the table.

    00a section 6: "Every `@` reference must be consumed by a rule. A reference no rule
    uses is deleted, not kept for context." The mirror of that is an @ref that resolves to
    nothing, which would silently fill a cell from an empty upstream.
    """
    count = 0
    names = [c.name for c in spec.columns]
    for col in spec.columns:
        down_id = ids.get(col.name.lower())
        if down_id is None:
            continue
        resolved, unresolved = resolve_at_refs(col.prompt_text, names)
        for ref in unresolved:
            findings.append(
                Finding(
                    code="AT_REF_UNRESOLVED",
                    subject_type="column",
                    subject_id=down_id,
                    subject_name=f"{spec.number} {col.name}",
                    observation=(
                        f"The prompt references @{ref} but no column of that name exists "
                        f"in Table {spec.number}."
                    ),
                    evidence={"reference": ref},
                )
            )
        declared = {u.lower() for u in col.upstream}
        detected = {r.lower() for r in resolved}
        for ref in declared | detected:
            up_id = ids.get(ref)
            if up_id is None:
                continue
            if up_id == down_id:
                continue
            source = "record" if ref in declared else "at_ref"
            conn.execute(
                """INSERT OR IGNORE INTO column_dep
                   (table_id, upstream_id, downstream_id, source) VALUES (?,?,?,?)""",
                (table_id, up_id, down_id, source),
            )
            count += 1
    return count
