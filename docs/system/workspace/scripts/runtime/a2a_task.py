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
import time
import threading
import http.client
from datetime import datetime, timezone
from typing import Optional, List, Dict, Callable

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
    return PROJECT or os.environ.get("SESSION_PARENT_PROJECT") or os.getcwd()


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

    def _rest_request(self, method: str, path: str, body: Optional[Dict] = None,
                      timeout: float = 30.0) -> dict:
        """Send standard HTTP request to A2A Server REST endpoints (bypass JSON-RPC).

        Used for Freely-specific operations (create, update) that carry
        extended fields (e.g., worker_pid, session_id)
        not preserved by the JSON-RPC tasks/send → execute() path.
        """
        self._ensure()
        if self._url:
            return self._http_request(method, path, body, timeout)
        # Unix socket: send standard HTTP request to REST endpoint
        data_bytes = json.dumps(body, default=str).encode() if body else b""
        request = (f"{method} {path} HTTP/1.1\r\n"
                   f"Host: localhost\r\n"
                   f"Content-Type: application/json\r\n"
                   f"Content-Length: {len(data_bytes)}\r\n"
                   f"Connection: close\r\n\r\n")

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect(self._socket_path)
            sock.sendall(request.encode() + data_bytes)
            data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk: break
                data += chunk
        finally:
            sock.close()
        return self._parse_response(data.decode("utf-8", errors="replace"))

    def _unix_request(self, method: str, path: str, body=None, timeout=30.0) -> dict:
        # Map REST-style paths to A2A JSON-RPC 2.0 methods.
        # The A2A Server uses official SDK create_jsonrpc_routes at POST /.
        _base = path.split("?")[0]
        _rpc_map = {
            ("POST", "/tasks"):            "tasks/send",
            ("GET",  "/tasks"):            "tasks/list",
            ("PATCH","/tasks"):            "tasks/push",
            ("GET",  "/tasks/latest-manager"):    "tasks/get",
        }
        # Build key: (method, base_path_stripped_of_task_id)
        import re
        _stripped = re.sub(r'/tasks/[^/]+', '/tasks', _base)
        rpc_method = _rpc_map.get((method, _stripped), f"tasks/{method.lower()}")
        params = body if body is not None else {}
        # If the path had a task_id segment, inject it
        _m = re.match(r'/tasks/([^/]+)', _base)
        if _m and "task_id" not in params:
            params = dict(params, taskId=_m.group(1))

        jsonrpc_req = {"jsonrpc": "2.0", "id": 1, "method": rpc_method, "params": params}
        http_body = json.dumps(jsonrpc_req, default=str, ensure_ascii=False)
        http_body_bytes = http_body.encode('utf-8')
        # Content-Length MUST be byte count (RFC 7230). len(str) causes
        # Content-Length mismatch for non-ASCII → h11 "Invalid HTTP request".
        request = (f"POST / HTTP/1.1\r\n"
                   f"Content-Type: application/json; charset=utf-8\r\n"
                   f"Content-Length: {len(http_body_bytes)}\r\n"
                   f"Connection: close\r\n\r\n")

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect(self._socket_path)
            sock.sendall(request.encode('ascii') + http_body_bytes)
            data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk: break
                data += chunk
        finally:
            sock.close()
        return self._parse_jsonrpc_response(data.decode("utf-8", errors="replace"))

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
        """Parse HTTP response body (legacy REST path — kept for _http_request)."""
        body_start = text.find("\r\n\r\n")
        if body_start == -1: body_start = text.find("\n\n")
        if body_start != -1: return json.loads(text[body_start + 4:])
        return {"error": "empty response"}

    @staticmethod
    def _parse_jsonrpc_response(text: str) -> dict:
        """Parse JSON-RPC 2.0 response from A2A Server."""
        body_start = text.find("\r\n\r\n")
        if body_start == -1: body_start = text.find("\n\n")
        body = text[body_start + 4:] if body_start != -1 else text
        try:
            rpc = json.loads(body)
        except json.JSONDecodeError:
            return {"error": "invalid JSON-RPC response", "raw": body[:200]}
        if "error" in rpc:
            err = rpc["error"]
            return {"error": err.get("message", str(err)), "code": err.get("code", -1)}
        result = rpc.get("result", {})
        # A2A SDK wraps results in Task objects; extract the data
        if isinstance(result, dict):
            return result
        return {"result": result}

    # ── Task API ───────────────────────────────────────────────────────

    def create(self, **kwargs) -> dict:
        """Create task via REST endpoint (preserves Freely-specific fields)."""
        return self._rest_request("POST", "/tasks", dict(kwargs))

    def get(self, task_id: str) -> Optional[dict]:
        r = self._request("GET", f"/tasks/{task_id}")
        return r if "id" in r else None

    def update(self, task_id: str, **fields) -> dict:
        """Update task via REST endpoint (preserves Freely-specific fields)."""
        return self._rest_request("PATCH", f"/tasks/{task_id}",
                                  dict(fields))

    def list(self, **filters) -> List[dict]:
        params = [f"{k}={v}" for k, v in filters.items() if v]
        path = "/tasks?" + "&".join(params) if params else "/tasks"
        return self._rest_request("GET", path).get("tasks", [])

    def latest_manager(self) -> Optional[dict]:
        """Get latest manager task via A2A Server (authoritative)."""
        r = self._rest_request("GET", "/tasks/latest-manager")
        return r if "task_id" in r else None

    def launched_pids(self, raw_key: str = "") -> List[dict]:
        """Get launched worker PIDs via A2A Server."""
        path = f"/tasks/launched-pids?raw_key={raw_key}" if raw_key else "/tasks/launched-pids"
        return self._rest_request("GET", path).get("rows", [])

    def add_message(self, task_id: str, role: str = "worker",
                    msg_type: str = "text", content: str = "") -> dict:
        """Add message via A2A Server endpoint."""
        return self._request("POST", f"/tasks/{task_id}/messages",
                            {"role": role, "type": msg_type, "content": content})

    def set_worker_pid(self, task_id: str, worker_pid: str) -> dict:
        """Set worker PID via A2A Server endpoint."""
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

    # ── SSE Client ────────────────────────────────────────────────────────

    def stream_task(self, task_id: str, on_event: Callable[[dict], None] = None,
                    timeout: float = 0, last_event_id: str = "") -> dict:
        """Connect to GET /tasks/{task_id}/stream and yield SSE events.

        Returns a dict with keys: 'status' (ok/error/timeout), 'events' (list of parsed
        events), 'last_event_id' (str|None), 'terminal' (bool — stream closed AND task
        is in a terminal state per A2A spec).
        """
        result = {"status": "ok", "events": [], "last_event_id": None, "terminal": False}
        sp = _a2a_socket_path(self.project)

        try:
            conn = http.client.HTTPConnection("localhost")
            conn.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            conn.sock.settimeout(timeout if timeout > 0 else 30.0)
            conn.sock.connect(sp)

            conn.putrequest("GET", f"/tasks/{task_id}/stream")
            conn.putheader("Accept", "text/event-stream")
            conn.putheader("Connection", "keep-alive")
            if last_event_id:
                conn.putheader("Last-Event-ID", last_event_id)
            conn.endheaders()

            resp = conn.getresponse()
            if resp.status != 200:
                result["status"] = "error"
                result["error"] = f"HTTP {resp.status}: {resp.read().decode()[:200]}"
                conn.close()
                return result

            event_type = ""
            event_data_lines = []
            event_id = ""

            while True:
                line = resp.readline().decode("utf-8", errors="replace")
                if line == "":
                    break
                line = line.rstrip("\n").rstrip("\r")

                if line.startswith("event:"):
                    event_type = line[6:].lstrip()
                elif line.startswith("data:"):
                    event_data_lines.append(line[5:].lstrip())
                elif line.startswith("id:"):
                    event_id = line[3:].lstrip()
                elif line == "" and event_data_lines:
                    event_data = "\n".join(event_data_lines)
                    event = self._parse_sse_event(event_type, event_data, event_id)
                    result["events"].append(event)
                    result["last_event_id"] = event_id or result["last_event_id"]
                    if on_event:
                        on_event(event)
                    event_type, event_data_lines, event_id = "", [], ""

            conn.close()

            # Determine if terminal: check task state after stream close
            try:
                task = self.get(task_id)
                state = task.get("state", task.get("status", ""))
                if state in ("completed", "failed", "canceled", "rejected"):
                    result["terminal"] = True
                else:
                    result["terminal"] = False
            except Exception:
                result["terminal"] = True  # Conservative: treat as terminal
            return result

        except socket.timeout:
            result["status"] = "timeout"
            return result
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            return result

    def _parse_sse_event(self, event_type: str, data: str, event_id: str) -> dict:
        """Parse an SSE event data payload into a dict."""
        event = {"event_type": event_type, "id": event_id}
        try:
            payload = json.loads(data)
            event.update(payload)
        except json.JSONDecodeError:
            event["raw_data"] = data
        return event

    def resubscribe(self, task_id: str, last_event_id: str = "",
                    on_event: Callable[[dict], None] = None,
                    max_retries: int = 6, base_delay: float = 1.0) -> dict:
        """Reconnect to SSE with exponential backoff after disconnect.

        Retry delays: base_delay → 2× → 4× → 8× → 16× → cap at 30s.
        Uses Last-Event-ID header for server-side resume on reconnect.
        Returns the last stream_task result (after max_retries or terminal).
        """
        delay = base_delay
        resume_id = last_event_id
        result = {"status": "error", "events": [], "last_event_id": last_event_id,
                  "terminal": False, "retries": 0}

        for attempt in range(max_retries):
            result = self.stream_task(task_id, on_event=on_event, timeout=30.0,
                                     last_event_id=resume_id)
            result["retries"] = attempt

            # Propagate latest event id for next retry
            if result.get("last_event_id"):
                resume_id = result["last_event_id"]

            # Stop if task is genuinely terminal
            if result["status"] == "ok" and result["terminal"]:
                return result

            # Retry on non-terminal disconnect or error
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay = min(delay * 2, 30.0)

        return result


