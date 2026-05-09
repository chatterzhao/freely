#!/usr/bin/env python3
"""handoff.py: SQLite CRUD for manager-worker handoff state.

One table (handoffs), one role field (manager|worker). Replaces
file-based exit-contract.env + worker-prompts/*.txt as launch data source.
"""

import argparse
import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone


DB_PATH = None


def _now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute("PRAGMA foreign_keys=OFF")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _connect()
    conn.executescript("""
        DROP TABLE IF EXISTS worker_delegation;
        CREATE TABLE IF NOT EXISTS handoffs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            handoff_id TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL CHECK(role IN ('manager','worker')),
            raw_key TEXT NOT NULL,
            worktree TEXT DEFAULT '',
            branch TEXT DEFAULT '',
            prompt_file TEXT NOT NULL,
            parent_handoff_id TEXT DEFAULT '',
            intent_kind TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending'
                CHECK(status IN ('pending','launched','completed','rejected','blocked')),
            exit_kind TEXT DEFAULT '',
            session_id TEXT DEFAULT '',
            launched_at TEXT DEFAULT '',
            completed_at TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL DEFAULT ''
        );
        CREATE INDEX IF NOT EXISTS idx_handoffs_role_status ON handoffs(role, status);
        CREATE INDEX IF NOT EXISTS idx_handoffs_raw_key ON handoffs(raw_key);
        CREATE INDEX IF NOT EXISTS idx_handoffs_worktree ON handoffs(worktree);
        CREATE INDEX IF NOT EXISTS idx_handoffs_parent ON handoffs(parent_handoff_id);
    """)
    conn.commit()
    conn.close()


def insert(role, raw_key, prompt_file, worktree="", branch="",
           parent_handoff_id="", intent_kind=""):
    conn = _connect()
    hid = _now_utc().replace("T", "").replace("Z", "").replace("-", "").replace(":", "") + "-" + uuid.uuid4().hex[:6]
    now = _now_utc()
    conn.execute(
        """INSERT INTO handoffs (handoff_id, role, raw_key, worktree, branch,
           prompt_file, parent_handoff_id, intent_kind, status, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,'pending',?,?)""",
        (hid, role, raw_key, worktree, branch, prompt_file,
         parent_handoff_id, intent_kind, now, now))
    conn.commit()
    conn.close()
    return hid


def update_status(handoff_id, status, exit_kind="", session_id=""):
    conn = _connect()
    now = _now_utc()
    cols = ["status=?", "updated_at=?"]
    params = [status, now, handoff_id]
    if status == "launched":
        cols.append("launched_at=?")
        params.insert(-1, now)
    if status in ("completed", "rejected", "blocked"):
        cols.append("completed_at=?")
        params.insert(-1, now)
    if exit_kind:
        cols.append("exit_kind=?")
        params.insert(-1, exit_kind)
    if session_id:
        cols.append("session_id=?")
        params.insert(-1, session_id)
    sql = f"UPDATE handoffs SET {', '.join(cols)} WHERE handoff_id=?"
    conn.execute(sql, params)
    conn.commit()
    conn.close()


