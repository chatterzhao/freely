#!/usr/bin/env python3
"""Chat-inbox SQLite module.

Stores chat intakes in .freely/chat-inbox.db (git-ignored) to avoid
polluting protected branches with docs/issues/ writes.

Usage:
  python3 chat-inbox.py init --db <path>
  python3 chat-inbox.py add --db <path> --type new-issue --issue-id raw-xxx --message "..."
  python3 chat-inbox.py list --db <path> [--limit 50]
  python3 chat-inbox.py query-by-issue --db <path> --issue-id raw-xxx [--consumed 0]
  python3 chat-inbox.py consume --db <path> --id <ts> [--materialized-as <ref>]
  python3 chat-inbox.py discard --db <path> --id <ts>
  python3 chat-inbox.py reset --db <path> --id <ts>
  python3 chat-inbox.py show --db <path> --id <ts>
  python3 chat-inbox.py materialize --db <path> --id <ts> --target <issue_dir>
"""

import argparse
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_timestamp() -> int:
    """Return current UTC timestamp as YYYYMMDDHHMMSS integer."""
    return int(datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"))


def _connect(db_path: str) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=OFF")
    return conn


# ── public API ──────────────────────────────────────────────


def init_db(db_path: str) -> None:
    conn = _connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY,
            chat_type TEXT NOT NULL,
            issue_id TEXT NOT NULL,
            author TEXT NOT NULL DEFAULT 'human',
            channel TEXT NOT NULL DEFAULT 'chat',
            message TEXT NOT NULL,
            consumed INTEGER NOT NULL DEFAULT 0,
            session_refs TEXT DEFAULT '[]',
            intake_id TEXT DEFAULT '',
            materialized_as TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT ''
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_consumed ON chats(consumed)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_issue_id ON chats(issue_id)"
    )
    conn.commit()
    conn.close()


def add_chat(
    db_path: str,
    chat_type: str,
    issue_id: str,
    message: str,
    author: str = "human",
    channel: str = "chat",
    session_refs: str = "[]",
    intake_id: str = "",
) -> int:
    """Insert a chat record. Returns the chat id (UTC timestamp).
    Retries on PRIMARY KEY collision (+1 second, up to 3 times).
    """
    chat_id = _utc_timestamp()
    conn = _connect(db_path)
    for attempt in range(3):
        try:
            conn.execute(
                "INSERT INTO chats (id, chat_type, issue_id, author, channel, "
                "message, consumed, session_refs, intake_id, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, ?)",
                (chat_id, chat_type, issue_id, author, channel,
                 message, session_refs, intake_id, _now_utc()),
            )
            conn.commit()
            conn.close()
            return chat_id
        except sqlite3.IntegrityError:
            if attempt < 2:
                chat_id += 1
                continue
            conn.close()
            raise
    conn.close()
    return chat_id


