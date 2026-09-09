"""Spreadsheets and delimited files.

00a classifies these as Records — cap tables, stock ledgers, employee censuses, loss runs —
and an as-of date is what makes one usable. They are input documents, so they have to survive
ingestion as tables rather than as prose.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from diligence_kernel.vault import tabular
from diligence_kernel.vault.ingest import KNOWN_UNREADABLE, SUPPORTED, ingest_path
from diligence_kernel.vault.search import search_unit

from .fixtures.build_fixtures import CAP_TABLE_AS_OF, CAP_TABLE_ROWS, CENSUS_ROWS

WORKBOOK = "cap-table-and-census.xlsx"
SCHEDULE = "ucc-lien-schedule.csv"


@pytest.fixture
def vault(loaded, dataroom):
    ingest_path(loaded, dataroom)
    return loaded


def _text(conn, filename: str) -> str:
    return conn.execute(
        "SELECT full_text FROM document WHERE filename = ?", (filename,)
    ).fetchone()["full_text"]


def _chunks(conn, filename: str) -> list[str]:
    return [
        r["text"]
        for r in conn.execute(
            """SELECT c.text FROM chunk c JOIN document d ON d.id = c.document_id
               WHERE d.filename = ? ORDER BY c.chunk_index""",
            (filename,),
        )
    ]


# --- reading -------------------------------------------------------------------------------


def test_every_sheet_of_a_workbook_is_read(vault):
    text = _text(vault, WORKBOOK)
    assert "# Sheet: Cap Table" in text
    assert "# Sheet: Employee Census" in text
    for holder, *_ in CAP_TABLE_ROWS:
        assert holder in text


def test_the_as_of_date_survives_as_preamble(vault):
    """00a: an as-of date is what makes a Record usable."""
    assert CAP_TABLE_AS_OF in _text(vault, WORKBOOK)


def test_a_csv_schedule_is_read_as_a_table(vault):
    text = _text(vault, SCHEDULE)
    assert "# Sheet: ucc-lien-schedule" in text
    assert "Secured Party" in text
    assert "Halstead Equipment Finance LLC" in text


def test_header_detection_skips_title_and_as_of_rows():
    sheets = tabular.read_sheets(Path(__file__).parent / "fixtures" / "dataroom" / WORKBOOK)
    cap = next(s for s in sheets if s.name == "Cap Table")
    assert cap.header[0] == "Holder"
    assert cap.row_count == len(CAP_TABLE_ROWS), "the title and as-of rows are not data"
    assert any(CAP_TABLE_AS_OF in line for line in cap.preamble)

    census = next(s for s in sheets if s.name == "Employee Census")
    assert census.header[0] == "Employee ID"
    assert census.row_count == CENSUS_ROWS


# --- the failure this exists to prevent -------------------------------------------------------


def test_every_chunk_carries_its_sheet_name_and_header(vault):
    """A chunk of unlabelled numbers is the failure: salary and bonus become indistinguishable."""
    for chunk in _chunks(vault, WORKBOOK):
        assert chunk.startswith("# Sheet: ")
        header = "Employee ID" if "Employee Census" in chunk else "Holder"
        assert header in chunk, "a continuation chunk restates its columns"


def test_a_continuation_chunk_is_marked_as_one(vault):
    chunks = _chunks(vault, WORKBOOK)
    continued = [c for c in chunks if "(continued)" in c.splitlines()[0]]
    assert continued, "the census is long enough to span chunks"
    assert "Base Salary" in continued[0]


def test_sheets_do_not_run_together(vault):
    chunks = _chunks(vault, WORKBOOK)
    mixed = [c for c in chunks if "Cap Table" in c and "Employee Census" in c]
    assert mixed == [], "a chunk belongs to one sheet"


def test_tabular_offsets_are_exact(vault):
    rows = vault.execute(
        """SELECT c.text, c.char_start, c.char_end, d.full_text
           FROM chunk c JOIN document d ON d.id = c.document_id
           WHERE d.filename IN (?, ?)""",
        (WORKBOOK, SCHEDULE),
    ).fetchall()
    assert rows
    for row in rows:
        assert row["full_text"][row["char_start"] : row["char_end"]] == row["text"]


def test_a_row_late_in_the_census_is_retrievable_with_its_columns(vault):
    """Retrieval has to return a row a reader can interpret."""
    unit = vault.execute("SELECT id FROM document WHERE filename = ?", (WORKBOOK,)).fetchone()
    vault.execute(
        "INSERT INTO review_unit (table_id, position, label, unit_key, created_at) "
        "VALUES ((SELECT id FROM review_table WHERE number='05'), 1, 'wb', 'wb', '2026-01-01')"
    )
    unit_id = vault.execute("SELECT id FROM review_unit WHERE unit_key='wb'").fetchone()["id"]
    vault.execute(
        "INSERT INTO unit_document (unit_id, document_id) VALUES (?, ?)",
        (unit_id, int(unit["id"])),
    )
    vault.commit()

    passages = search_unit(vault, unit_id, "Employee 38 base salary visa status", limit=3)
    assert passages
    hit = next((p for p in passages if "Employee 38" in p.text), None)
    assert hit is not None
    assert "Base Salary" in hit.text, "the retrieved passage names its own columns"


# --- format coverage ---------------------------------------------------------------------------


@pytest.mark.parametrize("suffix", [".xlsx", ".xlsm", ".csv", ".tsv"])
def test_tabular_formats_are_supported(suffix):
    assert suffix in SUPPORTED
    assert tabular.is_tabular(suffix)


@pytest.mark.parametrize("suffix", [".pdf", ".docx", ".txt", ".md", ".html", ".htm"])
def test_prose_formats_are_supported(suffix):
    assert suffix in SUPPORTED


def test_a_format_we_cannot_read_is_reported_not_skipped_silently(loaded, tmp_path):
    """An unread file must not look like an absent one; the coverage register depends on it."""
    room = tmp_path / "room"
    room.mkdir()
    (room / "board-deck.pptx").write_bytes(b"stub")
    (room / "board-minutes.rtf").write_bytes(b"stub")
    (room / "old-schedule.xls").write_bytes(b"stub")
    counts, findings = ingest_path(loaded, room)

    assert counts["unsupported"] == 3
    reported = {f.subject_name for f in findings if f.code == "DOCUMENT_FORMAT_UNREADABLE"}
    assert reported == {"board-deck.pptx", "board-minutes.rtf", "old-schedule.xls"}
    assert all(
        ".xlsx" in f.observation or "not supported" in f.observation
        for f in findings
        if f.subject_name == "old-schedule.xls"
    )


def test_known_unreadable_formats_are_not_also_claimed_as_supported():
    assert not (set(KNOWN_UNREADABLE) & SUPPORTED)


def test_a_headerless_sheet_is_reported(loaded, tmp_path):
    room = tmp_path / "room"
    room.mkdir()
    (room / "raw.csv").write_text("1\n2\n3\n")
    _, findings = ingest_path(loaded, room)
    codes = {f.code for f in findings}
    assert "SHEET_WITHOUT_HEADER" in codes or "DOCUMENT_EMPTY" in codes


def test_an_empty_workbook_reports_itself(loaded, tmp_path):
    from openpyxl import Workbook

    room = tmp_path / "room"
    room.mkdir()
    wb = Workbook()
    wb.save(str(room / "blank.xlsx"))
    _, findings = ingest_path(loaded, room)
    codes = {f.code for f in findings}
    assert "DOCUMENT_EMPTY" in codes
    assert "SHEET_EMPTY" in codes
