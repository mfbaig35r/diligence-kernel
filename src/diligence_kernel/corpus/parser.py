"""Deterministic parser for the review-table prompt inventories.

The corpus is mechanically regular: every inventory carries a `## Table` block, Table
Instructions in a fenced block, a dependency map, a column index, and one `### N. Name`
record per column whose prompt is a fenced block. That regularity is load-bearing, so this
parser never guesses. Anything it cannot resolve becomes a finding, not a silent default.

The one real subtlety: prompt section headings (`## Task`, `## Output format`) live *inside*
fenced blocks. Every scan here is fence-aware.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..constants import NATIVE_TYPE_ALIASES, NON_TABLE_PREFIXES
from ..findings import Finding

FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
COLUMN_RECORD_RE = re.compile(r"^###\s+(\d+)\.\s+(.+?)\s*$")
BULLET_RE = re.compile(r"^-\s+([A-Z][^:]{2,60}):\s*(.*)$")
FILENAME_RE = re.compile(r"^(?P<prefix>\d{2}[a-z]?)-(?P<slug>.+?)(?:-prompt-inventory)?\.md$")
BACKTICKED_RE = re.compile(r"`([^`]+)`")
AT_REF_RE = re.compile(r"@([A-Z][A-Za-z0-9''\u2010-\u2015\-/&()., ]*[A-Za-z0-9)])")

NONE_TOKENS = frozenset({"none", "—", "-", "n/a", ""})


@dataclass(slots=True)
class ColumnSpec:
    position: int
    name: str
    native_type: str | None
    type_caveat: str | None = None
    configured_options: list[str] = field(default_factory=list)
    #: Text in the options bullet that is not a backticked value — a cross-reference such as
    #: "the same 18 workstream values". When set, `configured_options` is incomplete.
    options_note: str | None = None
    upstream: list[str] = field(default_factory=list)
    downstream: list[str] = field(default_factory=list)
    purpose: str | None = None
    prompt_text: str = ""
    prompt_sections: list[str] = field(default_factory=list)
    at_refs: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "position": self.position,
            "name": self.name,
            "native_type": self.native_type,
            "type_caveat": self.type_caveat,
            "options_note": self.options_note,
            "configured_options": self.configured_options,
            "upstream": self.upstream,
            "downstream": self.downstream,
            "purpose": self.purpose,
            "prompt_text": self.prompt_text,
            "prompt_sections": self.prompt_sections,
            "at_refs": self.at_refs,
        }


@dataclass(slots=True)
class TableSpec:
    number: str
    slug: str
    title: str
    source_path: str
    review_unit: str | None = None
    grouping_enabled: bool = False
    max_docs_per_unit: int | None = None
    vault_project: str | None = None
    inventory_version: str | None = None
    table_instructions: str = ""
    dependency_map: str = ""
    columns: list[ColumnSpec] = field(default_factory=list)
    index_rows: list[dict[str, str]] = field(default_factory=list)
    test_set: list[str] = field(default_factory=list)
    human_review_fields: list[str] = field(default_factory=list)

    @property
    def is_table(self) -> bool:
        return self.number not in NON_TABLE_PREFIXES


# ---------------------------------------------------------------------------
# fence-aware scanning
# ---------------------------------------------------------------------------


def _fence_mask(lines: list[str]) -> list[bool]:
    """True for every line inside a fenced block, including the fence lines themselves."""
    mask = [False] * len(lines)
    open_fence: str | None = None
    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if open_fence is None:
            if m:
                open_fence = m.group(1)[0] * 3
                mask[i] = True
        else:
            mask[i] = True
            if m and m.group(1).startswith(open_fence):
                open_fence = None
    return mask


def _sections(lines: list[str], mask: list[bool], level: int) -> list[tuple[str, int, int]]:
    """Return (heading_text, body_start, body_end) for each heading at `level`, outside fences."""
    marks: list[tuple[str, int]] = []
    for i, line in enumerate(lines):
        if mask[i]:
            continue
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == level:
            marks.append((m.group(2), i))
    out: list[tuple[str, int, int]] = []
    for text, start in marks:
        # a section ends at the next heading of this level or shallower, outside fences
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if mask[j]:
                continue
            hm = HEADING_RE.match(lines[j])
            if hm and len(hm.group(1)) <= level:
                end = j
                break
        out.append((text, start + 1, end))
    return out


def _first_fenced_block(lines: list[str], start: int, end: int) -> str:
    """Text inside the first fenced block in [start, end), fences stripped."""
    open_fence: str | None = None
    body: list[str] = []
    for i in range(start, min(end, len(lines))):
        m = FENCE_RE.match(lines[i])
        if open_fence is None:
            if m:
                open_fence = m.group(1)[0] * 3
            continue
        if m and m.group(1).startswith(open_fence):
            break
        body.append(lines[i])
    return "\n".join(body).strip()


def _join_bullets(lines: list[str], start: int, end: int) -> list[tuple[str, str]]:
    """Collect `- Key: value` bullets, folding wrapped continuation lines into the value."""
    out: list[tuple[str, str]] = []
    mask = _fence_mask(lines[start:end])
    i = 0
    body = lines[start:end]
    while i < len(body):
        if mask[i]:
            i += 1
            continue
        m = BULLET_RE.match(body[i])
        if not m:
            i += 1
            continue
        key, value = m.group(1).strip(), m.group(2).strip()
        j = i + 1
        while j < len(body) and not mask[j]:
            nxt = body[j]
            if not nxt.strip() or BULLET_RE.match(nxt) or nxt.startswith(("-", "#", "|", "```")):
                break
            if nxt.startswith(("  ", "\t")):
                value += " " + nxt.strip()
                j += 1
                continue
            break
        out.append((key, value))
        i = j
    return out


def _split_names(raw: str) -> list[str]:
    """Split an Upstream/Downstream bullet into column names."""
    raw = raw.strip().rstrip(".")
    if raw.lower() in NONE_TOKENS:
        return []
    backticked = BACKTICKED_RE.findall(raw)
    parts = backticked if backticked else re.split(r"[;,]", raw)
    names: list[str] = []
    for p in parts:
        n = p.strip().strip("`").lstrip("@").strip()
        if not n or n.lower() in NONE_TOKENS:
            continue
        names.append(n)
    return names


def _parse_markdown_table(lines: list[str], start: int, end: int) -> list[dict[str, str]]:
    """Parse the first pipe table in [start, end) into a list of dicts keyed by header."""
    mask = _fence_mask(lines[start:end])
    body = lines[start:end]
    rows: list[list[str]] = []
    for i, line in enumerate(body):
        if mask[i]:
            continue
        s = line.strip()
        if not s.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return []
    header = [h.strip().lower() for h in rows[0]]
    out: list[dict[str, str]] = []
    for cells in rows[1:]:
        if all(set(c) <= {"-", ":", " "} for c in cells if c):
            continue
        out.append({header[k]: cells[k] for k in range(min(len(header), len(cells)))})
    return out


# ---------------------------------------------------------------------------
# the parse
# ---------------------------------------------------------------------------


def parse_inventory(path: Path) -> tuple[TableSpec, list[Finding]]:
    """Parse one inventory file. Returns the spec and findings for anything unresolved."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    mask = _fence_mask(lines)
    findings: list[Finding] = []

    fm = FILENAME_RE.match(path.name)
    if not fm:
        raise ValueError(f"unrecognised inventory filename: {path.name}")
    number, slug = fm.group("prefix"), fm.group("slug")

    h1 = next(
        (
            m.group(2)
            for i, ln in enumerate(lines)
            if not mask[i] and (m := HEADING_RE.match(ln)) and len(m.group(1)) == 1
        ),
        path.stem,
    )
    title = re.sub(r"^Prompt Inventory\s*[—–-]\s*", "", h1).strip()

    spec = TableSpec(number=number, slug=slug, title=title, source_path=str(path))
    h2 = _sections(lines, mask, 2)
    by_name = {name.strip().lower(): (s, e) for name, s, e in h2}

    # --- ## Table -----------------------------------------------------------------
    if (rng := by_name.get("table")) is not None:
        for key, value in _join_bullets(lines, *rng):
            k = key.lower()
            v = value.strip()
            if k == "review unit":
                spec.review_unit = _clean_inline(v)
            elif k == "grouping used":
                spec.grouping_enabled = v.lower().lstrip("*").startswith("yes")
                if dm := re.search(r"up to (\d+) documents", v):
                    spec.max_docs_per_unit = int(dm.group(1))
            elif k == "project":
                spec.vault_project = _clean_inline(v)
            elif k == "inventory version":
                spec.inventory_version = _clean_inline(v)

    # --- ## Table Instructions ------------------------------------------------------
    if (rng := by_name.get("table instructions")) is not None:
        spec.table_instructions = _first_fenced_block(lines, *rng)

    # --- ## Dependency map ----------------------------------------------------------
    if (rng := by_name.get("dependency map")) is not None:
        spec.dependency_map = _first_fenced_block(lines, *rng)

    # --- ## Column index ------------------------------------------------------------
    if (rng := by_name.get("column index")) is not None:
        spec.index_rows = _parse_markdown_table(lines, *rng)

    # --- ## Test set ----------------------------------------------------------------
    if (rng := by_name.get("test set")) is not None:
        s, e = rng
        for i in range(s, e):
            if mask[i]:
                continue
            if tm := re.match(r"^-\s*\[[ xX]\]\s*(.+?)\s*$", lines[i]):
                spec.test_set.append(_clean_inline(tm.group(1)))

    # --- ## Human-review fields -----------------------------------------------------
    if (rng := by_name.get("human-review fields")) is not None:
        for row in _parse_markdown_table(lines, *rng):
            name = _clean_inline(next(iter(row.values()), ""))
            if name:
                spec.human_review_fields.append(name)

    # --- ## Column records ----------------------------------------------------------
    if (rng := by_name.get("column records")) is not None:
        spec.columns, record_findings = _parse_column_records(lines, mask, *rng, number, str(path))
        findings.extend(record_findings)

    findings.extend(_cross_check(spec))
    return spec, findings


