#!/usr/bin/env python3
"""Discussion event ingestion for issue comments, PR reviews, CI, and chat.

This module is deliberately small and dependency-free. It normalizes platform
payloads into one append-only event shape, applies a deterministic admission
gate, and stores events by stable event_id (idempotent).
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Iterable


SOURCES = {
    "issue", "issue_comment", "pr_review", "pr_review_comment", "ci", "chat",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS discussion_events (
    event_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    source_event_id TEXT NOT NULL,
    thread_key TEXT NOT NULL,
    subject_kind TEXT,
    subject_id TEXT,
    raw_key TEXT,
    actor_login TEXT,
    actor_id TEXT,
    actor_association TEXT,
    actor_is_bot INTEGER NOT NULL DEFAULT 0,
    kind TEXT NOT NULL,
    body_ref TEXT,
    body_preview TEXT,
    created_at TEXT NOT NULL,
    addressed INTEGER NOT NULL DEFAULT 0,
    strength TEXT NOT NULL DEFAULT 'inferred',
    disposition TEXT NOT NULL DEFAULT 'observe',
    disposition_reason TEXT,
    dedupe_hash TEXT,
    read_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_discussion_events_thread ON discussion_events(thread_key, created_at);
CREATE INDEX IF NOT EXISTS idx_discussion_events_unread ON discussion_events(read_at);
CREATE INDEX IF NOT EXISTS idx_discussion_events_source ON discussion_events(source);
"""


def _login(author: Any) -> str:
    if isinstance(author, dict):
        return str(author.get("login") or author.get("name") or author.get("id") or "")
    return str(author or "")


def _actor(author: Any) -> dict:
    login = _login(author)
    is_bot = bool(login.endswith("[bot]") or login.endswith("-bot") or login == "github-actions")
    association = ""
    if isinstance(author, dict):
        association = str(author.get("association") or author.get("author_association") or "")
    return {"login": login or "unknown", "id": str(author.get("id", "")) if isinstance(author, dict) else "",
            "association": association, "is_bot": is_bot}


def _thread(repo: str, kind: str, number: Any) -> str:
    return f"github:{repo}#{number}" if repo else f"github:#{number}"


def normalize(source: str, raw: dict, repo: str = "") -> dict:
    if source not in SOURCES:
        raise ValueError(f"unsupported source: {source}")
    if source == "issue":
        number = raw.get("number") or raw.get("id")
        eid = f"issue:{raw.get('id') or number}"
        thread = _thread(repo, "issue", number)
        subject = {"kind": "issue", "id": str(number), "raw_key": raw.get("raw_key", "")}
        kind = "issue.updated"
        body = raw.get("body") or ""
        created = raw.get("updated_at") or raw.get("created_at") or ""
        addressed = True
    elif source == "issue_comment":
        number = raw.get("issue_number") or raw.get("number") or raw.get("issue", {}).get("number")
        eid = f"issue_comment:{raw.get('id')}"
        thread = _thread(repo, "issue", number)
        subject = {"kind": "issue", "id": str(number), "raw_key": raw.get("raw_key", "")}
        kind = "comment.created"
        body = raw.get("body") or ""
        created = raw.get("created_at") or ""
        addressed = bool(raw.get("addressed", True))
    elif source == "pr_review":
        number = raw.get("pr_number") or raw.get("number") or raw.get("pull_request", {}).get("number")
        eid = f"pr_review:{raw.get('id')}"
        thread = _thread(repo, "pr", number)
        subject = {"kind": "pr", "id": str(number), "raw_key": raw.get("raw_key", "")}
        kind = f"review.{str(raw.get('state') or 'commented').lower()}"
        body = raw.get("body") or ""
        created = raw.get("submitted_at") or raw.get("created_at") or ""
        addressed = True
    elif source == "pr_review_comment":
        number = raw.get("pr_number") or raw.get("number") or raw.get("pull_request", {}).get("number")
        eid = f"pr_review_comment:{raw.get('id')}"
        thread = _thread(repo, "pr", number)
        subject = {"kind": "pr", "id": str(number), "raw_key": raw.get("raw_key", "")}
        kind = "comment.created"
        body = raw.get("body") or ""
        created = raw.get("created_at") or ""
        addressed = bool(raw.get("addressed", True))
    elif source == "ci":
        number = raw.get("pr_number") or raw.get("number")
        eid = f"ci:{raw.get('id')}"
        thread = _thread(repo, "pr", number)
        subject = {"kind": "pr", "id": str(number), "raw_key": raw.get("raw_key", "")}
        kind = f"ci.{str(raw.get('conclusion') or 'unknown').lower()}"
        body = f"{raw.get('name', 'check')}: {raw.get('conclusion', 'unknown')}"
        created = raw.get("completed_at") or raw.get("created_at") or ""
        addressed = False
    else:  # chat
        cid = raw.get("id")
        eid = f"chat:{cid}"
        thread = f"chat:{raw.get('chat_type') or 'default'}"
        subject = {"kind": "chat", "id": str(cid), "raw_key": raw.get("raw_key", "")}
        kind = "chat.message"
        body = raw.get("message") or raw.get("body") or ""
        created = raw.get("created_at") or ""
        addressed = bool(raw.get("addressed", True))

    actor = _actor(raw.get("author") or raw.get("user") or raw.get("actor") or raw.get("login"))
    preview = body[:500]
    dedupe = hashlib.sha256(f"{eid}|{thread}|{actor['login']}|{created}".encode()).hexdigest()
    return {
        "event_id": eid,
        "source": source,
        "source_event_id": str(raw.get("id", "")),
        "thread_key": thread,
        "subject_kind": subject["kind"],
        "subject_id": subject["id"],
        "raw_key": subject["raw_key"],
        "actor": actor,
        "kind": kind,
        "body_ref": raw.get("body_ref"),
        "body_preview": preview,
        "created_at": created or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "addressed": bool(addressed),
        "strength": raw.get("strength", "explicit" if addressed else "inferred"),
        "dedupe_hash": dedupe,
    }


