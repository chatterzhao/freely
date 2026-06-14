#!/usr/bin/env python3
"""acp_bridge_v2.py — ACP Bridge using official agent-client-protocol SDK.

Replaces the hand-rolled JSON-RPC in acp-bridge.py with the official
agent-client-protocol SDK (v0.10.1). Provides a persistent Unix-socket
relay between AI CLI agents (claude-agent-acp, codex-acp, opencode) and
Freely's monitor scripts.

Key improvements over v1:
- Uses acp.Agent / acp.Client from the official SDK (Pydantic models)
- ACP-native SessionUpdate enum (AgentThoughtChunk, Plan, etc.)
- Fixed threading: proper thread lifecycle, consistent locking, watchdog
- Legacy fallback via FREELY_ACP_LEGACY_FALLBACK=1 environment variable
"""

import argparse
import hashlib
import json
import os
import signal
import socket
import sys
import threading
import time
from datetime import datetime, timezone
from typing import Optional, Dict, List

# ── Official ACP SDK ──────────────────────────────────────────────────────
try:
    from acp import (
        Agent, Client,
        NewSessionRequest, PromptRequest,
        SessionNotification,
        InitializeRequest, InitializeResponse,
        SetSessionModeRequest,
        spawn_agent_process,
        connect_to_agent,
    )
    from acp.helpers import (
        text_block,
        start_tool_call,
        update_agent_message,
        update_agent_thought,
        update_tool_call,
    )
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _short_hash(project: str) -> str:
    return hashlib.sha256(os.path.abspath(project).encode()).hexdigest()[:16]


def _socket_path(project: str) -> str:
    return f"/tmp/freely-acp-{_short_hash(project)}.sock"


def _pid_file(project: str) -> str:
    return f"/tmp/freely-acp-{_short_hash(project)}.pid"


# ── Legacy fallback import ────────────────────────────────────────────────
def _use_legacy() -> bool:
    return os.environ.get("FREELY_ACP_LEGACY_FALLBACK", "0") == "1"


# ── ACP Bridge V2 ──────────────────────────────────────────────────────────