#: Words an options bullet may carry around its backticked values without meaning more.
_OPTIONS_FILLER = re.compile(
    r"\b(?:in\s+UI\s+order|plus|and|or|the|following|these|options?|values?|listed|below)\b",
    re.I,
)


def _options_prose(value: str) -> str | None:
    """Text in an options bullet that is not a backticked value.

    `- Configured options, in UI order: the same 18 workstream values, plus \`None\`` names a
    vocabulary the bullet does not spell out. Returning only the backticked part would hand
    the engine a controlled list missing eighteen of its twenty entries, and the model would
    comply with the truncation. So the prose is captured and the list is marked incomplete.
    """
    without = BACKTICKED_RE.sub(" ", value)
    residue = _OPTIONS_FILLER.sub(" ", without)
    residue = re.sub(r"[,;.:\s]+", " ", residue).strip()
    return " ".join(value.split()) if residue else None


def _split_type_caveat(value: str) -> tuple[str, str | None]:
    r"""Split `Date — confirm the type accepts \`Not stated\`` into type and caveat.

    A record's type bullet often carries a pre-run verification note after an em dash.
    00a section 8 calls those notes load-bearing, so they are kept, not discarded.
    """
    parts = re.split(r"\s+[—–]\s+|\s+--\s+", value, maxsplit=1)
    head = parts[0].strip()
    caveat = parts[1].strip().strip("`") if len(parts) > 1 and parts[1].strip() else None
    return head, caveat


