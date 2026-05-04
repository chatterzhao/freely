#!/usr/bin/env python3
"""worker-store.py: SQLite CRUD for worker delegation state.

Replaces file-based manager-exit-contract.env with SQLite for
atomic state tracking and queryability.
"""

import argparse
import json
import os
import sqlite3
from datetime import datetime, timezone


DB_PATH = None  # set by main()


def _now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute("PRAGMA foreign_keys=OFF")
    return conn


def init_db():
    conn = _connect()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS worker_delegation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            delegation_id TEXT NOT NULL,
            prompt_file TEXT NOT NULL,
            worktree TEXT NOT NULL,
            branch TEXT NOT NULL,
            intent_kind TEXT DEFAULT '',
            owner_issue TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            launched_at TEXT DEFAULT '',
            completed_at TEXT DEFAULT '',
            exit_kind TEXT DEFAULT '',
            session_id TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL DEFAULT ''
        );
        CREATE INDEX IF NOT EXISTS idx_wd_status ON worker_delegation(status);
        CREATE INDEX IF NOT EXISTS idx_wd_delegation ON worker_delegation(delegation_id);
        CREATE INDEX IF NOT EXISTS idx_wd_prompt ON worker_delegation(prompt_file);
    """)
    conn.commit()
    conn.close()


def upsert_delegation(delegation_id, prompt_files, worktree, branch,
                      intent_kind="", owner_issue=""):
    """Create or update a delegation batch. prompt_files is a comma-separated string."""
    conn = _connect()
    now = _now_utc()
    ids = []
    for pf in prompt_files.split(","):
        pf = pf.strip()
        if not pf:
            continue
        existing = conn.execute(
            "SELECT id, status FROM worker_delegation WHERE prompt_file = ? ORDER BY id DESC LIMIT 1",
            (pf,),
        ).fetchone()
        if existing:
            # Update existing
            conn.execute(
                "UPDATE worker_delegation SET delegation_id=?, worktree=?, branch=?, "
                "intent_kind=?, owner_issue=?, updated_at=? WHERE id=?",
                (delegation_id, worktree, branch, intent_kind, owner_issue, now, existing[0]),
            )
            ids.append(existing[0])
        else:
            # Insert new
            cur = conn.execute(
                "INSERT INTO worker_delegation (delegation_id, prompt_file, worktree, "
                "branch, intent_kind, owner_issue, status, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, ?)",
                (delegation_id, pf, worktree, branch, intent_kind, owner_issue, now, now),
            )
            ids.append(cur.lastrowid)
    conn.commit()
    conn.close()
    return ids


def update_status(prompt_file, status, exit_kind="", session_id=""):
    """Update worker status. Called by runtime when launching/completing workers."""
    conn = _connect()
    now = _now_utc()
    if status == "launched":
        conn.execute(
            "UPDATE worker_delegation SET status=?, launched_at=?, session_id=?, updated_at=? "
            "WHERE prompt_file=? AND status='pending'",
            (status, now, session_id, now, prompt_file),
        )
    elif status in ("running", "completed", "failed"):
        conn.execute(
            "UPDATE worker_delegation SET status=?, exit_kind=?, updated_at=?, "
            "completed_at=CASE WHEN ? IN ('completed','failed') THEN ? ELSE completed_at END "
            "WHERE prompt_file=? AND status IN ('pending','launched','running')",
            (status, exit_kind, now, status, now, prompt_file),
        )
    conn.commit()
    # Return count of running workers
    count = conn.execute(
        "SELECT COUNT(*) FROM worker_delegation WHERE status IN ('pending','launched','running')"
    ).fetchone()[0]
    conn.close()
    return count


def has_running_workers():
    """Manager checks this before re-patrolling."""
    conn = _connect()
    count = conn.execute(
        "SELECT COUNT(*) FROM worker_delegation WHERE status IN ('pending','launched','running')"
    ).fetchone()[0]
    conn.close()
    return count > 0


def get_active_delegations():
    """Get all non-completed delegations."""
    conn = _connect()
    rows = conn.execute(
        "SELECT id, delegation_id, prompt_file, worktree, branch, intent_kind, "
        "status, launched_at, exit_kind, session_id "
        "FROM worker_delegation WHERE status != 'completed' AND status != 'failed' "
        "ORDER BY id ASC"
    ).fetchall()
    conn.close()
    return rows


def get_pending_prompts_csv():
    """Get CSV of prompt files that still need launching."""
    conn = _connect()
    rows = conn.execute(
        "SELECT prompt_file FROM worker_delegation WHERE status='pending'"
    ).fetchall()
    conn.close()
    return ",".join(r[0] for r in rows)


def migrate_from_exit_contract(project_dir):
    """One-time migration: read old exit-contract.env and worker-prompts/ into SQLite."""
    contract_file = os.path.join(project_dir, ".freely", "run", "manager-exit-contract.env")
    if not os.path.isfile(contract_file):
        return False
    # Read EXIT_KIND and WORKER_PROMPTS_CSV
    exit_kind = ""
    prompts_csv = ""
    with open(contract_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("EXIT_KIND="):
                exit_kind = line.split("=", 1)[1].strip('"')
            elif line.startswith("WORKER_PROMPTS_CSV="):
                prompts_csv = line.split("=", 1)[1].strip('"')
    if exit_kind != "delegate_workers" or not prompts_csv:
        return False
    delegation_id = f"migrated-{_now_utc()}"
    # For migration, use the project dir as worktree
    worktree = project_dir
    branch = "develop"
    # Parse branch from first prompt file
    for pf in prompts_csv.split(","):
        pf = pf.strip()
        if pf and os.path.isfile(pf):
            with open(pf) as f2:
                for line in f2:
                    if line.startswith("Branch:"):
                        # Parse "- branch_name"
                        pass
            break
    upsert_delegation(delegation_id, prompts_csv, worktree, branch)
    # Rename old file to prevent double migration
    os.rename(contract_file, contract_file + ".migrated")
    return True


def mark_stale_as_failed(timeout_minutes=30):
    """Mark workers that haven't been updated as failed."""
    conn = _connect()
    now = _now_utc()
    conn.execute(
        "UPDATE worker_delegation SET status='failed', exit_kind='timeout', updated_at=? "
        "WHERE status IN ('pending','launched','running') "
        "AND updated_at < datetime('now', ? || ' minutes')",
        (now, f"-{timeout_minutes}"),
    )
    conn.commit()
    conn.close()


