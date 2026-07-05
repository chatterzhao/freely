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
    agent_list_by_raw_key, agent_next_free, agent_assign, agent_get_session,
    acp_session_connect
)
from input_required_reason import InputRequiredReason


def _acp_bridge_socket(project: str, base_tool: str = "") -> Optional[str]:
    """Find the ACP bridge Unix socket for this project/tool."""
    import hashlib
    h = hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]
    suffix = f"-{base_tool}" if base_tool else ""
    sock_path = f"/tmp/freely-acp-{h}{suffix}.sock"
    return sock_path if os.path.exists(sock_path) else None


def _acp_rpc(project: str, method: str, params: dict, base_tool: str = "") -> Optional[dict]:
    """Send a JSON-RPC call to the ACP bridge and return the result."""
    bridge = _acp_bridge_socket(project, base_tool)
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







def watchdog_run(project: str, a2a_socket: str):
    """Main Watchdog loop: subscribe to SSE, handle events.

    Runs liveness/staleness checks on a background timer via socket timeout,
    so they execute even during an active SSE connection (not just on reconnect).
    """
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

        # Run checks between reconnections too (belt-and-suspenders)
        if time.time() - last_liveness_check > 120:
            try:
                _check_agent_liveness(project)
                last_liveness_check = time.time()
            except Exception:
                pass
        try:
            _check_session_staleness(project)
        except Exception:
            pass


def _subscribe_and_process(project: str, a2a_socket: str):
    """Connect to A2A SSE and process events.

    Uses socket timeout to periodically run liveness/staleness checks
    even during an active SSE connection (not just on reconnect).
    """
    import socket as sock

    s = sock.socket(sock.AF_UNIX, sock.SOCK_STREAM)
    s.settimeout(30.0)  # 30s recv timeout → periodic background checks
    s.connect(a2a_socket)
    s.sendall(b"GET /tasks/stream HTTP/1.1\r\nHost: localhost\r\nAccept: text/event-stream\r\n\r\n")

    buf = b""
    # Timer state as mutable dict (so _run_periodic_checks can update it)
    _timers = {"last_liveness": time.time(), "last_staleness": 0.0}
    LIVENESS_INTERVAL = 120.0  # C12: every 2 minutes
    STALENESS_INTERVAL = 300.0  # C13: every 5 minutes

    while True:
        try:
            chunk = s.recv(4096)
        except sock.timeout:
            # Timeout is expected — run background checks while SSE is idle
            _run_periodic_checks(project, _timers, LIVENESS_INTERVAL, STALENESS_INTERVAL)
            continue
        except OSError:
            break  # socket closed

        if not chunk:
            break
        buf += chunk
        while b"\n\n" in buf:
            event, buf = buf.split(b"\n\n", 1)
            _handle_sse_event(project, event.decode())

        # After processing events, run checks if intervals have elapsed
        now = time.time()
        if now - _timers["last_liveness"] > LIVENESS_INTERVAL or now - _timers["last_staleness"] > STALENESS_INTERVAL:
            _run_periodic_checks(project, _timers, LIVENESS_INTERVAL, STALENESS_INTERVAL)


