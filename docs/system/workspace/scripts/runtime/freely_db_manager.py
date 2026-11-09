#!/usr/bin/env python3
"""freely_db_manager.py — Unified SQLite access daemon for Freely.

Single long-running process, single SQLite connection. All 40+ operations
across chats, sessions, a2a_tasks, task_mode_gate, and tool_failure_log
tables go through this daemon via Unix-domain-socket JSON-RPC.

Lifecycle:
  python3 freely_db_manager.py start --project <path> [--foreground]
  python3 freely_db_manager.py stop --project <path>
  python3 freely_db_manager.py status --project <path>
"""

import argparse
import fcntl
import hashlib
import json
import os
import re
import signal
import socket
import sqlite3
import sys
import time
import uuid
from datetime import datetime, timezone

# Import a2a_task parser for parse/extract (lazy-loaded at first use)
_task_parser = None

def _get_task_parser():
    global _task_parser
    if _task_parser is None:
        from a2a_task_parser import (
            extract_task_block, validate_task_json, normalize_fields, normalize_exit_kind
        )
        _task_parser = (extract_task_block, validate_task_json, normalize_fields, normalize_exit_kind)
    return _task_parser


# ── Path helpers ──────────────────────────────────────────────────────────

def _short_hash(project: str) -> str:
    return hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]


def _socket_path(project: str) -> str:
    return f"/tmp/freely-db-{_short_hash(project)}.sock"


def _pid_file(project: str) -> str:
    return f"/tmp/freely-db-{_short_hash(project)}.pid"


def _log_file(project: str) -> str:
    return os.path.join(project, ".freely", "run", "db-daemon.log")


# ── Timestamp helpers ─────────────────────────────────────────────────────

