"""Table 05 is the vault's classifier.

Its review unit is one file and it runs over everything, which is why 00a builds it first:
"Everything routes through it." Running it produces cells like any other table; this module
projects those cells into the `classification` row that every other table's routing reads.

The projection is a copy, not a judgment. A cell holding a fallback state projects as no
value, because `Not addressed` is not a workstream.
"""

from __future__ import annotations

import sqlite3

from ..db import now
from ..engine.validate import is_fallback
from ..findings import Finding

INTAKE_TABLE = "05"

#: Table 05 column name -> classification field. Columns not listed stay in the cells only.
COLUMN_TO_FIELD: dict[str, str] = {
    "Workstream": "workstream",
    "Secondary Workstream": "secondary_workstream",
    "Document Type": "document_type",
    "Document Role": "document_role",
    "Subject Entity": "subject_entity",
    "Counterparty": "counterparty",
    "Document Date": "document_date",
    "Operative Date": "operative_date",
    "Amends or Issued Under": "amends_or_issued_under",
    "Compilation Flag": "compilation_flag",
    "Completeness": "completeness",
    "Language": "language",
    "Routing Disposition": "routing_disposition",
}


def project_intake(
    conn: sqlite3.Connection, *, run_id: int | None = None
) -> tuple[dict[str, int], list[Finding]]:
    """Copy Table 05's filled cells into the classification row for each file."""
    table = conn.execute("SELECT id FROM review_table WHERE number = ?", (INTAKE_TABLE,)).fetchone()
    if table is None:
        return {"classified": 0}, [
            Finding(
                code="INTAKE_TABLE_NOT_LOADED",
                subject_type="table",
                subject_id=None,
                subject_name=f"Table {INTAKE_TABLE}",
                observation="The intake table is not loaded, so no classification can be projected.",
                evidence={},
            )
        ]

    rows = conn.execute(
        """SELECT u.id AS unit_id, ud.document_id AS document_id, c.name AS column_name,
                  cell.value AS value
           FROM review_unit u
           JOIN unit_document ud ON ud.unit_id = u.id
           JOIN cell ON cell.unit_id = u.id
           JOIN column_def c ON c.id = cell.column_id
           WHERE u.table_id = ? AND cell.value IS NOT NULL""",
        (int(table["id"]),),
    ).fetchall()

    per_document: dict[int, dict[str, str]] = {}
    for row in rows:
        field = COLUMN_TO_FIELD.get(row["column_name"])
        if field is None:
            continue
        value = (row["value"] or "").strip()
        if not value or is_fallback(value):
            continue
        per_document.setdefault(int(row["document_id"]), {})[field] = value

    findings: list[Finding] = []
    classified = 0
    for document_id, fields in per_document.items():
        if "workstream" not in fields:
            name = conn.execute(
                "SELECT filename FROM document WHERE id = ?", (document_id,)
            ).fetchone()
            findings.append(
                Finding(
                    code="DOCUMENT_WITHOUT_WORKSTREAM",
                    subject_type="document",
                    subject_id=document_id,
                    subject_name=name["filename"] if name else str(document_id),
                    observation=(
                        "Table 05 returned no workstream for this file, so no workstream table "
                        "will see it."
                    ),
                    evidence={"document_id": document_id},
                )
            )
        keys = [*fields, "run_id", "classified_at"]
        values = [*fields.values(), run_id, now()]
        conn.execute(
            f"""INSERT INTO classification (document_id, {", ".join(keys)})
                VALUES (?{", ?" * len(keys)})
                ON CONFLICT(document_id) DO UPDATE SET
                {", ".join(f"{k}=excluded.{k}" for k in keys)}""",
            (document_id, *values),
        )
        classified += 1
    conn.commit()
    return {"classified": classified}, findings
