"""SQLite connection and versioned schema for one matter.

One matter is one database file. It holds the parsed corpus (derived, rebuildable), the
vault (documents, chunks, embeddings), the review units, and every filled cell with its
evidence. The markdown corpus stays the source of truth; nothing here is authored.

Migrations are append-only. Never edit an applied version.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

ENV_VAR = "DILIGENCE_KERNEL_DB"
DEFAULT_PATH = Path.home() / ".diligence-kernel" / "matter.db"


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds")


def db_path() -> Path:
    raw = os.environ.get(ENV_VAR)
    return Path(raw).expanduser() if raw else DEFAULT_PATH


MIGRATIONS: list[tuple[int, str]] = [
    (
        1,
        """
CREATE TABLE schema_version (
    version    INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

-- ---------------------------------------------------------------- matter
CREATE TABLE matter (
    id          INTEGER PRIMARY KEY CHECK (id = 1),   -- one matter per database file
    name        TEXT NOT NULL,
    side        TEXT CHECK (side IN ('buy','sell') OR side IS NULL),
    as_of_date  TEXT,                                  -- the diligence as-of date
    objective   TEXT,
    corpus_root TEXT,
    created_at  TEXT NOT NULL
);

CREATE TABLE entity (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE COLLATE NOCASE,  -- exact legal name
    jurisdiction TEXT,
    role         TEXT,
    is_subject   INTEGER NOT NULL DEFAULT 1,
    created_at   TEXT NOT NULL
);

-- ------------------------------------------------- corpus (derived from markdown)
CREATE TABLE review_table (
    id                 INTEGER PRIMARY KEY,
    number             TEXT NOT NULL UNIQUE,           -- '01'..'25', the only identifier
    slug               TEXT NOT NULL,
    title              TEXT NOT NULL,
    review_unit        TEXT,
    grouping_enabled   INTEGER NOT NULL DEFAULT 0,
    max_docs_per_unit  INTEGER,
    vault_project      TEXT,
    inventory_version  TEXT,
    table_instructions TEXT,
    dependency_map     TEXT,
    source_path        TEXT NOT NULL,
    source_sha256      TEXT NOT NULL,
    ingested_at        TEXT NOT NULL
);

CREATE TABLE column_def (
    id                 INTEGER PRIMARY KEY,
    table_id           INTEGER NOT NULL REFERENCES review_table(id) ON DELETE CASCADE,
    position           INTEGER NOT NULL,
    name               TEXT NOT NULL COLLATE NOCASE,
    native_type        TEXT NOT NULL,
    type_caveat        TEXT,
    configured_options TEXT,          -- json list, Classify only, in UI order
    purpose            TEXT,
    prompt_text        TEXT NOT NULL,
    prompt_chars       INTEGER NOT NULL,
    prompt_sections    TEXT NOT NULL DEFAULT '[]',
    stage              INTEGER,        -- topological stage; 1 has no upstream
    UNIQUE (table_id, name)
);
CREATE INDEX idx_column_table ON column_def(table_id, position);

CREATE TABLE column_dep (
    id           INTEGER PRIMARY KEY,
    table_id     INTEGER NOT NULL REFERENCES review_table(id) ON DELETE CASCADE,
    upstream_id  INTEGER NOT NULL REFERENCES column_def(id) ON DELETE CASCADE,
    downstream_id INTEGER NOT NULL REFERENCES column_def(id) ON DELETE CASCADE,
    source       TEXT NOT NULL,        -- 'record' | 'at_ref'
    UNIQUE (upstream_id, downstream_id, source)
);

CREATE TABLE test_case (
    id       INTEGER PRIMARY KEY,
    table_id INTEGER NOT NULL REFERENCES review_table(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    text     TEXT NOT NULL
);

-- -------------------------------------------------------------------- vault
CREATE TABLE document (
    id             INTEGER PRIMARY KEY,
    source_path    TEXT NOT NULL UNIQUE,
    filename       TEXT NOT NULL,
    sha256         TEXT NOT NULL,
    bytes          INTEGER,
    page_count     INTEGER,
    full_text      TEXT,
    extract_status TEXT NOT NULL DEFAULT 'pending',  -- pending|extracted|failed
    extract_error  TEXT,
    ingested_at    TEXT NOT NULL,
    UNIQUE (sha256, source_path)
);
CREATE INDEX idx_document_sha ON document(sha256);

CREATE TABLE chunk (
    id            INTEGER PRIMARY KEY,
    document_id   INTEGER NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    chunk_index   INTEGER NOT NULL,
    text          TEXT NOT NULL,
    char_start    INTEGER,             -- offset into document.full_text; span-exact retrieval
    char_end      INTEGER,
    page_start    INTEGER,
    page_end      INTEGER,
    section_heading TEXT,
    token_estimate  INTEGER,
    embedding     BLOB,                -- float32 little-endian
    embedding_dim INTEGER,
    UNIQUE (document_id, chunk_index)
);
CREATE INDEX idx_chunk_document ON chunk(document_id, chunk_index);

CREATE VIRTUAL TABLE chunk_fts USING fts5(
    text, content='chunk', content_rowid='id', tokenize='porter unicode61'
);
CREATE TRIGGER chunk_ai AFTER INSERT ON chunk BEGIN
    INSERT INTO chunk_fts(rowid, text) VALUES (new.id, new.text);
END;
CREATE TRIGGER chunk_ad AFTER DELETE ON chunk BEGIN
    INSERT INTO chunk_fts(chunk_fts, rowid, text) VALUES('delete', old.id, old.text);
END;
CREATE TRIGGER chunk_au AFTER UPDATE ON chunk BEGIN
    INSERT INTO chunk_fts(chunk_fts, rowid, text) VALUES('delete', old.id, old.text);
    INSERT INTO chunk_fts(rowid, text) VALUES (new.id, new.text);
END;

-- Table 05 output, one row per file. This is the routing record for the whole vault.
CREATE TABLE classification (
    id             INTEGER PRIMARY KEY,
    document_id    INTEGER NOT NULL UNIQUE REFERENCES document(id) ON DELETE CASCADE,
    run_id         INTEGER REFERENCES run(id),
    workstream     TEXT,
    secondary_workstream TEXT,
    document_type  TEXT,
    document_role  TEXT,
    subject_entity TEXT,
    counterparty   TEXT,
    document_date  TEXT,
    operative_date TEXT,
    amends_or_issued_under TEXT,
    compilation_flag TEXT,
    completeness   TEXT,
    language       TEXT,
    routing_disposition TEXT,
    classified_at  TEXT
);
CREATE INDEX idx_classification_workstream ON classification(workstream, document_type);

-- ---------------------------------------------------------------- review units
CREATE TABLE review_unit (
    id           INTEGER PRIMARY KEY,
    table_id     INTEGER NOT NULL REFERENCES review_table(id) ON DELETE CASCADE,
    position     INTEGER NOT NULL,
    label        TEXT NOT NULL,        -- what one row is, in the reviewer's words
    unit_key     TEXT NOT NULL,        -- stable grouping key (family / entity / property)
    assembled_by TEXT NOT NULL DEFAULT 'auto',   -- auto | human
    note         TEXT,
    created_at   TEXT NOT NULL,
    UNIQUE (table_id, unit_key)
);

CREATE TABLE unit_document (
    unit_id     INTEGER NOT NULL REFERENCES review_unit(id) ON DELETE CASCADE,
    document_id INTEGER NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    role        TEXT,                  -- Base | Amendment | Restatement | SOW | ...
    PRIMARY KEY (unit_id, document_id)
);

-- -------------------------------------------------------------------- runs
CREATE TABLE run (
    id            INTEGER PRIMARY KEY,
    table_id      INTEGER NOT NULL REFERENCES review_table(id),
    status        TEXT NOT NULL DEFAULT 'pending',  -- pending|running|paused|complete|failed|cancelled
    scope         TEXT NOT NULL DEFAULT '{}',       -- json: unit ids, column names, rerun reason
    model         TEXT,
    cells_total   INTEGER NOT NULL DEFAULT 0,
    cells_done    INTEGER NOT NULL DEFAULT 0,
    cells_failed  INTEGER NOT NULL DEFAULT 0,
    input_tokens  INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    error         TEXT,
    started_at    TEXT,
    finished_at   TEXT,
    created_at    TEXT NOT NULL
);
CREATE INDEX idx_run_table ON run(table_id, created_at);

-- -------------------------------------------------------------------- cells
CREATE TABLE cell (
    id             INTEGER PRIMARY KEY,
    unit_id        INTEGER NOT NULL REFERENCES review_unit(id) ON DELETE CASCADE,
    column_id      INTEGER NOT NULL REFERENCES column_def(id) ON DELETE CASCADE,
    run_id         INTEGER REFERENCES run(id),
    value          TEXT,
    is_fallback    INTEGER NOT NULL DEFAULT 0,
    validation     TEXT NOT NULL DEFAULT '[]',   -- json list of violation codes
    review_status  TEXT NOT NULL DEFAULT 'Unreviewed',
    reviewed_by    TEXT,
    materiality    TEXT,
    deal_consequence TEXT,
    locked         INTEGER NOT NULL DEFAULT 0,
    stale          INTEGER NOT NULL DEFAULT 0,
    prompt_chars   INTEGER,
    input_tokens   INTEGER,
    output_tokens  INTEGER,
    filled_at      TEXT,
    UNIQUE (unit_id, column_id)
);
CREATE INDEX idx_cell_column ON cell(column_id);
CREATE INDEX idx_cell_run ON cell(run_id);

-- Every cell names the evidence it was filled from. A cell without evidence is a
-- candidate nobody can check, which is the failure mode this whole system exists to avoid.
CREATE TABLE cell_evidence (
    id          INTEGER PRIMARY KEY,
    cell_id     INTEGER NOT NULL REFERENCES cell(id) ON DELETE CASCADE,
    chunk_id    INTEGER REFERENCES chunk(id) ON DELETE SET NULL,
    document_id INTEGER NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    quote       TEXT,
    char_start  INTEGER,
    char_end    INTEGER,
    rank        INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX idx_evidence_cell ON cell_evidence(cell_id, rank);

CREATE TABLE cell_history (
    id            INTEGER PRIMARY KEY,
    cell_id       INTEGER NOT NULL REFERENCES cell(id) ON DELETE CASCADE,
    run_id        INTEGER REFERENCES run(id),
    previous_value TEXT,
    new_value     TEXT,
    reason        TEXT,
    actor         TEXT,
    changed_at    TEXT NOT NULL
);
""",
    ),
    (
        2,
        """
-- Where a document's text came from. OCR text is a transcription, not the document, so
-- every cell drawn from it inherits that caveat and says so.
ALTER TABLE document ADD COLUMN text_source TEXT NOT NULL DEFAULT 'extracted';
ALTER TABLE document ADD COLUMN ocr_engine TEXT;
ALTER TABLE document ADD COLUMN ocr_confidence REAL;
CREATE INDEX idx_document_text_source ON document(text_source);
""",
    ),
]


def connect(path: Path | None = None) -> sqlite3.Connection:
    target = path or db_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA synchronous=NORMAL")
    migrate(conn)
    return conn


def migrate(conn: sqlite3.Connection) -> int:
    have = 0
    try:
        row = conn.execute("SELECT MAX(version) AS v FROM schema_version").fetchone()
        have = row["v"] or 0
    except sqlite3.OperationalError:
        have = 0
    for version, sql in MIGRATIONS:
        if version <= have:
            continue
        conn.executescript(sql)
        conn.execute(
            "INSERT INTO schema_version (version, applied_at) VALUES (?, ?)", (version, now())
        )
        conn.commit()
        have = version
    return have


def schema_version(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT MAX(version) AS v FROM schema_version").fetchone()
    return (row["v"] if row else 0) or 0