def _run_periodic_checks(project: str, timers: dict,
                         liveness_interval: float, staleness_interval: float):
    """Run liveness/staleness checks if their intervals have elapsed.

    Updates timers dict in-place so intervals are respected across calls.
    """
    now = time.time()
    if now - timers["last_liveness"] > liveness_interval:
        try:
            _check_agent_liveness(project)
            timers["last_liveness"] = now
        except Exception:
            pass
    if now - timers["last_staleness"] > staleness_interval:
        try:
            _check_session_staleness(project)
            timers["last_staleness"] = now
        except Exception:
            pass


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

    # Metadata fields are top-level in the SSE data dict (see PATCH handler L773-795)
    metadata = {
        k: data.get(k, "") for k in (
            "reason", "from_agent", "needs_agent", "needs_role",
            "raw_key", "message", "task_id", "review_stage",
            "verdict", "completion_summary", "summary", "required_fixes",
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
    """Worker/Manager needs reviewer."""
    raw_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")

    existing = agent_list_by_raw_key(project, raw_key)
    rid = None
    if existing and existing.get("reviewer_id"):
        rid = existing["reviewer_id"].split(":")[0] if ":" in str(existing.get("reviewer_id", "")) else existing.get("reviewer_id", "")
    if not rid:
        rid = agent_next_free(project, "reviewer", 99)
    if not rid:
        print(f"[watchdog] no reviewer available for {raw_key}", file=sys.stderr)
        return

    is_gate = (reason == InputRequiredReason.NEEDS_REVIEW_GATE)
    task_msg = _build_review_task_message(raw_key, from_agent, reason)
    reviewer_slot = _get_agent_slot(project, "reviewer", rid)

    sid, op = acp_session_connect(
        project, raw_key, "reviewer", rid,
        slot=reviewer_slot, message=task_msg,
        force_new=is_gate
    )
    if sid:
        print(f"[watchdog] reviewer {rid} connected via {op} session={sid[:20]}... for {raw_key}", file=sys.stderr)
    else:
        print(f"[watchdog] reviewer {rid} session creation failed for {raw_key}", file=sys.stderr)


def _build_review_task_message(raw_key: str, from_agent: str, reason: InputRequiredReason) -> str:
    """Build the initial review task prompt for a Reviewer session."""
    stage = reason.value.split(":")[-1] if ":" in reason.value else reason.value
    return (
        f"[Freely Watchdog] {from_agent} 需要审查。\n"
        f"raw_key: {raw_key}\n"
        f"审查阶段: {stage}\n"
        f"原因: {reason.value}\n"
        f"请根据 Skill 指令进行审查，完成后调 a2a-exit 声明 verdict。"
    )


def _handle_needs_manager(project: str, metadata: dict, reason: InputRequiredReason):
    """Agent needs manager decision. Resume manager ACP session."""
    issue_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")
    MANAGER_KEY = "__manager__"
    print(f"[watchdog] routing to manager: {from_agent} needs decision on {issue_key} ({reason.value})", file=sys.stderr)

    mgr_msg = f"[Freely Watchdog] {from_agent} needs manager input on {issue_key}. Reason: {reason.value}."
    manager_slot = _get_agent_slot(project, "manager", "manager_01")

    sid, op = acp_session_connect(
        project, MANAGER_KEY, "manager", "manager_01",
        slot=manager_slot, message=mgr_msg
    )
    if sid:
        print(f"[watchdog] manager connected via {op} session={sid[:20]}...", file=sys.stderr)
    else:
        print(f"[watchdog] could not route to manager — needs human attention", file=sys.stderr)

def _handle_needs_worker(project: str, metadata: dict, reason: InputRequiredReason):
    """Reviewer/Manager needs worker retry/task."""
    raw_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")
    verdict_msg = _build_worker_verdict_message(raw_key, from_agent, reason, metadata)
    print(f"[watchdog] routing to worker for {raw_key}: {reason.value} (from {from_agent})", file=sys.stderr)

    row = agent_list_by_raw_key(project, raw_key)
    wid = None
    if row and row.get("worker_id"):
        wid = row["worker_id"].split(":")[0] if ":" in str(row.get("worker_id", "")) else row.get("worker_id", "")
    if not wid:
        wid = agent_next_free(project, "worker", 10)
    if not wid:
        print(f"[watchdog] no worker available, delegating to manager", file=sys.stderr)
        _handle_needs_manager(project, metadata, InputRequiredReason.from_string("needs-manager-decision"))
        return

    worker_slot = _get_agent_slot(project, "worker", wid)
    sid, op = acp_session_connect(
        project, raw_key, "worker", wid,
        slot=worker_slot, message=verdict_msg
    )
    if sid:
        print(f"[watchdog] worker {wid} connected via {op} session={sid[:20]}... for {raw_key}", file=sys.stderr)
    else:
        print(f"[watchdog] worker {wid} session creation failed, delegating to manager", file=sys.stderr)
        _handle_needs_manager(project, metadata, InputRequiredReason.from_string("needs-manager-decision"))

def _build_worker_verdict_message(raw_key: str, from_agent: str,
                                   reason: InputRequiredReason, metadata: dict) -> str:
    """Build the verdict/fix message for a Worker session.

    Includes verdict details from metadata (if available) so the Worker
    doesn't need to query a2a_tasks for the reviewer's findings.
    """
    parts = [
        f"[Freely Watchdog] {from_agent} 有反馈给你。",
        f"raw_key: {raw_key}",
        f"原因: {reason.value}",
    ]
    # Include reviewer's verdict details if present in SSE metadata
    verdict = metadata.get("verdict", "")
    if verdict:
        parts.append(f"审查结论: {verdict}")
    summary = metadata.get("summary", metadata.get("completion_summary", ""))
    if summary:
        parts.append(f"摘要: {summary}")
    message = metadata.get("message", "")
    if message:
        parts.append(f"消息: {message}")
    parts.append("请根据 Skill 指令处理，完成后调 a2a-exit 声明状态。")
    return "\n".join(parts)


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


# ── CLI Entry Point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Freely SSE Watchdog (Python)")
    parser.add_argument("--project", required=True, help="Project root path")
    parser.add_argument("--a2a-socket", required=True, help="Path to A2A Unix socket")
    args = parser.parse_args()
    print(f"[watchdog] starting: project={args.project} socket={args.a2a_socket}", file=sys.stderr)
    watchdog_run(args.project, args.a2a_socket)


def _get_agent_slot(project: str, role: str, agent_id: str) -> str:
    """Get slot from agent-table for a given role/agent."""
    try:
        import subprocess, os
        aq = os.path.join(project, "bin", "agent-table-query")
        if os.path.isfile(aq):
            result = subprocess.run([aq, "--get-slot", agent_id],
                                    capture_output=True, text=True, cwd=project)
            return result.stdout.strip()
    except Exception:
        pass
    return ""
