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
    """With OCR off, an unreadable file says so instead of disappearing."""
    _, findings = ingest_path(loaded, dataroom)
    codes = [f.code for f in findings if f.subject_name == SCAN]
    assert codes == ["OCR_UNAVAILABLE", "DOCUMENT_EMPTY"]
    # It is still in the vault, so it can be counted as produced but unreadable.
    assert _full_text(loaded, SCAN) == ""
    row = loaded.execute("SELECT text_source FROM document WHERE filename = ?", (SCAN,)).fetchone()
    assert row["text_source"] == "extracted"


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


# --- OCR ------------------------------------------------------------------------------------


def test_ocr_reads_a_scan_that_has_no_text_layer(loaded, dataroom, ocr_on):
    """The fixture is an image of text: nothing extracts, so OCR has to do the reading."""
    from .fixtures.build_fixtures import SCAN_TEXT

    counts, findings = ingest_path(loaded, dataroom)
    assert counts["ocred"] == 1

    text = _full_text(loaded, SCAN)
    assert "MEMORANDUM OF LEASE" in text
    assert "HALSTEAD PROPERTY HOLDINGS LLC" in text
    # Most of the authored lines come back; OCR is not required to be perfect.
    recovered = sum(1 for line in SCAN_TEXT if line.strip() and line in text)
    assert recovered >= len([x for x in SCAN_TEXT if x.strip()]) * 0.7

    codes = {f.code for f in findings if f.subject_name == SCAN}
    assert "DOCUMENT_OCRED" in codes
    assert "DOCUMENT_EMPTY" not in codes


def test_an_ocred_document_records_that_its_text_is_a_transcription(loaded, dataroom, ocr_on):
    ingest_path(loaded, dataroom)
    row = loaded.execute(
        "SELECT text_source, ocr_engine, ocr_confidence FROM document WHERE filename = ?",
        (SCAN,),
    ).fetchone()
    assert row["text_source"] == "ocr"
    assert row["ocr_engine"] == "tesseract"
    assert 0.0 < row["ocr_confidence"] <= 1.0

    # Documents with a text layer are untouched by any of this.
    lease = loaded.execute(
        "SELECT text_source, ocr_engine FROM document WHERE filename = ?", (LEASE,)
    ).fetchone()
    assert lease["text_source"] == "extracted"
    assert lease["ocr_engine"] is None


def test_ocred_text_is_chunked_and_searchable(loaded, dataroom, ocr_on):
    ingest_path(loaded, dataroom)
    rows = loaded.execute(
        """SELECT c.text, c.char_start, c.char_end, d.full_text
           FROM chunk c JOIN document d ON d.id = c.document_id WHERE d.filename = ?""",
        (SCAN,),
    ).fetchall()
    assert rows, "the transcription is chunked like any other text"
    for row in rows:
        assert row["full_text"][row["char_start"] : row["char_end"]].strip() == row["text"].strip()


def test_a_verbatim_cell_says_it_was_checked_against_a_transcription():
    """The circularity that matters: OCR text is a reading, so a match proves less."""
    from diligence_kernel.engine.validate import validate_provenance

    assert validate_provenance("Verbatim", unit_has_ocr=False) == []
    assert validate_provenance("Free Response", unit_has_ocr=True) == []

    violations = validate_provenance("Verbatim", unit_has_ocr=True)
    assert [v.code for v in violations] == ["VERBATIM_FROM_OCR"]
    assert "not the document" in violations[0].detail


def test_the_model_is_told_which_documents_are_transcriptions(loaded, dataroom, ocr_on):
    from diligence_kernel.engine.llm import TRANSCRIPTION_CAVEAT

    from .stub import StubFiller

    ingest_path(loaded, dataroom)
    filler = StubFiller()
    blocks = [
        {
            "filename": SCAN,
            "role": None,
            "text": "EXHIBIT A",
            "text_source": "ocr",
            "ocr_engine": "tesseract",
            "ocr_confidence": 0.95,
        },
    ]
    prefix = filler.build_system(table_instructions="", unit_label="u", evidence_blocks=blocks)
    assert 'source="ocr (tesseract, 95% confidence)"' in prefix.text
    assert TRANSCRIPTION_CAVEAT.strip() in prefix.text

    # A unit of ordinary documents carries no caveat and no source attribute.
    clean = filler.build_system(
        table_instructions="",
        unit_label="u",
        evidence_blocks=[
            {"filename": LEASE, "role": "Base", "text": "x", "text_source": "extracted"}
        ],
    )
    assert "source=" not in clean.text
    assert TRANSCRIPTION_CAVEAT.strip() not in clean.text


def test_ocr_can_be_turned_off(loaded, dataroom, monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_OCR", "off")
    counts, findings = ingest_path(loaded, dataroom)
    assert counts["ocred"] == 0
    unavailable = [f for f in findings if f.code == "OCR_UNAVAILABLE"]
    assert unavailable and "off" in unavailable[0].observation
