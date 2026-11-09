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
from agent_identity_value import (
    bare_agent_ids, first_agent_id, parse_agent_entries, session_entry,
)
from input_required_reason import InputRequiredReason


import time as _time

def _log(msg: str) -> None:
    """Timestamped watchdog log line (routing forensics need instance-attributable timestamps)."""
    ts = _time.strftime("%H:%M:%SZ", _time.gmtime())
    print(f"[watchdog {ts}] {msg}", file=sys.stderr)


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
        _log(f"ACP RPC error ({method}): {e}")
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
            _log(f"SSE error: {e}, reconnecting in {backoff}s")
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
    """Parse SSE event and route based on event type."""
    data = {}
    for line in event_text.split("\n"):
        if line.startswith("data: "):
            try:
                data = json.loads(line[6:])
            except json.JSONDecodeError:
                pass

    # ── message_added: agent-to-agent message via A2A → ACP delivery ──
    event_type = data.get("event_type", "")
    if event_type == "message_added":
        _handle_message_delivery(project, data)
        return

    # A2A _notify_sse sends: {"task_id":..., "state":..., "reason":..., ...}
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

    _log(f"input-required: reason={reason.value} needs_role={needs_role}")

    if needs_role == "reviewer":
        _handle_needs_reviewer(project, metadata, reason)
    elif needs_role == "manager":
        _handle_needs_manager(project, metadata, reason)
    elif needs_role == "worker":
        _handle_needs_worker(project, metadata, reason)


def _normalize_raw_key(raw_key: str) -> str:
    """Ensure raw_key has the 'raw-' prefix for consistent lookups."""
    from raw_key_canon import try_canonicalize_raw_key
    if not raw_key:
        return raw_key
    return try_canonicalize_raw_key(raw_key, default=raw_key)


def _handle_needs_reviewer(project: str, metadata: dict, reason: InputRequiredReason):
    """Worker/Manager needs reviewer."""
    raw_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")

    try:
        existing = agent_list_by_raw_key(project, raw_key) if raw_key else {}
    except Exception as e:
        _log(f"FAIL-CLOSED: agent_working query failed for reviewer route: {e}")
        return
    rid = None
    if existing and existing.get("reviewer_id"):
        rid = first_agent_id(existing["reviewer_id"])
    if not rid:
        if not raw_key:
            _log("FAIL-CLOSED: missing raw_key for reviewer assign")
            return
        try:
            rid = agent_next_free(project, "reviewer", 99, raw_key=raw_key)
        except Exception as e:
            _log(f"FAIL-CLOSED: reviewer next_free_and_assign failed: {e}")
            return
    if not rid:
        _log(f"no reviewer available for {raw_key}")
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
        _log(f"reviewer {rid} connected via {op} session={sid[:20]}... for {raw_key}")
    else:
        _log(f"reviewer {rid} session creation failed for {raw_key}")


def _build_review_task_message(raw_key: str, from_agent: str, reason: InputRequiredReason) -> str:
    """Build the initial review task prompt for a Reviewer session."""
    stage = reason.value.split(":")[-1] if ":" in reason.value else reason.value
    return (
        f"[Freely Watchdog] {from_agent} 需要审查。\n"
        f"raw_key: {raw_key}\n"
        f"审查阶段: {stage}\n"
        f"原因: {reason.value}\n"
        f"请根据 Skill 指令进行审查，完成后执行 `a2a-exit --state completed --summary '<verdict-json>' --role reviewer`。"
    )


def _handle_needs_manager(project: str, metadata: dict, reason: InputRequiredReason):
    """Agent needs manager decision. Resume manager ACP session."""
    issue_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")
    MANAGER_KEY = "__manager__"
    _log(f"routing to manager: {from_agent} needs decision on {issue_key} ({reason.value})")

    mgr_msg = f"[Freely Watchdog] {from_agent} needs manager input on {issue_key}. Reason: {reason.value}."
    try:
        mid = agent_next_free(project, "manager", 1, raw_key=MANAGER_KEY)
    except Exception as e:
        _log(f"FAIL-CLOSED: manager assign failed: {e}")
        return
    if not mid:
        _log("FAIL-CLOSED: no manager available")
        return
    manager_slot = _get_agent_slot(project, "manager", mid)

    sid, op = acp_session_connect(
        project, MANAGER_KEY, "manager", mid,
        slot=manager_slot, message=mgr_msg
    )
    if sid:
        _log(f"manager connected via {op} session={sid[:20]}...")
    else:
        _log("could not route to manager — needs human attention")