def _clean_inline(v: str) -> str:
    """Strip markdown emphasis and backticks from a short inline value."""
    v = v.strip()
    v = re.sub(r"\*\*(.+?)\*\*", r"\1", v)
    v = re.sub(r"\*(.+?)\*", r"\1", v)
    return v.strip().strip("`").strip()


def _parse_column_records(
    lines: list[str], mask: list[bool], start: int, end: int, table_number: str, source: str
) -> tuple[list[ColumnSpec], list[Finding]]:
    findings: list[Finding] = []
    marks: list[tuple[int, str, int]] = []
    for i in range(start, end):
        if mask[i]:
            continue
        if m := COLUMN_RECORD_RE.match(lines[i]):
            marks.append((int(m.group(1)), m.group(2).strip(), i))

    columns: list[ColumnSpec] = []
    for idx, (pos, name, line_no) in enumerate(marks):
        body_end = marks[idx + 1][2] if idx + 1 < len(marks) else end
        col = ColumnSpec(position=pos, name=_clean_inline(name), native_type=None)

        for key, value in _join_bullets(lines, line_no + 1, body_end):
            k = key.lower()
            if k == "native type":
                raw, caveat = _split_type_caveat(_clean_inline(value))
                col.native_type = NATIVE_TYPE_ALIASES.get(raw.lower(), raw)
                col.type_caveat = caveat
            elif k.startswith("configured options"):
                col.configured_options = [
                    o.strip() for o in BACKTICKED_RE.findall(value) if o.strip()
                ]
                col.options_note = _options_prose(value)
            elif k == "upstream":
                col.upstream = _split_names(value)
            elif k == "downstream":
                col.downstream = _split_names(value)
            elif k == "purpose":
                col.purpose = _clean_inline(value)

        col.prompt_text = _first_fenced_block(lines, line_no + 1, body_end)
        col.prompt_sections = _prompt_sections(col.prompt_text)
        col.at_refs = _at_refs(col.prompt_text)

        if not col.prompt_text:
            findings.append(
                Finding(
                    code="PROMPT_MISSING",
                    subject_type="column",
                    subject_id=None,
                    subject_name=f"{table_number}.{pos} {col.name}",
                    observation="The column record has no fenced prompt block.",
                    evidence={"source": source, "line": line_no + 1},
                )
            )
        if col.native_type is None:
            findings.append(
                Finding(
                    code="NATIVE_TYPE_MISSING",
                    subject_type="column",
                    subject_id=None,
                    subject_name=f"{table_number}.{pos} {col.name}",
                    observation="The column record states no native type.",
                    evidence={"source": source, "line": line_no + 1},
                )
            )
        elif col.native_type == "Classify" and col.options_note:
            findings.append(
                Finding(
                    code="OPTIONS_NOT_ENUMERATED",
                    subject_type="column",
                    subject_id=None,
                    subject_name=f"{table_number}.{pos} {col.name}",
                    observation=(
                        "The options bullet names a vocabulary it does not spell out "
                        f"({col.options_note!r}), so only {len(col.configured_options)} of the "
                        "column's options could be read. A truncated controlled list would be "
                        "presented to the model as complete."
                    ),
                    evidence={
                        "source": source,
                        "line": line_no + 1,
                        "parsed": col.configured_options,
                        "bullet": col.options_note,
                    },
                )
            )
        elif col.native_type == "Classify" and not col.configured_options:
            findings.append(
                Finding(
                    code="CLASSIFY_OPTIONS_ABSENT",
                    subject_type="column",
                    subject_id=None,
                    subject_name=f"{table_number}.{pos} {col.name}",
                    observation="A Classify column lists no configured options in its record.",
                    evidence={
                        "source": source,
                        "line": line_no + 1,
                        "prompt_sections": col.prompt_sections,
                    },
                )
            )
        columns.append(col)
    return columns, findings