def main():
    global DB_PATH
    parser = argparse.ArgumentParser(description="Worker delegation SQLite store")
    parser.add_argument("--db", required=True, help="Path to freely.db")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("init")
    p = sub.add_parser("migrate")
    p.add_argument("--project", required=True)

    p = sub.add_parser("upsert")
    p.add_argument("--delegation-id", required=True)
    p.add_argument("--prompts-csv", required=True)
    p.add_argument("--worktree", required=True)
    p.add_argument("--branch", default="develop")
    p.add_argument("--intent-kind", default="")
    p.add_argument("--owner-issue", default="")

    p = sub.add_parser("update-status")
    p.add_argument("--prompt-file", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--exit-kind", default="")
    p.add_argument("--session-id", default="")

    p = sub.add_parser("has-running")
    p = sub.add_parser("get-pending-csv")
    p = sub.add_parser("mark-stale")
    p.add_argument("--timeout-minutes", type=int, default=30)

    args = parser.parse_args()
    DB_PATH = args.db

    if args.cmd == "init":
        init_db()
    elif args.cmd == "migrate":
        ok = migrate_from_exit_contract(args.project)
        print("migrated" if ok else "nothing-to-migrate")
    elif args.cmd == "upsert":
        ids = upsert_delegation(args.delegation_id, args.prompts_csv,
                                args.worktree, args.branch,
                                args.intent_kind, args.owner_issue)
        print(",".join(str(i) for i in ids))
    elif args.cmd == "update-status":
        count = update_status(args.prompt_file, args.status, args.exit_kind, args.session_id)
        print(f"running_count={count}")
    elif args.cmd == "has-running":
        print("true" if has_running_workers() else "false")
    elif args.cmd == "get-pending-csv":
        print(get_pending_prompts_csv())
    elif args.cmd == "mark-stale":
        mark_stale_as_failed(args.timeout_minutes)
        print("done")


if __name__ == "__main__":
    main()
