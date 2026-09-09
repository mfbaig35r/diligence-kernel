"""What happens when the pipeline meets a document instead of a text file.

Every hazard below was observed on a real PDF extraction, not imagined. The Verbatim check
is the reason they matter: 00a says the whole spot-check design rests on it, so a correct
quotation rejected because an extractor inserted a hyphen is worse than no check at all.
"""

from __future__ import annotations

import pytest

from diligence_kernel.engine.validate import validate_verbatim
from diligence_kernel.vault.cleaning import strip_running_lines
from diligence_kernel.vault.ingest import ingest_path, page_boundaries_from_text

from .fixtures.build_fixtures import ASSIGNMENT_CLAUSE

LEASE = "cedar-point-lease.pdf"
AMENDMENT = "cedar-point-lease-amendment-1.docx"
SCAN = "cedar-point-exhibit-a-scan.pdf"


@pytest.fixture
def vault(loaded, dataroom):
    ingest_path(loaded, dataroom)
    return loaded


def _full_text(conn, filename: str) -> str:
    row = conn.execute("SELECT full_text FROM document WHERE filename = ?", (filename,)).fetchone()
    assert row is not None, filename
    return row["full_text"] or ""


# --- extraction ---------------------------------------------------------------------------


def test_pdf_docx_and_text_all_extract(vault):
    rows = {
        r["filename"]: r
        for r in vault.execute("SELECT filename, extract_status, page_count FROM document")
    }
    assert rows[LEASE]["extract_status"] == "extracted"
    assert rows[LEASE]["page_count"] == 2
    assert rows[AMENDMENT]["extract_status"] == "extracted"
    assert "First Amendment" in _full_text(vault, AMENDMENT)


def test_a_scan_reports_itself_rather_than_vanishing(loaded, dataroom):
    _, findings = ingest_path(loaded, dataroom)
    scan = [f for f in findings if f.subject_name == SCAN]
    assert len(scan) == 1
    assert scan[0].code == "DOCUMENT_EMPTY"
    assert "OCR" in scan[0].observation
    # It is still in the vault, so it can be counted as produced but unreadable.
    assert _full_text(loaded, SCAN) == ""


def test_chunk_offsets_round_trip_through_pdf_extraction(vault):
    rows = vault.execute(
        """SELECT c.text, c.char_start, c.char_end, d.full_text
           FROM chunk c JOIN document d ON d.id = c.document_id
           WHERE d.filename = ?""",
        (LEASE,),
    ).fetchall()
    assert rows
    for row in rows:
        assert row["full_text"][row["char_start"] : row["char_end"]].strip() == row["text"].strip()


def test_pages_are_attributed_to_chunks(vault):
    rows = vault.execute(
        """SELECT c.page_start, c.page_end FROM chunk c JOIN document d ON d.id = c.document_id
           WHERE d.filename = ? ORDER BY c.chunk_index""",
        (LEASE,),
    ).fetchall()
    pages = [(r["page_start"], r["page_end"]) for r in rows]
    assert all(p[0] is not None for p in pages)
    assert pages == sorted(pages), "page attribution follows document order"
    assert max(p[1] for p in pages) == 2


# --- running headers and footers ------------------------------------------------------------


def test_running_headers_and_footers_are_removed(vault):
    text = _full_text(vault, LEASE)
    assert "CEDAR POINT COMMERCE CENTER" not in text, "running header removed"
    assert "Confidential Page" not in text, "running footer removed, despite the page number"
    assert "COMMERCIAL LEASE AGREEMENT" in text, "the document's own title is kept"


def test_a_sentence_spanning_a_page_break_is_left_whole(vault):
    """The failure this fixes: boilerplate wedged into the middle of a clause."""
    text = _full_text(vault, LEASE)
    assert (
        validate_verbatim(
            "any consent required under Section 4 or Section 5 must be obtained separately", [text]
        )
        == []
    )


def test_a_single_page_document_is_left_alone():
    result = strip_running_lines(["Only page.\nNothing repeats here."])
    assert result.lines_removed == 0
    assert result.full_text == "Only page.\nNothing repeats here."


