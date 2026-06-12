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
    parser.add_argument("--db", default=None, help="ignored (compat)")  # legacy compat
    sub = parser.add_subparsers(dest="cmd")

    # create
    p_create = sub.add_parser("create")
    p_create.add_argument("--skill", default="")
    p_create.add_argument("--worktree", default="")
    p_create.add_argument("--branch", default="")
    p_create.add_argument("--raw-key", default=None)
    p_create.add_argument("--prompt-file", default="")
    p_create.add_argument("--message", default="")

    # get
    p_get = sub.add_parser("get")
    p_get.add_argument("--handoff-id", dest="task_id", default="")

    # list
    p_list = sub.add_parser("list")
    p_list.add_argument("--role", default="worker")  # legacy compat
    p_list.add_argument("--status", default=None)
    p_list.add_argument("--raw-key", default=None)
    p_list.add_argument("--worktree", default=None)

    # update
    p_update = sub.add_parser("update")
    p_update.add_argument("--handoff-id", dest="task_id", default="")
    p_update.add_argument("--state", default=None)
    p_update.add_argument("--exit-kind", default=None)
    p_update.add_argument("--status", default=None)  # legacy compat

    # latest-manager
    p_lm = sub.add_parser("latest-manager")

    # latest-completed-worker
    p_lcw = sub.add_parser("latest-completed-worker")
    p_lcw.add_argument("--raw-key", default=None)

    # update-last-activity
    p_ula = sub.add_parser("update-last-activity")
    p_ula.add_argument("--handoff-id", dest="task_id", default="")

    # auto-consume
    p_ac = sub.add_parser("auto-consume")
    p_ac.add_argument("--raw-key", default="")

    # insert (legacy compat)
    p_insert = sub.add_parser("insert")
    p_insert.add_argument("--role", default="manager")
    p_insert.add_argument("--raw-key", default="")
    p_insert.add_argument("--worktree", default="")
    p_insert.add_argument("--branch", default="")
    p_insert.add_argument("--prompt-file", default="")
    p_insert.add_argument("--intent-kind", default="")

    args = parser.parse_args()

    if args.cmd == "create":
        tid = create_task(
            skill=args.skill or "", worktree=args.worktree or "",
            branch=args.branch or "", raw_key=getattr(args, 'raw_key', None) or "",
            prompt_file=getattr(args, 'prompt_file', "") or "",
            message=getattr(args, 'message', "") or "")
        print(json.dumps({"task_id": tid}))
    elif args.cmd == "get":
        t = get_task(args.task_id)
        print(json.dumps(t or {}))
    elif args.cmd == "list":
        agent_id = None
        if hasattr(args, 'role') and args.role == 'worker':
            agent_id = 'worker'
        elif hasattr(args, 'role') and args.role == 'manager':
            agent_id = 'manager'
        state_map = {
            'launched': 'working', 'pending': 'submitted',
            'completed': 'completed', 'blocked': 'input-required',
            'rejected': 'failed', 'consumed': 'completed',
        }
        state = None
        if getattr(args, 'status', None):
            state = state_map.get(args.status, args.status)
        if hasattr(args, 'raw_key') and args.raw_key:
            rows = list_by_raw_key(args.raw_key)
        elif hasattr(args, 'worktree') and args.worktree:
            rows = list_by_worktree(args.worktree, state)
        else:
            rows = list_tasks(state=state, agent_id=agent_id)
        print(json.dumps({"rows": rows}))
    elif args.cmd == "update":
        kwargs = {}
        if getattr(args, 'status', None):
            sm = {'launched': 'working', 'pending': 'submitted',
                  'completed': 'completed', 'blocked': 'input-required'}
            kwargs['state'] = sm.get(args.status, args.status)
        if getattr(args, 'state', None): kwargs['state'] = args.state
        if getattr(args, 'exit_kind', None): kwargs['exit_kind'] = args.exit_kind
        print(json.dumps({"affected": update_task(args.task_id, **kwargs)}))
    elif args.cmd == "latest-manager":
        t = latest_manager()
        print(json.dumps(t or {}))
    elif args.cmd == "latest-completed-worker":
        rows = list_by_raw_key(getattr(args, 'raw_key', None) or "")
        completed = [r for r in rows if r.get('state') == 'completed' and r.get('agent_id') == 'worker']
        print(json.dumps(completed[0] if completed else {}))
    elif args.cmd == "update-last-activity":
        print(json.dumps({"affected": update_task(args.task_id)}))
    elif args.cmd == "auto-consume":
        rk = getattr(args, 'raw_key', '') or ""
        rows = list_by_raw_key(rk)
        affected = 0
        for r in rows:
            if r.get('state') in ('completed', 'failed') and r.get('agent_id') == 'worker':
                affected += update_task(r.get('task_id', ''), state='completed')
        print(json.dumps({"affected": affected}))
    elif args.cmd == "insert":
        tid = insert_handoff(
            role=getattr(args, 'role', 'manager'), raw_key=getattr(args, 'raw_key', '') or '',
            worktree=getattr(args, 'worktree', '') or '',
            branch=getattr(args, 'branch', '') or '',
            prompt_file=getattr(args, 'prompt_file', '') or '',
            intent_kind=getattr(args, 'intent_kind', '') or '')
        print(json.dumps({"handoff_id": tid}))
    return 0
