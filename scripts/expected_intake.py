"""Ground truth for the fixture data room, for scoring a Table 05 run.

These are the fixtures' authored facts, not legal judgments. Where a document genuinely
admits more than one answer, every acceptable answer is listed — a classifier that returns
any of them is right, and one that returns a single confident answer to an ambiguous
question is wrong in a way that matters more than a miss.
"""

from __future__ import annotations

#: filename -> column -> acceptable values. `None` means "a fallback state is correct here".
EXPECTED: dict[str, dict[str, set[str | None]]] = {
    "msa-base.txt": {
        "Workstream": {"Contracts"},
        "Document Role": {"Operative instrument"},
        "Document Date": {"2022-03-14"},
        "Counterparty": {"Northwind Logistics Inc."},
        "Execution Status": {"Executed", "All documents executed", "Fully executed"},
        "Amends or Issued Under": {None},
    },
    "msa-amendment-1.txt": {
        "Workstream": {"Contracts"},
        "Document Role": {"Operative instrument"},
        "Document Date": {"2024-01-09"},
        "Counterparty": {"Northwind Logistics Inc."},
        # The whole of Table 01's family assembly depends on this being right.
        "Amends or Issued Under": {"NAMES_THE_MSA"},
    },
    "supply-agreement.txt": {
        "Workstream": {"Contracts"},
        "Document Role": {"Operative instrument"},
        "Document Date": {"2023-08-01"},
        "Counterparty": {"Cedar Components GmbH"},
        "Execution Status": {"Unsigned", "Base unsigned", "Not executed"},
    },
    "cedar-point-lease.pdf": {
        "Workstream": {"Real Estate"},
        "Document Role": {"Operative instrument"},
        "Document Date": {"2021-05-14"},
        "Counterparty": {"Halstead Property Holdings LLC"},
    },
    "cedar-point-lease-amendment-1.docx": {
        "Workstream": {"Real Estate"},
        "Document Date": {"2024-03-02"},
        "Amends or Issued Under": {"NAMES_THE_LEASE"},
    },
    "cedar-point-exhibit-a-scan.pdf": {
        # Read only through OCR. Anything correct here is a win.
        "Workstream": {"Real Estate"},
        "Document Role": {"Record", "Operative instrument"},
        "Document Date": {"2021-05-14"},
    },
    "cedar-point-consent-thread.eml": {
        # Correspondence, not the agreement it carries.
        "Workstream": {"Real Estate", "Deal Documents"},
        "Document Role": {"Correspondence", "Record"},
        "Document Date": {"2026-02-19"},
    },
    "cap-table-and-census.xlsx": {
        # Two workstreams in one file. `Unable to determine` is the honest answer, and the
        # Compilation Flag is where the real signal belongs.
        "Workstream": {"Corporate", "Employment", None},
        "Document Role": {"Record"},
        "Compilation Flag": {"COMPILATION"},
    },
    "ucc-lien-schedule.csv": {
        "Workstream": {"Finance"},
        "Document Role": {"Record"},
    },
}

#: Columns where a wrong answer breaks something downstream, rather than merely being wrong.
LOAD_BEARING = ("Workstream", "Amends or Issued Under", "Compilation Flag")