def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_timestamp() -> int:
    """Second-precision UTC timestamp: YYYYMMDDHHMMSS (14 digits).
    Fits in SQLite INTEGER (max 9.2e18). Single-writer daemon eliminates collisions.
    """
    return int(datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"))


def _bare_to_iso(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 14 and raw[8] == "T":
        return raw
    if len(raw) == 14 and raw.isdigit():
        return f"{raw[:8]}T{raw[8:]}Z"
    return raw


def _iso_to_bare(val: str) -> str:
    val = val.strip()
    if len(val) >= 14 and val[8] == "T":
        core = val[:8] + val[9:].replace("Z", "")
        return core
    return val


# ── Daemon ────────────────────────────────────────────────────────────────

class DbDaemon:
    def __init__(self, project: str):
        self.project = os.path.abspath(project)
        self.db_path = os.path.join(self.project, ".freely", "freely.db")
        self.socket_path = _socket_path(self.project)
        self.pid_file = _pid_file(self.project)
        self.log_path = _log_file(self.project)
        self.conn: sqlite3.Connection | None = None
        self.running = False
        self.requests_served = 0
        self.errors = 0
        self.uptime = 0.0

        # Per-second sequence counter for unique chat IDs
        self._chat_seq = 0
        self._chat_last_ts = 0

    def log(self, msg: str) -> None:
        ts = _now_utc()
        try:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            with open(self.log_path, "a") as f:
                f.write(f"[{ts}] {msg}\n")
        except OSError:
            pass

    def _open_db(self) -> None:
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=OFF")
        self.conn.execute("PRAGMA busy_timeout=5000")
        self.conn.row_factory = sqlite3.Row

    def _ensure_tables(self) -> None:
        c = self.conn

        # chats
        c.execute("""
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
                created_at TEXT NOT NULL DEFAULT '',
                conversation_id INTEGER DEFAULT 0
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_consumed ON chats(consumed)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_issue_id ON chats(issue_id)")
        try:
            c.execute("ALTER TABLE chats ADD COLUMN conversation_id INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass

        # sessions
        c.execute("""
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
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON sessions(session_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_project_status ON sessions(project, status)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_project_role_status ON sessions(project, role, status)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_parent ON sessions(parent_session_id)")

        # discussions
        c.execute("""
            CREATE TABLE IF NOT EXISTS discussions (
                session_id TEXT PRIMARY KEY,
                owner TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'active',
                platform_ids TEXT DEFAULT '{}',
                created_at TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL DEFAULT ''
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_discussions_status ON discussions(status)")

        # tool_switch_events
        c.execute("""
            CREATE TABLE IF NOT EXISTS tool_switch_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                trigger_error TEXT NOT NULL DEFAULT 'startup',
                old_tool TEXT NOT NULL DEFAULT '',
                old_session_id TEXT NOT NULL DEFAULT '',
                old_jsonl_path TEXT NOT NULL DEFAULT '',
                old_cycle_log TEXT NOT NULL DEFAULT '',
                new_tool TEXT NOT NULL DEFAULT '',
                new_session_id TEXT NOT NULL DEFAULT '',
                cross_tool INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'succeeded'
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_switch_status ON tool_switch_events(status)")

        # task_mode_gate
        c.execute("""
            CREATE TABLE IF NOT EXISTS task_mode_gate (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                mode TEXT NOT NULL DEFAULT 'wait',
                task_scan_id TEXT DEFAULT '',
                mode_just_switched INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL DEFAULT ''
            )
        """)
        # tool_failure_log — dead tool tracking for auto-switch
        c.execute("""
            CREATE TABLE IF NOT EXISTS tool_failure_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool TEXT NOT NULL,
                slot TEXT NOT NULL DEFAULT '',
                reason TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT ''
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_tool_failure_tool ON tool_failure_log(tool, slot)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_tool_failure_created ON tool_failure_log(created_at)")

        # a2a_tasks — A2A protocol Task storage (aligns with Google A2A spec + Freely extensions)
        c.execute("""
            CREATE TABLE IF NOT EXISTS a2a_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL DEFAULT '',
                description TEXT NOT NULL DEFAULT '',
                state TEXT NOT NULL DEFAULT 'submitted'
                    CHECK(state IN ('submitted','working','input-required','canceled','completed','failed')),
                agent_id TEXT NOT NULL DEFAULT '',
                skill TEXT NOT NULL DEFAULT '',
                session_id TEXT NOT NULL DEFAULT '',
                message TEXT NOT NULL DEFAULT '',
                -- Freely extension fields
                raw_key TEXT NOT NULL DEFAULT '',
                prompt_file TEXT NOT NULL DEFAULT '',
                worktree TEXT NOT NULL DEFAULT '',
                branch TEXT NOT NULL DEFAULT '',
                exit_kind TEXT NOT NULL DEFAULT '',
                reason TEXT NOT NULL DEFAULT '',
                progress TEXT NOT NULL DEFAULT '',
                next_action TEXT NOT NULL DEFAULT '',
                completion_summary TEXT NOT NULL DEFAULT '',
                evidence_paths TEXT NOT NULL DEFAULT '',
                worker_prompts_csv TEXT NOT NULL DEFAULT '',
                error TEXT NOT NULL DEFAULT '',
                -- Runtime tracking
                worker_pid TEXT NOT NULL DEFAULT '',
                -- delivery_status removed (SSE replaces polling-based delivery)
                -- Message history (A2A standard: array of {role,type,content})
                messages_json TEXT NOT NULL DEFAULT '[]',
                -- Lifecycle timestamps
                launched_at TEXT NOT NULL DEFAULT '',
                completed_at TEXT NOT NULL DEFAULT '',
                -- Standard timestamps
                created_at TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL DEFAULT ''
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_a2a_tasks_state ON a2a_tasks(state)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_a2a_tasks_agent ON a2a_tasks(agent_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_a2a_tasks_skill ON a2a_tasks(skill)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_a2a_tasks_worktree ON a2a_tasks(worktree)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_a2a_tasks_session ON a2a_tasks(session_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_a2a_tasks_raw_key ON a2a_tasks(raw_key)")

        # Schema migrations for a2a_tasks (Freely extensions)
        existing_cols = {row[1] for row in c.execute("PRAGMA table_info(a2a_tasks)")}
        for col_name, col_def in [
            ("raw_key", "TEXT NOT NULL DEFAULT ''"),
            ("worktree", "TEXT NOT NULL DEFAULT ''"),
            ("branch", "TEXT NOT NULL DEFAULT ''"),
            ("exit_kind", "TEXT NOT NULL DEFAULT ''"),
            ("reason", "TEXT NOT NULL DEFAULT ''"),
            ("progress", "TEXT NOT NULL DEFAULT ''"),
            ("next_action", "TEXT NOT NULL DEFAULT ''"),
            ("completion_summary", "TEXT NOT NULL DEFAULT ''"),
            ("evidence_paths", "TEXT NOT NULL DEFAULT ''"),
            ("error", "TEXT NOT NULL DEFAULT ''"),
            ("worker_pid", "TEXT NOT NULL DEFAULT ''"),
            ("messages_json", "TEXT NOT NULL DEFAULT '[]'"),
            ("launched_at", "TEXT NOT NULL DEFAULT ''"),
            ("completed_at", "TEXT NOT NULL DEFAULT ''"),
        ]:
            if col_name not in existing_cols:
                try:
                    c.execute(f"ALTER TABLE a2a_tasks ADD COLUMN {col_name} {col_def}")
                except Exception:
                    pass

        # agent_working — tracks which agent is on which worktree (replaces agent-id.env)
        c.execute("""
            CREATE TABLE IF NOT EXISTS agent_working (
                raw_key         TEXT PRIMARY KEY,
                worktree        TEXT NOT NULL DEFAULT '',
                branch          TEXT NOT NULL DEFAULT '',
                test_worktree   TEXT DEFAULT '',
                test_branch     TEXT DEFAULT '',
                slot            TEXT DEFAULT '',
                manager_id      TEXT DEFAULT NULL,
                worker_id       TEXT DEFAULT NULL,
                reviewer_id     TEXT DEFAULT NULL,
                created_at      TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_aw_worker ON agent_working(worker_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_aw_manager ON agent_working(manager_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_aw_reviewer ON agent_working(reviewer_id)")

        # reviews — persisted review verdicts per raw_key per stage (replaces in-memory-only)
        c.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_key TEXT NOT NULL,
                review_stage TEXT NOT NULL,
                verdict TEXT NOT NULL,
                reviewed_by TEXT NOT NULL DEFAULT '',
                reviewed_at TEXT NOT NULL DEFAULT (datetime('now')),
                findings TEXT DEFAULT '[]',
                UNIQUE(raw_key, review_stage)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_reviews_raw_key ON reviews(raw_key)")

        # Schema migration: review_stage for a2a_tasks
        try:
            c.execute("ALTER TABLE a2a_tasks ADD COLUMN review_stage TEXT DEFAULT ''")
        except Exception:
            pass

        self.conn.commit()
        self.log("all tables ensured")

    # ── Request dispatcher ────────────────────────────────────────────

    def dispatch(self, method: str, params: dict) -> dict:
        handler = HANDLERS.get(method)
        if handler is None:
            self.errors += 1
            raise ValueError(f"unknown method: {method}")
        try:
            return handler(self, params)
        except Exception:
            self.errors += 1
            raise

    # ── chat helpers ──────────────────────────────────────────────────

    def _generate_chat_id(self) -> int:
        """Generate chat PK with second precision + per-second sequence.
        Single-writer daemon: serial writes eliminate race-condition collisions.
        Sequence handles sub-second consecutive calls."""
        ts = _utc_timestamp()
        if ts == self._chat_last_ts:
            self._chat_seq += 1
            return ts + self._chat_seq
        self._chat_last_ts = ts
        self._chat_seq = 0
        return ts

    def _existing_daemon_alive(self) -> bool:
        """True when a live daemon already answers on our socket path."""
        if not os.path.exists(self.socket_path):
            return False
        probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        probe.settimeout(1.0)
        try:
            probe.connect(self.socket_path)
            return True
        except OSError:
            return False
        finally:
            probe.close()

    def _run_socket_server(self) -> None:
        # Never unlink a socket a live daemon is still serving: that single line
        # is how an orphan daemon took the whole project's DB offline.
        if self._existing_daemon_alive():
            self.log("a live db daemon already serves this project; refusing to bind")
            self.running = False
            return
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(self.socket_path)
        sock.listen(8)
        os.chmod(self.socket_path, 0o700)
        sock.settimeout(1.0)
        self.log(f"listening on {self.socket_path}")

        try:
            while self.running:
                try:
                    conn, _ = sock.accept()
                    self._handle_client(conn)
                except socket.timeout:
                    continue
                except OSError as e:
                    self.log(f"socket accept error: {e}")
                    continue
        finally:
            sock.close()
            if os.path.exists(self.socket_path):
                os.unlink(self.socket_path)

    def _handle_client(self, conn: socket.socket) -> None:
        try:
            conn.settimeout(30)
            data = b""
            while True:
                try:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    if b"\n" in data:
                        break
                except socket.timeout:
                    break
            if not data:
                return

            request = json.loads(data.decode().strip())
            method = request.get("method", "")
            params = request.get("params", {})
            req_id = request.get("id", 0)

            result = self.dispatch(method, params)
            self.requests_served += 1

            response = {"jsonrpc": "2.0", "id": req_id, "result": result}
            conn.sendall((json.dumps(response, default=str) + "\n").encode())
        except Exception as e:
            self.errors += 1
            error_resp = {
                "jsonrpc": "2.0",
                "id": request.get("id", 0) if "request" in dir() else 0,
                "error": {"code": -32000, "message": str(e)},
            }
            try:
                conn.sendall((json.dumps(error_resp) + "\n").encode())
            except OSError:
                pass
        finally:
            try:
                conn.close()
            except OSError:
                pass

    # ── Lifecycle ─────────────────────────────────────────────────────

    def start(self) -> None:
        try:
            self._open_db()
            self._ensure_tables()
            self.running = True
            self.uptime = time.time()
            self._run_socket_server()
        except Exception as e:
            import traceback
            self.log(f"FATAL: daemon crashed with {type(e).__name__}: {e}")
            self.log(traceback.format_exc())
            raise

    def stop(self) -> None:
        self.running = False
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
        self.log("daemon stopped")


# ── Method handlers ───────────────────────────────────────────────────────

HANDLERS = {}

def _h(method: str):
    """Decorator to register a handler."""
    def dec(fn):
        HANDLERS[method] = fn
        return fn
    return dec


# ── db.* ──────────────────────────────────────────────────────────────────

@_h("db.ping")
def h_db_ping(daemon: DbDaemon, params: dict) -> dict:
    return {"pong": True}


@_h("db.stats")
def h_db_stats(daemon: DbDaemon, params: dict) -> dict:
    return {
        "uptime": int(time.time() - daemon.uptime),
        "requests_served": daemon.requests_served,
        "errors": daemon.errors,
    }


# ── chat.* ────────────────────────────────────────────────────────────────

@_h("chat.add")
def h_chat_add(daemon: DbDaemon, params: dict) -> dict:
    chat_type = params["chat_type"]
    issue_id = params.get("issue_id", "pending")
    message = params["message"]
    author = params.get("author", "human")
    channel = params.get("channel", "chat")
    session_refs = params.get("session_refs", "[]")
    intake_id = params.get("intake_id", "")
    conversation_id = int(params.get("conversation_id", 0))

    for attempt in range(5):
        chat_id = daemon._generate_chat_id()
        try:
            daemon.conn.execute(
                "INSERT INTO chats (id, chat_type, issue_id, author, channel, "
                "message, consumed, session_refs, intake_id, created_at, conversation_id) "
                "VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?)",
                (chat_id, chat_type, issue_id, author, channel,
                 message, session_refs, intake_id, _now_utc(), conversation_id),
            )
            if chat_type == "chat-message" and conversation_id == 0:
                daemon.conn.execute(
                    "UPDATE chats SET conversation_id = ? WHERE id = ?",
                    (chat_id, chat_id),
                )
            daemon.conn.commit()
            return {"chat_id": _bare_to_iso(str(chat_id))}
        except sqlite3.IntegrityError:
            if attempt < 4:
                continue
            raise


@_h("chat.list")
def h_chat_list(daemon: DbDaemon, params: dict) -> dict:
    limit = int(params.get("limit", 50))
    rows = daemon.conn.execute(
        "SELECT * FROM chats WHERE consumed = 0 AND (conversation_id = 0 OR conversation_id IS NULL) "
        "ORDER BY id ASC LIMIT ?", (limit,)
    ).fetchall()
    return {"rows": [dict(r) for r in rows]}


@_h("chat.list-conversations")
def h_chat_list_conversations(daemon: DbDaemon, params: dict) -> dict:
    rows = daemon.conn.execute(
        "SELECT conversation_id, COUNT(*) as cnt, MIN(created_at) as first_at, MIN(id) as first_id "
        "FROM chats WHERE consumed = 0 AND conversation_id > 0 "
        "GROUP BY conversation_id ORDER BY MIN(id)"
    ).fetchall()
    return {"rows": [dict(r) for r in rows]}


@_h("chat.query-by-issue")
def h_chat_query_by_issue(daemon: DbDaemon, params: dict) -> dict:
    issue_id = params["issue_id"]
    consumed = params.get("consumed")
    if consumed is not None:
        rows = daemon.conn.execute(
            "SELECT * FROM chats WHERE issue_id = ? AND consumed = ? ORDER BY id ASC",
            (issue_id, int(consumed)),
        ).fetchall()
    else:
        rows = daemon.conn.execute(
            "SELECT * FROM chats WHERE issue_id = ? ORDER BY id ASC",
            (issue_id,),
        ).fetchall()
    return {"rows": [dict(r) for r in rows]}


@_h("chat.show")
def h_chat_show(daemon: DbDaemon, params: dict) -> dict:
    chat_id = params["chat_id"]
    chat_id_bare = int(_iso_to_bare(str(chat_id))) if not str(chat_id).isdigit() else int(chat_id)
    row = daemon.conn.execute(
        "SELECT * FROM chats WHERE id = ?", (chat_id_bare,)
    ).fetchone()
    if not row:
        alt = _bare_to_iso(str(chat_id)) if str(chat_id).isdigit() else _iso_to_bare(str(chat_id))
        try:
            row = daemon.conn.execute(
                "SELECT * FROM chats WHERE id = ?", (int(alt),)
            ).fetchone()
        except (ValueError, TypeError):
            pass
    if row:
        return {"found": True, "chat": dict(row)}
    return {"found": False}


@_h("chat.consume")
def h_chat_consume(daemon: DbDaemon, params: dict) -> dict:
    chat_id = params["chat_id"]
    materialized_as = params.get("materialized_as", "")
    bare = _iso_to_bare(str(chat_id))
    daemon.conn.execute(
        "UPDATE chats SET consumed = 1, materialized_as = ? WHERE id = ?",
        (materialized_as, int(bare) if bare.isdigit() else bare),
    )
    changed = daemon.conn.total_changes > 0
    daemon.conn.commit()
    return {"changed": changed}


@_h("chat.discard")
def h_chat_discard(daemon: DbDaemon, params: dict) -> dict:
    chat_id = params["chat_id"]
    bare = _iso_to_bare(str(chat_id))
    daemon.conn.execute(
        "UPDATE chats SET consumed = -1 WHERE id = ?",
        (int(bare) if bare.isdigit() else bare,),
    )
    changed = daemon.conn.total_changes > 0
    daemon.conn.commit()
    return {"changed": changed}


@_h("chat.reset")
def h_chat_reset(daemon: DbDaemon, params: dict) -> dict:
    chat_id = params["chat_id"]
    bare = _iso_to_bare(str(chat_id))
    daemon.conn.execute(
        "UPDATE chats SET consumed = 0 WHERE id = ?",
        (int(bare) if bare.isdigit() else bare,),
    )
    changed = daemon.conn.total_changes > 0
    daemon.conn.commit()
    return {"changed": changed}


    return {"changed": changed}


@_h("chat.update-conversation-id")
def h_chat_update_conversation_id(daemon: DbDaemon, params: dict) -> dict:
    chat_id = params["chat_id"]
    conv_id = int(params["conversation_id"])
    bare = _iso_to_bare(str(chat_id))
    daemon.conn.execute(
        "UPDATE chats SET conversation_id = ? WHERE id = ?",
        (conv_id, int(bare) if bare.isdigit() else bare),
    )
    changed = daemon.conn.total_changes > 0
    daemon.conn.commit()
    return {"changed": changed}


@_h("chat.query-active-conversation")
def h_chat_query_active_conversation(daemon: DbDaemon, params: dict) -> dict:
    row = daemon.conn.execute(
        "SELECT conversation_id FROM chats WHERE chat_type = 'chat-message' "
        "AND consumed = 0 AND conversation_id > 0 ORDER BY id DESC LIMIT 1"
    ).fetchone()
    return {"conversation_id": row[0] if row else None}


@_h("chat.conversation-messages")
def h_chat_conversation_messages(daemon: DbDaemon, params: dict) -> dict:
    conv_id = int(params["conversation_id"])
    rows = daemon.conn.execute(
        "SELECT * FROM chats WHERE conversation_id = ? AND consumed = 0 ORDER BY id ASC",
        (conv_id,),
    ).fetchall()
    return {"rows": [dict(r) for r in rows]}


@_h("chat.consume-conversation")
def h_chat_consume_conversation(daemon: DbDaemon, params: dict) -> dict:
    conv_id = int(params["conversation_id"])
    action = params["action"]
    target_dir = params.get("target", "")
    rows = daemon.conn.execute(
        "SELECT * FROM chats WHERE conversation_id = ? AND consumed = 0 ORDER BY id ASC",
        (conv_id,),
    ).fetchall()
    if not rows:
        return {"count": 0}

    messages = [dict(r) for r in rows]
    count = 0
    now = _now_utc()


    if action == "materialize-all-as-comment" and target_dir:
        for m in messages:
            author = m.get("author", "human")
            channel = m.get("channel", "chat")
            created_at = m.get("created_at", now)
            msg = m.get("message", "")
            comment_id = f"comment-{created_at.replace(':', '').replace('-', '')}"
            os.makedirs(os.path.dirname(target_dir), exist_ok=True)
            with open(target_dir, "a", encoding="utf-8") as f:
                f.write(f"\n### {comment_id}\n{{source: chat, author: {author}, channel: {channel}}}\n\n{msg}\n")
            daemon.conn.execute("UPDATE chats SET consumed = 1 WHERE id = ?", (m["id"],))
            count += 1

    daemon.conn.commit()
    return {"count": count}


# ── discuss.* ─────────────────────────────────────────────────────────────

@_h("discuss.create")
def h_discuss_create(daemon: DbDaemon, params: dict) -> dict:
	session_id = params["session_id"]
	owner = params.get("owner", "")
	now = _now_utc()
	daemon.conn.execute(
		"INSERT INTO discussions (session_id, owner, status, platform_ids, created_at, updated_at) "
		"VALUES (?, ?, 'active', '{}', ?, ?)",
		(session_id, owner, now, now),
	)
	daemon.conn.commit()
	return {"session_id": session_id, "ok": True}


@_h("discuss.update-status")
def h_discuss_update_status(daemon: DbDaemon, params: dict) -> dict:
	session_id = params["session_id"]
	status = params.get("status", "closed")
	platform_ids = params.get("platform_ids", "")
	now = _now_utc()
	if platform_ids:
		daemon.conn.execute(
			"UPDATE discussions SET status=?, platform_ids=?, updated_at=? WHERE session_id=?",
			(status, platform_ids, now, session_id),
		)
	else:
		daemon.conn.execute(
			"UPDATE discussions SET status=?, updated_at=? WHERE session_id=?",
			(status, now, session_id),
		)
	daemon.conn.commit()
	return {"session_id": session_id, "status": status, "ok": True}


@_h("discuss.get")
def h_discuss_get(daemon: DbDaemon, params: dict) -> dict:
	session_id = params["session_id"]
	row = daemon.conn.execute(
		"SELECT session_id, owner, status, platform_ids, created_at, updated_at "
		"FROM discussions WHERE session_id=?",
		(session_id,),
	).fetchone()
	if not row:
		return {}
	return {
		"session_id": row[0], "owner": row[1], "status": row[2],
		"platform_ids": row[3], "created_at": row[4], "updated_at": row[5],
	}


@_h("discuss.list-active")
def h_discuss_list_active(daemon: DbDaemon, params: dict) -> dict:
	rows = daemon.conn.execute(
		"SELECT session_id, owner, status, created_at FROM discussions "
		"WHERE status='active' ORDER BY created_at DESC"
	).fetchall()
	return {"sessions": [{"session_id": r[0], "owner": r[1], "status": r[2], "created_at": r[3]} for r in rows]}


@_h("chat.count-comments-for-key")
def h_chat_count_comments(daemon: DbDaemon, params: dict) -> dict:
    key = params["key"]
    row = daemon.conn.execute(
        "SELECT COUNT(*) FROM chats WHERE consumed = 0 AND chat_type = 'comment' "
        "AND (issue_id = ? OR issue_id LIKE ?)", (key, f"{key}%")
    ).fetchone()
    return {"count": row[0]}



# ── session.* ─────────────────────────────────────────────────────────────

@_h("session.upsert")
def h_session_upsert(daemon: DbDaemon, params: dict) -> dict:
    session_id = params["session_id"]
    project = params.get("project", daemon.project)
    tool = params["tool"]
    role = params.get("role", "manager")
    parent_session_id = params.get("parent_session_id", "")
    launch_kind = params.get("launch_kind", "fresh")
    tool_adapter = params.get("tool_adapter", "direct")
    resume_mode = params.get("resume_mode", "")
    error_reason = params.get("error_reason", "")
    metadata_json = params.get("metadata_json", "{}")
    now = _now_utc()

    existing = daemon.conn.execute(
        "SELECT session_id FROM sessions WHERE session_id = ?", (session_id,)
    ).fetchone()

    if existing:
        daemon.conn.execute(
            "UPDATE sessions SET project=?, tool=?, role=?, parent_session_id=?, "
            "launch_kind=?, tool_adapter=?, resume_mode=?, status='active', "
            "error_reason=?, metadata_json=?, updated_at=? WHERE session_id=?",
            (project, tool, role, parent_session_id, launch_kind, tool_adapter,
             resume_mode, error_reason, metadata_json, now, session_id),
        )
    else:
        daemon.conn.execute(
            "INSERT INTO sessions (session_id, project, tool, role, parent_session_id, "
            "launch_kind, tool_adapter, resume_mode, status, error_reason, metadata_json, "
            "created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,'active',?,?,?,?)",
            (session_id, project, tool, role, parent_session_id, launch_kind,
             tool_adapter, resume_mode, error_reason, metadata_json, now, now),
        )
    daemon.conn.commit()
    return {"session_id": session_id}


@_h("session.get-active")
def h_session_get_active(daemon: DbDaemon, params: dict) -> dict:
    project = params.get("project", daemon.project)
    role = params.get("role", "manager")
    tool_like = params.get("tool_like", "")
    if tool_like:
        row = daemon.conn.execute(
            "SELECT session_id FROM sessions WHERE project=? AND role=? AND status='active' "
            "AND tool LIKE ? ORDER BY updated_at DESC LIMIT 1",
            (project, role, tool_like)
        ).fetchone()
    else:
        row = daemon.conn.execute(
            "SELECT session_id FROM sessions WHERE project=? AND role=? AND status='active' "
            "ORDER BY updated_at DESC LIMIT 1", (project, role)
        ).fetchone()
    return {"session_id": row[0] if row else None}


@_h("session.get-parent")
def h_session_get_parent(daemon: DbDaemon, params: dict) -> dict:
    row = daemon.conn.execute(
        "SELECT parent_session_id FROM sessions WHERE session_id=?",
        (params["session_id"],)
    ).fetchone()
    return {"parent_session_id": row[0] if row and row[0] else None}


@_h("session.show")
def h_session_show(daemon: DbDaemon, params: dict) -> dict:
    row = daemon.conn.execute(
        "SELECT * FROM sessions WHERE session_id=?", (params["session_id"],)
    ).fetchone()
    if row:
        return {"found": True, "session": dict(row)}
    return {"found": False}


@_h("session.complete")
def h_session_complete(daemon: DbDaemon, params: dict) -> dict:
    status = params.get("status", "completed")
    error_reason = params.get("error_reason", "")
    daemon.conn.execute(
        "UPDATE sessions SET status=?, error_reason=?, updated_at=? WHERE session_id=?",
        (status, error_reason, _now_utc(), params["session_id"]),
    )
    changed = daemon.conn.total_changes > 0
    daemon.conn.commit()
    return {"changed": changed}


@_h("session.list")
def h_session_list(daemon: DbDaemon, params: dict) -> dict:
    project = params.get("project", daemon.project)
    status = params.get("status")
    role = params.get("role")
    if status and role:
        rows = daemon.conn.execute(
            "SELECT * FROM sessions WHERE project=? AND status=? AND role=? ORDER BY updated_at DESC",
            (project, status, role),
        ).fetchall()
    elif status:
        rows = daemon.conn.execute(
            "SELECT * FROM sessions WHERE project=? AND status=? ORDER BY updated_at DESC",
            (project, status),
        ).fetchall()
    elif role:
        rows = daemon.conn.execute(
            "SELECT * FROM sessions WHERE project=? AND role=? ORDER BY updated_at DESC",
            (project, role),
        ).fetchall()
    else:
        rows = daemon.conn.execute(
            "SELECT * FROM sessions WHERE project=? ORDER BY updated_at DESC",
            (project,),
        ).fetchall()
    return {"rows": [dict(r) for r in rows]}


@_h("session.list-children")
def h_session_list_children(daemon: DbDaemon, params: dict) -> dict:
    rows = daemon.conn.execute(
        "SELECT * FROM sessions WHERE parent_session_id=? ORDER BY updated_at DESC",
        (params["parent_session_id"],),
    ).fetchall()
    return {"rows": [dict(r) for r in rows]}


@_h("session.count-active")
def h_session_count_active(daemon: DbDaemon, params: dict) -> dict:
    project = params.get("project", daemon.project)
    row = daemon.conn.execute(
        "SELECT COUNT(*) FROM sessions WHERE project=? AND status='active'",
        (project,),
    ).fetchone()
    return {"count": row[0]}


@_h("session.tool-switch-read")
def h_session_tool_switch_read(daemon: DbDaemon, params: dict) -> dict:
    row = daemon.conn.execute(
        "SELECT * FROM tool_switch_events WHERE status='succeeded' ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if row is None:
        return {"found": False}
    return {"found": True, "record": dict(row)}


@_h("session.tool-switch-write")
def h_session_tool_switch_write(daemon: DbDaemon, params: dict) -> dict:
    trigger_error = params.get("trigger_error", "startup")
    old_tool = params.get("old_tool", "")
    old_session_id = params.get("old_session_id", "")
    old_jsonl_path = params.get("old_jsonl_path", "")
    old_cycle_log = params.get("old_cycle_log", "")
    new_tool = params.get("new_tool", "")
    new_session_id = params.get("new_session_id", "")

    cross_tool = 0
    if old_tool and new_tool:
        base_old = old_tool.split("-")[0] if "-" in old_tool else old_tool
        base_new = new_tool.split("-")[0] if "-" in new_tool else new_tool
        cross_tool = 1 if base_old != base_new else 0

    daemon.conn.execute("UPDATE tool_switch_events SET status='stale' WHERE status!='stale'")
    daemon.conn.execute(
        "INSERT INTO tool_switch_events (trigger_error, old_tool, old_session_id, "
        "old_jsonl_path, old_cycle_log, new_tool, new_session_id, cross_tool, status) "
        "VALUES (?,?,?,?,?,?,?,?,'succeeded')",
        (trigger_error, old_tool, old_session_id, old_jsonl_path, old_cycle_log,
         new_tool, new_session_id, cross_tool),
    )
    daemon.conn.commit()
    return {"ok": True}


@_h("session.tool-switch-update-sid")
def h_session_tool_switch_update_sid(daemon: DbDaemon, params: dict) -> dict:
    daemon.conn.execute(
        "UPDATE tool_switch_events SET new_session_id=? "
        "WHERE status='succeeded' AND id=(SELECT MAX(id) FROM tool_switch_events WHERE status='succeeded')",
        (params["new_session_id"],),
    )
    changed = daemon.conn.total_changes > 0
    daemon.conn.commit()
    return {"changed": changed}


# ── task-mode.* ───────────────────────────────────────────────────────────

@_h("task-mode.init")
def h_task_mode_init(daemon: DbDaemon, params: dict) -> dict:
    default = params.get("default", "wait")
    row = daemon.conn.execute("SELECT COUNT(*) FROM task_mode_gate").fetchone()
    if row[0] == 0:
        daemon.conn.execute(
            "INSERT INTO task_mode_gate (id, mode, task_scan_id, updated_at) "
            "VALUES (1, ?, '', datetime('now'))", (default,)
        )
        daemon.conn.commit()
    return {"ok": True}


@_h("task-mode.read")
def h_task_mode_read(daemon: DbDaemon, params: dict) -> dict:
    row = daemon.conn.execute(
        "SELECT mode FROM task_mode_gate WHERE id=1"
    ).fetchone()
    mode = row[0] if row else "wait"
    return {"mode": mode}


@_h("task-mode.read-with-scan")
def h_task_mode_read_with_scan(daemon: DbDaemon, params: dict) -> dict:
    row = daemon.conn.execute(
        "SELECT mode, task_scan_id FROM task_mode_gate WHERE id=1"
    ).fetchone()
    if row:
        return {"mode": row[0], "task_scan_id": row[1] or ""}
    return {"mode": "wait", "task_scan_id": ""}


@_h("task-mode.write")
def h_task_mode_write(daemon: DbDaemon, params: dict) -> dict:
    mode = params["mode"]
    scan_id = params.get("scan_id", "")
    now = _now_utc()
    daemon.conn.execute(
        "INSERT OR REPLACE INTO task_mode_gate (id, mode, task_scan_id, mode_just_switched, updated_at) "
        "VALUES (1, ?, ?, 1, ?)", (mode, scan_id, now)
    )
    daemon.conn.commit()
    return {"ok": True}


@_h("task-mode.read-just-switched")
def h_task_mode_read_just_switched(daemon: DbDaemon, params: dict) -> dict:
    row = daemon.conn.execute(
        "SELECT mode_just_switched FROM task_mode_gate WHERE id=1"
    ).fetchone()
    val = row[0] if row else 0
    daemon.conn.execute(
        "UPDATE task_mode_gate SET mode_just_switched=0 WHERE id=1 AND mode_just_switched=1"
    )
    daemon.conn.commit()
    return {"just_switched": val}


# ── tool.failure-log ──────────────────────────────────────────────────────

@_h("tool.failure-add")
def h_tool_failure_add(daemon: DbDaemon, params: dict) -> dict:
    """Record a tool failure."""
    daemon.conn.execute(
        "INSERT INTO tool_failure_log (tool, slot, reason, created_at) VALUES (?, ?, ?, ?)",
        (params["tool"], params.get("slot", ""), params.get("reason", ""), _now_utc()),
    )
    daemon.conn.commit()
    return {"ok": True}


@_h("tool.failure-count")
def h_tool_failure_count(daemon: DbDaemon, params: dict) -> dict:
    """Count failures for a tool+slot in the last N seconds."""
    window = int(params.get("window_secs", 3600))
    cutoff = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")  # approximate
    row = daemon.conn.execute(
        "SELECT COUNT(*) FROM tool_failure_log WHERE tool=? AND slot=? "
        "AND datetime(created_at) > datetime('now', ? || ' seconds')",
        (params["tool"], params.get("slot", ""), f"-{window}"),
    ).fetchone()
    return {"count": row[0]}


@_h("tool.failure-clear")
def h_tool_failure_clear(daemon: DbDaemon, params: dict) -> dict:
    """Clear all failures for a tool+slot (resurrection)."""
    daemon.conn.execute(
        "DELETE FROM tool_failure_log WHERE tool=? AND slot=?",
        (params["tool"], params.get("slot", "")),
    )
    daemon.conn.commit()
    return {"ok": True}


@_h("tool.failure-list-dead")
def h_tool_failure_list_dead(daemon: DbDaemon, params: dict) -> dict:
    """List tools that have >= threshold failures in the window."""
    window = int(params.get("window_secs", 3600))
    threshold = int(params.get("threshold", 3))
    rows = daemon.conn.execute(
        "SELECT tool, slot, COUNT(*) as cnt FROM tool_failure_log "
        "WHERE datetime(created_at) > datetime('now', ? || ' seconds') "
        "GROUP BY tool, slot HAVING cnt >= ?",
        (f"-{window}", threshold),
    ).fetchall()
    return {"tools": [{"tool": r[0], "slot": r[1], "count": r[2]} for r in rows]}



# ── a2a_task.* ──────────────────────────────────────────────────────────────

@_h("a2a_task.insert")
def h_a2a_task_insert(daemon: DbDaemon, params: dict) -> dict:
    """Insert a new A2A Task (with Freely extension fields)."""
    now = _now_utc()
    task_id = params.get("task_id", str(uuid.uuid4()))
    # ── L2: DB-layer validation for worker tasks ──
    _agent_id = params.get("agent_id", "")
    if _agent_id.startswith("worker"):
        _wt = (params.get("worktree", "") or "").strip()
        _br = (params.get("branch", "") or "").strip()
        _rk = (params.get("raw_key", "") or "").strip()
        _msg = (params.get("message", "") or "").strip()
        if not _wt or not _br or not _rk or not _msg:
            return {"error": f"worker task rejected: missing fields (worktree={bool(_wt)} branch={bool(_br)} raw_key={bool(_rk)} message={bool(_msg)})"}
    c = daemon.conn.execute(
        """INSERT INTO a2a_tasks
           (task_id, name, description, state, agent_id, skill, session_id, message,
            created_at, updated_at, prompt_file, worktree, branch, exit_kind, reason,
            progress, next_action, completion_summary, evidence_paths, error)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            task_id,
            params.get("name", ""),
            params.get("description", ""),
            params.get("state", "submitted"),
            params.get("agent_id", ""),
            params.get("skill", ""),
            params.get("session_id", ""),
            params.get("message", ""),
            now,
            now,
            params.get("prompt_file", ""),
            params.get("worktree", ""),
            params.get("branch", ""),
            params.get("exit_kind", ""),
            params.get("reason", ""),
            params.get("progress", ""),
            params.get("next_action", ""),
            params.get("completion_summary", ""),
            params.get("evidence_paths", ""),
            params.get("error", ""),
        ),
    )
    daemon.conn.commit()
    return {"task_id": task_id, "affected": 1}


@_h("a2a_task.get")
def h_a2a_task_get(daemon: DbDaemon, params: dict) -> dict:
    """Get a single A2A Task by task_id."""
    row = daemon.conn.execute(
        "SELECT * FROM a2a_tasks WHERE task_id = ?", (params["task_id"],)
    ).fetchone()
    if not row:
        return {"record": None}
    cols = [desc[1] for desc in daemon.conn.execute("PRAGMA table_info(a2a_tasks)").fetchall()]
    return {"record": dict(zip(cols, row))}


@_h("a2a_task.update")
def h_a2a_task_update(daemon: DbDaemon, params: dict) -> dict:
    """Update A2A Task fields (excluding id/created_at)."""
    task_id = params.pop("task_id")
    params.pop("updated_at", None)  # Handled by caller or use _now_utc()
    if not params:
        return {"affected": 0}
    now = _now_utc()
    set_cols = ", ".join(f"{k} = ?" for k in params.keys())
    c = daemon.conn.execute(
        f"UPDATE a2a_tasks SET {set_cols}, updated_at = ? WHERE task_id = ?",
        list(params.values()) + [now, task_id],
    )
    daemon.conn.commit()
    return {"affected": c.rowcount}


@_h("a2a_task.delete")
def h_a2a_task_delete(daemon: DbDaemon, params: dict) -> dict:
    """Delete an A2A Task."""
    c = daemon.conn.execute(
        "DELETE FROM a2a_tasks WHERE task_id = ?", (params["task_id"],)
    )
    daemon.conn.commit()
    return {"affected": c.rowcount}


@_h("a2a_task.list")
def h_a2a_task_list(daemon: DbDaemon, params: dict) -> dict:
    """List all A2A Tasks, optionally filtered by state/agent_id/skill."""
    sql = "SELECT * FROM a2a_tasks"
    filters = []
    vals = []
    if "state" in params and params["state"]:
        filters.append("state = ?")
        vals.append(params["state"])
    if "agent_id" in params and params["agent_id"]:
        _aid = params["agent_id"]
        # Role string (no _NN suffix) → prefix match; instance ID → exact match
        if re.match(r'^(manager|worker|reviewer)$', _aid):
            filters.append("agent_id LIKE ?")
            vals.append(f"{_aid}_%")
        else:
            filters.append("agent_id = ?")
            vals.append(_aid)
    if "skill" in params and params["skill"]:
        filters.append("skill = ?")
        vals.append(params["skill"])
    if filters:
        sql += " WHERE " + " AND ".join(filters)
    sql += " ORDER BY created_at DESC"
    rows = daemon.conn.execute(sql, vals).fetchall()
    cols = [desc[1] for desc in daemon.conn.execute("PRAGMA table_info(a2a_tasks)").fetchall()]
    return {"rows": [dict(zip(cols, r)) for r in rows]}


@_h("a2a_task.list-by-worktree")
def h_a2a_task_list_by_worktree(daemon: DbDaemon, params: dict) -> dict:
    """List A2A Tasks by worktree, optionally filtered by state."""
    sql = "SELECT * FROM a2a_tasks WHERE worktree = ?"
    vals = [params["worktree"]]
    if "state" in params and params["state"]:
        sql += " AND state = ?"
        vals.append(params["state"])
    sql += " ORDER BY created_at DESC"
    rows = daemon.conn.execute(sql, vals).fetchall()
    cols = [desc[1] for desc in daemon.conn.execute("PRAGMA table_info(a2a_tasks)").fetchall()]
    return {"rows": [dict(zip(cols, r)) for r in rows]}



@_h("a2a_task.list-by-raw-key")
def h_a2a_task_list_by_raw_key(daemon: DbDaemon, params: dict) -> dict:
    """List A2A Tasks by raw_key, ordered by created_at DESC."""
    rows = daemon.conn.execute(
        "SELECT * FROM a2a_tasks WHERE raw_key = ? ORDER BY created_at DESC",
        (params["raw_key"],),
    ).fetchall()
    cols = [desc[1] for desc in daemon.conn.execute("PRAGMA table_info(a2a_tasks)").fetchall()]
    return {"rows": [dict(zip(cols, r)) for r in rows]}


@_h("a2a_task.list-active")
def h_a2a_task_list_active(daemon: DbDaemon, params: dict) -> dict:
    """List A2A Tasks in active states (submitted, working, input-required)."""
    rows = daemon.conn.execute(
        "SELECT * FROM a2a_tasks WHERE state IN ('submitted','working','input-required') ORDER BY updated_at DESC"
    ).fetchall()
    cols = [desc[1] for desc in daemon.conn.execute("PRAGMA table_info(a2a_tasks)").fetchall()]
    return {"rows": [dict(zip(cols, r)) for r in rows]}


@_h("a2a_task.latest-manager")
def h_a2a_task_latest_manager(daemon: DbDaemon, params: dict) -> dict:
    """Get latest manager task (agent_id starts with 'manager')."""
    rows = daemon.conn.execute(
        "SELECT * FROM a2a_tasks WHERE agent_id LIKE 'manager%' ORDER BY created_at DESC LIMIT 1"
    ).fetchall()
    cols = [desc[1] for desc in daemon.conn.execute("PRAGMA table_info(a2a_tasks)").fetchall()]
    return {"rows": [dict(zip(cols, r)) for r in rows]}


# ── Valid roles for A2A messages ────────────────────────────────────────
_A2A_VALID_ROLES = {"manager", "worker", "reviewer"}

@_h("a2a_task.update-message")
def h_a2a_task_update_message(daemon: DbDaemon, params: dict) -> dict:
    """Append a message to messages_json and update state + message fields.

    Validation (SQLite layer gate):
    - content must be non-empty
    - role must be valid (manager/worker/reviewer)
    - task must exist

    On validation failure, returns structured error with fix_hint and example
    so the AI caller can reorganize its data and re-submit correctly.
    """
    task_id = params.get("task_id", "")
    msg_role = params.get("role", "worker")
    msg_type = params.get("type", "text")
    msg_content = params.get("content", "")

    # ── Gate 1: content must be non-empty ──
    if not msg_content or not msg_content.strip():
        return {
            "valid": False,
            "affected": 0,
            "error": "消息内容不能为空 (content must not be empty)",
            "fix_hint": (
                "请重新组织你的消息数据再写入，不要重试同样的空内容。"
                "确保 'content' 字段包含有效的消息正文，至少 1 个字符。"
            ),
            "example": {
                "role": msg_role,
                "type": msg_type,
                "content": "你的具体消息内容写在这里，说明你想告诉对方什么",
            },
        }

    # ── Gate 2: role must be valid ──
    if msg_role not in _A2A_VALID_ROLES:
        return {
            "valid": False,
            "affected": 0,
            "error": f"无效的角色 '{msg_role}'，合法值: {', '.join(sorted(_A2A_VALID_ROLES))}",
            "fix_hint": (
                f"角色 '{msg_role}' 不在合法范围内。"
                f"请将 'role' 字段改为以下之一: {', '.join(sorted(_A2A_VALID_ROLES))}。"
                f"例如 manager 给 worker 发消息时 role='worker'，worker 回复时 role='manager'。"
            ),
            "example": {"role": "manager", "type": "text", "content": "..."},
        }

    # ── Gate 3: task must exist ──
    row = daemon.conn.execute(
        "SELECT messages_json FROM a2a_tasks WHERE task_id = ?", (task_id,)
    ).fetchone()
    if not row:
        return {
            "valid": False,
            "affected": 0,
            "error": f"任务 {task_id[:24]}... 不存在，无法写入消息",
            "fix_hint": (
                "请先确认 task_id 是否正确。用 a2a_task.py list 查看当前所有任务。"
                "如果任务已被删除或从未创建，需要先 a2a-exit --state submitted 创建新任务。"
            ),
        }

    import json as _json
    messages = _json.loads(row[0] or "[]")
    messages.append({
        "role": msg_role,
        "type": msg_type,
        "content": msg_content,
        "timestamp": _now_utc(),
    })

    now = _now_utc()
    daemon.conn.execute(
        "UPDATE a2a_tasks SET message = ?, messages_json = ?, updated_at = ? WHERE task_id = ?",
        (msg_content, _json.dumps(messages, ensure_ascii=False), now, task_id),
    )
    daemon.conn.commit()
    return {"valid": True, "affected": 1}


@_h("a2a_task.update-worker-pid")
def h_a2a_task_update_worker_pid(daemon: DbDaemon, params: dict) -> dict:
    """Record worker PID for process health checks."""
    daemon.conn.execute(
        "UPDATE a2a_tasks SET worker_pid = ?, updated_at = ? WHERE task_id = ?",
        (params["worker_pid"], _now_utc(), params["task_id"]),
    )
    daemon.conn.commit()
    return {"affected": daemon.conn.total_changes}


@_h("a2a_task.get-launched-pids")
def h_a2a_task_get_launched_pids(daemon: DbDaemon, params: dict) -> dict:
    """Get task_id + worker_pid for launched workers, optionally filtered by raw_key."""
    raw_key = params.get("raw_key", "")
    if raw_key:
        rows = daemon.conn.execute(
            "SELECT task_id, worker_pid, worktree FROM a2a_tasks "
            "WHERE (agent_id LIKE 'worker_%' OR agent_id = 'worker') AND state = 'working' AND raw_key = ? AND worker_pid != ''",
            (raw_key,),
        ).fetchall()
    else:
        rows = daemon.conn.execute(
            "SELECT task_id, worker_pid, worktree FROM a2a_tasks "
            "WHERE (agent_id LIKE 'worker_%' OR agent_id = 'worker') AND state = 'working' AND worker_pid != ''"
        ).fetchall()
    cols = ["task_id", "worker_pid", "worktree"]
    return {"rows": [dict(zip(cols, r)) for r in rows]}


# delivery_status RPC handlers removed — SSE replaces polling-based delivery

# ── agent_working.* handlers ──────────────────────────────────────────

def _aw_canon_raw_key(raw_key: str) -> str:
    """Normalize raw_key for all agent_working handlers (shared boundary)."""
    try:
        from raw_key_canon import canonicalize_raw_key
        return canonicalize_raw_key(raw_key)
    except Exception as exc:
        raise ValueError(f"invalid raw_key: {raw_key!r}") from exc


from agent_identity_value import (
    agent_ids as _aw_agent_ids,
    first_agent_id as _aw_first_agent_id,
    format_agent_entries as _aw_format_agent_entries,
    parse_agent_entries as _aw_parse_agent_entries,
)


@_h("agent_working.upsert")
def h_aw_upsert(daemon: DbDaemon, params: dict) -> dict:
    """agent_assign: INSERT or UPDATE agent_working row.

    For reviewer_id column: APPENDS new pairs (comma-separated) instead
    of overwriting. Multiple reviewers can review the same raw_key.
    For other columns (worker_id, manager_id): overwrites (one per raw_key).
    """
    raw_key = _aw_canon_raw_key(params["raw_key"])
    col = params["col"]; val = params["val"]
    # Defense-in-depth: validate col matches expected {role}_id pattern
    import re as _re
    if not _re.match(r'^(manager|worker|reviewer)_id$', col):
        return {"status": "error", "message": f"invalid column: {col}"}
    c = daemon.conn
    row = c.execute("SELECT * FROM agent_working WHERE raw_key = ?", (raw_key,)).fetchone()
    if row:
        if col == "reviewer_id" and row[col]:
            # Append new reviewer pair (comma-separated). Update existing pair
            # if same agent_id already present, otherwise append.
            existing = _aw_parse_agent_entries(row[col] or "")
            existing.update(_aw_parse_agent_entries(val))
            val = _aw_format_agent_entries(existing)
        slot_val = params.get("slot","")
        if slot_val:
            c.execute(f"UPDATE agent_working SET {col}=?, slot=?, updated_at=datetime('now') WHERE raw_key=?",
                      (val, slot_val, raw_key))
        else:
            c.execute(f"UPDATE agent_working SET {col}=?, updated_at=datetime('now') WHERE raw_key=?",
                      (val, raw_key))
    else:
        c.execute(
            "INSERT INTO agent_working (raw_key, worktree, branch, test_worktree, test_branch, slot, {col}) "
            "VALUES (?,?,?,?,?,?,?)".format(col=col),
            (raw_key, params.get("worktree",""), params.get("branch",""),
             params.get("test_worktree",""), params.get("test_branch",""),
             params.get("slot",""), val))
    daemon.conn.commit()
    return {"status": "ok"}


@_h("agent_working.upsert_only")
def h_aw_upsert_only(daemon: DbDaemon, params: dict) -> dict:
    """Reviewer-only: UPDATE existing row. Fails if row doesn't exist.

    Reviewer must never create a new agent_working row — the row is
    created by Worker (UPSERT). If the row doesn't exist, the worktree
    was already wt-closed or there's a bug.
    """
    raw_key = _aw_canon_raw_key(params["raw_key"])
    col = params["col"]; val = params["val"]
    import re as _re
    if not _re.match(r'^(manager|worker|reviewer)_id$', col):
        return {"status": "error", "message": f"invalid column: {col}"}
    c = daemon.conn
    row = c.execute("SELECT * FROM agent_working WHERE raw_key = ?", (raw_key,)).fetchone()
    if not row:
        return {"status": "error", "message": f"row not found for {raw_key} — worktree may be closed"}
    # Same append logic as h_aw_upsert for reviewer_id
    if col == "reviewer_id" and row[col]:
        existing = _aw_parse_agent_entries(row[col] or "")
        existing.update(_aw_parse_agent_entries(val))
        val = _aw_format_agent_entries(existing)
    slot_val = params.get("slot","")
    if slot_val:
        c.execute(f"UPDATE agent_working SET {col}=?, slot=?, updated_at=datetime('now') WHERE raw_key=?",
                  (val, slot_val, raw_key))
    else:
        c.execute(f"UPDATE agent_working SET {col}=?, updated_at=datetime('now') WHERE raw_key=?",
                  (val, raw_key))
    daemon.conn.commit()
    return {"status": "ok"}


@_h("agent_working.release")
def h_aw_release(daemon: DbDaemon, params: dict) -> dict:
    """agent_release: strip session from agent_id column."""
    raw_key = _aw_canon_raw_key(params["raw_key"]); role = params.get("role",""); col = f"{role}_id"
    agent_id = params.get("agent_id","")
    if role not in ("manager", "worker", "reviewer"):
        return {"status": "error", "message": f"invalid role: {role}"}
    if role == "reviewer" and not agent_id:
        return {"status": "error", "message": "agent_id required for reviewer release"}
    c = daemon.conn
    row = c.execute(f"SELECT {col} FROM agent_working WHERE raw_key = ?", (raw_key,)).fetchone()
    if not row: return {"status": "not_found"}
    current = row[col] or ""
    if role == "reviewer" and agent_id:
        entries = _aw_parse_agent_entries(current)
        entries.pop(agent_id, None)
        new_val = _aw_format_agent_entries(entries)
    else:
        entries = _aw_parse_agent_entries(current)
        current_agent_id = next(iter(entries), None)
        if agent_id and current_agent_id and agent_id != current_agent_id:
            return {"status": "not_found"}
        current_session_id = entries.get(current_agent_id) if current_agent_id else None
        # Established session → clear only the session and retain assignment.
        # Bare reservation → release the assignment itself.
        new_val = current_agent_id if current_session_id else None
    c.execute(f"UPDATE agent_working SET {col}=?, updated_at=datetime('now') WHERE raw_key=?",
              (new_val, raw_key))
    daemon.conn.commit()
    return {"status": "ok"}


@_h("agent_working.delete")
def h_aw_delete(daemon: DbDaemon, params: dict) -> dict:
    """agent_release_all: delete row by raw_key."""
    daemon.conn.execute("DELETE FROM agent_working WHERE raw_key = ?", (_aw_canon_raw_key(params["raw_key"]),))
    daemon.conn.commit()
    return {"status": "ok"}


@_h("agent_working.get_session")
def h_aw_get_session(daemon: DbDaemon, params: dict) -> dict:
    """agent_get_session: return session_id for agent."""
    raw_key = _aw_canon_raw_key(params["raw_key"]); role = params.get("role","")
    if role not in ("manager", "worker", "reviewer"):
        return {"session_id": None}
    col = f"{role}_id"
    agent_id = params.get("agent_id","")
    row = daemon.conn.execute(f"SELECT {col} FROM agent_working WHERE raw_key = ?", (raw_key,)).fetchone()
    if not row or not row[col]: return {"session_id": None}
    if role == "reviewer":
        entries = _aw_parse_agent_entries(row[col])
        if agent_id:
            return {"session_id": entries.get(agent_id)}
        return {"session_id": next((sid for sid in entries.values() if sid), None)}
    entries = _aw_parse_agent_entries(row[col])
    if agent_id:
        return {"session_id": entries.get(agent_id)}
    return {"session_id": next(iter(entries.values()), None)}


def _aw_parse_occupied(role: str, val: str) -> set:
    """Parse occupied ids from bare reservations and established sessions."""
    return _aw_agent_ids(val)


def _aw_existing_agent_for_role(role: str, col_val: str) -> str | None:
    """Return first assigned agent_id for role if already present on the row."""
    return _aw_first_agent_id(col_val)


@_h("agent_working.next_free")
def h_aw_next_free(daemon: DbDaemon, params: dict) -> dict:
    """agent_next_free: compute next free agent NN from pool."""
    role = params["role"]; pool_size = int(params.get("pool_size","10"))
    if role not in ("manager", "worker", "reviewer"):
        return {"agent_id": None}
    col = f"{role}_id"; prefix = f"{role}_"
    rows = daemon.conn.execute(f"SELECT {col} FROM agent_working WHERE {col} IS NOT NULL").fetchall()
    occupied = set()
    for r in rows:
        occupied |= _aw_parse_occupied(role, r[col] or "")
    all_ids = {f"{prefix}{i:02d}" for i in range(1, pool_size + 1)}
    free = sorted(all_ids - occupied)
    return {"agent_id": free[0] if free else None, "free_list": free}


@_h("agent_working.next_free_and_assign")
def h_aw_next_free_and_assign(daemon: DbDaemon, params: dict) -> dict:
    """Atomic next_free + assign: allocate a free agent and immediately write it.

    Idempotent for same raw_key + role: if the row already has an agent for that
    role, return the existing agent_id without overwriting.
    """
    role = params["role"]
    raw_key = _aw_canon_raw_key(params["raw_key"])
    pool_size = int(params.get("pool_size", "10"))
    if role not in ("manager", "worker", "reviewer"):
        return {"agent_id": None, "assigned": False}
    col = f"{role}_id"
    prefix = f"{role}_"

    # Idempotent: same raw_key + role already assigned → return existing
    existing = daemon.conn.execute(
        f"SELECT {col} FROM agent_working WHERE raw_key = ?", (raw_key,)
    ).fetchone()
    if existing and existing[col]:
        prior = _aw_existing_agent_for_role(role, existing[col])
        if prior:
            return {"agent_id": prior, "assigned": True, "idempotent": True}

    rows = daemon.conn.execute(
        f"SELECT raw_key, {col} FROM agent_working WHERE {col} IS NOT NULL"
    ).fetchall()
    occupied = set()
    for r in rows:
        occupied |= _aw_parse_occupied(role, r[col] or "")
    all_ids = {f"{prefix}{i:02d}" for i in range(1, pool_size + 1)}
    free = sorted(all_ids - occupied)
    if not free:
        return {"agent_id": None, "assigned": False}
    agent_id = free[0]
    if existing is not None:
        daemon.conn.execute(
            f"UPDATE agent_working SET {col}=?, updated_at=datetime('now') WHERE raw_key=?",
            (agent_id, raw_key),
        )
    else:
        daemon.conn.execute(
            f"INSERT INTO agent_working (raw_key, {col}, updated_at) VALUES (?, ?, datetime('now'))"
            f" ON CONFLICT(raw_key) DO UPDATE SET {col}=excluded.{col}, updated_at=excluded.updated_at",
            (raw_key, agent_id),
        )
    daemon.conn.commit()
    return {"agent_id": agent_id, "assigned": True, "idempotent": False}


@_h("agent_working.get")
def h_aw_get(daemon: DbDaemon, params: dict) -> dict:
    """agent_list_by_raw_key: return full row as dict."""
    row = daemon.conn.execute("SELECT * FROM agent_working WHERE raw_key = ?", (_aw_canon_raw_key(params["raw_key"]),)).fetchone()
    if not row: return {"row": {}}
    cols = [d[1] for d in daemon.conn.execute("PRAGMA table_info(agent_working)").fetchall()]
    return {"row": dict(zip(cols, row))}


@_h("agent_working.cleanup_stale")
def h_aw_cleanup_stale(daemon: DbDaemon, params: dict) -> dict:
    """agent_cleanup_stale: remove rows for missing worktrees."""
    import os as _os
    max_age = int(params.get("max_age_hours","24"))
    rows = daemon.conn.execute("SELECT raw_key, worktree, test_worktree FROM agent_working").fetchall()
    cleaned = 0
    for r in rows:
        if r["worktree"] and not _os.path.exists(r["worktree"]):
            daemon.conn.execute("DELETE FROM agent_working WHERE raw_key = ?", (r["raw_key"],))
            cleaned += 1
        elif r["test_worktree"] and not _os.path.exists(r["test_worktree"]):
            daemon.conn.execute("UPDATE agent_working SET test_worktree=NULL, test_branch=NULL WHERE raw_key=?",
                               (r["raw_key"],))
            cleaned += 1
    daemon.conn.commit()
    return {"cleaned": cleaned}



@_h("agent_working.get_all")
def h_aw_get_all(daemon: DbDaemon, params: dict) -> dict:
    rows = daemon.conn.execute("SELECT * FROM agent_working").fetchall()
    cols = [d[1] for d in daemon.conn.execute("PRAGMA table_info(agent_working)").fetchall()]
    return {"rows": [dict(zip(cols, r)) for r in rows]}

@_h("agent_working.stats")
def h_aw_stats(daemon: DbDaemon, params: dict) -> dict:
    """agent_stats: occupancy per role.

    Occupied counts reuse _aw_parse_occupied so bare agent_id and
    agent_id:session (including multi-reviewer CSV) count consistently.
    """
    result = {}
    for role, pool in [("manager", 1), ("worker", 10), ("reviewer", 99)]:
        col = f"{role}_id"
        rows = daemon.conn.execute(
            f"SELECT {col} FROM agent_working WHERE {col} IS NOT NULL"
        ).fetchall()
        occupied_ids: set = set()
        for r in rows:
            occupied_ids |= _aw_parse_occupied(role, r[col] or "")
        occupied = len(occupied_ids)
        result[role] = {"occupied": occupied, "pool": pool, "free": pool - occupied}
    return result

# ── Review persistence ──────────────────────────────────────────────────────

@_h("agent_working.record_review")
def h_aw_record_review(daemon: DbDaemon, params: dict) -> dict:
    """Persist review verdict. UPSERT by (raw_key, review_stage)."""
    raw_key = _aw_canon_raw_key(params["raw_key"])
    review_stage = params["review_stage"]
    verdict = params["verdict"]
    reviewed_by = params.get("reviewed_by", "")
    findings = params.get("findings", "[]")
    if verdict not in ("PASS", "FAIL"):
        return {"status": "error", "message": f"verdict must be PASS or FAIL, got: {verdict}"}
    daemon.conn.execute("""
        INSERT INTO reviews (raw_key, review_stage, verdict, reviewed_by, reviewed_at, findings)
        VALUES (?,?,?,?,datetime('now'),?)
        ON CONFLICT(raw_key, review_stage) DO UPDATE SET
            verdict=excluded.verdict,
            reviewed_by=excluded.reviewed_by,
            reviewed_at=datetime('now'),
            findings=excluded.findings
    """, (raw_key, review_stage, verdict, reviewed_by, findings))
    daemon.conn.commit()
    return {"status": "ok", "raw_key": raw_key, "review_stage": review_stage}


@_h("agent_working.get_reviews")
def h_aw_get_reviews(daemon: DbDaemon, params: dict) -> dict:
    """Return all review records for a raw_key as {stage: {verdict, ...}}."""
    rows = daemon.conn.execute(
        "SELECT * FROM reviews WHERE raw_key=? ORDER BY review_stage",
        (_aw_canon_raw_key(params["raw_key"]),)
    ).fetchall()
    reviews = {}
    for r in rows:
        reviews[r["review_stage"]] = {
            "verdict": r["verdict"],
            "reviewed_by": r["reviewed_by"],
            "reviewed_at": r["reviewed_at"],
            "findings": r["findings"],
        }
    return {"reviews": reviews}


# ── CLI ───────────────────────────────────────────────────────────────────

def cmd_start(args) -> int:
    project = args.project
    pid_file = _pid_file(project)
    socket_path = _socket_path(project)

    # Check already running
    if os.path.exists(pid_file):
        try:
            with open(pid_file) as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, 0)
            print(f"freely-db daemon already running (PID {old_pid})")
            return 0
        except (OSError, ValueError):
            os.unlink(pid_file)

    daemon = DbDaemon(project)

    # Singleton lock BEFORE forking (raw-20261103T132622Z). The old code did
    # check-then-act on the pid file: two concurrent starts could both unlink,
    # both fork, and both bind — the second unlinked the first's socket and the
    # whole project lost its DB. The lock is taken here and inherited by the
    # forked child, so exactly one process ever owns it.
    os.makedirs(os.path.dirname(pid_file), exist_ok=True)
    lock_handle = open(pid_file, "a+")
    try:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        lock_handle.close()
        print("freely-db daemon already running (singleton lock held)")
        return 0

    if not args.foreground:
        pid = os.fork()
        if pid > 0:
            time.sleep(0.3)
            if os.path.exists(_pid_file(daemon.project)):
                print(f"freely-db daemon started (PID {pid})")
                return 0
            else:
                print("[ERROR] db daemon failed to start", file=sys.stderr)
                return 1

    # Child or foreground. The pid file is the lock file: write through the
    # inherited handle so the recorded pid and the held lock never disagree.
    lock_handle.seek(0)
    lock_handle.truncate()
    lock_handle.write(str(os.getpid()))
    lock_handle.flush()
    os.fsync(lock_handle.fileno())

    def _cleanup(signum=None, frame=None):
        sig_name = signal.Signals(signum).name if signum is not None else "EXIT"
        daemon.log(f"daemon received signal {sig_name}, stopping")
        daemon.stop()
        # Only the owner may remove the shared files: an orphan daemon exiting
        # must not delete a healthy daemon's socket/pid (raw-20261103T132622Z).
        try:
            recorded_owner = open(pid_file).read().strip()
        except OSError:
            recorded_owner = ""
        if recorded_owner == str(os.getpid()):
            if os.path.exists(pid_file):
                os.unlink(pid_file)
            if os.path.exists(socket_path):
                os.unlink(socket_path)
        else:
            daemon.log(
                f"not the owner (pid file holds {recorded_owner!r}); leaving pid/socket intact"
            )
        sys.exit(0)

    signal.signal(signal.SIGTERM, _cleanup)
    signal.signal(signal.SIGINT, _cleanup)

    try:
        daemon.start()
    except Exception as e:
        print(f"[ERROR] daemon start failed: {e}", file=sys.stderr)
        return 1
    return 0


def cmd_stop(args) -> int:
    project = args.project
    pid_file = _pid_file(project)
    socket_path = _socket_path(project)

    if not os.path.exists(pid_file):
        print("freely-db daemon not running")
        if os.path.exists(socket_path):
            os.unlink(socket_path)
        return 0

    try:
        with open(pid_file) as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
        print(f"freely-db daemon stopped (PID {pid})")
    except (OSError, ValueError) as e:
        print(f"failed to stop: {e}")

    if os.path.exists(pid_file):
        os.unlink(pid_file)
    if os.path.exists(socket_path):
        os.unlink(socket_path)
    return 0


def cmd_status(args) -> int:
    project = args.project
    pid_file = _pid_file(project)
    socket_path = _socket_path(project)

    if not os.path.exists(pid_file):
        print("stopped")
        return 1

    try:
        with open(pid_file) as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)
    except (OSError, ValueError):
        print("stopped (stale pid)")
        if os.path.exists(socket_path):
            os.unlink(socket_path)
        return 1

    # Health check via socket
    if os.path.exists(socket_path):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect(socket_path)
            req = json.dumps({"jsonrpc": "2.0", "id": 9999, "method": "db.ping", "params": {}}) + "\n"
            sock.sendall(req.encode())
            data = sock.recv(4096)
            sock.close()
            resp = json.loads(data.decode())
            if "result" in resp:
                print(f"running (PID {pid})")
                return 0
        except Exception:
            pass

    print(f"unhealthy (PID {pid})")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Freely unified DB daemon")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("start")
    p.add_argument("--project", required=True)
    p.add_argument("--foreground", action="store_true")

    p = sub.add_parser("stop")
    p.add_argument("--project", required=True)

    p = sub.add_parser("status")
    p.add_argument("--project", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    if args.command == "start":
        return cmd_start(args)
    elif args.command == "stop":
        return cmd_stop(args)
    elif args.command == "status":
        return cmd_status(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
