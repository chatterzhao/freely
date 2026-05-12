#!/usr/bin/env python3
"""Session-store SQLite module — lives in .freely/freely.db alongside chat-inbox.

Authoritative store for AI tool session IDs. Replaces fragile text-parsing
from cycle logs and filesystem scanning of tool session directories.

In ACP mode, session IDs come from the ACP protocol (session/new, session/resume)
and are stored here. Freely reads back the active session ID to decide resume vs
fresh launch — no more scanning cycle logs or ~/.claude/projects/ for JSONL files.

Usage:
  python3 session-store.py init --db <path>
  python3 session-store.py upsert --db <path> --session-id <uuid> --project <path> \\
      --tool <name> [--role manager|worker] [--parent-session-id <uuid>] \\
      [--launch-kind fresh|resume|fork] [--tool-adapter direct|acp]
  python3 session-store.py get-active --db <path> --project <path> [--role manager]
  python3 session-store.py get-parent --db <path> --session-id <uuid>
  python3 session-store.py complete --db <path> --session-id <uuid> [--status completed|failed]
  python3 session-store.py list --db <path> --project <path> [--status active]
  python3 session-store.py list-children --db <path> --parent-session-id <uuid>
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _connect(db_path: str) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=OFF")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


# ── public API ──────────────────────────────────────────────────────────


def init_db(db_path: str) -> None:
    conn = _connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL UNIQUE,
            project TEXT NOT NULL,
            tool TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'manager',
            parent_session_id TEXT DEFAULT '',
            launch_kind TEXT NOT NULL DEFAULT 'fresh',
            tool_adapter TEXT NOT NULL DEFAULT 'direct',
            resume_mode TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'active',
            error_reason TEXT DEFAULT '',
            metadata_json TEXT DEFAULT '{}',
            created_at TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL DEFAULT ''
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_session_id ON sessions(session_id)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_project_status ON sessions(project, status)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_project_role_status ON sessions(project, role, status)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_parent ON sessions(parent_session_id)"
    )
    conn.commit()
    conn.close()


def upsert_session(
    db_path: str,
    session_id: str,
    project: str,
    tool: str,
    role: str = "manager",
    parent_session_id: str = "",
    launch_kind: str = "fresh",
    tool_adapter: str = "direct",
    resume_mode: str = "",
    error_reason: str = "",
    metadata: dict | None = None,
) -> str:
    """Insert or update a session record. Returns the session_id on success."""
    now = _now_utc()
    meta_json = json.dumps(metadata or {}, separators=(",", ":"))
    conn = _connect(db_path)

    existing = conn.execute(
        "SELECT session_id FROM sessions WHERE session_id = ?",
        (session_id,),
    ).fetchone()

    if existing:
        conn.execute(
            "UPDATE sessions SET project = ?, tool = ?, role = ?, "
            "parent_session_id = ?, launch_kind = ?, tool_adapter = ?, "
            "resume_mode = ?, status = 'active', error_reason = ?, "
            "metadata_json = ?, updated_at = ? "
            "WHERE session_id = ?",
            (project, tool, role, parent_session_id, launch_kind,
             tool_adapter, resume_mode, error_reason, meta_json, now, session_id),
        )
    else:
        conn.execute(
            "INSERT INTO sessions (session_id, project, tool, role, "
            "parent_session_id, launch_kind, tool_adapter, resume_mode, "
            "status, error_reason, metadata_json, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, ?, ?, ?)",
            (session_id, project, tool, role, parent_session_id,
             launch_kind, tool_adapter, resume_mode, error_reason,
             meta_json, now, now),
        )

    conn.commit()
    conn.close()
    return session_id


def get_active(db_path: str, project: str, role: str = "manager") -> str | None:
    """Return the session_id of the active session for a project/role, or None."""
    conn = _connect(db_path)
    row = conn.execute(
        "SELECT session_id FROM sessions "
        "WHERE project = ? AND role = ? AND status = 'active' "
        "ORDER BY updated_at DESC LIMIT 1",
        (project, role),
    ).fetchone()
    conn.close()
    return row[0] if row else None


def get_parent(db_path: str, session_id: str) -> str | None:
    """Return the parent_session_id for a session, or None."""
    conn = _connect(db_path)
    row = conn.execute(
        "SELECT parent_session_id FROM sessions WHERE session_id = ?",
        (session_id,),
    ).fetchone()
    conn.close()
    if row and row[0]:
        return row[0]
    return None


def get_session(db_path: str, session_id: str) -> dict | None:
    """Return full session record."""
    conn = _connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def complete_session(
    db_path: str, session_id: str, status: str = "completed",
    error_reason: str = "",
) -> bool:
    """Mark a session as completed or failed."""
    conn = _connect(db_path)
    conn.execute(
        "UPDATE sessions SET status = ?, error_reason = ?, updated_at = ? "
        "WHERE session_id = ?",
        (status, error_reason, _now_utc(), session_id),
    )
    changed = conn.total_changes > 0
    conn.commit()
    conn.close()
    return changed


def list_sessions(
    db_path: str, project: str, status: str | None = None,
    role: str | None = None,
) -> list[dict]:
    """List sessions for a project, optionally filtered by status and role."""
    conn = _connect(db_path)
    conn.row_factory = sqlite3.Row
    if status and role:
        rows = conn.execute(
            "SELECT * FROM sessions WHERE project = ? AND status = ? AND role = ? "
            "ORDER BY updated_at DESC",
            (project, status, role),
        ).fetchall()
    elif status:
        rows = conn.execute(
            "SELECT * FROM sessions WHERE project = ? AND status = ? "
            "ORDER BY updated_at DESC",
            (project, status),
        ).fetchall()
    elif role:
        rows = conn.execute(
            "SELECT * FROM sessions WHERE project = ? AND role = ? "
            "ORDER BY updated_at DESC",
            (project, role),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM sessions WHERE project = ? "
            "ORDER BY updated_at DESC",
            (project,),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_children(db_path: str, parent_session_id: str) -> list[dict]:
    """List child sessions for a given parent."""
    conn = _connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM sessions WHERE parent_session_id = ? "
        "ORDER BY updated_at DESC",
        (parent_session_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def count_active(db_path: str, project: str) -> int:
    """Return count of active sessions for a project."""
    conn = _connect(db_path)
    row = conn.execute(
        "SELECT COUNT(*) FROM sessions WHERE project = ? AND status = 'active'",
        (project,),
    ).fetchone()
    conn.close()
    return row[0] if row else 0


# ── CLI ─────────────────────────────────────────────────────────────────


def _main() -> int:
    parser = argparse.ArgumentParser(description="Session-store SQLite module")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("init")
    p.add_argument("--db", required=True)

    p = sub.add_parser("upsert")
    p.add_argument("--db", required=True)
    p.add_argument("--session-id", required=True)
    p.add_argument("--project", required=True)
    p.add_argument("--tool", required=True)
    p.add_argument("--role", default="manager")
    p.add_argument("--parent-session-id", default="")
    p.add_argument("--launch-kind", default="fresh")
    p.add_argument("--tool-adapter", default="direct")
    p.add_argument("--resume-mode", default="")
    p.add_argument("--error-reason", default="")
    p.add_argument("--metadata-json", default="{}")

    p = sub.add_parser("get-active")
    p.add_argument("--db", required=True)
    p.add_argument("--project", required=True)
    p.add_argument("--role", default="manager")

    p = sub.add_parser("get-parent")
    p.add_argument("--db", required=True)
    p.add_argument("--session-id", required=True)

    p = sub.add_parser("show")
    p.add_argument("--db", required=True)
    p.add_argument("--session-id", required=True)

    p = sub.add_parser("complete")
    p.add_argument("--db", required=True)
    p.add_argument("--session-id", required=True)
    p.add_argument("--status", default="completed")
    p.add_argument("--error-reason", default="")

    p = sub.add_parser("list")
    p.add_argument("--db", required=True)
    p.add_argument("--project", required=True)
    p.add_argument("--status", default=None)
    p.add_argument("--role", default=None)

    p = sub.add_parser("list-children")
    p.add_argument("--db", required=True)
    p.add_argument("--parent-session-id", required=True)

    p = sub.add_parser("count-active")
    p.add_argument("--db", required=True)
    p.add_argument("--project", required=True)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return 1

    if args.cmd == "init":
        init_db(args.db)
        print(f"freely.db sessions table initialized: {args.db}")
        return 0

    if args.cmd == "upsert":
        metadata = {}
        if args.metadata_json and args.metadata_json != "{}":
            try:
                metadata = json.loads(args.metadata_json)
            except json.JSONDecodeError:
                print(f"ERROR: invalid --metadata-json", file=sys.stderr)
                return 1
        sid = upsert_session(
            args.db, args.session_id, args.project, args.tool,
            args.role, args.parent_session_id, args.launch_kind,
            args.tool_adapter, args.resume_mode, args.error_reason,
            metadata,
        )
        print(sid)
        return 0

    if args.cmd == "get-active":
        sid = get_active(args.db, args.project, args.role)
        if sid:
            print(sid)
            return 0
        print("")
        return 1

    if args.cmd == "get-parent":
        parent = get_parent(args.db, args.session_id)
        if parent:
            print(parent)
            return 0
        print("")
        return 1

    if args.cmd == "show":
        rec = get_session(args.db, args.session_id)
        if rec:
            for k, v in rec.items():
                print(f"{k}: {v}")
            return 0
        print("NOT_FOUND")
        return 1

    if args.cmd == "complete":
        ok = complete_session(args.db, args.session_id, args.status, args.error_reason)
        print("OK" if ok else "NOT_FOUND")
        return 0 if ok else 1

    if args.cmd == "list":
        rows = list_sessions(args.db, args.project, args.status, args.role)
        for r in rows:
            print(
                f"{r['session_id']}\t{r['role']}\t{r['launch_kind']}\t"
                f"{r['status']}\t{r['updated_at']}"
            )
        return 0

    if args.cmd == "list-children":
        rows = list_children(args.db, args.parent_session_id)
        for r in rows:
            print(
                f"{r['session_id']}\t{r['role']}\t{r['launch_kind']}\t"
                f"{r['status']}\t{r['updated_at']}"
            )
        return 0

    if args.cmd == "count-active":
        n = count_active(args.db, args.project)
        print(f"{n}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(_main())
