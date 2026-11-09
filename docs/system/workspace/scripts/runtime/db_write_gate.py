#!/usr/bin/env python3
"""Single entry point for SQLite access that is not the long-lived db daemon.

`freely_db_manager.py` owns the single writer connection by design
(`three-loop-capability-lifecycle.md`). Everything else was connecting straight
to `.freely/freely.db`, which broke that invariant (raw-20261104T075910Z).

Two factories keep the intent explicit and machine-checkable:

- `connect_reader(db)` — read-only URI connection (`mode=ro`). Never creates the
  file, never takes a write lock, never sees an uncommitted row.
- `connect_writer(db)` — short-lived writer that takes `BEGIN IMMEDIATE` before
  its first mutation and retries on `database is locked`, so two short writers
  serialize instead of racing.

`bin/check-db-writers` enforces that every `sqlite3.connect` in the workspace is
one of: this module, the daemon, or an explicit read-only/registered call.
"""
from __future__ import annotations

import sqlite3
import time
from pathlib import Path

BUSY_TIMEOUT_MS = 5000
RETRY_DEADLINE_SECS = 10.0


def connect_reader(db_path: str | Path) -> sqlite3.Connection:
    """Read-only connection. Raises if the database does not exist."""
    path = Path(db_path)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=BUSY_TIMEOUT_MS / 1000)
    conn.execute("PRAGMA query_only = ON")
    return conn


def connect_reader_if_exists(db_path: str | Path) -> sqlite3.Connection | None:
    """Read-only connection, or None when the database is absent."""
    if not Path(db_path).exists():
        return None
    return connect_reader(db_path)


def connect_writer(db_path: str | Path) -> sqlite3.Connection:
    """Short-lived writer that serializes with other writers."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=BUSY_TIMEOUT_MS / 1000)
    conn.execute(f"PRAGMA busy_timeout = {BUSY_TIMEOUT_MS}")
    return conn


def write_tx(db_path: str | Path, fn):
    """Run `fn(conn)` inside BEGIN IMMEDIATE, retrying transient lock errors."""
    deadline = time.monotonic() + RETRY_DEADLINE_SECS
    attempt = 0
    while True:
        conn = connect_writer(db_path)
        try:
            conn.execute("BEGIN IMMEDIATE")
            result = fn(conn)
            conn.commit()
            return result
        except sqlite3.OperationalError as exc:
            conn.rollback()
            if "locked" not in str(exc).lower() or time.monotonic() >= deadline:
                raise
            attempt += 1
            time.sleep(min(0.05 * (2 ** attempt), 0.5))
        finally:
            conn.close()
