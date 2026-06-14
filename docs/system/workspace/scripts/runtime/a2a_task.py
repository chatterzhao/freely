#!/usr/bin/env python3
"""a2a_task.py — A2A Protocol Client

Communicates via A2A protocol (HTTP over Unix socket to A2A Server).
AI replies are A2A Messages; the state block at the end drives Task state transitions.

A2A states: submitted, working, completed, failed, input-required, pending-input
"""

import argparse
import json
import os
import socket
from datetime import datetime, timezone
from typing import Optional, List, Dict

# ── Path helpers ─────────────────────────────────────────────────────────

def _short_hash(project: str) -> str:
    import hashlib
    return hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]

def _a2a_socket_path(project: str) -> str:
    return f"/tmp/freely-a2a-{_short_hash(project)}.sock"

def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

PROJECT = None

def _resolve_project() -> str:
    return PROJECT or os.getcwd()


# ── A2A Protocol Client ───────────────────────────────────────────────────

class A2AClient:
    """A2A Protocol Client with dual transport.

    Supports:
    - unix:///path/to/socket  (local agents, zero network overhead)
    - http://host:port         (remote agents, network communication)
    - auto                     (discover: scan local sockets → try remote URL)
    """

    def __init__(self, project: str = "", url: str = ""):
        self.project = project or _resolve_project()
        self._url = url or os.environ.get("A2A_REMOTE_URL", "")
        self._socket_path = _a2a_socket_path(self.project) if not self._url else ""
        self._discovered_endpoints: List[str] = []

    @property
    def _endpoint(self) -> str:
        """Resolve the active endpoint (Unix socket or HTTP URL)."""
        if self._url:
            return self._url
        if self._socket_path and os.path.exists(self._socket_path):
            return f"unix://{self._socket_path}"
        return f"unix://{self._socket_path}"  # Will fail if not running

    def discover_agents(self) -> List[str]:
        """Discover local A2A agents via Unix socket scanning."""
        import glob
        endpoints = []
        for sock in glob.glob("/tmp/freely-a2a-*.sock"):
            if sock != self._socket_path:
                endpoints.append(f"unix://{sock}")
        self._discovered_endpoints = endpoints
        return endpoints

    def connect(self, target: str) -> "A2AClient":
        """Create a client connected to a specific agent endpoint."""
        if target.startswith("unix://"):
            sock_path = target[7:]
            c = A2AClient.__new__(A2AClient)
            c.project = self.project
            c._url = ""
            c._socket_path = sock_path
            c._discovered_endpoints = []
            return c
        elif target.startswith("http://") or target.startswith("https://"):
            c = A2AClient.__new__(A2AClient)
            c.project = self.project
            c._url = target
            c._socket_path = ""
            c._discovered_endpoints = []
            return c
        raise ValueError(f"Unsupported target: {target}")

    def _ensure(self):
        if self._url:
            # Remote: no local socket check needed
            return
        if not os.path.exists(self._socket_path):
            raise RuntimeError(
                f"A2A Server not running at {self._socket_path}. "
                f"Start with: a2a_server.py --project {self.project} --start"
            )

    def _request(self, method: str, path: str, body: Optional[Dict] = None,
                 timeout: float = 30.0) -> dict:
        """Send HTTP request via Unix socket or TCP."""
        self._ensure()
        if self._url:
            return self._http_request(method, path, body, timeout)
        else:
            return self._unix_request(method, path, body, timeout)

    def _unix_request(self, method: str, path: str, body=None, timeout=30.0) -> dict:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect(self._socket_path)
            if body is not None:
                body_json = json.dumps(body, default=str)
                request = (f"{method} {path} HTTP/1.1\r\n"
                          f"Content-Type: application/json\r\n"
                          f"Content-Length: {len(body_json)}\r\n"
                          f"Connection: close\r\n\r\n{body_json}")
            else:
                request = f"{method} {path} HTTP/1.1\r\nConnection: close\r\n\r\n"
            sock.sendall(request.encode())
            data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk: break
                data += chunk
        finally:
            sock.close()
        return self._parse_response(data.decode("utf-8", errors="replace"))

    def _http_request(self, method: str, path: str, body=None, timeout=30.0) -> dict:
        """HTTP request via TCP (uses urllib for zero extra deps)."""
        import urllib.request
        full_url = f"{self._url.rstrip('/')}{path}"
        data_bytes = json.dumps(body, default=str).encode() if body else None
        req = urllib.request.Request(full_url, data=data_bytes, method=method)
        req.add_header("Content-Type", "application/json")
        req.add_header("Connection", "close")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            try:
                return json.loads(e.read().decode())
            except:
                return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def _parse_response(text: str) -> dict:
        body_start = text.find("\r\n\r\n")
        if body_start == -1: body_start = text.find("\n\n")
        if body_start != -1: return json.loads(text[body_start + 4:])
        return {"error": "empty response"}

    # ── Task API ───────────────────────────────────────────────────────

    def create(self, **kwargs) -> dict:
        return self._request("POST", "/tasks", {k: v for k, v in kwargs.items() if v})

    def get(self, task_id: str) -> Optional[dict]:
        r = self._request("GET", f"/tasks/{task_id}")
        return r if "id" in r else None

    def update(self, task_id: str, **fields) -> dict:
        return self._request("PATCH", f"/tasks/{task_id}",
                            {k: v for k, v in fields.items() if v})

    def list(self, **filters) -> List[dict]:
        params = [f"{k}={v}" for k, v in filters.items() if v]
        path = "/tasks?" + "&".join(params) if params else "/tasks"
        return self._request("GET", path).get("tasks", [])

    def latest_manager(self) -> Optional[dict]:
        r = self._request("GET", "/tasks/latest-manager")
        return r if "id" in r else None

    def pending_delivery(self) -> List[dict]:
        return self._request("GET", "/tasks/pending-delivery").get("tasks", [])

    def launched_pids(self, raw_key: str = "") -> List[dict]:
        path = f"/tasks/launched-pids?raw_key={raw_key}" if raw_key else "/tasks/launched-pids"
        return self._request("GET", path).get("rows", [])

    def add_message(self, task_id: str, role: str = "worker",
                    msg_type: str = "text", content: str = "") -> dict:
        return self._request("POST", f"/tasks/{task_id}/messages",
                            {"role": role, "type": msg_type, "content": content})

    def mark_delivered(self, task_id: str) -> dict:
        return self._request("PATCH", f"/tasks/{task_id}/delivery",
                            {"delivery_status": "delivered"})

    def set_worker_pid(self, task_id: str, worker_pid: str) -> dict:
        return self._request("PATCH", f"/tasks/{task_id}/worker-pid",
                            {"worker_pid": worker_pid})

    def delete(self, task_id: str) -> dict:
        return self.update(task_id, state="canceled")

    def mark_stale(self, timeout_minutes: int = 30) -> int:
        """Mark timed-out working tasks as input-required."""
        affected = 0
        for t in self.list(state="working"):
            updated = t.get("updatedAt", t.get("updated_at", ""))
            if updated:
                from datetime import datetime, timezone, timedelta
                try:
                    dt = datetime.strptime(updated[:19], "%Y-%m-%dT%H:%M:%S")
                    if datetime.now(timezone.utc) - dt.replace(tzinfo=timezone.utc) > timedelta(minutes=timeout_minutes):
                        self.update(t["id"], state="input-required", error="timed out")
                        affected += 1
                except (ValueError, KeyError):
                    pass
        return affected