_client_lock = threading.Lock()
_client_instance = None

def _client() -> A2AClient:
    global _client_instance
    if _client_instance is None:
        with _client_lock:
            if _client_instance is None:
                _client_instance = A2AClient(_resolve_project())
    return _client_instance

_sse_pool_lock = threading.Lock()
_sse_pool_instance = None

def _sse_pool() -> SSEPool:
    global _sse_pool_instance
    if _sse_pool_instance is None:
        with _sse_pool_lock:
            if _sse_pool_instance is None:
                _sse_pool_instance = SSEPool(_resolve_project())
    return _sse_pool_instance


# ── SSE Connection Pool ─────────────────────────────────────────────────

class SSEPool:
    """Manager-side SSE connection metadata registry (Phase 1 foundation).

    Phase 1: Tracks which tasks are being streamed, max 10 entries,
    heartbeat timestamps, stale detection. Does NOT open/manage actual
    connections — that integration happens in Phase 2 (freely bash script
    uses stream_task/resubscribe and calls SSEPool for bookkeeping).

    Phase 2 (planned): Integration with freely script — when Manager
    opens an SSE stream for a Worker, it registers in the pool. When
    stale_ids() returns tasks, Manager resubscribes or marks them dead.
    """

    def __init__(self, project: str, max_connections: int = 10):
        self.project = project
        self.max_connections = max_connections
        self._pool: Dict[str, Dict] = {}
        self._lock = threading.Lock()

    def active_count(self) -> int:
        with self._lock:
            return len(self._pool)

    def add(self, task_id: str, on_event: Callable[[dict], None] = None) -> bool:
        with self._lock:
            if task_id in self._pool:
                return True
            if len(self._pool) >= self.max_connections:
                return False
            self._pool[task_id] = {
                "task_id": task_id, "added_at": _now_utc(),
                "on_event": on_event, "last_event_at": None,
            }
            return True

    def remove(self, task_id: str):
        with self._lock:
            self._pool.pop(task_id, None)

    def heartbeat(self, task_id: str):
        with self._lock:
            if task_id in self._pool:
                self._pool[task_id]["last_event_at"] = _now_utc()

    def stale_ids(self, timeout_seconds: int = 120) -> List[str]:
        cutoff = datetime.now(timezone.utc)
        stale = []
        with self._lock:
            for tid, info in self._pool.items():
                last = info.get("last_event_at")
                if not last:
                    stale.append(tid)  # No heartbeat ever → stale
                else:
                    dt = datetime.strptime(last[:19], "%Y-%m-%dT%H:%M:%S")
                    if (cutoff - dt.replace(tzinfo=timezone.utc)).total_seconds() > timeout_seconds:
                        stale.append(tid)
        return stale

    def close_all(self):
        with self._lock:
            self._pool.clear()

    def list_active(self) -> List[str]:
        with self._lock:
            return list(self._pool.keys())


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