class AcpBridgeV2:
    """Persistent ACP bridge using the official agent-client-protocol SDK.

    Manages the lifecycle of an ACP agent subprocess (e.g. claude-agent-acp),
    exposes a Unix socket for client connections, and handles session
    creation, resumption, and prompt dispatch.
    """

    def __init__(self, project: str, acp_bin: str, acp_args: Optional[List[str]] = None,
                 session_timeout: int = 1800, idle_timeout: int = 900):
        self.project = os.path.abspath(project)
        self.acp_bin = acp_bin
        self.acp_args = acp_args or []
        self.socket_path = _socket_path(self.project)
        self.pid_file = _pid_file(self.project)
        self.session_timeout = session_timeout
        self.idle_timeout = idle_timeout

        # Session state
        self._lock = threading.RLock()
        self._agent: Optional[Agent] = None
        self._session_id: Optional[str] = None
        self._clients: List[socket.socket] = []
        self._running = False
        self._watchdog_thread: Optional[threading.Thread] = None
        self._last_activity: float = 0.0

    # ── Lifecycle ────────────────────────────────────────────────────────

    def start(self) -> None:
        """Start the bridge: spawn agent, create socket, begin serving."""
        if not SDK_AVAILABLE:
            raise RuntimeError("agent-client-protocol SDK not installed")
        if not os.path.exists(self.acp_bin) and self.acp_bin != "claude-agent-acp":
            # For PATH-based binaries, the SDK handles resolution
            pass

        with self._lock:
            self._running = True
            self._last_activity = time.time()
            self._spawn_agent()
            self._start_watchdog()

        self._write_pid()
        self._serve()

    def stop(self) -> None:
        """Gracefully stop the bridge."""
        with self._lock:
            self._running = False
            self._stop_watchdog()
            for client in self._clients:
                try:
                    client.close()
                except Exception:
                    pass
            self._clients.clear()
        self._cleanup_files()

    # ── Agent management ─────────────────────────────────────────────────

    def _spawn_agent(self) -> None:
        """Spawn the ACP agent subprocess using the SDK."""
        cmd = [self.acp_bin] + self.acp_args
        self._agent = spawn_agent_process(cmd)
        self._log(f"agent spawned: {' '.join(cmd)}")

    def _restart_agent(self) -> None:
        """Restart the agent subprocess after a crash."""
        with self._lock:
            # Join old process if possible
            self._session_id = None
            self._spawn_agent()

    # ── Watchdog ─────────────────────────────────────────────────────────

    def _start_watchdog(self) -> None:
        """Start watchdog thread to monitor agent health."""
        def _watch():
            while True:
                with self._lock:
                    if not self._running:
                        break
                time.sleep(5)
                with self._lock:
                    if not self._running:
                        break
                    idle = time.time() - self._last_activity
                    if idle > self.idle_timeout:
                        self._log(f"idle timeout ({idle:.0f}s > {self.idle_timeout}s), restarting agent")
                        self._restart_agent()
                        self._last_activity = time.time()

        self._watchdog_thread = threading.Thread(target=_watch, daemon=True)
        self._watchdog_thread.start()

    def _stop_watchdog(self) -> None:
        """Stop the watchdog thread."""
        # Daemon thread will exit when self._running is False
        pass

    # ── Session management ───────────────────────────────────────────────

    def session_new(self, cwd: str = "", mcp_servers: Optional[List] = None,
                    permission_mode: str = "default") -> Optional[str]:
        """Create a new ACP session via the SDK."""
        with self._lock:
            if self._agent is None:
                self._spawn_agent()
            try:
                req = NewSessionRequest(
                    cwd=cwd or self.project,
                    mcpServers=mcp_servers or [],
                )
                resp = self._agent.new_session(req)
                self._session_id = resp.sessionId
                self._last_activity = time.time()

                # Apply permission mode for Claude-specific behavior
                if permission_mode != "default":
                    try:
                        mode_req = SetSessionModeRequest(mode=permission_mode)
                        self._agent.set_mode(mode_req)
                    except Exception:
                        pass  # Non-Claude agents may not support set_mode

                return self._session_id
            except Exception as e:
                self._log(f"session_new failed: {e}")
                return None

    def session_resume(self, session_id: str, cwd: str = "") -> Optional[str]:
        """Resume an existing ACP session."""
        with self._lock:
            if self._agent is None:
                return None
            try:
                req = NewSessionRequest(
                    cwd=cwd or self.project,
                    resume=session_id,
                )
                resp = self._agent.new_session(req)
                self._session_id = resp.sessionId
                self._last_activity = time.time()
                return self._session_id
            except Exception as e:
                self._log(f"session_resume failed: {e}")
                return None

    def session_prompt(self, prompt_text: str) -> dict:
        """Send a prompt and collect the response with structured updates."""
        with self._lock:
            if self._agent is None or self._session_id is None:
                return {"error": "no active session"}

            self._last_activity = time.time()
            result = {
                "stop_reason": "",
                "text": "",
                "tool_calls": [],
                "thoughts": [],
                "plan": None,
                "context_ratio": None,
            }

            try:
                req = PromptRequest(
                    sessionId=self._session_id,
                    blocks=[text_block(prompt_text)],
                )
                resp = self._agent.prompt(req)

                # Collect structured response
                result["stop_reason"] = getattr(resp, "stopReason", "") or ""
                result["context_ratio"] = getattr(resp, "contextRatio", None)

                for update in getattr(resp, "updates", []) or []:
                    kind = getattr(update, "kind", "")
                    if kind == "agent_message_chunk":
                        chunk = getattr(update, "text", "")
                        result["text"] += chunk
                    elif kind == "agent_thought_chunk":
                        thought = getattr(update, "text", "")
                        result["thoughts"].append(thought)
                    elif kind == "tool_call":
                        result["tool_calls"].append({
                            "call_id": getattr(update, "callId", ""),
                            "name": getattr(update, "name", ""),
                            "arguments": getattr(update, "arguments", {}),
                        })
                    elif kind == "tool_call_update":
                        result["tool_calls"].append({
                            "call_id": getattr(update, "callId", ""),
                            "status": getattr(update, "status", ""),
                            "output": getattr(update, "output", ""),
                        })
                    elif kind == "plan":
                        result["plan"] = {
                            "steps": getattr(update, "steps", []),
                        }
                    elif kind == "current_mode_update":
                        result["mode"] = getattr(update, "mode", "")

            except Exception as e:
                result["error"] = str(e)
                self._log(f"session_prompt error: {e}")

            return result

    # ── Unix socket server ───────────────────────────────────────────────

    def _serve(self) -> None:
        """Accept client connections on Unix socket and handle JSON-RPC requests."""
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.socket_path)
        server.listen(5)
        server.settimeout(1.0)
        os.chmod(self.socket_path, 0o600)

        self._log(f"listening on {self.socket_path}")

        while True:
            with self._lock:
                if not self._running:
                    break
            try:
                client, _ = server.accept()
                t = threading.Thread(target=self._handle_client, args=(client,), daemon=True)
                with self._lock:
                    self._clients.append(client)
                t.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self._running:
                    self._log(f"accept error: {e}")

        server.close()
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)

    def _handle_client(self, client: socket.socket) -> None:
        """Handle a single client connection with JSON-RPC protocol."""
        client.settimeout(30.0)
        try:
            data = b""
            while True:
                try:
                    chunk = client.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    if b"\n" in data:
                        break
                except socket.timeout:
                    break

            if not data:
                return

            request = json.loads(data.decode("utf-8", errors="replace"))
            method = request.get("method", "")
            req_id = request.get("id", 0)
            params = request.get("params", {})

            response = self._dispatch(method, params)
            response["jsonrpc"] = "2.0"
            response["id"] = req_id

            client.sendall(json.dumps(response, default=str).encode() + b"\n")
        except Exception as e:
            try:
                client.sendall(json.dumps({
                    "jsonrpc": "2.0", "id": 0,
                    "error": {"code": -32603, "message": str(e)},
                }).encode() + b"\n")
            except Exception:
                pass
        finally:
            with self._lock:
                if client in self._clients:
                    self._clients.remove(client)
            try:
                client.close()
            except Exception:
                pass

    def _dispatch(self, method: str, params: dict) -> dict:
        """Dispatch JSON-RPC method to the appropriate handler."""
        try:
            if method == "session/new":
                sid = self.session_new(
                    cwd=params.get("cwd", ""),
                    mcp_servers=params.get("mcpServers"),
                    permission_mode=params.get("permissionMode", "default"),
                )
                return {"result": {"sessionId": sid}} if sid else {"error": {"code": -1, "message": "session_new failed"}}

            elif method == "session/resume":
                sid = self.session_resume(
                    session_id=params.get("sessionId", ""),
                    cwd=params.get("cwd", ""),
                )
                return {"result": {"sessionId": sid}} if sid else {"error": {"code": -1, "message": "session_resume failed"}}

            elif method == "session/prompt":
                result = self.session_prompt(params.get("prompt", ""))
                return {"result": result}

            elif method == "ping":
                return {"result": "pong"}

            elif method == "shutdown":
                self.stop()
                return {"result": "ok"}

            else:
                return {"error": {"code": -32601, "message": f"unknown method: {method}"}}

        except Exception as e:
            return {"error": {"code": -32603, "message": str(e)}}

    # ── Helpers ──────────────────────────────────────────────────────────

    def _write_pid(self) -> None:
        try:
            with open(self.pid_file, "w") as f:
                f.write(str(os.getpid()))
        except Exception:
            pass

    def _cleanup_files(self) -> None:
        for path in [self.socket_path, self.pid_file]:
            try:
                if os.path.exists(path):
                    os.unlink(path)
            except Exception:
                pass

    def _log(self, msg: str) -> None:
        ts = _now_utc()
        print(f"[{ts}] [acp-bridge-v2] {msg}", file=sys.stderr, flush=True)