def query_pending(db_path: str, limit: int = 50) -> list[dict]:
    """Return unconsumed chats, oldest first."""
    conn = _connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM chats WHERE consumed = 0 ORDER BY id ASC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def query_by_issue(
    db_path: str, issue_id: str, consumed: int | None = None
) -> list[dict]:
    conn = _connect(db_path)
    conn.row_factory = sqlite3.Row
    if consumed is not None:
        rows = conn.execute(
            "SELECT * FROM chats WHERE issue_id = ? AND consumed = ? ORDER BY id ASC",
            (issue_id, consumed),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM chats WHERE issue_id = ? ORDER BY id ASC",
            (issue_id,),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def show(db_path: str, chat_id: int) -> dict | None:
    conn = _connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM chats WHERE id = ?", (chat_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def _update_consumed(db_path: str, chat_id: int, value: int, materialized_as: str = "") -> bool:
    conn = _connect(db_path)
    conn.execute(
        "UPDATE chats SET consumed = ?, materialized_as = ? WHERE id = ?",
        (value, materialized_as, chat_id),
    )
    changed = conn.total_changes > 0
    conn.commit()
    conn.close()
    return changed


def consume(db_path: str, chat_id: int, materialized_as: str = "") -> bool:
    return _update_consumed(db_path, chat_id, 1, materialized_as)


def discard(db_path: str, chat_id: int) -> bool:
    return _update_consumed(db_path, chat_id, -1)


def reset(db_path: str, chat_id: int) -> bool:
    return _update_consumed(db_path, chat_id, 0)


def materialize(db_path: str, chat_id: int, target_dir: str) -> bool:
    """Create docs/issues/{issue_id}/issue.md from a chat record.
    Returns True on success.
    """
    chat = show(db_path, chat_id)
    if not chat:
        return False
    issue_id = chat["issue_id"]
    author = chat.get("author", "human")
    channel = chat.get("channel", "chat")
    created_at = chat.get("created_at", _now_utc())
    session_refs = chat.get("session_refs", "[]")
    intake_id = chat.get("intake_id", "")
    message = chat.get("message", "")

    os.makedirs(target_dir, exist_ok=True)
    issue_file = os.path.join(target_dir, "issue.md")

    with open(issue_file, "w", encoding="utf-8") as f:
        f.write(
            f"---\n"
            f"local_id: {issue_id}\n"
            f"kind: raw\n"
            f"status: proposed\n"
            f"platform_ids: {{}}\n"
            f"primary_platform: \"\"\n"
            f"canonical_issue_path: \"\"\n"
            f"last_synced_comment_at: {{}}\n"
            f"hash: \"\"\n"
            f"created_at: {created_at}\n"
            f"updated_at: {created_at}\n"
            f"intake_id: {intake_id}\n"
            f"author: {author}\n"
            f"channel: {channel}\n"
            f"session_refs: {session_refs}\n"
            f"---\n\n"
            f"{message}\n"
        )
    return True


def materialize_comment(db_path: str, chat_id: int, issue_file: str) -> bool:
    """Append a comment chat to an existing issue.md file."""
    chat = show(db_path, chat_id)
    if not chat:
        return False
    author = chat.get("author", "human")
    channel = chat.get("channel", "chat")
    created_at = chat.get("created_at", _now_utc())
    message = chat.get("message", "")

    comment_id = f"comment-{created_at.replace(':', '').replace('-', '')}"
    os.makedirs(os.path.dirname(issue_file), exist_ok=True)

    with open(issue_file, "a", encoding="utf-8") as f:
        f.write(
            f"\n### {comment_id}\n"
            f"{{source: chat, author: {author}, channel: {channel}}}\n\n"
            f"{message}\n"
        )
    return True


# ── CLI ─────────────────────────────────────────────────────


def _main() -> int:
    parser = argparse.ArgumentParser(description="Chat-inbox SQLite module")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("init")
    p.add_argument("--db", required=True)

    p = sub.add_parser("add")
    p.add_argument("--db", required=True)
    p.add_argument("--type", required=True, dest="chat_type")
    p.add_argument("--issue-id", required=True)
    p.add_argument("--message", required=True)
    p.add_argument("--author", default="human")
    p.add_argument("--channel", default="chat")
    p.add_argument("--session-refs", default="[]")
    p.add_argument("--intake-id", default="")

    p = sub.add_parser("list")
    p.add_argument("--db", required=True)
    p.add_argument("--limit", type=int, default=50)

    p = sub.add_parser("query-by-issue")
    p.add_argument("--db", required=True)
    p.add_argument("--issue-id", required=True)
    p.add_argument("--consumed", type=int, default=None)

    p = sub.add_parser("consume")
    p.add_argument("--db", required=True)
    p.add_argument("--id", type=int, required=True, dest="chat_id")
    p.add_argument("--materialized-as", default="")

    p = sub.add_parser("_update_issue_id")
    p.add_argument("--db", required=True)
    p.add_argument("--id", type=int, required=True, dest="chat_id")
    p.add_argument("--issue-id", required=True)

    p = sub.add_parser("discard")
    p.add_argument("--db", required=True)
    p.add_argument("--id", type=int, required=True, dest="chat_id")

    p = sub.add_parser("reset")
    p.add_argument("--db", required=True)
    p.add_argument("--id", type=int, required=True, dest="chat_id")

    p = sub.add_parser("show")
    p.add_argument("--db", required=True)
    p.add_argument("--id", type=int, required=True, dest="chat_id")

    p = sub.add_parser("materialize")
    p.add_argument("--db", required=True)
    p.add_argument("--id", type=int, required=True, dest="chat_id")
    p.add_argument("--target", required=True)

    p = sub.add_parser("materialize-comment")
    p.add_argument("--db", required=True)
    p.add_argument("--id", type=int, required=True, dest="chat_id")
    p.add_argument("--issue-file", required=True)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return 1

    if args.cmd == "init":
        init_db(args.db)
        print(f"chat-inbox.db initialized: {args.db}")
        return 0

    if args.cmd == "add":
        chat_id = add_chat(
            args.db, args.chat_type, args.issue_id, args.message,
            args.author, args.channel, args.session_refs, args.intake_id,
        )
        print(chat_id)
        return 0

    if args.cmd == "list":
        rows = query_pending(args.db, args.limit)
        for r in rows:
            print(
                f"{r['id']}\t{r['chat_type']}\t{r['issue_id']}\t"
                f"{r.get('message', '')[:80]}"
            )
        return 0

    if args.cmd == "query-by-issue":
        rows = query_by_issue(args.db, args.issue_id, args.consumed)
        for r in rows:
            print(
                f"{r['id']}\t{r['chat_type']}\t{r['consumed']}\t"
                f"{r.get('message', '')[:80]}"
            )
        return 0

    if args.cmd == "consume":
        ok = consume(args.db, args.chat_id, args.materialized_as)
        print("OK" if ok else "NOT_FOUND")
        return 0 if ok else 1

    if args.cmd == "_update_issue_id":
        conn = _connect(args.db)
        conn.execute(
            "UPDATE chats SET issue_id = ? WHERE id = ?",
            (args.issue_id, args.chat_id),
        )
        conn.commit()
        conn.close()
        print("OK")
        return 0

    if args.cmd == "discard":
        ok = discard(args.db, args.chat_id)
        print("OK" if ok else "NOT_FOUND")
        return 0 if ok else 1

    if args.cmd == "reset":
        ok = reset(args.db, args.chat_id)
        print("OK" if ok else "NOT_FOUND")
        return 0 if ok else 1

    if args.cmd == "show":
        chat = show(args.db, args.chat_id)
        if chat:
            for k, v in chat.items():
                print(f"{k}: {v}")
            return 0
        print("NOT_FOUND")
        return 1

    if args.cmd == "materialize":
        ok = materialize(args.db, args.chat_id, args.target)
        print("OK" if ok else "NOT_FOUND")
        return 0 if ok else 1

    if args.cmd == "materialize-comment":
        ok = materialize_comment(args.db, args.chat_id, args.issue_file)
        print("OK" if ok else "NOT_FOUND")
        return 0 if ok else 1

    return 1


if __name__ == "__main__":
    sys.exit(_main())
