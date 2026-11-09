#!/usr/bin/env python3
"""Append-only task/handoff/message store with ownership and handback."""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any

TERMINAL = {"completed", "failed", "canceled"}

SCHEMA = """
CREATE TABLE IF NOT EXISTS delegation_tasks (
    task_id TEXT PRIMARY KEY, thread_key TEXT NOT NULL, state TEXT NOT NULL,
    owner TEXT, lease_until INTEGER NOT NULL DEFAULT 0,
    handback_done INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS handoffs (
    handoff_id TEXT PRIMARY KEY, task_id TEXT NOT NULL, parent_handoff_id TEXT,
    from_role TEXT, to_role TEXT, from_agent TEXT, to_agent TEXT,
    intent TEXT, artifacts_json TEXT, context_refs_json TEXT,
    expected_output TEXT, status TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS handoff_messages (
    message_id TEXT PRIMARY KEY, handoff_id TEXT, task_id TEXT NOT NULL,
    role TEXT, parts_json TEXT NOT NULL, created_at TEXT NOT NULL,
    read_by_json TEXT NOT NULL DEFAULT '[]'
);
CREATE INDEX IF NOT EXISTS idx_handoff_tasks_thread ON delegation_tasks(thread_key);
CREATE INDEX IF NOT EXISTS idx_handoff_messages_task ON handoff_messages(task_id, created_at);
"""


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class HandoffStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # db-writer: handoff_store: 委托任务 store（自建表 + 写入），登记于 State 契约
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def _task(self, task_id: str) -> dict:
        row = self.conn.execute("SELECT * FROM delegation_tasks WHERE task_id=?", (task_id,)).fetchone()
        if not row:
            raise KeyError(task_id)
        return dict(row)

    def create(self, task_id: str, thread_key: str, owner: str = "manager") -> dict:
        now = _now()
        self.conn.execute(
            "INSERT INTO delegation_tasks(task_id,thread_key,state,owner,lease_until,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
            (task_id, thread_key, "pending", owner, 0, now, now),
        )
        self.conn.commit()
        return self._task(task_id)

    def assign(self, task_id: str, worker: str, lease: int = 10) -> dict:
        task = self._task(task_id)
        if task["state"] in TERMINAL:
            raise ValueError("terminal task cannot be assigned")
        now = _now()
        self.conn.execute("UPDATE delegation_tasks SET state='working', owner=?, lease_until=?, updated_at=? WHERE task_id=?",
                          (worker, lease, now, task_id))
        self._append_handoff(task_id, task.get("owner"), worker, "assignment")
        self.conn.commit()
        return self._task(task_id)

    def complete(self, task_id: str) -> dict:
        self.conn.execute("UPDATE delegation_tasks SET state='completed', updated_at=? WHERE task_id=?", (_now(), task_id))
        self.conn.commit()
        return self._task(task_id)

    def followup(self, task_id: str, now: int = 0, actor: str = "") -> dict:
        task = self._task(task_id)
        if task["state"] in TERMINAL:
            if task.get("owner") and int(task.get("lease_until") or 0) >= now:
                return {"owner": task["owner"], "action": "lease_owner"}
            self.conn.execute("UPDATE delegation_tasks SET owner='manager', updated_at=? WHERE task_id=?", (_now(), task_id))
            self.conn.commit()
            return {"owner": "manager", "action": "handback_expired"}
        if task.get("owner"):
            return {"owner": task["owner"], "action": "direct"}
        self.conn.execute("UPDATE delegation_tasks SET owner='manager', updated_at=? WHERE task_id=?", (_now(), task_id))
        self.conn.commit()
        return {"owner": "manager", "action": "unowned_to_manager"}

    def handback(self, task_id: str, target_task: str, reason: str = "") -> dict:
        task = self._task(task_id)
        if task.get("handback_done"):
            return {"action": "duplicate_handback_rejected"}
        self.conn.execute("UPDATE delegation_tasks SET handback_done=1, owner='manager', updated_at=? WHERE task_id=?",
                          (_now(), task_id))
        self._append_handoff(task_id, task.get("owner"), "manager", "handback", target=target_task, reason=reason)
        self.conn.commit()
        return {"action": "handback_once", "target": target_task}

    def stop(self, task_id: str) -> dict:
        self.conn.execute("UPDATE delegation_tasks SET state='canceled', owner='human', updated_at=? WHERE task_id=?",
                          (_now(), task_id))
        self.conn.commit()
        return {"owner": "human", "state": "canceled"}

    def worker_died(self, task_id: str) -> dict:
        task = self._task(task_id)
        if task["state"] in TERMINAL:
            return {"action": "terminal_unchanged", "task_state": task["state"]}
        self.conn.execute("UPDATE delegation_tasks SET state='working', owner='manager', updated_at=? WHERE task_id=?",
                          (_now(), task_id))
        self._append_handoff(task_id, "worker", "manager", "recovery")
        self.conn.commit()
        return {"action": "recovery_note", "task_state": "working"}

    def reviewer_fail(self, task_id: str, rounds: int) -> dict:
        if rounds >= 3:
            self.conn.execute("UPDATE delegation_tasks SET state='blocked', owner='manager', updated_at=? WHERE task_id=?",
                              (_now(), task_id))
            self.conn.commit()
            return {"action": "handback_manager", "rounds": rounds}
        return {"action": "changes_requested", "rounds": rounds}

    def state(self, task_id: str) -> str:
        return self._task(task_id)["state"]

    def messages(self, task_id: str) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM handoff_messages WHERE task_id=? ORDER BY created_at", (task_id,)).fetchall()
        return [dict(r) for r in rows]

    def append_message(self, task_id: str, role: str, parts: list[dict], handoff_id: str = "") -> dict:
        message_id = f"M-{task_id}-{len(self.messages(task_id)) + 1}"
        self.conn.execute(
            "INSERT INTO handoff_messages(message_id,handoff_id,task_id,role,parts_json,created_at,read_by_json) VALUES(?,?,?,?,?,?,?)",
            (message_id, handoff_id, task_id, role, json.dumps(parts, ensure_ascii=False), _now(), "[]"),
        )
        self.conn.commit()
        return {"message_id": message_id, "task_id": task_id, "role": role}

    def _append_handoff(self, task_id: str, from_agent: Any, to_agent: str, kind: str, **extra: Any) -> None:
        handoff_id = f"H-{task_id}-{kind}-{int(time.time() * 1000)}"
        self.conn.execute(
            """INSERT INTO handoffs(handoff_id,task_id,parent_handoff_id,from_role,to_role,from_agent,to_agent,
               intent,artifacts_json,context_refs_json,expected_output,status,created_at)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (handoff_id, task_id, None, kind, kind, str(from_agent), to_agent, "", "[]", "[]", "", "done", _now()),
        )
