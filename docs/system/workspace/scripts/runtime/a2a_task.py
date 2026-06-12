#!/usr/bin/env python3
"""a2a_task.py — A2A Task DB API (A2A Client Protocol).

Replaces handoff.py. All task state management uses a2a_tasks table via
freely_db_manager daemon (Unix socket JSON-RPC).

Handoff legacy:
  handoff.py.bak — original handoff implementation, replaced 2026-06-12
  migrate_handoff_to_a2a.py.bak — one-shot migration tool, completed
"""

import argparse
import json
import os
import socket
import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict

# ── Daemon socket RPC ────────────────────────────────────────────────────

PROJECT = None

def _short_hash(project: str) -> str:
    import hashlib
    return hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]

def _socket_path(project: str) -> str:
    return f"/tmp/freely-db-{_short_hash(project)}.sock"

def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _db_rpc(method: str, params: dict, timeout: float = 30.0) -> dict:
    project = PROJECT or os.getcwd()
    sp = _socket_path(project)
    req = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect(sp)
        sock.sendall((json.dumps(req, default=str) + "\n").encode())
        sock.shutdown(socket.SHUT_WR)
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk: break
            data += chunk
    finally:
        sock.close()
    resp = json.loads(data.decode())
    if "error" in resp:
        raise RuntimeError(resp["error"].get("message", str(resp["error"])))
    return resp.get("result", {})


# ── A2A Task State ────────────────────────────────────────────────────────

class TaskState:
    SUBMITTED = "submitted"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    INPUT_REQUIRED = "input-required"
    PENDING_INPUT = "pending-input"
    CANCELED = "canceled"

# exit_kind → A2A state
EXIT_KIND_TO_STATE = {
    'manager_working': TaskState.SUBMITTED,
    'worker_working': TaskState.WORKING,
    'worker_done': TaskState.COMPLETED,
    'worker_blocked': TaskState.INPUT_REQUIRED,
    'worker_handoff_needed': TaskState.PENDING_INPUT,
    'delegate_workers': TaskState.SUBMITTED,
    'resume_manager': TaskState.COMPLETED,
    'stop_ai': TaskState.FAILED,
}


# ── Public API ────────────────────────────────────────────────────────────

def create_task(
    skill: str = "",
    worktree: str = "",
    branch: str = "",
    raw_key: str = "",
    prompt_file: str = "",
    session_id: str = "",
    message: str = "",
    name: str = "",
    description: str = "",
    agent_id: str = "manager",
) -> str:
    """Create a new A2A task. Returns task_id."""
    result = _db_rpc("a2a_task.insert", {
        "name": name or skill,
        "description": description,
        "state": TaskState.SUBMITTED,
        "agent_id": agent_id,
        "skill": skill,
        "session_id": session_id,
        "message": message,
        "raw_key": raw_key,
        "worktree": worktree,
        "branch": branch,
        "prompt_file": prompt_file,
    })
    return result.get("task_id", "")


def get_task(task_id: str) -> Optional[dict]:
    """Get task by ID."""
    r = _db_rpc("a2a_task.get", {"task_id": task_id})
    return r.get("record")


def update_task(task_id: str, **kwargs) -> int:
    """Update task fields. Returns affected row count."""
    kwargs["task_id"] = task_id
    kwargs["updated_at"] = _now_utc()
    r = _db_rpc("a2a_task.update", kwargs)
    return r.get("affected", 0)


def update_from_exit_kind(task_id: str, exit_kind: str,
                          reason: str = "", progress: str = "",
                          next_action: str = "", completion_summary: str = "",
                          evidence_paths: str = "", error: str = "") -> int:
    """Update task state from exit_kind."""
    state = EXIT_KIND_TO_STATE.get(exit_kind, TaskState.WORKING)
    return update_task(
        task_id=task_id, state=state, exit_kind=exit_kind,
        reason=reason, progress=progress, next_action=next_action,
        completion_summary=completion_summary, evidence_paths=evidence_paths,
        error=error,
    )


def delete_task(task_id: str) -> int:
    """Delete task by ID."""
    r = _db_rpc("a2a_task.delete", {"task_id": task_id})
    return r.get("affected", 0)