_client_instance = None

def _client() -> A2AClient:
    global _client_instance
    if _client_instance is None:
        _client_instance = A2AClient(_resolve_project())
    return _client_instance


# ── A2A Task States ───────────────────────────────────────────────────────

class State:
    SUBMITTED = "submitted"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    INPUT_REQUIRED = "input-required"
    PENDING_INPUT = "pending-input"
    CANCELED = "canceled"


# ── Public API ────────────────────────────────────────────────────────────

def create_task(**kwargs) -> str:
    return _client().create(**kwargs).get("id", "")

def get_task(task_id: str) -> Optional[dict]:
    return _client().get(task_id)

def update_task(task_id: str, **kwargs) -> int:
    return 1 if "id" in _client().update(task_id, **kwargs) else 0

def delete_task(task_id: str) -> int:
    return 1 if "id" in _client().delete(task_id) else 0

def list_tasks(state: str = "", agent_id: str = "",
               skill: str = "", worktree: str = "",
               raw_key: str = "") -> List[dict]:
    return _client().list(state=state, agent_id=agent_id, skill=skill,
                          worktree=worktree, raw_key=raw_key)

def list_by_raw_key(raw_key: str) -> List[dict]:
    return _client().list(raw_key=raw_key)

def list_by_worktree(worktree: str, state: str = "") -> List[dict]:
    return _client().list(worktree=worktree, state=state)

