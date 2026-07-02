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
    """Resume an existing ACP session with optional prompt.

    When prompt is provided: session/resume + prompt = wake up + deliver message.
    This is the primary mechanism for agent-to-agent message delivery.
    Returns after session resume confirmation (does NOT wait for AI completion).
    """
    params = {"sessionId": session_id}
    if prompt:
        params["prompt"] = prompt
    result = _acp_rpc(project, "session/resume", params)
    if result and "error" not in result:
        print(f"[watchdog] ACP session resume ok: {session_id[:20]}...", file=sys.stderr)
        return True
    return False


def _acp_session_prompt(project: str, session_id: str, message: str) -> bool:
    """Send a message to an ALIVE ACP session.

    Semantic wrapper around _acp_session_resume. Use this when the target
    agent's session is known to be alive (e.g., Worker waiting for Reviewer
    verdict). The message is delivered via session/resume + prompt.

    For dead sessions, use _acp_session_resume without prompt first,
    then _acp_session_prompt after resume succeeds.
    """
    return _acp_session_resume(project, session_id, prompt=message)


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


def _acp_session_fork(project: str, parent_role: str, child_role: str,
                      child_agent_id: str, raw_key: str) -> Optional[str]:
    """Fork a child session from parent agent's session.

    Forks from Manager session — inherits project governance context
    (CONSTITUTION, LAWS, codebase map) without Worker's implementation bias.

    Manager session is stored under hardcoded key "__manager__" (Manager has
    no issue key — it's the orchestrator, not tied to any raw issue).
    Returns session_id on success, None on failure.
    """
    # Manager session stored under "__manager__", not issue raw_key
    lookup_key = "__manager__" if parent_role == "manager" else raw_key
    mgr_sid = agent_get_session(project, lookup_key, parent_role)
    if not mgr_sid:
        print(f"[watchdog] no {parent_role} session to fork from (key={lookup_key})", file=sys.stderr)
        return None

    params = {
        "sessionId": mgr_sid,
        "role": child_role,
        "agentId": child_agent_id,
    }
    result = _acp_rpc(project, "session/fork", params)
    if result and "result" in result:
        sid = result["result"].get("sessionId", "")
        if sid:
            print(f"[watchdog] ACP session/fork: {parent_role}→{child_role} {child_agent_id} → {sid}", file=sys.stderr)
            return sid
    print(f"[watchdog] ACP session/fork failed, will fallback to session/new", file=sys.stderr)
    return None


def _should_use_fork(project: str, raw_key: str, reason: InputRequiredReason) -> bool:
    """Determine if session/fork from Manager is appropriate.

    session/fork from Manager is safe because Manager has governance context
    but NOT Worker's implementation details (Manager runs in develop worktree).
    session/fork from Worker is FORBIDDEN (self-review bias).

    session/new is used for:
    - Gate reviews (needs-review:gate) — maximum impartiality for critical gates
    - Cross-tool scenarios — different AI tool can't fork
    """
    # Gate review: always use session/new for maximum impartiality
    if reason == InputRequiredReason.NEEDS_REVIEW_GATE:
        return False

    # Manager session is stored under hardcoded raw_key "__manager__"
    # (Manager has no issue key — it's the orchestrator, not tied to any raw issue)
    mgr_sid = agent_get_session(project, "__manager__", "manager")
    if not mgr_sid:
        return False

    # Check same tool (simplified: same project = same tool config)
    # Full implementation would compare agent-table slot values
    return True


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
    """Worker/Manager needs reviewer.

    Session selection decision tree (§19 in brainstorms.md):
      1. Same raw_key previously reviewed? → session/resume (best cache + impartial)
      2. Gate review (needs-review:gate)? → session/new always (impartiality > cache)
      3. Manager session available + same tool? → session/fork (cache + neutral)
      4. Fallback → session/new (cold start, maximum impartiality)

    session/fork from Manager is safe: Manager has governance context
    (CONSTITUTION, LAWS, codebase) but NOT Worker's implementation details.
    session/fork from Worker is FORBIDDEN (self-review bias).
    """
    raw_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")

    # Step 1: Check if reviewer already exists for this raw_key
    existing = agent_list_by_raw_key(project, raw_key)
    if existing and existing.get("reviewer_id"):
        sid = agent_get_session(project, raw_key, "reviewer")
        if sid:
            # Same reviewer has alive session → send review task via prompt
            task_msg = _build_review_task_message(raw_key, from_agent, reason)
            if _acp_session_prompt(project, sid, task_msg):
                print(f"[watchdog] review task delivered to reviewer {sid[:20]}... for {raw_key}", file=sys.stderr)
                return
            # Prompt failed (session dead / bridge error) — log and return.
            # Do NOT fall through: would allocate a second reviewer for same raw_key.
            print(f"[watchdog] reviewer session {sid[:20]}... prompt failed for {raw_key}, will retry on next cycle", file=sys.stderr)
            return
        else:
            # Reviewer assigned but session dead → try fork from Manager, then new
            rid = existing["reviewer_id"].split(":")[0] if ":" in str(existing.get("reviewer_id", "")) else existing.get("reviewer_id", "")
            if rid:
                print(f"[watchdog] reviewer {rid} assigned but session dead for {raw_key}", file=sys.stderr)
                _create_reviewer_session(project, raw_key, rid, from_agent, reason)
            return

    # Step 2: Allocate next free reviewer
    reviewer_id = agent_next_free(project, "reviewer", 99)
    if not reviewer_id:
        print(f"[watchdog] no free reviewer slots", file=sys.stderr)
        return

    print(f"[watchdog] dispatching reviewer {reviewer_id} for {raw_key} (from {from_agent}, reason={reason.value})", file=sys.stderr)
    _create_reviewer_session(project, raw_key, reviewer_id, from_agent, reason)


