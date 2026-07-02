"""Runtime Watchdog — SSE subscriber for input-required events.
Monitors A2A SSE stream, detects when new agents need to be created,
and routes input-required events to the correct handler."""

import json
import time
import urllib.request
import os
import sys
import socket as _socket
from typing import Optional

# Add project root for imports
PROJECT_ROOT = os.environ.get("PROJECT_ROOT", os.getcwd())
sys.path.insert(0, os.path.join(PROJECT_ROOT, "docs", "system", "workspace", "scripts", "runtime"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "docs", "system", "workspace", "agents"))

from agent_working import (
    agent_list_by_raw_key, agent_next_free, agent_assign, agent_get_session
)
from input_required_reason import InputRequiredReason


def _acp_bridge_socket(project: str) -> Optional[str]:
    """Find the ACP bridge Unix socket for this project."""
    import hashlib
    h = hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]
    sock_path = f"/tmp/freely-acp-{h}.sock"
    return sock_path if os.path.exists(sock_path) else None


def _acp_rpc(project: str, method: str, params: dict) -> Optional[dict]:
    """Send a JSON-RPC call to the ACP bridge and return the result."""
    bridge = _acp_bridge_socket(project)
    if not bridge:
        return None
    try:
        s = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(bridge)
        req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}) + "\n"
        s.sendall(req.encode())
        resp = s.recv(4096)
        s.close()
        return json.loads(resp.decode())
    except Exception as e:
        print(f"[watchdog] ACP RPC error ({method}): {e}", file=sys.stderr)
        return None


def _acp_session_resume(project: str, session_id: str, prompt: str = None) -> bool:
    """Resume an existing ACP session with optional prompt."""
    params = {"sessionId": session_id}
    if prompt:
        params["prompt"] = prompt
    result = _acp_rpc(project, "session/resume", params)
    if result and "error" not in result:
        print(f"[watchdog] ACP session resume ok: {session_id}", file=sys.stderr)
        return True
    return False


def _acp_session_new(project: str, role: str, agent_id: str, slot: str = None) -> Optional[str]:
    """Create a new ACP session and return the session_id."""
    params = {"role": role, "agentId": agent_id}
    if slot:
        params["slot"] = slot
    result = _acp_rpc(project, "session/new", params)
    if result and "result" in result:
        sid = result["result"].get("sessionId", "")
        if sid:
            print(f"[watchdog] ACP session/new: {agent_id} → {sid}", file=sys.stderr)
            return sid
    return None


def watchdog_run(project: str, a2a_socket: str):
    """Main Watchdog loop: subscribe to SSE, handle events."""
    sse_url = f"unix://{a2a_socket}/tasks/stream"
    backoff = 1
    max_backoff = 30
    last_liveness_check = 0

    while True:
        try:
            _subscribe_and_process(project, a2a_socket)
            backoff = 1  # reset on clean disconnect
        except Exception as e:
            print(f"[watchdog] SSE error: {e}, reconnecting in {backoff}s", file=sys.stderr)
            time.sleep(backoff)
            backoff = min(backoff * 2, max_backoff)

        # C12: periodic agent crash detection
        if time.time() - last_liveness_check > 120:
            try:
                _check_agent_liveness(project)
                last_liveness_check = time.time()
            except Exception:
                pass

        # C13: periodic session staleness check
        try:
            _check_session_staleness(project)
        except Exception:
            pass


def _subscribe_and_process(project: str, a2a_socket: str):
    """Connect to A2A SSE and process events."""
    import http.client
    import socket as sock

    # Connect via Unix socket
    s = sock.socket(sock.AF_UNIX, sock.SOCK_STREAM)
    s.connect(a2a_socket)
    s.sendall(b"GET /tasks/stream HTTP/1.1\r\nHost: localhost\r\nAccept: text/event-stream\r\n\r\n")

    buf = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk
        while b"\n\n" in buf:
            event, buf = buf.split(b"\n\n", 1)
            _handle_sse_event(project, event.decode())