def get(handoff_id):
    conn = _connect()
    row = conn.execute("SELECT * FROM handoffs WHERE handoff_id=?", (handoff_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_by_role(role, status=None, limit=50):
    conn = _connect()
    if status:
        rows = conn.execute(
            "SELECT * FROM handoffs WHERE role=? AND status=? ORDER BY created_at DESC LIMIT ?",
            (role, status, limit)).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM handoffs WHERE role=? ORDER BY created_at DESC LIMIT ?",
            (role, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_by_raw_key(raw_key, role=None):
    conn = _connect()
    if role:
        rows = conn.execute(
            "SELECT * FROM handoffs WHERE raw_key=? AND role=? ORDER BY created_at DESC",
            (raw_key, role)).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM handoffs WHERE raw_key=? ORDER BY created_at DESC",
            (raw_key,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def active_workers_for_worktree(worktree):
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM handoffs WHERE worktree=? AND role='worker' AND status IN ('pending','launched')",
        (worktree,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def latest_manager():
    conn = _connect()
    row = conn.execute(
        "SELECT * FROM handoffs WHERE role='manager' ORDER BY created_at DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def children_of(parent_handoff_id):
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM handoffs WHERE parent_handoff_id=? AND role='worker' ORDER BY created_at",
        (parent_handoff_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_stale(timeout_minutes=30):
    conn = _connect()
    now_dt = datetime.now(timezone.utc)
    cutoff = now_dt.replace(minute=now_dt.minute - timeout_minutes).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.execute(
        "UPDATE handoffs SET status='blocked', exit_kind='timeout', updated_at=? "
        "WHERE role='worker' AND status='launched' AND launched_at < ?",
        (_now_utc(), cutoff))
    conn.commit()
    conn.close()



# --- CLI ---
def main():
    global DB_PATH
    parser = argparse.ArgumentParser(description="handoff.py — manager-worker handoff SQLite store")
    sub = parser.add_subparsers(dest="cmd")

    p_init = sub.add_parser("init")
    p_init.add_argument("--db", required=True)

    p_insert = sub.add_parser("insert")
    p_insert.add_argument("--db", required=True)
    p_insert.add_argument("--role", required=True, choices=["manager", "worker"])
    p_insert.add_argument("--raw-key", required=True)
    p_insert.add_argument("--prompt-file", required=True)
    p_insert.add_argument("--worktree", default="")
    p_insert.add_argument("--branch", default="")
    p_insert.add_argument("--parent", default="")
    p_insert.add_argument("--intent-kind", default="")

    p_update = sub.add_parser("update")
    p_update.add_argument("--db", required=True)
    p_update.add_argument("--handoff-id", required=True)
    p_update.add_argument("--status", required=True)
    p_update.add_argument("--exit-kind", default="")
    p_update.add_argument("--session-id", default="")

    p_get = sub.add_parser("get")
    p_get.add_argument("--db", required=True)
    p_get.add_argument("--handoff-id", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("--db", required=True)
    p_list.add_argument("--role", default="worker")
    p_list.add_argument("--status", default="")

    p_list_key = sub.add_parser("list-key")
    p_list_key.add_argument("--db", required=True)
    p_list_key.add_argument("--raw-key", required=True)

    p_active = sub.add_parser("active-workers")
    p_active.add_argument("--db", required=True)
    p_active.add_argument("--worktree", required=True)

    p_latest = sub.add_parser("latest-manager")
    p_latest.add_argument("--db", required=True)

    p_stale = sub.add_parser("mark-stale")
    p_stale.add_argument("--db", required=True)
    p_stale.add_argument("--timeout-minutes", type=int, default=30)

    args = parser.parse_args()
    DB_PATH = args.db

    if args.cmd == "init":
        init_db()
        print("ok")
    elif args.cmd == "insert":
        hid = insert(args.role, args.raw_key, args.prompt_file,
                     args.worktree, args.branch, args.parent, args.intent_kind)
        print(hid)
    elif args.cmd == "update":
        update_status(args.handoff_id, args.status, args.exit_kind, args.session_id)
        print("ok")
    elif args.cmd == "get":
        r = get(args.handoff_id)
        print(json.dumps(r, indent=2) if r else "null")
    elif args.cmd == "list":
        rows = list_by_role(args.role, args.status or None)
        print(json.dumps(rows, indent=2))
    elif args.cmd == "list-key":
        rows = list_by_raw_key(args.raw_key)
        print(json.dumps(rows, indent=2))
    elif args.cmd == "active-workers":
        rows = active_workers_for_worktree(args.worktree)
        print(json.dumps(rows, indent=2))
    elif args.cmd == "latest-manager":
        r = latest_manager()
        print(json.dumps(r, indent=2) if r else "null")
    elif args.cmd == "mark-stale":
        mark_stale(args.timeout_minutes)
        print("ok")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
