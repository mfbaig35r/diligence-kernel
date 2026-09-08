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


NOT_A_REFERENCE = frozenset(
    {
        "",
        "not applicable",
        "not addressed",
        "not stated",
        "unable to determine",
        "none",
    }
)


def _names_a_base(value: str | None) -> bool:
    return (value or "").strip().lower() not in NOT_A_REFERENCE


def _tokens(value: str | None) -> set[str]:
    return {t for t in NOISE_RE.sub(" ", (value or "").lower()).split() if len(t) > 2}


def _best_base(
    dependent: sqlite3.Row, bases: list[sqlite3.Row]
) -> tuple[sqlite3.Row | None, float, float | None]:
    """Match a dependent document to the base it names.

    The parties are the strong signal and gate the candidate set; the reference text is
    then scored against each candidate's own description. Returns the best candidate, its
    score, and the runner-up score so the caller can report an ambiguous match.
    """
    reference = _tokens(dependent["amends_or_issued_under"])
    subject = (dependent["subject_entity"] or "").strip().lower()
    counterparty = (dependent["counterparty"] or "").strip().lower()

    scored: list[tuple[float, sqlite3.Row]] = []
    for base in bases:
        if subject and (base["subject_entity"] or "").strip().lower() != subject:
            continue
        if counterparty and (base["counterparty"] or "").strip().lower() != counterparty:
            continue
        described = _tokens(base["document_type"]) | _tokens(base["filename"])
        overlap = len(reference & described) / len(reference) if reference else 0.0
        scored.append((overlap, base))

    if not scored:
        return None, 0.0, None
    scored.sort(key=lambda kv: kv[0], reverse=True)
    best_score, best = scored[0]
    if best_score == 0.0:
        # The parties still identify one candidate; a zero text overlap is not a mismatch
        # when only one base agreement exists between these two parties.
        if len(scored) > 1:
            return None, 0.0, None
        return best, 0.0, None
    runner_up = scored[1][0] if len(scored) > 1 else None
    return best, best_score, runner_up


def documents_in_scope(conn: sqlite3.Connection, table_number: str) -> list[sqlite3.Row]:
    """Documents Table 05 routed to this table's workstream.

    A document is in scope when its workstream (or secondary workstream) maps to a set of
    tables containing this one, and its routing disposition has not excluded it.
    """
    rows = conn.execute(
        """SELECT d.id, d.filename, d.sha256, c.workstream, c.secondary_workstream, c.document_type,
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
        findings.append(
            Finding(
                code="NO_DOCUMENTS_IN_SCOPE",
                subject_type="table",
                subject_id=int(table["id"]),
                subject_name=f"Table {table_number}",
                observation="No classified document routes to this table.",
                evidence={"table": table_number},
            )
        )
        return [], findings

    grouped: dict[str, ProposedUnit] = {}
    if not table["grouping_enabled"]:
        for row in rows:
            key = f"file:{row['sha256'][:16]}"
            grouped[key] = ProposedUnit(
                unit_key=key,
                label=row["filename"],
                document_ids=[int(row["id"])],
                roles={int(row["id"]): row["document_role"]},
            )
        return list(grouped.values()), findings

    # Grouped tables: a family is a base instrument plus everything issued under it. Bases
    # anchor the families; dependents name their base in prose, so they are matched to it
    # rather than keyed on their own text — an amendment's `Amends or Issued Under` value
    # and its base agreement's own description are never the same string.
    bases = [r for r in rows if not _names_a_base(r["amends_or_issued_under"])]
    dependents = [r for r in rows if _names_a_base(r["amends_or_issued_under"])]

    anchors: dict[int, str] = {}
    for row in bases:
        key = f"fam:{row['sha256'][:16]}"
        anchors[int(row["id"])] = key
        grouped[key] = ProposedUnit(
            unit_key=key,
            label=(row["subject_entity"] or "")
            and " — ".join(p for p in (row["subject_entity"], row["counterparty"]) if p)
            or row["filename"],
            document_ids=[int(row["id"])],
            roles={int(row["id"]): row["document_role"] or "Base"},
        )

    for row in dependents:
        match, score, runner_up = _best_base(row, bases)
        if match is None:
            key = f"orphan:{row['sha256'][:16]}"
            grouped[key] = ProposedUnit(
                unit_key=key,
                label=row["filename"],
                document_ids=[int(row["id"])],
                roles={int(row["id"]): row["document_role"]},
            )
            findings.append(
                Finding(
                    code="DEPENDENT_WITHOUT_BASE",
                    subject_type="unit",
                    subject_id=None,
                    subject_name=row["filename"],
                    observation=(
                        f"{row['filename']} states that it is issued under "
                        f"{row['amends_or_issued_under']!r}, but no base document in scope matches; "
                        "it was placed in a unit of its own."
                    ),
                    evidence={"table": table_number, "reference": row["amends_or_issued_under"]},
                )
            )
            continue
        if runner_up is not None and score - runner_up < 0.15:
            findings.append(
                Finding(
                    code="BASE_MATCH_AMBIGUOUS",
                    subject_type="unit",
                    subject_id=None,
                    subject_name=row["filename"],
                    observation=(
                        f"{row['filename']} matched more than one candidate base document about "
                        "equally well; confirm the family before relying on the row."
                    ),
                    evidence={"table": table_number, "reference": row["amends_or_issued_under"]},
                )
            )
        unit = grouped[anchors[int(match["id"])]]
        unit.document_ids.append(int(row["id"]))
        unit.roles[int(row["id"])] = row["document_role"]

    cap = table["max_docs_per_unit"]
    units = list(grouped.values())
    for unit in units:
        if cap and len(unit.document_ids) > cap:
            findings.append(
                Finding(
                    code="UNIT_EXCEEDS_GROUPING_CAP",
                    subject_type="unit",
                    subject_id=None,
                    subject_name=unit.label,
                    observation=(
                        f"The proposed unit holds {len(unit.document_ids)} documents against a stated "
                        f"cap of {cap}."
                    ),
                    evidence={"table": table_number, "document_count": len(unit.document_ids)},
                )
            )
        if unit.unit_key == "unassigned":
            findings.append(
                Finding(
                    code="UNIT_KEY_UNRESOLVED",
                    subject_type="unit",
                    subject_id=None,
                    subject_name=unit.label,
                    observation=(
                        f"{len(unit.document_ids)} documents could not be grouped by subject and were "
                        "collected into one unassigned unit."
                    ),
                    evidence={"table": table_number, "document_count": len(unit.document_ids)},
                )
            )
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