def _handle_sse_event(project: str, event_text: str):
    """Parse SSE event and route based on reason."""
    data = {}
    for line in event_text.split("\n"):
        if line.startswith("data: "):
            try:
                data = json.loads(line[6:])
            except json.JSONDecodeError:
                pass

    # A2A _notify_sse sends: {"task_id":..., "state":..., "reason":..., ...}
    # The event format is flat (not wrapped in statusUpdate), matching what
    # _notify_sse in a2a_server.py constructs at PATCH time.
    state = data.get("state", "")
    if state != "input-required":
        return

    # Metadata fields are top-level in the SSE data dict (see PATCH handler L740-745)
    metadata = {
        k: data.get(k, "") for k in (
            "reason", "from_agent", "needs_agent", "needs_role",
            "raw_key", "message", "task_id", "review_stage",
        )
    }
    reason_str = metadata.get("reason", "")
    reason = InputRequiredReason.from_string(reason_str)
    needs_role = reason.needs_role

    print(f"[watchdog] input-required: reason={reason.value} needs_role={needs_role}", file=sys.stderr)

    if needs_role == "reviewer":
        _handle_needs_reviewer(project, metadata, reason)
    elif needs_role == "manager":
        _handle_needs_manager(project, metadata, reason)
    elif needs_role == "worker":
        _handle_needs_worker(project, metadata, reason)


def _normalize_raw_key(raw_key: str) -> str:
    """Ensure raw_key has the 'raw-' prefix for consistent lookups."""
    if not raw_key:
        return raw_key
    return f"raw-{raw_key}" if not raw_key.startswith("raw-") else raw_key


def _handle_needs_reviewer(project: str, metadata: dict, reason: InputRequiredReason):
    """Worker/Manager needs reviewer. Create reviewer agent if not exists."""
    raw_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")

    # Check if reviewer already exists for this raw_key
    existing = agent_list_by_raw_key(project, raw_key)
    if existing and existing.get("reviewer_id"):
        # Reviewer already assigned — resume session if exists
        sid = agent_get_session(project, raw_key, "reviewer")
        if sid:
            print(f"[watchdog] reviewer session {sid} exists for {raw_key}, resuming", file=sys.stderr)
            _acp_session_resume(project, sid, f"Reviewer needed for {raw_key}, reason: {reason.value}")
        else:
            print(f"[watchdog] reviewer assigned but no session for {raw_key}, creating new session", file=sys.stderr)
            # Create ACP session for the reviewer
            rid = existing["reviewer_id"].split(":")[0] if ":" in str(existing.get("reviewer_id", "")) else existing.get("reviewer_id", "")
            if rid:
                new_sid = _acp_session_new(project, "reviewer", rid)
                if new_sid:
                    agent_assign(project, raw_key, "reviewer", f"{rid}:{new_sid}")
        return

    # Allocate next free reviewer
    reviewer_id = agent_next_free(project, "reviewer", 99)
    if not reviewer_id:
        print(f"[watchdog] no free reviewer slots", file=sys.stderr)
        return

    print(f"[watchdog] creating reviewer {reviewer_id} for {raw_key} (requested by {from_agent})", file=sys.stderr)
    # Create ACP session for the new reviewer
    new_sid = _acp_session_new(project, "reviewer", reviewer_id)
    if new_sid:
        agent_assign(project, raw_key, "reviewer", f"{reviewer_id}:{new_sid}")
        print(f"[watchdog] reviewer {reviewer_id} session={new_sid} assigned to {raw_key}", file=sys.stderr)
    else:
        # Session creation failed — still record the assignment for retry
        agent_assign(project, raw_key, "reviewer", reviewer_id)
        print(f"[watchdog] reviewer {reviewer_id} assigned (no session yet, will retry)", file=sys.stderr)


def _handle_needs_manager(project: str, metadata: dict, reason: InputRequiredReason):
    """Agent needs manager decision. Resume manager ACP session."""
    raw_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")
    print(f"[watchdog] routing to manager: {from_agent} needs decision on {raw_key} ({reason.value})", file=sys.stderr)

    # Look up manager session from agent_working
    sid = agent_get_session(project, raw_key, "manager")
    if sid:
        prompt = f"[Watchdog] Agent {from_agent} needs manager input on {raw_key}. Reason: {reason.value}.\nContinue from where you left off."
        if _acp_session_resume(project, sid, prompt):
            print(f"[watchdog] manager session {sid} resumed for {raw_key}", file=sys.stderr)
            return

    # No manager session — check if manager exists in agent_working
    row = agent_list_by_raw_key(project, raw_key)
    if row and row.get("manager_id"):
        mid = row["manager_id"].split(":")[0] if ":" in str(row.get("manager_id", "")) else row.get("manager_id", "")
        if mid:
            new_sid = _acp_session_new(project, "manager", mid)
            if new_sid:
                agent_assign(project, raw_key, "manager", f"{mid}:{new_sid}")
                print(f"[watchdog] created manager session {new_sid} for {raw_key}", file=sys.stderr)
                return

    print(f"[watchdog] could not route to manager for {raw_key} — needs human attention", file=sys.stderr)