def set_worker_pid(task_id: str, worker_pid: str) -> int:
    return 1 if _client().set_worker_pid(task_id, worker_pid).get("ok") else 0

def launched_pids(raw_key: str = "") -> List[dict]:
    return _client().launched_pids(raw_key)

def mark_stale(timeout_minutes: int = 30) -> int:
    return _client().mark_stale(timeout_minutes)

# Legacy aliases (for backward compat with freely bash)
update_worker_pid = set_worker_pid
get_launched_pids = launched_pids


# ── AI Reply Processing ──────────────────────────────────────────────────

def process_ai_reply(reply_text: str, role: str = "manager", raw_key: str = "",
                     worktree: str = "", branch: str = "", session_id: str = "") -> dict:
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
            session_id=session_id,
            message=fields.get("summary", ""),
            state=state,
            summary=fields.get("summary", ""),
            next=fields.get("next", ""),
            evidence=fields.get("evidence", ""),
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


VALID_STATES = {
    'submitted', 'working', 'completed', 'failed',
    'input-required', 'pending-input',
}

STATE_ALIASES = {
    'delegate': 'submitted', 'delegated': 'submitted', 'dispatch': 'submitted',
    'working': 'submitted', 'active': 'submitted', 'in_progress': 'working',
    'in-progress': 'working', 'progress': 'working',
    'done': 'completed', 'success': 'completed', 'finished': 'completed',
    'complete': 'completed', 'ok': 'completed', 'good': 'completed',
    'completed_no_op': 'completed', 'clean_success': 'completed',
    'completed_with_findings': 'completed', 'partial_success': 'completed',
    'completed_s_hint': 'completed', 'completed_with_evidence': 'completed',
    'completed_idle': 'completed', 'completed_independent': 'completed',
    'task_already_done': 'completed', 'noop': 'completed',
    'all_done': 'completed', 'finished_no_op': 'completed',
    'completed_no_changes': 'completed', 'normal': 'completed',
    'stopped': 'failed', 'paused': 'failed', 'exit': 'failed',
    'nothing': 'failed', 'no_work': 'failed', 'idle': 'failed',
    'stop': 'failed', 'error': 'failed',
    'blocked': 'input-required', 'block': 'input-required',
    'needs_manager': 'pending-input', 'needs_input': 'pending-input',
    'handoff': 'pending-input',
}