def test_page_numbers_do_not_defeat_the_match():
    pages = [
        "ACME CORP\nbody one\nPage 1 of 3",
        "ACME CORP\nbody two\nPage 2 of 3",
        "ACME CORP\nbody three\nPage 3 of 3",
    ]
    result = strip_running_lines(pages)
    assert result.lines_removed == 6
    assert result.full_text == "body one\n\nbody two\n\nbody three"


def test_a_line_that_does_not_repeat_enough_is_kept():
    pages = ["HEADER\nalpha", "HEADER\nbeta", "different\ngamma", "other\ndelta", "more\nepsilon"]
    result = strip_running_lines(pages)
    assert "HEADER" in result.full_text, "two pages in five is below the threshold"


def test_offsets_are_exact_after_cleaning():
    pages = ["HEADER\nalpha text", "HEADER\nbeta text"]
    result = strip_running_lines(pages)
    bounds = page_boundaries_from_text(result.pages)
    for number, start, end in bounds:
        assert result.full_text[start:end] == result.pages[number - 1]


# --- the verbatim comparison form --------------------------------------------------------------


@pytest.mark.parametrize(
    "name,quote,source",
    [
        (
            "line wrap",
            "voluntarily, involuntarily or by operation of law",
            "voluntarily,\ninvoluntarily or by operation of law",
        ),
        (
            "ligatures",
            "the office shall be notified of any final filing",
            "the oﬃce shall be notiﬁed of any ﬁnal ﬁling",
        ),
        ("soft hyphen", "non-exclusive right", "non­exclusive right"),
        ("hyphenated line break", "non-exclusive right", "non-\nexclusive right"),
        ("non-breaking space", "fifty percent (50%)", "fifty percent (50%)"),
        ("smart quotes", 'the "Premises" herein', "the “Premises” herein"),
        (
            "em dashes",
            "obligations - including payment - survive",
            "obligations — including payment — survive",
        ),
    ],
)
def test_extraction_artefacts_do_not_reject_a_correct_quotation(name, quote, source):
    assert validate_verbatim(quote, [source]) == [], name


def test_the_real_clause_from_the_real_pdf_validates(vault):
    """End to end: the clause as authored, against the clause as extracted."""
    assert validate_verbatim(ASSIGNMENT_CLAUSE, [_full_text(vault, LEASE)]) == []


@pytest.mark.parametrize(
    "wrong",
    [
        "Tenant may not transfer the lease without permission",
        "Tenant shall pay base rent of $99,999.00 per month",
        "Landlord shall not unreasonably withhold consent to any assignment whatsoever",
    ],
)
def test_paraphrase_is_still_rejected(vault, wrong):
    """The loosening must not cost the check its purpose."""
    violations = validate_verbatim(wrong, [_full_text(vault, LEASE)])
    assert [v.code for v in violations] == ["VERBATIM_NOT_IN_SOURCE"]


def test_a_textless_unit_is_reported_not_answered_from_nothing(vault):
    """A scan must not become a row of confident cells drawn from an empty page."""
    from diligence_kernel.engine.runner import RunScope, create_run, execute_run
    from diligence_kernel.vault.units import assemble_units

    from .stub import StubFiller

    assemble_units(vault, "05")
    scan_unit = vault.execute(
        """SELECT u.id FROM review_unit u JOIN unit_document ud ON ud.unit_id = u.id
           JOIN document d ON d.id = ud.document_id WHERE d.filename = ?""",
        (SCAN,),
    ).fetchone()
    assert scan_unit is not None, "the scan is still a row; it was produced"

    filler = StubFiller()
    run_id = create_run(vault, "05", RunScope(unit_ids=[int(scan_unit["id"])]), model="stub")
    summary, findings = execute_run(vault, run_id, filler=filler)

    assert filler.calls == [], "the model was never asked to read an empty page"
    assert summary["cells_done"] == 0
    assert [f.code for f in findings] == ["UNIT_HAS_NO_TEXT"]
    cells = vault.execute("SELECT COUNT(*) AS n FROM cell").fetchone()["n"]
    assert cells == 0
