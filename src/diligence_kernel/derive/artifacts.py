"""Derived artifacts: filters over persisted cells, never fresh questions.

00a section 2: "Never re-derive a consent schedule by asking Harvey a fresh question.
Filter and carry, so the schedule and its sources cannot disagree." Every artifact here is
a projection of cells that already exist. Nothing in this module calls a model, and nothing
invents a value that is not already in a cell.

An artifact reports the review status of every cell it carries, because a schedule built
from unreviewed candidates is a list of candidates, not a schedule.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field

from ..constants import MATERIALITY_VALUES
from ..findings import Finding


@dataclass(slots=True)
class ArtifactSpec:
    """Which columns feed an artifact, matched case-insensitively by name fragment."""

    key: str
    title: str
    column_patterns: tuple[str, ...]
    carry: tuple[str, ...] = ()
    description: str = ""
    exclude_fallbacks: bool = True


ARTIFACTS: dict[str, ArtifactSpec] = {
    "consent_schedule": ArtifactSpec(
        key="consent_schedule",
        title="Consent and approval schedule",
        column_patterns=(
            "consent trigger",
            "consent required",
            "change of control",
            "assignment restriction",
            "succession carve-out",
            "approval required",
            "landlord consent",
            "lender consent",
        ),
        carry=("Counterparty", "Subject Entity", "Target Contracting Entity", "Governing Law"),
        description=(
            "Every row whose provisions bear on whether the transaction needs a consent. "
            "Sourced from Contracts, Real Estate, Regulatory, Debt, Capitalization and Corporate."
        ),
    ),
    "coverage_register": ArtifactSpec(
        key="coverage_register",
        title="Coverage register — referenced but not produced",
        column_patterns=("referenced but not produced",),
        carry=("Documents in Unit", "Subject Entity", "Counterparty"),
        description=(
            "Documents the produced records refer to but that are absent. 00a routes this "
            "from every table into the supplemental request, which has the longest lead time."
        ),
    ),
    "closing_conditions": ArtifactSpec(
        key="closing_conditions",
        title="Closing conditions and calendar",
        column_patterns=(
            "closing condition",
            "notice period",
            "filing deadline",
            "expiry",
            "expiration",
            "renewal notice period",
            "termination notice",
        ),
        carry=("Subject Entity", "Counterparty"),
        description="Dated obligations and notice periods drawn from Regulatory, Debt and Corporate.",
    ),
    "transaction_payments": ArtifactSpec(
        key="transaction_payments",
        title="Transaction payments schedule",
        column_patterns=(
            "severance",
            "change of control payment",
            "acceleration",
            "transaction bonus",
            "retention",
            "prepayment",
            "make-whole",
            "payoff",
        ),
        carry=("Subject Entity", "Counterparty"),
        description=(
            "Amounts that may become payable on the transaction, each as stated in its source. "
            "00a section 7: totalling them happens in Excel, not here."
        ),
    ),
    "chain_gaps": ArtifactSpec(
        key="chain_gaps",
        title="Incomplete document chains",
        column_patterns=("chain completeness",),
        carry=("Documents in Unit", "Subject Entity", "Counterparty"),
        description=(
            "Rows whose family reveals a gap. A row with a missing amendment produces "
            "confidently wrong provision cells and nothing else detects it."
        ),
        exclude_fallbacks=False,
    ),
}

#: `Chain Completeness` values that are not gaps.
_NON_GAP = {"complete on its face", "not applicable"}


@dataclass(slots=True)
class ArtifactRow:
    table: str
    unit: str
    column: str
    value: str
    review_status: str
    materiality: str | None
    validation: list[str]
    carried: dict[str, str] = field(default_factory=dict)


def build_artifact(
    conn: sqlite3.Connection, key: str, *, min_review_status: str | None = None
) -> tuple[list[ArtifactRow], list[Finding]]:
    """Project the cells that feed one artifact. Returns rows and findings about them."""
    spec = ARTIFACTS.get(key)
    if spec is None:
        raise KeyError(f"Unknown artifact {key!r}. Known: {', '.join(sorted(ARTIFACTS))}.")

    clause = " OR ".join("LOWER(c.name) LIKE ?" for _ in spec.column_patterns)
    params = [f"%{p.lower()}%" for p in spec.column_patterns]
    rows = conn.execute(
        f"""SELECT t.number AS table_number, t.title AS table_title, u.id AS unit_id,
                   u.label AS unit_label, c.name AS column_name, cell.value AS value,
                   cell.review_status AS review_status, cell.materiality AS materiality,
                   cell.validation AS validation, cell.is_fallback AS is_fallback
            FROM cell
            JOIN column_def c ON c.id = cell.column_id
            JOIN review_unit u ON u.id = cell.unit_id
            JOIN review_table t ON t.id = c.table_id
            WHERE cell.value IS NOT NULL AND ({clause})
            ORDER BY t.number, u.position, c.position""",
        params,
    ).fetchall()

    import json

    out: list[ArtifactRow] = []
    unreviewed = 0
    flagged = 0
    for row in rows:
        value = (row["value"] or "").strip()
        if spec.exclude_fallbacks and row["is_fallback"]:
            continue
        if key == "chain_gaps" and value.lower() in _NON_GAP:
            continue
        if min_review_status and row["review_status"] != min_review_status:
            continue
        violations = json.loads(row["validation"] or "[]")
        if violations:
            flagged += 1
        if row["review_status"] == "Unreviewed":
            unreviewed += 1
        out.append(
            ArtifactRow(
                table=f"{row['table_number']} {row['table_title']}",
                unit=row["unit_label"],
                column=row["column_name"],
                value=value,
                review_status=row["review_status"],
                materiality=row["materiality"],
                validation=violations,
                carried=_carry(conn, int(row["unit_id"]), spec.carry),
            )
        )

    findings: list[Finding] = []
    if unreviewed:
        findings.append(
            Finding(
                code="ARTIFACT_CARRIES_UNREVIEWED_CELLS",
                subject_type="artifact",
                subject_id=None,
                subject_name=spec.title,
                observation=(
                    f"{unreviewed} of {len(out)} rows carry cells whose review status is still "
                    "Unreviewed."
                ),
                evidence={"artifact": key, "unreviewed": unreviewed, "rows": len(out)},
            )
        )
    if flagged:
        findings.append(
            Finding(
                code="ARTIFACT_CARRIES_FLAGGED_CELLS",
                subject_type="artifact",
                subject_id=None,
                subject_name=spec.title,
                observation=f"{flagged} rows carry cells with a recorded standards violation.",
                evidence={"artifact": key, "flagged": flagged},
            )
        )
    if not out:
        findings.append(
            Finding(
                code="ARTIFACT_EMPTY",
                subject_type="artifact",
                subject_id=None,
                subject_name=spec.title,
                observation="No filled cell matches this artifact's source columns.",
                evidence={"artifact": key, "patterns": list(spec.column_patterns)},
            )
        )
    return out, findings


def _carry(conn: sqlite3.Connection, unit_id: int, names: tuple[str, ...]) -> dict[str, str]:
    """Carry identifying columns from the same row, so a schedule row identifies itself."""
    if not names:
        return {}
    placeholders = ",".join("?" * len(names))
    rows = conn.execute(
        f"""SELECT c.name AS name, cell.value AS value FROM cell
            JOIN column_def c ON c.id = cell.column_id
            WHERE cell.unit_id = ? AND c.name COLLATE NOCASE IN ({placeholders})""",
        (unit_id, *names),
    ).fetchall()
    return {r["name"]: r["value"] for r in rows if r["value"]}


def issues_list(
    conn: sqlite3.Connection, *, materiality: tuple[str, ...] = ("Critical", "Material")
) -> tuple[list[ArtifactRow], list[Finding]]:
    """Every cell a human has marked material. 00a: the issues list is a filter, not a table."""
    import json

    unknown = [m for m in materiality if m not in MATERIALITY_VALUES]
    if unknown:
        raise ValueError(
            f"Unknown materiality {unknown}; 00a defines {', '.join(MATERIALITY_VALUES)}."
        )
    placeholders = ",".join("?" * len(materiality))
    rows = conn.execute(
        f"""SELECT t.number AS table_number, t.title AS table_title, u.id AS unit_id,
                   u.label AS unit_label, c.name AS column_name, cell.value AS value,
                   cell.review_status AS review_status, cell.materiality AS materiality,
                   cell.validation AS validation, cell.deal_consequence AS consequence
            FROM cell
            JOIN column_def c ON c.id = cell.column_id
            JOIN review_unit u ON u.id = cell.unit_id
            JOIN review_table t ON t.id = c.table_id
            WHERE cell.materiality IN ({placeholders})
            ORDER BY t.number, u.position, c.position""",
        materiality,
    ).fetchall()
    out = [
        ArtifactRow(
            table=f"{r['table_number']} {r['table_title']}",
            unit=r["unit_label"],
            column=r["column_name"],
            value=r["value"] or "",
            review_status=r["review_status"],
            materiality=r["materiality"],
            validation=json.loads(r["validation"] or "[]"),
            carried={"Deal consequence": r["consequence"]} if r["consequence"] else {},
        )
        for r in rows
    ]
    findings: list[Finding] = []
    if not out:
        findings.append(
            Finding(
                code="NO_MATERIALITY_RECORDED",
                subject_type="artifact",
                subject_id=None,
                subject_name="Issues list",
                observation=(
                    "No cell carries a materiality value; the issues list is built from the human "
                    "review column, which nobody has filled yet."
                ),
                evidence={"materiality": list(materiality)},
            )
        )
    return out, findings
