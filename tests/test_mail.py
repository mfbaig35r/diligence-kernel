"""Email, read as correspondence.

Tables 17, 23 and 25 are built around it, and their review unit is a matter of several
communications. So one message is one document, and what matters is that the headers, the
boundary with the quoted history, the attachments, and any privilege marking all survive.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from diligence_kernel.vault import mail
from diligence_kernel.vault.ingest import SUPPORTED, ingest_path

from .fixtures.build_fixtures import EMAIL_SUBJECT

EMAIL = "cedar-point-consent-thread.eml"
ATTACHED = "cedar-point-lease-amendment-1.docx"


@pytest.fixture
def vault(loaded, dataroom):
    ingest_path(loaded, dataroom)
    return loaded


def _doc(conn, filename: str):
    return conn.execute(
        """SELECT id, full_text, privilege_markings, parent_document_id
           FROM document WHERE filename = ? ORDER BY parent_document_id LIMIT 1""",
        (filename,),
    ).fetchone()


# --- reading ----------------------------------------------------------------------------


def test_eml_and_msg_are_supported():
    assert ".eml" in SUPPORTED and ".msg" in SUPPORTED
    assert mail.is_mail(".eml") and mail.is_mail(".msg")
    assert not mail.is_mail(".pdf")


def test_headers_are_normalized_into_the_text(vault):
    """Table 05 routes on these: the counterparty, the date, the subject."""
    text = _doc(vault, EMAIL)["full_text"]
    assert text.startswith("# Email")
    assert "From: Morgan Feld <m.feld@acmemfg.example>" in text
    assert "Cc: Priya Raman <p.raman@halsteadproperty.example>" in text
    assert "Date: Thu, 19 Feb 2026 16:42:11 +0000" in text
    assert f"Subject: {EMAIL_SUBJECT}" in text
    assert f"Attachments: {ATTACHED}" in text


def test_the_body_survives(vault):
    text = _doc(vault, EMAIL)["full_text"]
    assert "Attached is the executed First Amendment" in text
    assert "Please confirm whether you consider the notice requirement satisfied" in text


# --- the quoted chain ---------------------------------------------------------------------


def test_new_text_is_separated_from_quoted_history(vault):
    text = _doc(vault, EMAIL)["full_text"]
    marker = "--- quoted history"
    assert marker in text
    new, history = text.split(marker, 1)
    assert "Please confirm whether you consider" in new, "what this message says"
    assert "-----Original Message-----" in history, "what it repeats"
    assert "We are content to proceed" in history


def test_quoted_history_is_kept_not_discarded(vault):
    """It is still evidence; it is labelled so retrieval and dating are not confused."""
    assert "We are content to proceed on the basis discussed" in _doc(vault, EMAIL)["full_text"]


@pytest.mark.parametrize(
    "body,expected_new",
    [
        ("New text only.", "New text only."),
        ("New text.\n\n-----Original Message-----\nold", "New text."),
        ("New text.\n\nOn 12 February 2026, Priya Raman wrote:\nold", "New text."),
        ("New text.\n\n> quoted line\n> another", "New text."),
        ("New text.\n\nFrom: someone\nSent: yesterday\nold", "New text."),
    ],
)
def test_quote_markers_are_recognised(body, expected_new):
    new, _ = mail.split_quoted(body)
    assert new == expected_new


def test_a_message_with_no_quoted_chain_has_no_history():
    new, quoted = mail.split_quoted("Just a note.")
    assert new == "Just a note." and quoted == ""


# --- privilege -------------------------------------------------------------------------------


def test_a_privilege_marking_is_reported(loaded, dataroom):
    """00a: report the marking and stop. Never assess whether privilege applies."""
    _, findings = ingest_path(loaded, dataroom)
    marked = [f for f in findings if f.code == "PRIVILEGE_MARKING"]
    assert [f.subject_name for f in marked] == [EMAIL]
    assert "privileged and confidential" in marked[0].evidence["markings"]
    assert "not assessed" in marked[0].observation


def test_the_marking_is_stored_on_the_document(vault):
    import json

    stored = json.loads(_doc(vault, EMAIL)["privilege_markings"])
    assert "privileged and confidential" in stored


@pytest.mark.parametrize(
    "text,found",
    [
        ("PRIVILEGED AND CONFIDENTIAL", True),
        ("Attorney Work Product", True),
        ("Subject to legal professional privilege", True),
        ("This is an ordinary commercial letter.", False),
    ],
)
def test_privilege_detection(text, found):
    assert bool(mail.privilege_markings_in(text)) is found


# --- attachments ------------------------------------------------------------------------------


def test_an_attachment_is_ingested_as_a_document_in_its_own_right(loaded, dataroom):
    """In a data room the attachment is usually the agreement."""
    counts, findings = ingest_path(loaded, dataroom)
    assert counts["attachments"] == 1

    carried = loaded.execute(
        """SELECT d.filename, p.filename AS carrier FROM document d
           JOIN document p ON p.id = d.parent_document_id"""
    ).fetchall()
    assert [(r["filename"], r["carrier"]) for r in carried] == [(ATTACHED, EMAIL)]
    assert any(f.code == "ATTACHMENT_INGESTED" for f in findings)


def test_an_attachment_is_extracted_and_chunked_like_any_document(loaded, dataroom):
    ingest_path(loaded, dataroom)
    row = loaded.execute(
        """SELECT d.id, d.full_text FROM document d
           WHERE d.parent_document_id IS NOT NULL"""
    ).fetchone()
    assert "First Amendment" in row["full_text"]
    chunks = loaded.execute(
        "SELECT COUNT(*) AS n FROM chunk WHERE document_id = ?", (int(row["id"]),)
    ).fetchone()["n"]
    assert chunks > 0


def test_mail_furniture_is_not_treated_as_a_document(loaded, dataroom):
    """A signature image is not a produced document."""
    ingest_path(loaded, dataroom)
    names = {
        r["filename"]
        for r in loaded.execute(
            "SELECT filename FROM document WHERE parent_document_id IS NOT NULL"
        )
    }
    assert "image001.png" not in names
    assert names == {ATTACHED}


def test_attachments_are_written_beside_the_database_not_the_data_room(tmp_path, dataroom):
    """The data room may be read-only, and the next walk must not find them twice."""
    from diligence_kernel import db

    conn = db.connect(tmp_path / "matter.db")
    ingest_path(conn, dataroom)
    written = sorted(p.name for p in (tmp_path / "attachments").rglob("*") if p.is_file())
    assert written == [ATTACHED]
    assert not (Path(dataroom) / "attachments").exists()


def test_attachment_classifier(tmp_path):
    real = mail.Attachment("agreement.pdf", b"x" * 8000)
    assert real.is_document
    assert not mail.Attachment("image001.png", b"x" * 8000).is_document
    assert not mail.Attachment("smime.p7s", b"x" * 8000).is_document
    assert not mail.Attachment("tiny.pdf", b"x" * 10).is_document


def test_the_same_document_produced_twice_is_kept_twice(vault):
    """Table 05 carries a Duplicate Indicators column; duplication is a fact, not an error."""
    rows = vault.execute(
        "SELECT source_path, parent_document_id FROM document WHERE filename = ?", (ATTACHED,)
    ).fetchall()
    assert len(rows) == 2, "once in the data room, once carried by the email"
    assert {r["parent_document_id"] is None for r in rows} == {True, False}
    assert len({r["source_path"] for r in rows}) == 2


def test_a_duplicate_produced_file_is_still_its_own_row(loaded, dataroom):
    """Two produced copies are two rows. Keying units on content would drop one."""
    from diligence_kernel.vault.units import assemble_units, documents_in_scope

    ingest_path(loaded, dataroom)
    scope = documents_in_scope(loaded, "05")
    counts, _ = assemble_units(loaded, "05")
    assert counts["created"] == len(scope), "one row per produced file, duplicates included"

    rows = loaded.execute(
        """SELECT COUNT(*) AS n FROM review_unit u
           JOIN unit_document ud ON ud.unit_id = u.id
           JOIN document d ON d.id = ud.document_id
           WHERE d.filename = ?""",
        (ATTACHED,),
    ).fetchone()["n"]
    assert rows == 2, "the folder copy and the emailed copy are both visible to intake"


def test_msg_dispatches_to_the_outlook_reader(monkeypatch, tmp_path):
    """`.msg` needs extract-msg and is not exercised on a real file; the route is."""
    called: dict[str, Path] = {}
    monkeypatch.setattr(mail, "read_msg", lambda p: called.setdefault("path", p) or mail.Message())
    mail.read_message(tmp_path / "note.msg")
    assert called["path"].suffix == ".msg"


def test_extract_msg_is_installed():
    import extract_msg  # noqa: F401
