#!/usr/bin/env python3
"""Typed report/attention and batch decisions for Freely agents."""
from __future__ import annotations

import json
import sqlite3
import time
import uuid
from pathlib import Path

REPORT_STATES = {"progress", "waiting", "ready", "blocked", "failed", "dropped"}
DECISIONS = {"accept", "stop", "ignore", "unavailable"}
ATTENTION_KEYS = {"needed", "question", "target_role", "target_session", "human_action", "for_trigger_id"}

SCHEMA = """
CREATE TABLE IF NOT EXISTS agent_reports (
    report_id TEXT PRIMARY KEY, task_id TEXT NOT NULL, role TEXT NOT NULL,
    report_state TEXT NOT NULL, summary TEXT NOT NULL, next_action TEXT,
    attention_json TEXT, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS agent_decisions (
    decision_id TEXT PRIMARY KEY, trigger_id TEXT NOT NULL UNIQUE,
    decision TEXT NOT NULL, reason TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_agent_reports_task ON agent_reports(task_id, created_at);
"""


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def validate_attention(attention: dict | None) -> dict:
    if attention is None:
        return {"ok": True, "value": None}
    if not isinstance(attention, dict):
        return {"ok": False, "errors": ["attention must be an object"]}
    extra = set(attention) - ATTENTION_KEYS
    if extra:
        return {"ok": False, "errors": [f"unknown attention fields: {sorted(extra)}"]}
    needed = attention.get("needed")
    if not isinstance(needed, bool):
        return {"ok": False, "errors": ["attention.needed must be boolean"]}
    if not needed:
        if any(attention.get(k) for k in ATTENTION_KEYS - {"needed"}):
            return {"ok": False, "errors": ["attention.needed=false requires empty fields"]}
        return {"ok": True, "value": {"needed": False}}
    errors = []
    if not str(attention.get("question") or "").strip():
        errors.append("attention.question required")
    if not str(attention.get("target_role") or "").strip():
        errors.append("attention.target_role required")
    if errors:
        return {"ok": False, "errors": errors}
    return {"ok": True, "value": {k: attention.get(k) for k in ATTENTION_KEYS if k in attention}}


def validate_report(report: dict) -> dict:
    errors = []
    for key in ("task_id", "role", "report_state", "summary"):
        if not str(report.get(key) or "").strip():
            errors.append(f"{key} required")
    if report.get("report_state") not in REPORT_STATES:
        errors.append(f"invalid report_state: {report.get('report_state')}")
    att = validate_attention(report.get("attention"))
    if not att["ok"]:
        errors.extend(att["errors"])
    if errors:
        return {"ok": False, "errors": errors}
    return {"ok": True, "value": {
        "task_id": str(report["task_id"]), "role": str(report["role"]),
        "report_state": report["report_state"], "summary": str(report["summary"]),
        "next_action": str(report.get("next_action") or ""),
        "attention": att["value"],
    }}


class ReportStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # db-writer: agent_protocol: agent 协议 store（自建表 + 写入），登记于 State 契约
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def record(self, report: dict) -> dict:
        valid = validate_report(report)
        if not valid["ok"]:
            raise ValueError("; ".join(valid["errors"]))
        value = valid["value"]
        rid = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO agent_reports(report_id,task_id,role,report_state,summary,next_action,attention_json,created_at) VALUES(?,?,?,?,?,?,?,?)",
            (rid, value["task_id"], value["role"], value["report_state"], value["summary"],
             value["next_action"], json.dumps(value["attention"], ensure_ascii=False) if value["attention"] else None, _now()))
        self.conn.commit()
        return {"report_id": rid, **value}

    def list(self, task_id: str | None = None) -> list[dict]:
        if task_id:
            rows = self.conn.execute("SELECT * FROM agent_reports WHERE task_id=? ORDER BY created_at", (task_id,)).fetchall()
        else:
            rows = self.conn.execute("SELECT * FROM agent_reports ORDER BY created_at").fetchall()
        out = []
        for row in rows:
            item = dict(row)
            item["attention"] = json.loads(item.pop("attention_json")) if item.get("attention_json") else None
            out.append(item)
        return out


class DecisionStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # db-writer: agent_protocol: 第二入口（同一 store 的短连接），登记于 State 契约
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def record(self, trigger_id: str, decision: str, reason: str) -> int:
        if not trigger_id:
            raise ValueError("trigger_id required")
        if decision not in DECISIONS:
            raise ValueError(f"invalid decision: {decision}")
        if not str(reason or "").strip():
            raise ValueError("reason required")
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO agent_decisions(decision_id,trigger_id,decision,reason,created_at) VALUES(?,?,?,?,?)",
            (str(uuid.uuid4()), trigger_id, decision, reason, _now()))
        self.conn.commit()
        return cur.rowcount

    def list(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM agent_decisions ORDER BY created_at").fetchall()]