def list_active() -> List[dict]:
    return [t for t in _client().list()
            if t.get("state") in (State.SUBMITTED, State.WORKING, State.INPUT_REQUIRED)]

def list_active_workers(worktree: str) -> List[dict]:
    return _client().list(worktree=worktree, state=State.WORKING)

def latest_manager() -> Optional[dict]:
    return _client().latest_manager()

def update_message(task_id: str, content: str, role: str = "worker",
                   msg_type: str = "text") -> int:
    return 1 if _client().add_message(task_id, role, msg_type, content).get("ok") else 0

def pending_delivery() -> List[dict]:
    return _client().pending_delivery()

def mark_delivered(task_id: str) -> int:
    return 1 if _client().mark_delivered(task_id).get("ok") else 0

def set_worker_pid(task_id: str, worker_pid: str) -> int:
    return 1 if _client().set_worker_pid(task_id, worker_pid).get("ok") else 0

def launched_pids(raw_key: str = "") -> List[dict]:
    return _client().launched_pids(raw_key)

def mark_stale(timeout_minutes: int = 30) -> int:
    return _client().mark_stale(timeout_minutes)

# Legacy aliases (for backward compat with freely bash)
update_delivery_status = mark_delivered
update_worker_pid = set_worker_pid
get_launched_pids = launched_pids


# ── AI Reply Processing ──────────────────────────────────────────────────

def process_ai_reply(reply_text: str, role: str = "manager", raw_key: str = "",
                     prompt_file: str = "", worktree: str = "",
                     branch: str = "", session_id: str = "") -> dict:
    """Process AI reply: extract A2A state, create/update Task via A2A Server.

    The AI reply IS an A2A Message. The state block provides the task transition.
    """
    from a2a_task_parser import extract_state_block, validate_state_json, normalize_state_fields

    block = extract_state_block(reply_text)
    if not block:
        return {"ok": False, "errors": [{"field": "block", "error": "no state block found"}]}
    try:
        fields = json.loads(block)
    except json.JSONDecodeError as e:
        return {"ok": False, "errors": [{"field": "parse", "error": str(e)}]}
    normalize_state_fields(fields)
    ok, errors = validate_state_json(fields)
    if not ok:
        return {"ok": False, "errors": errors}

    state = fields["state"]

    # Communicate with A2A Server. If unreachable, return parsed state still.
    try:
        c = _client()
        r = c.create(
            skill=fields.get("skill", ""),
            agent_id=role, name=role,
            raw_key=raw_key, worktree=worktree, branch=branch,
            prompt_file=prompt_file, session_id=session_id,
            message=fields.get("summary", ""),
            state=state,
            summary=fields.get("summary", ""),
            next=fields.get("next", ""),
            evidence=fields.get("evidence", ""),
            worker_prompts_csv=fields.get("workers", ""),
        )
        task_id = r.get("id", "")
        c.add_message(task_id, role=role, msg_type="text", content=reply_text[:32768])
    except Exception as e:
        return {"ok": True, "state": state, "exit_kind": state,
                "task_id": "a2a_unreachable",
                "workers": fields.get("workers", ""),
                "summary": fields.get("summary", ""),
                "next": fields.get("next", ""),
                "evidence": fields.get("evidence", ""),
                "a2a_error": str(e)}

    return {"ok": True, "task_id": task_id, "state": state, "exit_kind": state,
            "workers": fields.get("workers", ""),
            "summary": fields.get("summary", ""),
            "next": fields.get("next", ""),
            "evidence": fields.get("evidence", "")}


def read_state_only(reply_text: str) -> dict:
    """Read A2A state from AI reply without any side effects."""
    from a2a_task_parser import extract_task_state
    return extract_task_state(reply_text)


# ── CLI ───────────────────────────────────────────────────────────────────