def list_tasks(state: Optional[str] = None, agent_id: Optional[str] = None,
               skill: Optional[str] = None) -> List[dict]:
    """List tasks with optional filters."""
    params = {}
    if state: params["state"] = state
    if agent_id: params["agent_id"] = agent_id
    if skill: params["skill"] = skill
    r = _db_rpc("a2a_task.list", params)
    return r.get("rows", [])


def list_by_raw_key(raw_key: str) -> List[dict]:
    """List tasks by raw_key."""
    r = _db_rpc("a2a_task.list-by-raw-key", {"raw_key": raw_key})
    return r.get("rows", [])


def list_by_worktree(worktree: str, state: Optional[str] = None) -> List[dict]:
    """List tasks by worktree."""
    params = {"worktree": worktree}
    if state: params["state"] = state
    r = _db_rpc("a2a_task.list-by-worktree", params)
    return r.get("rows", [])


def list_active() -> List[dict]:
    """List tasks in active states."""
    r = _db_rpc("a2a_task.list-active", {})
    return r.get("rows", [])


def latest_manager() -> Optional[dict]:
    """Get latest manager task."""
    r = _db_rpc("a2a_task.latest-manager", {})
    rows = r.get("rows", [])
    return rows[0] if rows else None


def update_message(task_id: str, content: str, role: str = "worker", msg_type: str = "text") -> int:
    """Append a message to the task."""
    r = _db_rpc("a2a_task.update-message", {
        "task_id": task_id, "role": role, "type": msg_type, "content": content,
    })
    return r.get("affected", 0)


# ── Legacy compat (will be removed once callers migrate) ──────────────────

def insert_handoff(role: str = "manager", raw_key: str = "", **kwargs) -> str:
    """Deprecated: use create_task() instead."""
    return create_task(
        agent_id=role, raw_key=raw_key,
        skill=kwargs.get("intent_kind", ""),
        worktree=kwargs.get("worktree", ""),
        branch=kwargs.get("branch", ""),
        prompt_file=kwargs.get("prompt_file", ""),
        session_id=kwargs.get("session_id", ""),
        message=kwargs.get("completion_summary", kwargs.get("reason", "")),
    )


# ── CLI ───────────────────────────────────────────────────────────────────

def _main() -> int:
    parser = argparse.ArgumentParser(description="A2A Task DB API")
    sub = parser.add_subparsers(dest="cmd")

    p_create = sub.add_parser("create")
    p_create.add_argument("--skill", default="")
    p_create.add_argument("--worktree", default="")
    p_create.add_argument("--branch", default="")
    p_create.add_argument("--raw-key", default="")
    p_create.add_argument("--prompt-file", default="")
    p_create.add_argument("--message", default="")

    p_get = sub.add_parser("get")
    p_get.add_argument("task_id")

    p_list = sub.add_parser("list")
    p_list.add_argument("--state", default=None)
    p_list.add_argument("--agent-id", default=None)
    p_list.add_argument("--raw-key", default=None)
    p_list.add_argument("--worktree", default=None)

    p_update = sub.add_parser("update")
    p_update.add_argument("task_id")
    p_update.add_argument("--state", default=None)
    p_update.add_argument("--exit-kind", default=None)

    args = parser.parse_args()

    if args.cmd == "create":
        tid = create_task(skill=args.skill, worktree=args.worktree,
                          branch=args.branch, raw_key=getattr(args, 'raw_key', ''),
                          prompt_file=getattr(args, 'prompt_file', ''),
                          message=getattr(args, 'message', ''))
        print(json.dumps({"task_id": tid}))
    elif args.cmd == "get":
        t = get_task(args.task_id)
        print(json.dumps(t or {}))
    elif args.cmd == "list":
        if hasattr(args, 'raw_key') and args.raw_key:
            rows = list_by_raw_key(args.raw_key)
        elif hasattr(args, 'worktree') and args.worktree:
            rows = list_by_worktree(args.worktree, args.state)
        else:
            rows = list_tasks(state=args.state, agent_id=getattr(args, 'agent_id', None))
        print(json.dumps({"rows": rows}))
    elif args.cmd == "update":
        kwargs = {}
        if args.state: kwargs["state"] = args.state
        if getattr(args, 'exit_kind', None): kwargs["exit_kind"] = args.exit_kind
        print(json.dumps({"affected": update_task(args.task_id, **kwargs)}))
    return 0

if __name__ == "__main__":
    raise SystemExit(_main())
