"""Assembling review units — deciding what one row is.

00a is emphatic that grouping surfaces differences among documents but does not establish
which one controls. So this module does exactly one thing: it puts documents that belong
to the same subject in one unit. It never decides which is operative; that is a human
column, and the engine has no opinion about it.

Routing comes from Table 05's output. A document with no classification is unrouted and
reported, never quietly dropped.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass

from ..constants import WORKSTREAM_TABLES
from ..db import now
from ..findings import Finding

NOISE_RE = re.compile(r"[^a-z0-9]+")


def normalize_key(*parts: str | None) -> str:
    """A stable grouping key from the parts that identify a subject."""
    cleaned = [NOISE_RE.sub(" ", (p or "").lower()).strip() for p in parts]
    return " | ".join(c for c in cleaned if c) or "unassigned"


def tables_for_workstream(workstream: str | None) -> tuple[str, ...]:
    if not workstream:
        return ()
    for name, numbers in WORKSTREAM_TABLES.items():
        if name.lower() == workstream.strip().lower():
            return numbers
    return ()


@dataclass(slots=True)
class ProposedUnit:
    unit_key: str
    label: str
    document_ids: list[int]
    roles: dict[int, str | None]


def documents_in_scope(conn: sqlite3.Connection, table_number: str) -> list[sqlite3.Row]:
    """Documents Table 05 routed to this table's workstream.

    A document is in scope when its workstream (or secondary workstream) maps to a set of
    tables containing this one, and its routing disposition has not excluded it.
    """
    rows = conn.execute(
        """SELECT d.id, d.filename, c.workstream, c.secondary_workstream, c.document_type,
                  c.subject_entity, c.counterparty, c.document_date, c.amends_or_issued_under,
                  c.routing_disposition, c.document_role
           FROM document d
           JOIN classification c ON c.document_id = d.id
           WHERE d.extract_status = 'extracted'
           ORDER BY c.document_date, d.filename"""
    ).fetchall()
    out = []
    for row in rows:
        disposition = (row["routing_disposition"] or "").strip().lower()
        if disposition.startswith(("exclude", "do not", "split")):
            continue
        primary = tables_for_workstream(row["workstream"])
        secondary = tables_for_workstream(row["secondary_workstream"])
        if table_number in primary or table_number in secondary:
            out.append(row)
    return out


def propose_units(
    conn: sqlite3.Connection, table_number: str
) -> tuple[list[ProposedUnit], list[Finding]]:
    """Propose the rows for a table without writing them."""
    findings: list[Finding] = []
    table = conn.execute(
        "SELECT id, title, review_unit, grouping_enabled, max_docs_per_unit FROM review_table WHERE number = ?",
        (table_number,),
    ).fetchone()
    if table is None:
        raise ValueError(f"Table {table_number} is not loaded in this matter.")

    rows = documents_in_scope(conn, table_number)
    if not rows:
        findings.append(Finding(
            code="NO_DOCUMENTS_IN_SCOPE", subject_type="table", subject_id=int(table["id"]),
            subject_name=f"Table {table_number}",
            observation="No classified document routes to this table.",
            evidence={"table": table_number},
        ))
        return [], findings

    grouped: dict[str, ProposedUnit] = {}
    if not table["grouping_enabled"]:
        for row in rows:
            key = f"file:{row['id']}"
            grouped[key] = ProposedUnit(
                unit_key=key, label=row["filename"],
                document_ids=[int(row["id"])], roles={int(row["id"]): row["document_role"]},
            )
    else:
        for row in rows:
            base = (row["amends_or_issued_under"] or "").strip()
            subject = (row["subject_entity"] or "").strip()
            counterparty = (row["counterparty"] or "").strip()
            doc_type = (row["document_type"] or "").strip()
            # A document that names its base instrument joins that family; otherwise the
            # subject and counterparty identify it.
            key = normalize_key(base) if base and base.lower() not in {"not applicable", "not addressed"} \
                else normalize_key(subject, counterparty, doc_type)
            unit = grouped.get(key)
            if unit is None:
                label = base or " — ".join(p for p in (subject, counterparty) if p) or row["filename"]
                unit = ProposedUnit(unit_key=key, label=label, document_ids=[], roles={})
                grouped[key] = unit
            unit.document_ids.append(int(row["id"]))
            unit.roles[int(row["id"])] = row["document_role"]

    cap = table["max_docs_per_unit"]
    units = list(grouped.values())
    for unit in units:
        if cap and len(unit.document_ids) > cap:
            findings.append(Finding(
                code="UNIT_EXCEEDS_GROUPING_CAP", subject_type="unit", subject_id=None,
                subject_name=unit.label,
                observation=(
                    f"The proposed unit holds {len(unit.document_ids)} documents against a stated "
                    f"cap of {cap}."
                ),
                evidence={"table": table_number, "document_count": len(unit.document_ids)},
            ))
        if unit.unit_key == "unassigned":
            findings.append(Finding(
                code="UNIT_KEY_UNRESOLVED", subject_type="unit", subject_id=None,
                subject_name=unit.label,
                observation=(
                    f"{len(unit.document_ids)} documents could not be grouped by subject and were "
                    "collected into one unassigned unit."
                ),
                evidence={"table": table_number, "document_count": len(unit.document_ids)},
            ))
    return units, findings


def assemble_units(
    conn: sqlite3.Connection, table_number: str, *, replace: bool = False
) -> tuple[dict[str, int], list[Finding]]:
    """Write the proposed units for a table. Existing human-assembled units are preserved."""
    units, findings = propose_units(conn, table_number)
    table = conn.execute("SELECT id FROM review_table WHERE number = ?", (table_number,)).fetchone()
    table_id = int(table["id"])

    if replace:
        conn.execute(
            "DELETE FROM review_unit WHERE table_id = ? AND assembled_by = 'auto'", (table_id,)
        )

    counts = {"created": 0, "existing": 0, "documents": 0}
    position = conn.execute(
        "SELECT COALESCE(MAX(position), 0) AS p FROM review_unit WHERE table_id = ?", (table_id,)
    ).fetchone()["p"]

    for unit in units:
        existing = conn.execute(
            "SELECT id FROM review_unit WHERE table_id = ? AND unit_key = ?",
            (table_id, unit.unit_key),
        ).fetchone()
        if existing:
            unit_id = int(existing["id"])
            counts["existing"] += 1
        else:
            position += 1
            cur = conn.execute(
                """INSERT INTO review_unit (table_id, position, label, unit_key, assembled_by, created_at)
                   VALUES (?,?,?,?, 'auto', ?)""",
                (table_id, position, unit.label[:300], unit.unit_key, now()),
            )
            unit_id = int(cur.lastrowid)
            counts["created"] += 1
        for doc_id in unit.document_ids:
            conn.execute(
                "INSERT OR IGNORE INTO unit_document (unit_id, document_id, role) VALUES (?,?,?)",
                (unit_id, doc_id, unit.roles.get(doc_id)),
            )
            counts["documents"] += 1

    conn.commit()
    return counts, findings


def unrouted_documents(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Extracted documents Table 05 has not classified. These are invisible to every table."""
    return conn.execute(
        """SELECT d.id, d.filename FROM document d
           LEFT JOIN classification c ON c.document_id = d.id
           WHERE d.extract_status = 'extracted' AND (c.id IS NULL OR c.workstream IS NULL)
           ORDER BY d.filename"""
    ).fetchall()