def _create_reviewer_session(project: str, raw_key: str, reviewer_id: str,
                              from_agent: str, reason: InputRequiredReason):
    """Create reviewer session using decision tree: fork → new.

    Tries session/fork from Manager first (cache + impartial).
    Falls back to session/new (cold start, maximum impartiality).
    Gate reviews ALWAYS use session/new.
    """
    session_mode = "new"  # default
    session_id = None

    # Gate reviews: session/new always (maximum impartiality for critical gates)
    if reason == InputRequiredReason.NEEDS_REVIEW_GATE:
        print(f"[watchdog] gate review → session/new (impartiality priority)", file=sys.stderr)
        session_id = _acp_session_new(project, "reviewer", reviewer_id)
        session_mode = "new"

    # Try fork from Manager (safe: Manager is neutral, has governance context)
    elif _should_use_fork(project, raw_key, reason):
        print(f"[watchdog] attempting session/fork from Manager for {reviewer_id}", file=sys.stderr)
        session_id = _acp_session_fork(project, "manager", "reviewer", reviewer_id, raw_key)
        if session_id:
            session_mode = "fork"
        else:
            # Fork failed → fallback to session/new
            print(f"[watchdog] fork failed, falling back to session/new", file=sys.stderr)
            session_id = _acp_session_new(project, "reviewer", reviewer_id)
            session_mode = "new"

    # Fallback: session/new
    else:
        print(f"[watchdog] session/new for {reviewer_id} (no fork available)", file=sys.stderr)
        session_id = _acp_session_new(project, "reviewer", reviewer_id)
        session_mode = "new"

    # Record assignment in agent_working (UPDATE ONLY — Worker created the row)
    if session_id:
        result = agent_assign(project, raw_key, "reviewer", f"{reviewer_id}:{session_id}",
                              update_only=True)
        if result and result.get("status") == "error":
            print(f"[watchdog] ERROR: reviewer update failed for {raw_key}: {result.get('message','')} — worktree may be closed", file=sys.stderr)
        else:
            print(f"[watchdog] reviewer {reviewer_id} session={session_id[:20]}... mode={session_mode} for {raw_key}", file=sys.stderr)
        # Deliver the review task to the newly created session
        task_msg = _build_review_task_message(raw_key, from_agent, reason)
        if not _acp_session_prompt(project, session_id, task_msg):
            print(f"[watchdog] WARNING: task delivery failed for {reviewer_id} session={session_id[:20]}...", file=sys.stderr)
    else:
        # Session creation failed — record assignment for retry (update_only)
        agent_assign(project, raw_key, "reviewer", reviewer_id, update_only=True)
        print(f"[watchdog] reviewer {reviewer_id} assigned (no session, will retry)", file=sys.stderr)


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
    """Agent needs manager decision. Resume manager ACP session.

    Manager uses hardcoded raw_key "__manager__" — it has no issue key.
    Manager is the orchestrator, running on develop worktree, with no
    associated test worktree.
    """
    issue_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")
    MANAGER_KEY = "__manager__"
    print(f"[watchdog] routing to manager: {from_agent} needs decision on {issue_key} ({reason.value})", file=sys.stderr)

    mgr_msg = f"[Freely Watchdog] {from_agent} needs manager input on {issue_key}. Reason: {reason.value}."

    # Step 1: Try session/prompt to alive manager session (keyed by __manager__)
    sid = agent_get_session(project, MANAGER_KEY, "manager")
    if sid:
        if _acp_session_prompt(project, sid, mgr_msg):
            print(f"[watchdog] manager session {sid[:20]}... notified", file=sys.stderr)
            return
        print(f"[watchdog] manager session dead, creating new", file=sys.stderr)

    # Step 2: No alive session — get or create manager entry
    # Manager is always manager_01 (pool=1). Bootstrap the __manager__ row
    # on first call if it doesn't exist yet.
    row = agent_list_by_raw_key(project, MANAGER_KEY)
    mid = None
    if row and row.get("manager_id"):
        mid = row["manager_id"].split(":")[0] if ":" in str(row.get("manager_id", "")) else row.get("manager_id", "")
    if not mid:
        mid = "manager_01"  # Manager always uses manager_01 (pool=1)

    new_sid = _acp_session_new(project, "manager", mid)
    if new_sid:
        agent_assign(project, MANAGER_KEY, "manager", f"{mid}:{new_sid}")
        _acp_session_prompt(project, new_sid, mgr_msg)
        print(f"[watchdog] manager {mid} session={new_sid[:20]}... bootstrapped" if not row else f"[watchdog] manager {mid} session={new_sid[:20]}...", file=sys.stderr)
        return

    print(f"[watchdog] could not route to manager for {issue_key} — needs human attention", file=sys.stderr)


