"""Standards from `00a-build-plan-and-standards.md`, encoded once.

These are not suggestions the prompts make; they are the contract the engine enforces
on a cell before it persists. Section references point back into `00a`.
"""

from __future__ import annotations

# --- 00a section 5: the fallback vocabulary -------------------------------------------

#: The only five absence states any cell may return.
FALLBACK_VOCABULARY: tuple[str, ...] = (
    "Not addressed",
    "Not stated",
    "Not applicable",
    "Incorporated terms",
    "Unable to determine",
)

#: `Not stated` is reserved for typed columns.
NOT_STATED_TYPES: frozenset[str] = frozenset({"Date", "Number", "Currency", "Duration"})

#: Synonyms 00a bans outright. Matched case-insensitively against a whole cell.
BANNED_FALLBACKS: tuple[str, ...] = (
    "N/A",
    "None",
    "Silent",
    "Unclear",
    "Not determinable",
    "Not found",
)

#: Positive findings that read like absences but are answers. Each is defined by the
#: column that uses it, so the engine allows them without treating them as fallbacks.
POSITIVE_NULL_FINDINGS: tuple[str, ...] = (
    "None identified",
    "None referenced",
    "None recorded",
    "None named",
    "None disclosed",
)

# --- 00a section 6: prompt construction standard --------------------------------------

#: Canonical section order inside a prompt. A prompt may omit sections; it may not
#: reorder them.
PROMPT_SECTION_ORDER: tuple[str, ...] = (
    "Established results",
    "Task",
    "Scope",
    "Options",
    "Response labels",
    "Classification rules",
    "Extraction rules",
    "Rules",
    "Fallback rules",
    "Output format",
)

#: 00a section 6: "Keep each prompt under 6,000 characters against the ~10,000 limit."
PROMPT_CHAR_BUDGET = 6000
PROMPT_CHAR_HARD_LIMIT = 10000

# --- Harvey native types ---------------------------------------------------------------

NATIVE_TYPES: tuple[str, ...] = (
    "Free Response",
    "Classify",
    "Date",
    "Number",
    "Currency",
    "Duration",
    "Verbatim",
)

#: How the inventories spell types, folded to the canonical spelling above.
NATIVE_TYPE_ALIASES: dict[str, str] = {
    "free response": "Free Response",
    "freeresponse": "Free Response",
    "fr": "Free Response",
    "classify": "Classify",
    "date": "Date",
    "number": "Number",
    "currency": "Currency",
    "duration": "Duration",
    "verbatim": "Verbatim",
}

#: Types whose answer must be reproduced from the source, not summarised. These take the
#: span-exact retrieval path, never the chunk-summary path.
SPAN_EXACT_TYPES: frozenset[str] = frozenset({"Verbatim"})

# --- 00a section 4: the universal spine -------------------------------------------------

UNIVERSAL_SPINE: tuple[str, ...] = (
    "Documents in Unit",
    "Subject entity",
    "Document type",
    "Execution status",
    "Document date",
    "Operative date",
    "Amends or issued under",
    "Chain completeness",
    "Referenced but not produced",
    "Governing law",
)

HUMAN_REVIEW_FIELDS: tuple[str, ...] = (
    "Review status",
    "Reviewed by",
    "Operative version confirmed",
    "Materiality",
    "Deal consequence",
)

REVIEW_STATUSES: tuple[str, ...] = ("Unreviewed", "Verified", "Corrected", "Disputed")
MATERIALITY_VALUES: tuple[str, ...] = ("Critical", "Material", "Monitor", "Immaterial")

COLUMN_STATUSES: tuple[str, ...] = ("draft", "testing", "verified", "retired")

# --- 00a section 7: report, never compute -----------------------------------------------

#: Cells are checked for arithmetic the engine must refuse to perform. A cell whose text
#: shows a computed total is a standards violation, not a finding.
ARITHMETIC_MARKERS: tuple[str, ...] = (
    "total of",
    "sum of",
    "net of",
    "aggregate of",
    "calculated as",
    "which equals",
    "for a total",
)

# --- 00a section 3: vault project structure ---------------------------------------------

#: Workstream -> the tables that run over it.
#:
#: **The keys are Table 05's own configured options, verbatim.** They were once hand-written
#: paraphrases (`Contracts`, `Finance`), which matched 4 of the corpus's 19 values — so a
#: document classified `Debt and Financing` routed to nothing and vanished from every table
#: while looking correctly classified. `WORKSTREAMS_WITHOUT_TABLES` records the values that
#: legitimately route nowhere, so an empty result is a stated fact rather than a silent miss.
WORKSTREAM_TABLES: dict[str, tuple[str, ...]] = {
    "Corporate and Entity Structure": ("02",),
    "Capitalization and Securities": ("03", "04"),
    "Commercial Contracts": ("01", "07"),
    # 00a section 2: served by Contracts Core filtered on Counterparty Type, not its own table.
    "Vendor and Supplier": ("01", "07"),
    "IP and Technology": ("10", "11", "12"),
    "Employment and HR": ("08", "09"),
    "Real Estate": ("13", "14"),
    "Environmental": ("21", "22", "23"),
    "Litigation and Disputes": ("15",),
    "Regulatory and Licenses": ("16", "17"),
    "Tax": ("24", "25"),
    "Insurance": ("20",),
    "Debt and Financing": ("18", "19"),
}

#: Workstreams Table 05 can return that no table in this corpus covers, and why. Routing to
#: nothing is correct for these; being unable to say so is not.
WORKSTREAMS_WITHOUT_TABLES: dict[str, str] = {
    "Privacy and Cybersecurity": (
        "00a section 2 lists this as an open scope question: no table is drafted for it, "
        "and for a modern target it is the most defensible addition"
    ),
    "Benefits and Pensions": "00a section 2 lists this as an open scope question; no table is drafted",
    "Compliance": "00a section 2 lists this as an open scope question; no table is drafted",
    "Related-Party": "no table in this corpus covers related-party material",
    "Deal Documents": "00a section 2: LOIs, draft SPAs and structure charts are read directly",
    "Unable to determine": "the classifier could not place the document",
}

#: 00a section 12. Pairs that must be built together because the first returns
#: `Incorporated terms` that only the second resolves.
PAIRED_TABLES: tuple[tuple[str, str], ...] = (("03", "04"), ("08", "09"), ("18", "19"))

#: 00a section 12, in order. Stop when the matter is covered.
BUILD_ORDER: tuple[str, ...] = (
    "05",
    "06",
    "01",
    "02",
    "03",
    "04",
    "10",
    "11",
    "12",
    "16",
    "17",
    "13",
    "14",
    "08",
    "09",
    "07",
    "15",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
)

#: Files in the corpus that are front matter or specification, not table inventories.
NON_TABLE_PREFIXES: frozenset[str] = frozenset({"00a", "00b", "06"})
