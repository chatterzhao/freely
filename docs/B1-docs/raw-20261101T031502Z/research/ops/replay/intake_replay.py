#!/usr/bin/env python3
"""C-F research replay: normalize discussion events and prove event_id dedupe.

Read-only spike. Does not import or modify the Freely runtime.
Real data: GitHub issue chatterzhao/freely#4070 comments, and public PR cli/cli#14879
review/check shapes (observed 2026-11-01). Chat is a fixture.
"""
import json
import sqlite3
import tempfile
from pathlib import Path

EVENTS = [
    {
        "source": "issue_comment",
        "source_event_id": "IC_kwDOSIGLwc8AAAABLGREcA",
        "thread_key": "github:chatterzhao/freely#4070",
        "subject": {"kind": "issue", "id": "4070", "raw_key": ""},
        "actor": {"login": "chatterzhao", "association": "OWNER", "is_bot": False},
        "kind": "comment.created",
        "body_preview": "Reproduction: after local commit 76727c0 ... pr-create-guarded stopped",
        "created_at": "2026-07-21T22:35:54Z",
        "addressed": True,
        "strength": "explicit",
    },
    {
        "source": "issue_comment",
        "source_event_id": "IC_kwDOSIGLwc8AAAABLGcLBQ",
        "thread_key": "github:chatterzhao/freely#4070",
        "subject": {"kind": "issue", "id": "4070", "raw_key": ""},
        "actor": {"login": "chatterzhao", "association": "OWNER", "is_bot": False},
        "kind": "comment.created",
        "body_preview": "Additional acceptance requirements: platform handling must be registry driven",
        "created_at": "2026-07-21T22:57:11Z",
        "addressed": True,
        "strength": "explicit",
    },
    {
        "source": "pr_review",
        "source_event_id": "PRR_kwDODKw3uc8AAAABVMAScg",
        "thread_key": "github:cli/cli#14879",
        "subject": {"kind": "pr", "id": "14879", "raw_key": ""},
        "actor": {"login": "williammartin", "association": "MEMBER", "is_bot": False},
        "kind": "review.approved",
        "body_preview": "",
        "created_at": "2026-10-30T18:23:44Z",
        "addressed": True,
        "strength": "explicit",
    },
    {
        "source": "ci",
        "source_event_id": "job_124213743645",
        "thread_key": "github:cli/cli#14879",
        "subject": {"kind": "pr", "id": "14879", "raw_key": ""},
        "actor": {"login": "github-actions[bot]", "association": "NONE", "is_bot": True},
        "kind": "ci.passed",
        "body_preview": "build (macos-latest): SUCCESS",
        "created_at": "2026-10-30T18:20:00Z",
        "addressed": False,
        "strength": "inferred",
    },
    {
        "source": "chat",
        "source_event_id": "chat_42",
        "thread_key": "chat:default",
        "subject": {"kind": "chat", "id": "42", "raw_key": ""},
        "actor": {"login": "owner", "association": "OWNER", "is_bot": False},
        "kind": "chat.message",
        "body_preview": "先把讨论入口补上",
        "created_at": "2026-11-01T03:02:00Z",
        "addressed": True,
        "strength": "explicit",
    },
]


def normalize(raw):
    eid = f"{raw['source']}:{raw['source_event_id']}"
    return {
        "event_id": eid,
        **raw,
        "dedupe_hash": f"{eid}|{raw['thread_key']}|{raw['actor']['login']}",
    }


def main():
    db = Path(tempfile.mkdtemp()) / "events.db"
    con = sqlite3.connect(db)
    con.execute("""CREATE TABLE events (
        event_id TEXT PRIMARY KEY, source TEXT, source_event_id TEXT,
        thread_key TEXT, actor TEXT, kind TEXT, body_preview TEXT,
        created_at TEXT, addressed INTEGER, strength TEXT, dedupe_hash TEXT
    )""")
    rows = [normalize(e) for e in EVENTS]
    for row in rows * 2:
        con.execute(
            "INSERT OR IGNORE INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (
                row["event_id"], row["source"], row["source_event_id"],
                row["thread_key"], json.dumps(row["actor"], ensure_ascii=False),
                row["kind"], row["body_preview"], row["created_at"],
                int(row["addressed"]), row["strength"], row["dedupe_hash"],
            ),
        )
    con.commit()
    total = con.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    unread = con.execute("SELECT COUNT(*) FROM events WHERE addressed=1").fetchone()[0]
    threads = con.execute("SELECT thread_key, COUNT(*) FROM events GROUP BY thread_key").fetchall()
    print(json.dumps({
        "fixture": str(db),
        "input_rows": len(rows) * 2,
        "stored_rows": total,
        "expected_stored": len(rows),
        "addressed": unread,
        "threads": threads,
        "dedupe_ok": total == len(rows),
    }, ensure_ascii=False, indent=2))
    if total != len(rows):
        raise SystemExit("dedupe failed")


if __name__ == "__main__":
    main()