def _main() -> int:
    parser = argparse.ArgumentParser(description="A2A Protocol Client")
    parser.add_argument("--db", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--project", default=None, help="Project path")
    sub = parser.add_subparsers(dest="cmd")

    p_create = sub.add_parser("create")
    p_create.add_argument("--skill", default="")
    p_create.add_argument("--worktree", default="")
    p_create.add_argument("--branch", default="")
    p_create.add_argument("--raw-key", default=None)
    p_create.add_argument("--prompt-file", default="")
    p_create.add_argument("--message", default="")
    p_create.add_argument("--agent-id", default="manager")

    p_insert = sub.add_parser("insert")
    p_insert.add_argument("--role", default="manager")
    p_insert.add_argument("--raw-key", default="")
    p_insert.add_argument("--worktree", default="")
    p_insert.add_argument("--branch", default="")
    p_insert.add_argument("--prompt-file", default="")
    p_insert.add_argument("--intent-kind", default="")

    p_get = sub.add_parser("get")
    p_get.add_argument("--task-id", default="")

    p_list = sub.add_parser("list")
    p_list.add_argument("--agent-id", default=None)
    p_list.add_argument("--state", default=None)
    p_list.add_argument("--raw-key", default=None)
    p_list.add_argument("--worktree", default=None)
    p_list.add_argument("--role", default=None, help=argparse.SUPPRESS)
    p_list.add_argument("--status", default=None, help=argparse.SUPPRESS)

    p_update = sub.add_parser("update")
    p_update.add_argument("--task-id", default="")
    p_update.add_argument("--state", default=None)
    p_update.add_argument("--exit-kind", default=None, help=argparse.SUPPRESS)
    p_update.add_argument("--status", default=None, help=argparse.SUPPRESS)

    sub.add_parser("latest-manager")
    p_lcw = sub.add_parser("latest-completed-worker")
    p_lcw.add_argument("--raw-key", default=None)
    p_ula = sub.add_parser("update-last-activity")
    p_ula.add_argument("--task-id", default="")
    p_ac = sub.add_parser("auto-consume")
    p_ac.add_argument("--raw-key", default="")

    p_parse = sub.add_parser("parse")
    p_parse.add_argument("--reply-text", default="")
    p_parse.add_argument("--role", default="manager")
    p_parse.add_argument("--raw-key", default="")
    p_parse.add_argument("--prompt-file", default="")
    p_parse.add_argument("--worktree", default="")
    p_parse.add_argument("--branch", default="")
    p_parse.add_argument("--session-id", default="")
    p_extract = sub.add_parser("extract")
    p_extract.add_argument("--reply-text", default="")

    p_aw = sub.add_parser("active-workers")
    p_aw.add_argument("--worktree", default="")
    p_haw = sub.add_parser("has-active-worker")
    p_haw.add_argument("--worktree", default="")
    p_lk = sub.add_parser("list-key")
    p_lk.add_argument("--raw-key", default="")

    p_lpd = sub.add_parser("list-pending-delivery")
    p_usa = sub.add_parser("update-send-to-ai")
    p_usa.add_argument("--task-id", default="")

    p_uwp = sub.add_parser("update-worker-pid")
    p_uwp.add_argument("--task-id", default="")
    p_uwp.add_argument("--worker-pid", default="")
    p_glp = sub.add_parser("get-launched-pids")
    p_glp.add_argument("--raw-key", default="")

    # init: no-op (daemon creates tables); kept for backward compat
    sub.add_parser("init")

    # mark-stale: mark timed-out working tasks as input-required
    p_ms = sub.add_parser("mark-stale")
    p_ms.add_argument("--timeout-minutes", default="30")

    # ── a2a-exit: AI explicitly sets A2A Task state (standard A2A pattern) ──
    p_exit = sub.add_parser("a2a-exit")
    p_exit.add_argument("--state", required=True, help="A2A state: submitted|working|completed|failed|input-required|pending-input")
    p_exit.add_argument("--summary", default="", help="Completion summary")
    p_exit.add_argument("--workers", default="", help="Worker prompts CSV (for delegate)")
    p_exit.add_argument("--next", default="", help="Next action")
    p_exit.add_argument("--evidence", default="", help="Evidence paths")
    p_exit.add_argument("--role", default="manager", help="Role: manager|worker")
    p_exit.add_argument("--raw-key", default="", help="Raw issue key")
    p_exit.add_argument("--worktree", default="", help="Worktree path")
    p_exit.add_argument("--branch", default="", help="Branch name")
    p_exit.add_argument("--prompt-file", default="", help="Prompt file path")
    p_exit.add_argument("--session-id", default="", help="Session ID")

    args, _ = parser.parse_known_args()

    global PROJECT
    if getattr(args, 'project', None):
        PROJECT = args.project

    _task_id = getattr(args, 'task_id', '') or ''
    # Legacy arg mapping
    if args.cmd == "list":
        if getattr(args, 'role', None) and not getattr(args, 'agent_id', None):
            args.agent_id = args.role
        if getattr(args, 'status', None) and not getattr(args, 'state', None):
            sm = {'launched': 'working', 'pending': 'submitted', 'completed': 'completed',
                  'blocked': 'input-required', 'rejected': 'failed', 'consumed': 'completed'}
            args.state = sm.get(args.status, args.status)
    if args.cmd == "update":
        if getattr(args, 'status', None) and not getattr(args, 'state', None):
            sm = {'launched': 'working', 'pending': 'submitted', 'completed': 'completed',
                  'blocked': 'input-required'}
            args.state = sm.get(args.status, args.status)
        # Map legacy --exit-kind to state
        if getattr(args, 'exit_kind', None) and not getattr(args, 'state', None):
            from a2a_task_parser import normalize_state
            args.state = normalize_state(args.exit_kind)

    try:
        if args.cmd == "create":
            tid = create_task(
                skill=getattr(args, 'skill', '') or "",
                worktree=getattr(args, 'worktree', '') or "",
                branch=getattr(args, 'branch', '') or "",
                raw_key=getattr(args, 'raw_key', None) or "",
                prompt_file=getattr(args, 'prompt_file', '') or "",
                message=getattr(args, 'message', '') or "",
                agent_id=getattr(args, 'agent_id', 'manager') or "manager")
            print(json.dumps({"task_id": tid}))
        elif args.cmd == "insert":
            tid = create_task(
                agent_id=getattr(args, 'role', 'manager') or "manager",
                raw_key=getattr(args, 'raw_key', '') or "",
                worktree=getattr(args, 'worktree', '') or "",
                branch=getattr(args, 'branch', '') or "",
                prompt_file=getattr(args, 'prompt_file', '') or "",
                skill=getattr(args, 'intent_kind', '') or "")
            print(json.dumps({"task_id": tid}))
        elif args.cmd == "get":
            t = get_task(_task_id)
            print(json.dumps(t or {}))
        elif args.cmd == "list":
            agent_id = getattr(args, 'agent_id', None) or None
            state = getattr(args, 'state', None) or None
            if hasattr(args, 'raw_key') and args.raw_key:
                rows = list_by_raw_key(args.raw_key)
            elif hasattr(args, 'worktree') and args.worktree:
                rows = list_by_worktree(args.worktree, state or "")
            else:
                rows = list_tasks(state=state or "", agent_id=agent_id or "")
            print(json.dumps({"rows": rows}))
        elif args.cmd == "update":
            kwargs = {}
            if getattr(args, 'state', None): kwargs['state'] = args.state
            print(json.dumps({"affected": update_task(_task_id, **kwargs)}))
        elif args.cmd == "latest-manager":
            t = latest_manager()
            print(json.dumps(t or {}))
        elif args.cmd == "latest-completed-worker":
            rows = list_by_raw_key(getattr(args, 'raw_key', None) or "")
            completed = [r for r in rows if r.get('state') == 'completed' and r.get('agent_id') == 'worker']
            print(json.dumps(completed[0] if completed else {}))
        elif args.cmd == "update-last-activity":
            print(json.dumps({"affected": update_task(_task_id)}))
        elif args.cmd == "auto-consume":
            rk = getattr(args, 'raw_key', '') or ""
            rows = list_by_raw_key(rk)
            affected = 0
            for r in rows:
                if r.get('state') in ('completed', 'failed') and r.get('agent_id') == 'worker':
                    affected += update_task(r.get('id', r.get('task_id', '')), state='completed')
            print(json.dumps({"affected": affected}))
        elif args.cmd == "parse":
            result = process_ai_reply(
                reply_text=getattr(args, 'reply_text', '') or "",
                role=getattr(args, 'role', 'manager') or "manager",
                raw_key=getattr(args, 'raw_key', '') or "",
                prompt_file=getattr(args, 'prompt_file', '') or "",
                worktree=getattr(args, 'worktree', '') or "",
                branch=getattr(args, 'branch', '') or "",
                session_id=getattr(args, 'session_id', '') or "")
            if result.get("ok"):
                print(json.dumps({"action": result.get("state", ""), "task_id": result.get("task_id", ""),
                                  "workers": result.get("workers", ""),
                                  "summary": result.get("summary", ""),
                                  "next": result.get("next", ""),
                                  "evidence": result.get("evidence", "")}))
            else:
                print(json.dumps({"action": "repair", "errors": result.get("errors", [])}))
        elif args.cmd == "extract":
            result = read_state_only(getattr(args, 'reply_text', '') or "")
            if result.get("ok"):
                print(json.dumps({"action": result.get("state", ""), "fields": result.get("fields", {})}))
            else:
                print(json.dumps({"action": "repair", "errors": result.get("errors", [])}))
        elif args.cmd == "active-workers":
            rows = list_active_workers(getattr(args, 'worktree', '') or "")
            print(json.dumps({"rows": rows}))
        elif args.cmd == "has-active-worker":
            rows = list_active_workers(getattr(args, 'worktree', '') or "")
            print("true" if rows else "false")
        elif args.cmd == "list-key":
            rows = list_by_raw_key(getattr(args, 'raw_key', '') or "")
            print(json.dumps(rows))
        elif args.cmd == "list-pending-delivery":
            rows = pending_delivery()
            print(json.dumps(rows))
        elif args.cmd == "update-send-to-ai":
            r = mark_delivered(_task_id)
            print(json.dumps({"affected": 1 if r else 0}))
        elif args.cmd == "update-worker-pid":
            r = set_worker_pid(_task_id, getattr(args, 'worker_pid', '') or "")
            print(json.dumps({"affected": 1 if r else 0}))
        elif args.cmd == "get-launched-pids":
            rows = launched_pids(getattr(args, 'raw_key', '') or "")
            print(json.dumps({"rows": rows}))
        elif args.cmd == "init":
            print(json.dumps({"ok": True}))
        elif args.cmd == "mark-stale":
            timeout = int(getattr(args, 'timeout_minutes', '30') or '30')
            affected = mark_stale(timeout)
            print(json.dumps({"affected": affected}))
        elif args.cmd == "a2a-exit":
            # ── AI explicitly sets A2A Task state via tool call ──
            # Standard A2A pattern: Agent declares state transition directly,
            # no text parsing needed. This is the primary exit path.
            from a2a_task_parser import normalize_state, VALID_STATES
            raw_state = getattr(args, 'state', '') or ''
            state = normalize_state(raw_state)
            if state not in VALID_STATES:
                print(json.dumps({"ok": False, "error": f"invalid state: {raw_state}"}))
            else:
                c = _client()
                r = c.create(
                    agent_id=getattr(args, 'role', 'manager') or "manager",
                    name=getattr(args, 'role', 'manager') or "manager",
                    raw_key=getattr(args, 'raw_key', '') or "",
                    worktree=getattr(args, 'worktree', '') or "",
                    branch=getattr(args, 'branch', '') or "",
                    prompt_file=getattr(args, 'prompt_file', '') or "",
                    session_id=getattr(args, 'session_id', '') or "",
                    message=getattr(args, 'summary', '') or "",
                    state=state,
                    summary=getattr(args, 'summary', '') or "",
                    next=getattr(args, 'next', '') or "",
                    evidence=getattr(args, 'evidence', '') or "",
                    worker_prompts_csv=getattr(args, 'workers', '') or "",
                )
                task_id = r.get("id", "")
                print(json.dumps({"ok": True, "task_id": task_id, "state": state,
                                  "exit_kind": state,
                                  "workers": getattr(args, 'workers', '') or "",
                                  "summary": getattr(args, 'summary', '') or "",
                                  "next": getattr(args, 'next', '') or "",
                                  "evidence": getattr(args, 'evidence', '') or ""}))
    except RuntimeError as e:
        print(json.dumps({"error": str(e)}))
    return 0


if __name__ == "__main__":
    exit(_main())