def _prompt_sections(prompt: str) -> list[str]:
    return [
        m.group(2).strip()
        for ln in prompt.splitlines()
        if (m := HEADING_RE.match(ln)) and len(m.group(1)) == 2
    ]


def _at_refs(prompt: str) -> list[str]:
    """Every `@Column` reference in a prompt, de-duplicated, in first-seen order."""
    seen: dict[str, None] = {}
    for raw in AT_REF_RE.findall(prompt):
        name = raw.strip().rstrip(".,;:")
        if name:
            seen.setdefault(name, None)
    return list(seen)


def resolve_at_refs(prompt: str, column_names: list[str]) -> tuple[list[str], list[str]]:
    """Resolve every `@` in a prompt against the table's own column names.

    Column names in this corpus contain em dashes and parentheses, so a regex cannot tell
    where a reference ends and prose resumes. Matching the longest known column name at
    each `@` can. Returns (resolved names, unresolved raw captures).
    """
    ordered = sorted(column_names, key=len, reverse=True)
    lowered = [(n.lower(), n) for n in ordered]
    resolved: dict[str, None] = {}
    unresolved: dict[str, None] = {}
    for m in re.finditer(r"@", prompt):
        tail = prompt[m.end() : m.end() + 120]
        tail_lower = tail.lower()
        hit = next((orig for low, orig in lowered if tail_lower.startswith(low)), None)
        if hit is not None:
            resolved.setdefault(hit, None)
            continue
        if rm := AT_REF_RE.match(prompt[m.start() :]):
            unresolved.setdefault(rm.group(1).strip().rstrip(".,;:"), None)
    return list(resolved), list(unresolved)