def _handle_needs_worker(project: str, metadata: dict, reason: InputRequiredReason):
    """Reviewer/Manager needs worker retry/task.

    Decision tree (same pattern as Reviewer):
      1. Worker session alive? → _acp_session_prompt (投递消息到活 session)
      2. Session dead? → _acp_session_resume 复活 → prompt
      3. No session? → fork from Manager → prompt
      4. Fork fails? → session/new → prompt
      5. Last resort → delegate to Manager

    ACP sessions persist across AI cycles (bridge idle timeout only checks
    AI responsiveness during active prompt processing, not between calls).
    So session/prompt to an alive Worker session is the normal happy path.
    """
    raw_key = _normalize_raw_key(metadata.get("raw_key", ""))
    from_agent = metadata.get("from_agent", "")
    verdict_msg = _build_worker_verdict_message(raw_key, from_agent, reason, metadata)
    print(f"[watchdog] routing to worker for {raw_key}: {reason.value} (from {from_agent})", file=sys.stderr)

    # Step 1: Try session/prompt to alive session
    sid = agent_get_session(project, raw_key, "worker")
    if sid:
        if _acp_session_prompt(project, sid, verdict_msg):
            print(f"[watchdog] worker verdict delivered to {sid[:20]}... for {raw_key}", file=sys.stderr)
            return
        print(f"[watchdog] worker session {sid[:20]}... dead, trying fork/new", file=sys.stderr)

    # Step 2: Get worker_id from agent_working
    row = agent_list_by_raw_key(project, raw_key)
    wid = None
    if row and row.get("worker_id"):
        wid = row["worker_id"].split(":")[0] if ":" in str(row.get("worker_id", "")) else row.get("worker_id", "")

    if wid:
        # Step 2a: Try fork from Manager first (cache savings, same as Reviewer path)
        session_id = _acp_session_fork(project, "manager", "worker", wid, raw_key)
        if session_id:
            agent_assign(project, raw_key, "worker", f"{wid}:{session_id}")
            print(f"[watchdog] worker {wid} forked from Manager session={session_id[:20]}... for {raw_key}", file=sys.stderr)
            _acp_session_prompt(project, session_id, verdict_msg)
            return

        # Step 2b: Fallback to session/new
        new_sid = _acp_session_new(project, "worker", wid)
        if new_sid:
            agent_assign(project, raw_key, "worker", f"{wid}:{new_sid}")
            print(f"[watchdog] worker {wid} new session={new_sid[:20]}... for {raw_key}", file=sys.stderr)
            _acp_session_prompt(project, new_sid, verdict_msg)
            return

    # Step 3: Last resort — delegate back to manager
    print(f"[watchdog] no worker session for {raw_key}, delegating to manager", file=sys.stderr)
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
