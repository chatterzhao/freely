"""Runtime Watchdog — SSE subscriber for input-required events.
Monitors A2A SSE stream, detects when new agents need to be created,
and routes input-required events to the correct handler."""

import json
import time
import urllib.request
import os
import sys
from typing import Optional

# Add project root for imports
PROJECT_ROOT = os.environ.get("PROJECT_ROOT", os.getcwd())
sys.path.insert(0, os.path.join(PROJECT_ROOT, "docs", "system", "workspace", "scripts", "runtime"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "docs", "system", "workspace", "agents"))

from agent_working import (
    agent_list_by_raw_key, agent_next_free, agent_assign, agent_get_session
)
from input_required_reason import InputRequiredReason


def watchdog_run(project: str, a2a_socket: str):
    """Main Watchdog loop: subscribe to SSE, handle events."""
    sse_url = f"http://localhost/tasks/stream"
    backoff = 1
    max_backoff = 30

    while True:
        try:
            _subscribe_and_process(project, a2a_socket)
            backoff = 1  # reset on clean disconnect
        except Exception as e:
            print(f"[watchdog] SSE error: {e}, reconnecting in {backoff}s", file=sys.stderr)
            time.sleep(backoff)
            backoff = min(backoff * 2, max_backoff)


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

    state = data.get("statusUpdate", {}).get("status", {}).get("state", "")
    if state != "input-required":
        return

    metadata = data.get("statusUpdate", {}).get("metadata", {})
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


def _handle_needs_reviewer(project: str, metadata: dict, reason: InputRequiredReason):
    """Worker/Manager needs reviewer. Create reviewer agent if not exists."""
    raw_key = metadata.get("raw_key", "")
    from_agent = metadata.get("from_agent", "")

    # Check if reviewer already exists for this raw_key
    existing = agent_list_by_raw_key(project, raw_key)
    if existing and existing.get("reviewer_id"):
        print(f"[watchdog] reviewer already assigned for {raw_key}, skipping", file=sys.stderr)
        return

    # Allocate next free reviewer
    reviewer_id = agent_next_free(project, "reviewer", 99)
    if not reviewer_id:
        print(f"[watchdog] no free reviewer slots", file=sys.stderr)
        return

    print(f"[watchdog] creating reviewer {reviewer_id} for {raw_key} (requested by {from_agent})", file=sys.stderr)
    # Record in agent_working table
    try:
        agent_assign(project, raw_key, "reviewer", reviewer_id)
        print(f"[watchdog] reviewer {reviewer_id} assigned to {raw_key}", file=sys.stderr)
    except Exception as e:
        print(f"[watchdog] failed to assign reviewer: {e}", file=sys.stderr)


def _handle_needs_manager(project: str, metadata: dict, reason: InputRequiredReason):
    """Agent needs manager decision. Manager already has session (resume)."""
    raw_key = metadata.get("raw_key", "")
    from_agent = metadata.get("from_agent", "")
    print(f"[watchdog] routing to manager: {from_agent} needs decision on {raw_key}", file=sys.stderr)


def _handle_needs_worker(project: str, metadata: dict, reason: InputRequiredReason):
    """Reviewer/Manager needs worker retry/task. Resume or notify worker."""
    raw_key = metadata.get("raw_key", "")
    from_agent = metadata.get("from_agent", "")
    print(f"[watchdog] routing to worker for {raw_key}: {reason.value} (from {from_agent})", file=sys.stderr)
    # Resume worker ACP session if exists
    session = agent_get_session(project, raw_key, "worker")
    if session:
        print(f"[watchdog] worker session {session} found for {raw_key}, routing guidance", file=sys.stderr)
    else:
        print(f"[watchdog] no worker session for {raw_key}, delegating to manager", file=sys.stderr)