def _handle_needs_worker(project: str, metadata: dict, reason: InputRequiredReason):
    """Reviewer/Manager needs worker retry/task."""
    raw_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")
    verdict_msg = _build_worker_verdict_message(raw_key, from_agent, reason, metadata)
    _log(f"routing to worker for {raw_key}: {reason.value} (from {from_agent})")

    try:
        row = agent_list_by_raw_key(project, raw_key) if raw_key else {}
    except Exception as e:
        _log(f"FAIL-CLOSED: agent_working query failed for worker route: {e}")
        return
    wid = None
    if row and row.get("worker_id"):
        wid = first_agent_id(row["worker_id"])
    if not wid:
        if not raw_key:
            _log("FAIL-CLOSED: missing raw_key for worker assign")
            return
        try:
            wid = agent_next_free(project, "worker", 10, raw_key=raw_key)
        except Exception as e:
            _log(f"FAIL-CLOSED: worker next_free_and_assign failed: {e}")
            return
    if not wid:
        _log("no worker available, delegating to manager")
        _handle_needs_manager(project, metadata, InputRequiredReason.from_string("needs-manager-decision"))
        return

    worker_slot = _get_agent_slot(project, "worker", wid)
    sid, op = acp_session_connect(
        project, raw_key, "worker", wid,
        slot=worker_slot, message=verdict_msg
    )
    if sid:
        _log(f"worker {wid} connected via {op} session={sid[:20]}... for {raw_key}")
    else:
        _log(f"worker {wid} session creation failed, delegating to manager")
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


# ── message_added: A2A message delivery via ACP session/prompt ───────────────

def _handle_message_delivery(project: str, data: dict):
    """Deliver an A2A message to the target agent via ACP session/prompt.

    Called when A2A Server emits a message_added SSE event.
    Looks up the target agent's session_id from agent_working table,
    then uses ACP bridge to forward the message via session/prompt.
    """
    task_id = data.get("task_id", "")
    role = data.get("role", "")
    content = data.get("content", "")
    if not task_id or not content:
        return

    # Get the raw_key from a2a_tasks to look up agent session
    import sqlite3
    db_path = os.path.join(project, ".freely", "freely.db")
    raw_key = ""
    task_agent_id = ""
    try:
        db = sqlite3.connect("file:" + db_path + "?mode=ro", uri=True)
        row = db.execute(
            "SELECT raw_key, agent_id FROM a2a_tasks WHERE task_id=?", (task_id,)
        ).fetchone()
        if row:
            raw_key = row[0] or ""
            task_agent_id = row[1] or ""
        db.close()
    except Exception:
        pass

    if not raw_key:
        _log(f"message_delivery: no raw_key for task {task_id[:16]}")
        return

    # Look up the target agent's session from agent_working
    row = agent_list_by_raw_key(project, raw_key)
    if not row:
        _log(f"message_delivery: no agent_working row for {raw_key}")
        return

    # Resolve one exact agent/session pair. Reviewer fields can contain multiple
    # entries, so selecting the final colon-delimited token is not valid.
    requested_agent_id = str(data.get("agent_id", "") or "")
    if not requested_agent_id and str(task_agent_id).startswith(f"{role}_"):
        requested_agent_id = str(task_agent_id)
    selected = session_entry(row.get(f"{role}_id", ""), requested_agent_id)
    if not selected:
        _log(f"message_delivery: no session for {role}/{requested_agent_id or '*'} on {raw_key}")
        return
    target_agent_id, session_id = selected

    slot = _get_agent_slot(project, role, target_agent_id)
    base_tool = slot.split("-", 1)[0] if slot else ""

    # Deliver via ACP session/prompt
    result = _acp_rpc(project, "session/prompt",
                      {"sessionId": session_id, "prompt": content},
                      base_tool=base_tool)
    if result:
        print(f"[watchdog] message_delivery: {role} session={session_id[:16]} "
              f"task={task_id[:16]} ok", file=sys.stderr)
    else:
        print(f"[watchdog] message_delivery: ACP failed for {role} "
              f"session={session_id[:16]}", file=sys.stderr)