def _cross_check(spec: TableSpec) -> list[Finding]:
    """Compare the column index against the column records. They must agree."""
    findings: list[Finding] = []
    if not spec.index_rows or not spec.columns:
        return findings

    def index_name(row: dict[str, str]) -> str:
        return _clean_inline(row.get("column", ""))

    indexed = {index_name(r) for r in spec.index_rows if index_name(r)}
    recorded = {c.name for c in spec.columns}
    for name in sorted(indexed - recorded):
        findings.append(
            Finding(
                code="INDEX_COLUMN_WITHOUT_RECORD",
                subject_type="table",
                subject_id=None,
                subject_name=f"Table {spec.number}",
                observation=f"The column index lists {name!r} but no column record defines it.",
                evidence={"column": name},
            )
        )
    for name in sorted(recorded - indexed):
        findings.append(
            Finding(
                code="RECORD_COLUMN_WITHOUT_INDEX",
                subject_type="table",
                subject_id=None,
                subject_name=f"Table {spec.number}",
                observation=f"A column record defines {name!r} but the column index omits it.",
                evidence={"column": name},
            )
        )

    by_name = {c.name: c for c in spec.columns}
    for row in spec.index_rows:
        name = index_name(row)
        col = by_name.get(name)
        if col is None:
            continue
        idx_raw, _ = _split_type_caveat(_clean_inline(row.get("native type", "")))
        idx_type = NATIVE_TYPE_ALIASES.get(idx_raw.lower(), idx_raw)
        if idx_type and col.native_type and idx_type != col.native_type:
            findings.append(
                Finding(
                    code="NATIVE_TYPE_DISAGREES",
                    subject_type="column",
                    subject_id=None,
                    subject_name=f"{spec.number} {name}",
                    observation=(
                        f"The column index calls {name!r} {idx_type} and its record calls it "
                        f"{col.native_type}."
                    ),
                    evidence={"index": idx_type, "record": col.native_type},
                )
            )
    return findings


def parse_corpus(root: Path) -> tuple[list[TableSpec], list[Finding]]:
    """Parse every inventory in `root`, in file-prefix order."""
    specs: list[TableSpec] = []
    findings: list[Finding] = []
    for path in sorted(root.glob("*.md")):
        if not FILENAME_RE.match(path.name):
            continue
        try:
            spec, fs = parse_inventory(path)
        except Exception as exc:  # a file we cannot parse is a finding, not a crash
            findings.append(
                Finding(
                    code="INVENTORY_UNPARSED",
                    subject_type="corpus",
                    subject_id=None,
                    subject_name=path.name,
                    observation=f"The inventory could not be parsed: {exc}",
                    evidence={"source": str(path)},
                )
            )
            continue
        specs.append(spec)
        findings.extend(fs)
    return specs, findings
