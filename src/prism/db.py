"""SQLite schema and connection helpers for Prism.

Owns the database file. No other module should open the SQLite file directly —
go through the service layer instead.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

DEFAULT_DB_PATH = Path.home() / ".prism" / "prism.db"


SCHEMA = """
CREATE TABLE IF NOT EXISTS domains (
    id       INTEGER PRIMARY KEY,
    slug     TEXT UNIQUE NOT NULL,
    name     TEXT NOT NULL,
    tier     INTEGER NOT NULL CHECK (tier IN (1, 2)),
    summary  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS statutes (
    id          INTEGER PRIMARY KEY,
    domain_id   INTEGER NOT NULL REFERENCES domains(id) ON DELETE CASCADE,
    citation    TEXT NOT NULL,
    title       TEXT NOT NULL,
    summary     TEXT NOT NULL,
    body_md     TEXT NOT NULL,
    source_url  TEXT
);

CREATE TABLE IF NOT EXISTS scenarios (
    id              INTEGER PRIMARY KEY,
    domain_id       INTEGER NOT NULL REFERENCES domains(id) ON DELETE CASCADE,
    slug            TEXT UNIQUE NOT NULL,
    title           TEXT NOT NULL,
    description_md  TEXT NOT NULL,
    walkthrough_md  TEXT NOT NULL,
    template_md     TEXT
);

CREATE TABLE IF NOT EXISTS scenario_statutes (
    scenario_id  INTEGER NOT NULL REFERENCES scenarios(id) ON DELETE CASCADE,
    statute_id   INTEGER NOT NULL REFERENCES statutes(id) ON DELETE CASCADE,
    PRIMARY KEY (scenario_id, statute_id)
);

CREATE TABLE IF NOT EXISTS ethical_frameworks (
    id              INTEGER PRIMARY KEY,
    slug            TEXT UNIQUE NOT NULL,
    name            TEXT NOT NULL,
    description_md  TEXT NOT NULL,
    key_questions   TEXT NOT NULL  -- JSON array
);

CREATE TABLE IF NOT EXISTS decisions (
    id                 INTEGER PRIMARY KEY,
    created_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    situation          TEXT NOT NULL,
    options            TEXT NOT NULL,  -- JSON array
    chosen             TEXT NOT NULL,
    reasoning          TEXT NOT NULL,
    expected_outcome   TEXT NOT NULL,
    confidence         INTEGER NOT NULL CHECK (confidence BETWEEN 0 AND 100),
    linked_scenario_id INTEGER REFERENCES scenarios(id) ON DELETE SET NULL,
    actual_outcome     TEXT,
    reviewed_at        DATETIME
);

CREATE TABLE IF NOT EXISTS bias_flags (
    id           INTEGER PRIMARY KEY,
    decision_id  INTEGER NOT NULL REFERENCES decisions(id) ON DELETE CASCADE,
    bias_slug    TEXT NOT NULL,
    evidence     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_statutes_domain ON statutes(domain_id);
CREATE INDEX IF NOT EXISTS idx_scenarios_domain ON scenarios(domain_id);
CREATE INDEX IF NOT EXISTS idx_decisions_created ON decisions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_bias_decision ON bias_flags(decision_id);
"""


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Open a connection with foreign keys enabled and rows as dicts."""
    path = ":memory:" if db_path == ":memory:" else str(db_path or DEFAULT_DB_PATH)
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    """Create tables if they don't already exist."""
    conn.executescript(SCHEMA)
    conn.commit()


@contextmanager
def session(db_path: str | Path | None = None) -> Iterator[sqlite3.Connection]:
    """Context manager for a connection that ensures init + cleanup."""
    conn = connect(db_path)
    try:
        init_schema(conn)
        yield conn
    finally:
        conn.close()