def normalize_state(raw: str) -> str:
    s = raw.strip().lower().replace('-', '_').replace(' ', '_')
    return STATE_ALIASES.get(s, s)

# ── CLI ───────────────────────────────────────────────────────────────────

def _main() -> int:
    parser = argparse.ArgumentParser(description="A2A Protocol Client (JSON-RPC 2.0)")
    parser.add_argument("--project", default=None, help="Project path")
    sub = parser.add_subparsers(dest="cmd")

    p_create = sub.add_parser("create")
    p_create.add_argument("--skill", default="")
    p_create.add_argument("--worktree", default="")
    p_create.add_argument("--branch", default="")
    p_create.add_argument("--raw-key", default=None)
    p_create.add_argument("--message", default="")
    p_create.add_argument("--agent-id", default="manager")

    p_insert = sub.add_parser("insert")
    p_insert.add_argument("--role", default="manager")
    p_insert.add_argument("--raw-key", default="")
    p_insert.add_argument("--worktree", default="")
    p_insert.add_argument("--branch", default="")
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
    p_update.add_argument("--session-id", default=None, help="Worker ACP session ID")
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

    p_uwp = sub.add_parser("update-worker-pid")
    p_uwp.add_argument("--task-id", default="")
    p_uwp.add_argument("--worker-pid", default="")
    p_glp = sub.add_parser("get-launched-pids")
    p_glp.add_argument("--raw-key", default="")

    # ── prompt: send a message to a worker via A2A session/prompt ──
    p_prompt = sub.add_parser("prompt")
    p_prompt.add_argument("--task-id", required=True, help="Target A2A task ID")
    p_prompt.add_argument("--message", required=True, help="Message to send to worker")



    # ── session.* commands ──────────────────────────────────────────────
    p_sx = sub.add_parser("session-export")
    p_sx.add_argument("--session-id", default="", help="Session ID to export")
    p_sx.add_argument("--output", default="", help="Output JSONL path")

    p_si = sub.add_parser("session-import")
    p_si.add_argument("--path", required=True, help="JSONL file to import")

    p_slk = sub.add_parser("session-last-exit-kind")
    p_slk.add_argument("--session-id", required=True, help="Session ID")

    # init: no-op (daemon creates tables); kept for backward compat
    sub.add_parser("init")

    # mark-stale: mark timed-out working tasks as input-required
    p_ms = sub.add_parser("mark-stale")
    p_ms.add_argument("--timeout-minutes", default="30")

    # ── SSE: stream task events ─────────────────────────────────────────
    p_stream = sub.add_parser("stream")
    p_stream.add_argument("--task-id", required=True)
    p_stream.add_argument("--timeout", type=float, default=30.0)
    p_stream.add_argument("--last-event-id", default="")
    p_stream.add_argument("--no-print", action="store_true",
                          help="Suppress event printing")

    p_resub = sub.add_parser("resubscribe")
    p_resub.add_argument("--task-id", required=True)
    p_resub.add_argument("--last-event-id", default="")
    p_resub.add_argument("--max-retries", type=int, default=6)
    p_resub.add_argument("--base-delay", type=float, default=1.0)

    # ── SSE Pool management ─────────────────────────────────────────────
    p_spool = sub.add_parser("sse-pool")
    p_spool_sub = p_spool.add_subparsers(dest="pool_cmd")
    p_spool_add = p_spool_sub.add_parser("add")
    p_spool_add.add_argument("--task-id", required=True)
    p_spool_rm = p_spool_sub.add_parser("remove")
    p_spool_rm.add_argument("--task-id", required=True)
    p_spool_sub.add_parser("count")
    p_spool_sub.add_parser("list")
    p_spool_close = p_spool_sub.add_parser("close")

    # ── a2a-task-update: Worker mid-execution progress reporting ──
    p_tu = sub.add_parser("a2a-task-update")
    p_tu.add_argument("--task-id", required=True, help="Existing task ID")
    p_tu.add_argument("--state", default="working", help="A2A state (usually working)")
    p_tu.add_argument("--progress", default="", help="Progress description")
    p_tu.add_argument("--message", default="", help="Status message")
    p_tu.add_argument("--artifact", default="", help="Artifact file path or content")
    p_tu.add_argument("--error", default="", help="Error details (if state=failed)")

    # ── a2a-exit: AI explicitly sets A2A Task state (standard A2A pattern) ──
    p_exit = sub.add_parser("a2a-exit")
    p_exit.add_argument("--state", required=True, help="A2A state: submitted|working|completed|failed|input-required|pending-input")
    p_exit.add_argument("--summary", default="", help="Completion summary")
    p_exit.add_argument("--next", default="", help="Next action")
    p_exit.add_argument("--evidence", default="", help="Evidence paths")
    p_exit.add_argument("--role", default="manager", help="Role: manager|worker")
    p_exit.add_argument("--agent-id", default=None, help=argparse.SUPPRESS)  # deprecated, use --role
    p_exit.add_argument("--raw-key", default="", help="Raw issue key")
    p_exit.add_argument("--worktree", default="", help="Worktree path")
    p_exit.add_argument("--branch", default="", help="Branch name")
    p_exit.add_argument("--task-id", default="", help="Existing task ID (updates instead of creating)")
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
            args.state = normalize_state(args.exit_kind)

    try:
        if args.cmd == "create":
            tid = create_task(
                skill=getattr(args, 'skill', '') or "",
                worktree=getattr(args, 'worktree', '') or "",
                branch=getattr(args, 'branch', '') or "",
                raw_key=getattr(args, 'raw_key', None) or "",
                message=getattr(args, 'message', '') or "",
                agent_id=getattr(args, 'agent_id', 'manager') or "manager")
            print(json.dumps({"task_id": tid}))
        elif args.cmd == "insert":
            tid = create_task(
                agent_id=getattr(args, 'role', 'manager') or "manager",
                raw_key=getattr(args, 'raw_key', '') or "",
                worktree=getattr(args, 'worktree', '') or "",
                branch=getattr(args, 'branch', '') or "",
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
            if getattr(args, 'session_id', None): kwargs['session_id'] = args.session_id
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
            reply_file = getattr(args, 'reply_file', '') or ''
            reply_text = getattr(args, 'reply_text', '') or ""
            if reply_file and os.path.isfile(reply_file):
                with open(reply_file) as f:
                    reply_text = f.read()
            result = process_ai_reply(
                reply_text=reply_text,
                role=getattr(args, 'role', 'manager') or "manager",
                raw_key=getattr(args, 'raw_key', '') or "",
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
        elif args.cmd == "update-worker-pid":
            r = set_worker_pid(_task_id, getattr(args, 'worker_pid', '') or "")
            print(json.dumps({"affected": 1 if r else 0}))
        elif args.cmd == "get-launched-pids":
            rows = launched_pids(getattr(args, 'raw_key', '') or "")
            print(json.dumps({"rows": rows}))
        elif args.cmd == "prompt":
            # Send a message to a worker's ACP session via A2A Server.
            # This stores the message on the task and, if the A2A Server has an
            # active SSE connection to the worker, it will be delivered in real-time.
            task_id = getattr(args, 'task_id', '') or ''
            message = getattr(args, 'message', '') or ''
            try:
                c = _client()
                r = c.add_message(task_id, role="manager", msg_type="text", content=message[:32768])
                print(json.dumps({"ok": True, "task_id": task_id, "sent": len(message)}))
            except Exception as e:
                print(json.dumps({"ok": False, "error": str(e)}))

        elif args.cmd == "init":
            print(json.dumps({"ok": True}))

        elif args.cmd == "session-export":
            sid = getattr(args, 'session_id', '') or ''
            output = getattr(args, 'output', '') or ''
            if not output:
                output = f"/tmp/freely-session-{sid}.jsonl"
            # Export session rounds as JSONL
            try:
                c = _client()
                tasks = c.list(raw_key=sid) if sid else []
                with open(output, 'w') as f:
                    for t in tasks:
                        f.write(json.dumps(t, default=str) + "\n")
                print(json.dumps({"ok": True, "output": output, "count": len(tasks)}))
            except Exception as e:
                print(json.dumps({"ok": False, "error": str(e)}))
        elif args.cmd == "session-import":
            path = getattr(args, 'path', '') or ''
            count = 0
            try:
                with open(path) as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                data = json.loads(line)
                                c = _client()
                                c.create(**data)
                                count += 1
                            except Exception:
                                pass
                print(json.dumps({"ok": True, "imported": count}))
            except Exception as e:
                print(json.dumps({"ok": False, "error": str(e)}))
        elif args.cmd == "session-last-exit-kind":
            sid = getattr(args, 'session_id', '') or ''
            try:
                c = _client()
                tasks = c.list(raw_key=sid) if sid else []
                # Find last task with a state set by a2a-exit
                for t in reversed(tasks):
                    state = t.get('state', '')
                    if state in ('submitted', 'completed', 'failed', 'working', 'input-required', 'pending-input'):
                        print(state)
                        break
                else:
                    print("")
            except Exception:
                print("")

        elif args.cmd == "mark-stale":
            timeout = int(getattr(args, 'timeout_minutes', '30') or '30')
            affected = mark_stale(timeout)
            print(json.dumps({"affected": affected}))

        elif args.cmd == "stream":
            c = _client()
            on_ev = None
            if not getattr(args, 'no_print', False):
                def _print_event(ev):
                    print(json.dumps(ev, ensure_ascii=False), flush=True)
                on_ev = _print_event
            result = c.stream_task(args.task_id, on_event=on_ev,
                                   timeout=args.timeout,
                                   last_event_id=getattr(args, 'last_event_id', '') or '')
            if result["status"] != "ok":
                print(json.dumps({"error": result.get("error", result["status"])}))

        elif args.cmd == "resubscribe":
            c = _client()
            on_ev = None
            if not getattr(args, 'no_print', False):
                def _print_event_r(ev):
                    print(json.dumps(ev, ensure_ascii=False), flush=True)
                on_ev = _print_event_r
            result = c.resubscribe(args.task_id, args.last_event_id,
                                   on_event=on_ev,
                                   max_retries=args.max_retries,
                                   base_delay=args.base_delay)
            print(json.dumps({"status": result["status"],
                              "terminal": result["terminal"],
                              "retries": result.get("retries", 0)}))

        elif args.cmd == "sse-pool":
            pool = _sse_pool()
            if args.pool_cmd == "add":
                ok = pool.add(args.task_id)
                print(json.dumps({"ok": ok, "active_count": pool.active_count()}))
            elif args.pool_cmd == "remove":
                pool.remove(args.task_id)
                print(json.dumps({"ok": True, "active_count": pool.active_count()}))
            elif args.pool_cmd == "count":
                print(json.dumps({"count": pool.active_count()}))
            elif args.pool_cmd == "list":
                print(json.dumps({"tasks": pool.list_active()}))
            elif args.pool_cmd == "close":
                pool.close_all()
                print(json.dumps({"ok": True, "message": "pool closed"}))
        elif args.cmd == "a2a-task-update":
            task_id = getattr(args, 'task_id', '') or ''
            if not task_id:
                print(json.dumps({"ok": False, "error": "--task-id is required"}))
            else:
                c = _client()
                fields = {"state": getattr(args, 'state', 'working') or "working"}
                if getattr(args, 'progress', ''): fields["progress"] = args.progress
                if getattr(args, 'message', ''): fields["summary"] = args.message
                if getattr(args, 'artifact', ''): fields["evidence_paths"] = args.artifact
                if getattr(args, 'error', ''): fields["error"] = args.error
                r = c.update(task_id, **fields)
                print(json.dumps({"ok": True, "task_id": task_id, "state": fields["state"]}))
        elif args.cmd == "a2a-exit":
            # Backward compat: --agent-id maps to --role (deprecated, use --role)
            if getattr(args, 'agent_id', None) and getattr(args, 'role', 'manager') == 'manager':
                args.role = args.agent_id
            raw_state = getattr(args, 'state', '') or ''
            state = normalize_state(raw_state)
            if state not in VALID_STATES:
                print(json.dumps({"ok": False, "error": f"invalid state: {raw_state}"}))
            else:
                c = _client()
                existing_task_id = getattr(args, 'task_id', '') or ''
                if existing_task_id:
                    r = c.update(existing_task_id, state=state,
                                 summary=getattr(args, 'summary', '') or "",
                                 next=getattr(args, 'next', '') or "",
                                 evidence=getattr(args, 'evidence', '') or "")
                    task_id = existing_task_id
                else:
                    r = c.create(
                        agent_id=getattr(args, 'role', 'manager') or "manager",
                        name=getattr(args, 'role', 'manager') or "manager",
                        raw_key=getattr(args, 'raw_key', '') or "",
                        worktree=getattr(args, 'worktree', '') or "",
                        branch=getattr(args, 'branch', '') or "",
                        session_id=getattr(args, 'session_id', '') or "",
                        message=getattr(args, 'summary', '') or "",
                        state=state,
                        summary=getattr(args, 'summary', '') or "",
                        next=getattr(args, 'next', '') or "",
                        evidence=getattr(args, 'evidence', '') or "",
                    )
                    task_id = r.get("id", "")
                run_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", ".freely", "run")
                try:
                    os.makedirs(run_dir, exist_ok=True)
                    with open(os.path.join(run_dir, "last-exit-task.env"), "w") as f:
                        workers_val = getattr(args, 'workers', '') or ''
                        f.write(f"TASK_ID={task_id}\nSTATE={state}\n")
                except Exception:
                    pass
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