def _handle_needs_worker(project: str, metadata: dict, reason: InputRequiredReason):
    """Reviewer/Manager needs worker retry/task. Resume worker ACP session."""
    raw_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")
    print(f"[watchdog] routing to worker for {raw_key}: {reason.value} (from {from_agent})", file=sys.stderr)

    # Resume worker ACP session if exists
    sid = agent_get_session(project, raw_key, "worker")
    if sid:
        prompt = f"[Watchdog] Agent {from_agent} requests your input on {raw_key}. Reason: {reason.value}.\nContinue."
        if _acp_session_resume(project, sid, prompt):
            print(f"[watchdog] worker session {sid} resumed for {raw_key}", file=sys.stderr)
            return

    # No worker session — try to create one from agent_working
    row = agent_list_by_raw_key(project, raw_key)
    if row and row.get("worker_id"):
        wid = row["worker_id"].split(":")[0] if ":" in str(row.get("worker_id", "")) else row.get("worker_id", "")
        if wid:
            new_sid = _acp_session_new(project, "worker", wid)
            if new_sid:
                agent_assign(project, raw_key, "worker", f"{wid}:{new_sid}")
                print(f"[watchdog] created worker session {new_sid} for {raw_key}", file=sys.stderr)
                return

    # Last resort: delegate back to manager
    print(f"[watchdog] no worker session for {raw_key}, delegating to manager", file=sys.stderr)
    _handle_needs_manager(project, metadata, InputRequiredReason.from_string("NEEDS_MANAGER_INPUT"))


# ── C12: Agent crash detection ────────────────────────────────────────────────

def _check_agent_liveness(project: str):
    """C12: Scan agent_working for dead agent processes and mark them."""
    import subprocess
    try:
        from agent_working import _db_rpc
        result = _db_rpc(project, "agent_working.get_all", {})
        rows = result.get("rows", [])
    except Exception:
        return

    for row in rows:
        raw_key = row.get("raw_key", "")
        for role in ("worker", "reviewer", "manager"):
            val = str(row.get(f"{role}_id", "") or "")
            if not val or ":" not in val:
                continue
            agent_id, session_id = val.split(":", 1)
            # Check if the process for this session is still alive
            try:
                # Look for a process with this session_id in the command line
                result = subprocess.run(
                    ["pgrep", "-f", session_id],
                    capture_output=True, text=True, timeout=3
                )
                if result.returncode != 0:
                    print(f"[watchdog] DEAD {role}: {agent_id} session={session_id} for {raw_key}", file=sys.stderr)
                    # Clear the dead session_id but keep the agent assigned
                    try:
                        _db_rpc(project, "agent_working.upsert", {
                            "raw_key": raw_key,
                            f"{role}_id": agent_id  # session_id cleared
                        })
                    except Exception:
                        pass
            except Exception as e:
                print(f"[watchdog] liveness check error for {agent_id}: {e}", file=sys.stderr)


# ── C13: Session staleness timeout ────────────────────────────────────────────

_last_staleness_check = 0
STALENESS_INTERVAL = 300  # 5 minutes between staleness scans
SESSION_STALE_SECONDS = 1800  # 30 minutes without activity = stale


def _check_session_staleness(project: str):
    """C13: Periodically scan for stale agent sessions and clean them up."""
    global _last_staleness_check
    now = time.time()
    if now - _last_staleness_check < STALENESS_INTERVAL:
        return
    _last_staleness_check = now

    try:
        from agent_working import _db_rpc, agent_release
        result = _db_rpc(project, "agent_working.get_all", {})
        rows = result.get("rows", [])
    except Exception:
        return

    for row in rows:
        raw_key = row.get("raw_key", "")
        for role in ("worker", "reviewer", "manager"):
            val = str(row.get(f"{role}_id", "") or "")
            if not val:
                continue
            # Stale: assigned but no session_id (never started within timeout)
            if ":" not in val:
                agent_id = val
                print(f"[watchdog] STALE {role} {agent_id} for {raw_key}: assigned but never started — releasing", file=sys.stderr)
                try:
                    agent_release(project, raw_key, role, agent_id)
                except Exception as e:
                    print(f"[watchdog] release failed for {agent_id}: {e}", file=sys.stderr)
