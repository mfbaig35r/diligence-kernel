from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from diligence_kernel import db
from diligence_kernel.corpus.loader import load_corpus

CORPUS = Path(__file__).resolve().parents[1] / "review-table-prompts"
DATAROOM = Path(__file__).parent / "fixtures" / "dataroom"


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