# ── CLI ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ACP Bridge V2 (SDK-based)")
    parser.add_argument("--project", required=True, help="Project path")
    parser.add_argument("--acp-bin", required=True, help="ACP binary (e.g. claude-agent-acp)")
    parser.add_argument("--acp-args", nargs="*", default=[], help="Extra args for ACP binary")
    parser.add_argument("--session-timeout", type=int, default=1800)
    parser.add_argument("--idle-timeout", type=int, default=900)
    parser.add_argument("--foreground", action="store_true", help="Run in foreground")
    args = parser.parse_args()

    if not SDK_AVAILABLE:
        print("ERROR: agent-client-protocol SDK not available. Install with: pip install agent-client-protocol", file=sys.stderr)
        sys.exit(1)

    if _use_legacy():
        print("WARNING: FREELY_ACP_LEGACY_FALLBACK=1 — using legacy acp-bridge.py", file=sys.stderr)
        # Fall back to old implementation
        import subprocess
        old_bridge = os.path.join(os.path.dirname(__file__), "acp-bridge.py")
        os.execv(sys.executable, [sys.executable, old_bridge] + sys.argv[1:])

    bridge = AcpBridgeV2(
        project=args.project,
        acp_bin=args.acp_bin,
        acp_args=args.acp_args,
        session_timeout=args.session_timeout,
        idle_timeout=args.idle_timeout,
    )
    bridge.start()


if __name__ == "__main__":
    main()