def admit(event: dict, policy: dict | None = None) -> dict:
    """Deterministic authoritative admission; never judges business value."""
    policy = policy or {}
    if event.get("source") not in policy.get("enabled_sources", SOURCES):
        return {"disposition": "ignore", "reason": "source_disabled"}
    actor = event.get("actor") or {}
    if actor.get("is_bot"):
        return {"disposition": "observe", "reason": "bot_filtered"}
    login = str(actor.get("login") or "unknown")
    allowed = policy.get("allowed_actors")
    if allowed and login not in allowed:
        return {"disposition": "ignore", "reason": "actor_not_allowed"}
    if login == "unknown":
        return {"disposition": "observe", "reason": "actor_unknown"}
    if not event.get("addressed"):
        return {"disposition": "observe", "reason": "not_addressed"}
    if event.get("strength") != "explicit":
        return {"disposition": "observe", "reason": "inferred"}
    return {"disposition": "accept", "reason": "explicit_addressed"}


class EventStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # db-writer: discussion_events: 讨论事件 store，登记于 State 契约
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def ingest(self, events: Iterable[dict], policy: dict | None = None) -> int:
        inserted = 0
        for event in events:
            decision = admit(event, policy)
            row = {
                "event_id": event["event_id"], "source": event["source"],
                "source_event_id": event.get("source_event_id", ""),
                "thread_key": event["thread_key"], "subject_kind": event.get("subject_kind"),
                "subject_id": event.get("subject_id"), "raw_key": event.get("raw_key"),
                "actor_login": event.get("actor", {}).get("login"),
                "actor_id": event.get("actor", {}).get("id", ""),
                "actor_association": event.get("actor", {}).get("association", ""),
                "actor_is_bot": int(bool(event.get("actor", {}).get("is_bot"))),
                "kind": event.get("kind", ""), "body_ref": event.get("body_ref"),
                "body_preview": event.get("body_preview", ""), "created_at": event.get("created_at", ""),
                "addressed": int(bool(event.get("addressed"))), "strength": event.get("strength", "inferred"),
                "disposition": decision["disposition"], "disposition_reason": decision["reason"],
                "dedupe_hash": event.get("dedupe_hash"),
            }
            cur = self.conn.execute(
                """INSERT OR IGNORE INTO discussion_events
                (event_id,source,source_event_id,thread_key,subject_kind,subject_id,raw_key,
                 actor_login,actor_id,actor_association,actor_is_bot,kind,body_ref,body_preview,
                 created_at,addressed,strength,disposition,disposition_reason,dedupe_hash)
                VALUES (:event_id,:source,:source_event_id,:thread_key,:subject_kind,:subject_id,:raw_key,
                        :actor_login,:actor_id,:actor_association,:actor_is_bot,:kind,:body_ref,:body_preview,
                        :created_at,:addressed,:strength,:disposition,:disposition_reason,:dedupe_hash)""", row)
            inserted += cur.rowcount
        self.conn.commit()
        return inserted

    def count(self) -> int:
        return int(self.conn.execute("SELECT COUNT(*) FROM discussion_events").fetchone()[0])

    def unread(self) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM discussion_events WHERE read_at IS NULL ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

    def mark_read(self, event_ids: Iterable[str]) -> None:
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        for eid in event_ids:
            self.conn.execute("UPDATE discussion_events SET read_at=? WHERE event_id=?", (now, eid))
        self.conn.commit()

    def summary(self) -> dict:
        rows = self.unread()
        by_source: dict[str, int] = {}
        for r in rows:
            by_source[r["source"]] = by_source.get(r["source"], 0) + 1
        return {"unread": len(rows), "by_source": by_source, "latest": rows[:10]}


def collect(project: str | Path, raw_events: list[dict] | None = None) -> dict:
    """Collect events for scan.

    Runtime pollers may append normalized/raw events to
    `.freely/run/discussion-events.json`. This function is intentionally
    side-effect free when the file is absent: it returns an empty summary.
    """
    project = Path(project)
    if raw_events is None:
        inbox = project / ".freely" / "run" / "discussion-events.json"
        raw_events = json.loads(inbox.read_text(encoding="utf-8")) if inbox.exists() else []
    store = EventStore(project / ".freely" / "freely.db")
    normalized = []
    for item in raw_events:
        source = item.get("source")
        raw = item.get("raw") or item.get("payload") or {}
        if source in SOURCES:
            normalized.append(normalize(source, raw, repo=item.get("repo", "")))
    store.ingest(normalized)
    return store.summary()
