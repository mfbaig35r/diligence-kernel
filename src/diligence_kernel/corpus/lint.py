"""Auditing the corpus against the standards it sets for itself.

`00a` states rules that the 591 prompts are supposed to follow. Most of them can be checked
mechanically, and the ones that can are checked here — once, over the whole corpus, rather
than one violation at a time in a run's results.

The distinction matters. A prompt that instructs a banned value produces one violation per
cell it fills: nine identical findings in a ten-document matter, thousands in a real one,
drowning everything else. That is a defect in one prompt, and it should be reported as one
finding against that prompt.

Nothing here rewrites a prompt. The `legal-review-table-builder` skill drafts; this reports.
"""

from __future__ import annotations

import json
import re
import sqlite3

from ..constants import (
    BANNED_FALLBACKS,
    FALLBACK_VOCABULARY,
    POSITIVE_NULL_FINDINGS,
    PROMPT_CHAR_BUDGET,
    PROMPT_SECTION_ORDER,
)
from ..findings import Finding

#: `Return exactly \`X\`` / `Use \`X\`` — what the prompt tells the model to answer with.
RETURN_INSTRUCTION = re.compile(r"(?:return|use)\s+(?:exactly\s+)?`([^`]+)`", re.I)


def lint_corpus(conn: sqlite3.Connection) -> list[Finding]:
    """Every mechanical check `00a` supports, over every loaded column."""
    findings: list[Finding] = []
    rows = conn.execute(
        """SELECT t.number, t.title, cd.id, cd.name, cd.native_type, cd.configured_options,
                  cd.prompt_text, cd.prompt_chars, cd.prompt_sections
           FROM column_def cd JOIN review_table t ON t.id = cd.table_id
           ORDER BY t.number, cd.position"""
    ).fetchall()
    for row in rows:
        subject = f"{row['number']} {row['name']}"
        options = json.loads(row["configured_options"] or "null") or []
        prompt = row["prompt_text"] or ""
        told = {m.strip() for m in RETURN_INSTRUCTION.findall(prompt)}

        findings.extend(_banned_values(row, subject, options, told))
        findings.extend(_unconfigured_return(row, subject, options, told))
        findings.extend(_over_budget(row, subject))
        findings.extend(_section_order(row, subject))
    return findings


def _banned_values(row, subject, options, told) -> list[Finding]:
    """A prompt or option list that uses a value 00a section 5 forbids.

    `00a` bans bare `None` and provides the positive-finding family for the case these
    columns actually mean: the search was run and nothing was found.
    """
    banned = {b.lower() for b in BANNED_FALLBACKS}
    in_options = [o for o in options if o.strip().lower() in banned]
    in_prompt = sorted(v for v in told if v.lower() in banned)
    if not in_options and not in_prompt:
        return []

    where = []
    if in_options:
        where.append(f"its configured options include {', '.join(repr(o) for o in in_options)}")
    if in_prompt:
        where.append(f"its prompt instructs {', '.join(repr(v) for v in in_prompt)}")
    suggestion = ", ".join(f"`{p}`" for p in POSITIVE_NULL_FINDINGS[:3])
    return [
        Finding(
            code="BANNED_VALUE_IN_PROMPT",
            subject_type="column",
            subject_id=int(row["id"]),
            subject_name=subject,
            observation=(
                f"The column returns a value 00a section 5 bans: {'; and '.join(where)}. Where the "
                f"meaning is that a search was run and found nothing, 00a's positive-finding form "
                f"({suggestion}) says so without colliding with the fallback vocabulary."
            ),
            evidence={"options": in_options, "prompt": in_prompt},
        )
    ]


def _unconfigured_return(row, subject, options, told) -> list[Finding]:
    """A Classify column told to return a value its own option list does not offer.

    Harvey's UI accepts only configured options, so such a cell cannot be filled as
    instructed. Only fallback states are checked: a reference to another column's value is
    not an instruction about this one.
    """
    if row["native_type"] != "Classify" or not options:
        return []
    lowered = {o.lower() for o in options}
    fallbacks = {f.lower() for f in FALLBACK_VOCABULARY}
    missing = sorted(v for v in told if v.lower() in fallbacks and v.lower() not in lowered)
    if not missing:
        return []
    return [
        Finding(
            code="RETURN_VALUE_NOT_CONFIGURED",
            subject_type="column",
            subject_id=int(row["id"]),
            subject_name=subject,
            observation=(
                f"The prompt instructs {', '.join(repr(m) for m in missing)}, which the column's "
                "configured options do not offer, so the cell cannot be filled as instructed."
            ),
            evidence={"instructed": missing, "options": options},
        )
    ]


def _over_budget(row, subject) -> list[Finding]:
    if (row["prompt_chars"] or 0) <= PROMPT_CHAR_BUDGET:
        return []
    return [
        Finding(
            code="PROMPT_OVER_BUDGET",
            subject_type="column",
            subject_id=int(row["id"]),
            subject_name=subject,
            observation=(
                f"The prompt is {row['prompt_chars']:,} characters against the {PROMPT_CHAR_BUDGET:,} "
                "00a section 6 allows, which leaves no room for the rules testing will add."
            ),
            evidence={"chars": row["prompt_chars"], "budget": PROMPT_CHAR_BUDGET},
        )
    ]


def _section_order(row, subject) -> list[Finding]:
    """00a section 6 fixes the order of a prompt's sections, ending with the output contract."""
    sections = [s for s in json.loads(row["prompt_sections"] or "[]") if s in PROMPT_SECTION_ORDER]
    if len(sections) < 2:
        return []
    rank = {name: i for i, name in enumerate(PROMPT_SECTION_ORDER)}
    order = [rank[s] for s in sections]
    if order == sorted(order):
        return []
    return [
        Finding(
            code="PROMPT_SECTIONS_OUT_OF_ORDER",
            subject_type="column",
            subject_id=int(row["id"]),
            subject_name=subject,
            observation=(
                f"The prompt's sections run {' -> '.join(sections)}, which departs from the order "
                "00a section 6 sets so that the final instruction is the output contract."
            ),
            evidence={"sections": sections},
        )
    ]
