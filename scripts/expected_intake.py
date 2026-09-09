"""Ground truth for the fixture data room, for scoring a Table 05 run.

The values here are Table 05's **own configured options**, verbatim. An earlier version used
paraphrases invented for the routing map — which scored the models wrong and hid a real bug,
because a document classified `Debt and Financing` matched no routing entry and vanished.

These are the fixtures' authored facts, not legal judgments. Where a document genuinely
admits more than one answer, every acceptable answer is listed — a classifier that returns
any of them is right, and one that returns a single confident answer to an ambiguous
question is wrong in a way that matters more than a miss.

**On changing an expectation.** Widening one to match what a model returned is how an eval
becomes worthless. Every correction here cites the fixture's own text as the reason, and says
so inline, so a later reader can check the justification rather than trust it.
"""

from __future__ import annotations

#: filename -> column -> acceptable values. `None` means "a fallback state is correct here".
EXPECTED: dict[str, dict[str, set[str | None]]] = {
    "msa-base.txt": {
        "Workstream": {"Commercial Contracts", "Vendor and Supplier"},
        "Document Role": {"Instrument"},
        "Document Type": {"Master Services Agreement", "Master services agreement"},
        "Document Date": {"2022-03-14"},
        "Operative Date": {"2022-03-14"},
        "Counterparty": {"Northwind Logistics Inc."},
        "Counterparty Type": {"Vendor or supplier", "Customer", "Other"},
        # The column instructs reporting the name exactly as printed, appending
        # " (variant of [listed name])" where it differs from the entity list. The scan
        # prints it in capitals, so the variant form is the instructed answer.
        "Subject Entity": {"Acme Manufacturing LLC", "NAMES_ACME"},
        "Execution Status": {"Executed", "All documents executed", "Fully executed", "Signed"},
        "Signature Evidence": {"Conformed signature", "Handwritten signature", "Wet or conformed"},
        "Language": {"English"},
        "Governing Law": {"New York"},
        "Completeness": {"Complete on its face"},
        "Compilation Flag": {"Single document"},
        # `Standalone` and `None marked` are positive findings, not fallbacks: 00a section 5
        # says a search run that found nothing is an answer, not an absence.
        "Amends or Issued Under": {None, "Standalone"},
        "Confidentiality Markings": {None, "None marked"},
        "Routing Disposition": {"Route to workstream table"},
    },
    "msa-amendment-1.txt": {
        "Workstream": {"Commercial Contracts", "Vendor and Supplier"},
        "Document Role": {"Instrument"},
        "Document Date": {"2024-01-09"},
        "Counterparty": {"Northwind Logistics Inc."},
        # The column instructs reporting the name exactly as printed, appending
        # " (variant of [listed name])" where it differs from the entity list. The scan
        # prints it in capitals, so the variant form is the instructed answer.
        "Subject Entity": {"Acme Manufacturing LLC", "NAMES_ACME"},
        "Language": {"English"},
        "Compilation Flag": {"Single document"},
        # The whole of Table 01's family assembly depends on this being right.
        "Amends or Issued Under": {"NAMES_THE_MSA"},
        # A recital references a Side Letter dated 2 June 2023 that is not in the data room.
        "Referenced but Not Produced": {"NAMES_THE_SIDE_LETTER"},
        "Routing Disposition": {"Route to workstream table"},
    },
    "supply-agreement.txt": {
        # A supply agreement is both; 00a routes Vendor and Supplier through Contracts Core.
        "Workstream": {"Commercial Contracts", "Vendor and Supplier"},
        "Document Role": {"Instrument"},
        "Document Date": {"2023-08-01"},
        "Counterparty": {"Cedar Components GmbH"},
        "Counterparty Type": {"Vendor or supplier", "Customer"},
        # The column instructs reporting the name exactly as printed, appending
        # " (variant of [listed name])" where it differs from the entity list. The scan
        # prints it in capitals, so the variant form is the instructed answer.
        "Subject Entity": {"Acme Manufacturing LLC", "NAMES_ACME"},
        # The fixture ends "This Agreement has not been signed by either party."
        "Execution Status": {"Unsigned", "Base unsigned", "Not executed", "Not signed"},
        # The fixture has no signature blocks at all — only the sentence that it is
        # unsigned — so "nothing to evaluate" is a defensible reading.
        "Signature Evidence": {"No signature", "None present", "Unsigned", "Not applicable"},
        "Language": {"English"},
        "Governing Law": {"Delaware"},
        "Compilation Flag": {"Single document"},
        "Amends or Issued Under": {None, "Standalone"},
        "Routing Disposition": {"Route to workstream table"},
    },
    "cedar-point-lease.pdf": {
        "Workstream": {"Real Estate"},
        "Document Role": {"Instrument"},
        "Document Type": {"Lease", "Commercial Lease Agreement", "Commercial lease"},
        "Document Date": {"2021-05-14"},
        "Counterparty": {"Halstead Property Holdings LLC"},
        # The column instructs reporting the name exactly as printed, appending
        # " (variant of [listed name])" where it differs from the entity list. The scan
        # prints it in capitals, so the variant form is the instructed answer.
        "Subject Entity": {"Acme Manufacturing LLC", "NAMES_ACME"},
        "Execution Status": {"Executed", "All documents executed", "Fully executed", "Signed"},
        "Language": {"English"},
        "Governing Law": {"Delaware"},
        "Completeness": {"Complete on its face"},
        "Compilation Flag": {"Single document"},
        "Amends or Issued Under": {None, "Standalone"},
        "Routing Disposition": {"Route to workstream table"},
    },
    "cedar-point-lease-amendment-1.docx": {
        "Workstream": {"Real Estate"},
        "Document Role": {"Instrument"},
        "Document Date": {"2024-03-02"},
        "Counterparty": {"Halstead Property Holdings LLC"},
        # The column instructs reporting the name exactly as printed, appending
        # " (variant of [listed name])" where it differs from the entity list. The scan
        # prints it in capitals, so the variant form is the instructed answer.
        "Subject Entity": {"Acme Manufacturing LLC", "NAMES_ACME"},
        "Language": {"English"},
        "Compilation Flag": {"Single document"},
        "Amends or Issued Under": {"NAMES_THE_LEASE"},
        "Routing Disposition": {"Route to workstream table"},
    },
    "cedar-point-exhibit-a-scan.pdf": {
        # Read only through OCR. Anything correct here is a win.
        "Workstream": {"Real Estate"},
        # Corrected after the first run, on the document's own text rather than on what the
        # model answered: the fixture ends "RECORDED: New Castle County Recorder of Deeds /
        # Instrument No. 2021-0041882". A recorded memorandum is a filing, so `Filing` was
        # right and this expectation was too narrow.
        "Document Role": {"Record", "Instrument", "Filing"},
        "Document Date": {"2021-05-14"},
        "Counterparty": {"Halstead Property Holdings LLC"},
        # The column instructs reporting the name exactly as printed, appending
        # " (variant of [listed name])" where it differs from the entity list. The scan
        # prints it in capitals, so the variant form is the instructed answer.
        "Subject Entity": {"Acme Manufacturing LLC", "NAMES_ACME"},
        "Language": {"English"},
        "Compilation Flag": {"Single document"},
    },
    "cedar-point-consent-thread.eml": {
        # Correspondence, not the agreement it carries.
        "Workstream": {"Real Estate", "Deal Documents"},
        "Document Role": {"Correspondence"},
        "Document Date": {"2026-02-19"},
        "Language": {"English"},
        # The subject line reads "PRIVILEGED AND CONFIDENTIAL".
        "Confidentiality Markings": {"NAMES_PRIVILEGE"},
        # It transmits the executed amendment and references the landlord's consent letter.
        "Referenced but Not Produced": {"NAMES_A_MISSING_DOCUMENT"},
    },
    "cap-table-and-census.xlsx": {
        # Two workstreams in one file. `Unable to determine` is the honest answer, and the
        # Compilation Flag is where the real signal belongs.
        "Workstream": {
            "Corporate and Entity Structure",
            "Capitalization and Securities",
            "Employment and HR",
            None,
        },
        "Document Role": {"Record"},
        "Compilation Flag": {"COMPILATION"},
        # 00a: an as-of date is what makes a Record usable.
        "Operative Date": {"2026-06-30"},
        # The column instructs reporting the name exactly as printed, appending
        # " (variant of [listed name])" where it differs from the entity list. The scan
        # prints it in capitals, so the variant form is the instructed answer.
        "Subject Entity": {"Acme Manufacturing LLC", "NAMES_ACME"},
        "Language": {"English"},
        "Execution Status": {None},
        "Routing Disposition": {"Split before review", "Human triage required"},
    },
    "ucc-lien-schedule.csv": {
        "Workstream": {"Debt and Financing"},
        "Document Role": {"Record"},
        # The column instructs reporting the name exactly as printed, appending
        # " (variant of [listed name])" where it differs from the entity list. The scan
        # prints it in capitals, so the variant form is the instructed answer.
        "Subject Entity": {"Acme Manufacturing LLC", "NAMES_ACME"},
        "Language": {"English"},
        "Execution Status": {None},
        "Compilation Flag": {"COMPILATION", "Single document"},
    },
}

#: Columns where a wrong answer breaks something downstream, rather than merely being wrong.
LOAD_BEARING = ("Workstream", "Amends or Issued Under", "Compilation Flag", "Routing Disposition")
