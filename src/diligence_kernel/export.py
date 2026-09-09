"""Emitting the corpus in the shape `prompt-graph` ingests.

The two servers divide the work: this kernel parses files, meets documents and produces
evidence; `prompt-graph` holds prompt versions, the cross-table dependency graph, the
evaluation log, and the change-log discipline `00a` section 11 requires. Neither can call the
other — MCP servers do not talk to each other — so the seam is a record shape, and Claude
carries it across.

`table_ingest` takes one normalized record per column. That is what this produces, from the
corpus the kernel already parsed, so nobody retypes 591 prompts.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any

#: prompt-graph's spelling of the native types.
NATIVE_TYPE = {
    "Free Response": "FreeResponse",
    "Classify": "Classify",
    "Date": "Date",
    "Currency": "Currency",
    "Number": "Number",
    "Duration": "Duration",
    "Verbatim": "Verbatim",
}

#: 00a's staged design, mapped from the topological stage the loader computed. prompt-graph
#: uses `role` to check ordering against the skill's staged pattern.
STAGE_ROLE = {1: "orientation", 2: "extraction", 3: "validation", 4: "reconciliation"}


def column_records(conn: sqlite3.Connection, table_number: str) -> list[dict[str, Any]]:
    """One `ColumnRecord` per column of a table, in table order."""
    rows = conn.execute(
        """SELECT cd.id, cd.position, cd.name, cd.native_type, cd.configured_options,
                  cd.purpose, cd.prompt_text, cd.stage
           FROM column_def cd JOIN review_table t ON t.id = cd.table_id
           WHERE t.number = ? ORDER BY cd.position""",
        (table_number,),
    ).fetchall()
    out: list[dict[str, Any]] = []
    for row in rows:
        upstream = [
            r["name"]
            for r in conn.execute(
                """SELECT c.name FROM column_dep d JOIN column_def c ON c.id = d.upstream_id
                   WHERE d.downstream_id = ? ORDER BY c.position""",
                (int(row["id"]),),
            )
        ]
        record: dict[str, Any] = {
            "name": row["name"],
            "position": row["position"],
            "native_type": NATIVE_TYPE.get(row["native_type"], row["native_type"]),
            "prompt_text": row["prompt_text"],
            "status": "draft",
        }
        if row["configured_options"]:
            record["configured_options"] = json.loads(row["configured_options"])
        if row["purpose"]:
            record["purpose"] = row["purpose"]
        if upstream:
            record["upstream_refs"] = upstream
        if (role := STAGE_ROLE.get(row["stage"] or 0)) is not None:
            record["role"] = role
        out.append(record)
    return out


def table_payload(conn: sqlite3.Connection, table_number: str) -> dict[str, Any]:
    """Everything one `table_ingest` call needs for a table."""
    table = conn.execute(
        """SELECT number, title, review_unit, grouping_enabled, max_docs_per_unit,
                  vault_project, table_instructions
           FROM review_table WHERE number = ?""",
        (table_number,),
    ).fetchone()
    if table is None:
        raise KeyError(f"Table {table_number} is not loaded.")
    return {
        "table": f"{table['number']} {table['title']}",
        "table_meta": {
            "review_unit": table["review_unit"],
            "platform": "harvey",
            "grouping_enabled": bool(table["grouping_enabled"]),
            "max_docs_per_unit": table["max_docs_per_unit"],
            "position": int(table["number"]) if table["number"].isdigit() else None,
        },
        "table_instructions": table["table_instructions"],
        "columns": column_records(conn, table_number),
    }


def write_payloads(
    conn: sqlite3.Connection, out_dir: str, tables: list[str] | None = None
) -> list[str]:
    """Write one JSON payload per table, so a large corpus need not pass through a prompt."""
    from pathlib import Path

    target = Path(out_dir).expanduser()
    target.mkdir(parents=True, exist_ok=True)
    numbers = tables or [
        r["number"] for r in conn.execute("SELECT number FROM review_table ORDER BY number")
    ]
    written: list[str] = []
    for number in numbers:
        path = target / f"table-{number}.json"
        path.write_text(json.dumps(table_payload(conn, number), indent=2), encoding="utf-8")
        written.append(str(path))
    return written