# ── C12: Agent crash detection ────────────────────────────────────────────────

def _session_state(project: str, role: str, agent_id: str, session_id: str) -> str:
    """Classify a session via ACP session/ping: alive / dead / unknown.

    `unknown` (bridge unreachable, or an error unrelated to the session) must
    not clear a binding: a transient bridge outage is not proof of death.
    """
    slot = _get_agent_slot(project, role, agent_id)
    base_tool = slot.split("-", 1)[0] if slot else ""
    result = _acp_rpc(project, "session/ping", {"sessionId": session_id}, base_tool=base_tool)
    if not isinstance(result, dict):
        return "unknown"
    error = result.get("error")
    if error:
        text = json.dumps(error, ensure_ascii=False).lower()
        return "dead" if "session" in text else "unknown"
    return "alive" if "result" in result else "unknown"


def _check_agent_liveness(project: str):
    """C12: Scan agent_working for dead agent sessions and mark them."""
    try:
        from agent_working import _db_rpc
        result = _db_rpc(project, "agent_working.get_all", {})
        rows = result.get("rows", [])
    except Exception:
        return

    for row in rows:
        raw_key = row.get("raw_key", "")
        for role in ("worker", "reviewer", "manager"):
            entries = parse_agent_entries(row.get(f"{role}_id", ""))
            for agent_id, session_id in entries.items():
                if not session_id:
                    continue
                try:
                    state = _session_state(project, role, agent_id, session_id)
                    if state == "unknown":
                        _log(f"UNKNOWN {role}: {agent_id} session={session_id} for {raw_key}")
                        continue
                    if state == "alive":
                        continue
                    _log(f"DEAD {role}: {agent_id} session={session_id} for {raw_key}")
                    try:
                        _db_rpc(project, "agent_working.upsert", {
                            "raw_key": raw_key,
                            "col": f"{role}_id",
                            "val": agent_id,
                        })
                    except Exception:
                        pass
                except Exception as e:
                    _log(f"liveness check error for {agent_id}: {e}")


# ── C13: Session staleness timeout ────────────────────────────────────────────

_last_staleness_check = 0
STALENESS_INTERVAL = 300  # 5 minutes between staleness scans
SESSION_STALE_SECONDS = 1800  # 30 minutes without activity = stale


def _reservation_is_stale(row: dict, now: float) -> bool:
    """Only release bare reservations after the configured inactivity window."""
    from datetime import datetime, timezone

    updated_at = str(row.get("updated_at", "") or "").strip()
    if not updated_at:
        return False
    try:
        normalized = updated_at.replace("Z", "+00:00")
        updated = datetime.fromisoformat(normalized)
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=timezone.utc)
        return now - updated.timestamp() >= SESSION_STALE_SECONDS
    except ValueError:
        return False


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
        if not _reservation_is_stale(row, now):
            continue
        raw_key = row.get("raw_key", "")
        for role in ("worker", "reviewer", "manager"):
            for agent_id in bare_agent_ids(row.get(f"{role}_id", "")):
                _log(f"STALE {role} {agent_id} for {raw_key}: assigned but never started — releasing")
                try:
                    agent_release(project, raw_key, role, agent_id)
                except Exception as e:
                    _log(f"release failed for {agent_id}: {e}")


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


# ── CLI Entry Point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Freely SSE Watchdog (Python)")
    parser.add_argument("--project", required=True, help="Project root path")
    parser.add_argument("--a2a-socket", required=True, help="Path to A2A Unix socket")
    args = parser.parse_args()
    _log(f"starting: project={args.project} socket={args.a2a_socket}")
    watchdog_run(args.project, args.a2a_socket)


