from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from diligence_kernel import db
from diligence_kernel.corpus.loader import load_corpus

CORPUS = Path(__file__).resolve().parents[1] / "review-table-prompts"
DATAROOM = Path(__file__).parent / "fixtures" / "dataroom"

#: The fixture data room, named once so a count is never hardcoded in a test.
DOCUMENTS = (
    "msa-base.txt",
    "msa-amendment-1.txt",
    "supply-agreement.txt",
    "cedar-point-lease.pdf",
    "cedar-point-lease-amendment-1.docx",
    "cedar-point-exhibit-a-scan.pdf",
    "cap-table-and-census.xlsx",
    "ucc-lien-schedule.csv",
)
#: The one with no text layer. It ingests, but no cell can be filled from it.
UNREADABLE = "cedar-point-exhibit-a-scan.pdf"
READABLE = tuple(d for d in DOCUMENTS if d != UNREADABLE)


@pytest.fixture(autouse=True)
def _ocr_off(monkeypatch):
    """OCR is slow and is exercised deliberately, not incidentally on every ingest.

    Tests that need it opt in with the `ocr_on` fixture.
    """
    monkeypatch.setenv("DILIGENCE_KERNEL_OCR", "off")


@pytest.fixture
def ocr_on(monkeypatch):
    monkeypatch.setenv("DILIGENCE_KERNEL_OCR", "tesseract")


@pytest.fixture
def conn(tmp_path) -> sqlite3.Connection:
    return db.connect(tmp_path / "matter.db")


@pytest.fixture
def loaded(conn) -> sqlite3.Connection:
    load_corpus(conn, CORPUS)
    return conn


@pytest.fixture
def corpus_root() -> Path:
    return CORPUS


@pytest.fixture
def dataroom() -> Path:
    return DATAROOM
