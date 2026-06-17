#!/usr/bin/env python3
"""acp-bridge.py — ACP Bridge entry point.

Routes to acp_bridge_v2.py (SDK-based) by default.
Set FREELY_ACP_USE_SDK=0 to use the legacy hand-rolled JSON-RPC implementation.
Set FREELY_ACP_LEGACY_FALLBACK=1 to force legacy mode (same as USE_SDK=0).
"""

import os, sys

_use_legacy = os.environ.get("FREELY_ACP_LEGACY_FALLBACK", "0") == "1" or               os.environ.get("FREELY_ACP_USE_SDK", "1") == "0"

if not _use_legacy:
    try:
        from acp import Agent  # noqa: check SDK availability
        _v2_path = os.path.join(os.path.dirname(__file__), "acp_bridge_v2.py")
        if os.path.exists(_v2_path):
            os.execv(sys.executable, [sys.executable, _v2_path] + sys.argv[1:])
    except ImportError:
        print("[acp-bridge] agent-client-protocol SDK not available, falling back to legacy", file=sys.stderr)

import argparse
import json
import os
import signal
import socket
import subprocess
import sys
import time
import threading

BRIDGE_TIMEOUT = int(os.environ.get("ACP_BRIDGE_SESSION_TIMEOUT", "1800"))
ACP_IDLE_TIMEOUT = int(os.environ.get("ACP_BRIDGE_IDLE_TIMEOUT", "900"))
ACP_PERMISSION_MODE = os.environ.get("CLAUDE_CODE_PERMISSION_MODE") or "bypassPermissions"
if not os.environ.get("CLAUDE_CODE_PERMISSION_MODE"):
    import sys as _sys
    _sys.stderr.write("[acp-bridge] CLAUDE_CODE_PERMISSION_MODE not set — defaulting to bypassPermissions. "
                       "Set via monitor-ai-acp.sh _bridge_ensure_running or export manually.\n")
    _sys.stderr.flush()


def _short_hash(project: str) -> str:
    """Deterministic short hash of project path for socket/pid files."""
    import hashlib
    return hashlib.sha256(project.encode()).hexdigest()[:16]


def _runtime_dir(project):
    return os.path.join(project, ".freely", "run")


def _pid_file(project):
    return f"/tmp/freely-acp-{_short_hash(project)}.pid"


def _socket_path(project):
    return f"/tmp/freely-acp-{_short_hash(project)}.sock"


def _log_file(project):
    return os.path.join(_runtime_dir(project), "acp-bridge.log")


def _context_ratio_file(project):
    """Path to file where bridge writes the latest context fill ratio."""
    return os.path.join(_runtime_dir(project), "bridge-context-ratio.txt")


def _truncate_log(log_file):
    """Truncate bridge log so stale errors from prior runs don't pollute detection."""
    try:
        with open(log_file, "w") as f:
            pass
    except OSError:
        pass


def _kill_descendants(parent_pid):
    """Kill a process and all its descendants to prevent orphan process leaks."""
    import signal as _signal
    try:
        parent = subprocess.run(
            ["pgrep", "-P", str(parent_pid)],
            capture_output=True, text=True, timeout=5,
        )
        for child_pid in parent.stdout.strip().split():
            if child_pid:
                _kill_descendants(int(child_pid))
    except Exception:
        pass
    try:
        os.kill(parent_pid, _signal.SIGTERM)
    except OSError:
        pass
    # Wait briefly for graceful exit, then force kill
    try:
        os.waitpid(parent_pid, os.WNOHANG)
        time.sleep(0.5)
        os.kill(parent_pid, _signal.SIGKILL)
    except OSError:
        pass


class AcpBridge:
    """Relays JSON-RPC between Unix socket clients and claude-agent-acp stdin/stdout."""

    def __init__(self, project, acp_bin="claude-agent-acp", log_file=None, acp_args=None):
        self.project = project
        self.acp_bin = acp_bin
        self.acp_args = acp_args or []  # tool-specific ACP server args (e.g. "acp" for opencode)
        self.log_file = log_file or _log_file(project)
        self.server_proc = None
        self.server_lock = threading.Lock()
        self.pending = {}  # request_id -> {"event": Event, "response": dict, "method": str}
        self.request_counter = 0
        self.running = False
        self.socket_path = _socket_path(project)
        self.server_ready = threading.Event()
        self._restarting = False
        self.clients = []  # connected client sockets for notification broadcast
        self.clients_lock = threading.Lock()
        self.last_activity_ts = time.time()
        self.activity_lock = threading.Lock()
        self.stdin_write_lock = threading.Lock()
        self._stdout_master_fd = None
        self._stdout_reader = None
        self._fatal_detected = False       # set when bridge detects fatal error
        self._idle_timeout_detected = False  # set when idle timeout triggers

    def log(self, msg):
        ts = time.strftime("%Y-%m-%dT%H:%M:%S")
        line = f"[{ts}] {msg}\n"
        try:
            with open(self.log_file, "a") as f:
                f.write(line)
        except OSError:
            pass

    def _popen_with_pty(self, env):
        """Start ACP server process with PTY stdout to prevent block buffering.

        Uses os.openpty() so the child process sees a terminal-like stdout,
        which forces line-buffered output instead of the 4KB-16KB block
        buffering that pipes cause.  Every \\n triggers an immediate flush.
        """
        # Close previous PTY master fd if any (from a prior process)
        if self._stdout_master_fd is not None:
            try:
                if self._stdout_reader is not None:
                    self._stdout_reader.close()
                else:
                    os.close(self._stdout_master_fd)
            except OSError:
                pass
            self._stdout_master_fd = None
            self._stdout_reader = None

        master_fd, slave_fd = os.openpty()
        try:
            proc = subprocess.Popen(
                [self.acp_bin] + (self.acp_args if self.acp_args else []),
                stdin=subprocess.PIPE,
                stdout=slave_fd,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                env=env,
            )
        except BaseException:
            os.close(master_fd)
            os.close(slave_fd)
            raise
        os.close(slave_fd)  # child owns slave; close parent's copy
        self._stdout_master_fd = master_fd
        self._stdout_reader = os.fdopen(master_fd, 'r')
        return proc

    def start_server(self):
        """Launch claude-agent-acp and initialize handshake."""
        _truncate_log(self.log_file)
        self.log(f"starting ACP server: {self.acp_bin}")
        # Inherit environment but let explicitly-set vars (from alias settings) win
        env = os.environ.copy()
        # Permission mode is set via session/set_mode RPC after session creation.
        # --permission-mode CLI flag is claude-agent-acp-specific; codex-acp, opencode lack it.
        self.server_proc = self._popen_with_pty(env)

        # Start reader threads
        self.running = True
        self.server_ready.clear()
        self.stdout_thread = threading.Thread(target=self._read_stdout, daemon=True)
        self.stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
        self.stdout_thread.start()
        self.stderr_thread.start()

        # Initialize handshake
        try:
            result = self._send_request("initialize", {
                "protocolVersion": 1,
                "clientInfo": {"name": "freely-bridge", "title": "Freely ACP Bridge", "version": "0.2"},
                "clientCapabilities": {"loadSession": True, "resumeSession": True},
            }, timeout=30)
            self.server_ready.set()
            self.log(f"initialize OK: {json.dumps(result)[:200]}")
        except Exception as e:
            self.log(f"initialize failed: {e}")
            raise

    def _ensure_server_alive(self):
        """Check if server is alive and initialized; restart + init if needed."""
        if self.server_proc is not None and self.server_proc.poll() is None:
            return  # alive and well
        if not self.running:
            return
        # Server is dead — restart from scratch
        self.log("server process dead, full restart")
        if self.server_proc:
            try: self.server_proc.stdin.close()
            except OSError: pass
            _kill_descendants(self.server_proc.pid)
        self.server_proc = None
        _truncate_log(self.log_file)
        self.server_ready.clear()
        # Clear stale pending requests
        with self.server_lock:
            for req_id, slot in list(self.pending.items()):
                slot["event"].set(); del self.pending[req_id]
        # Restart
        env = os.environ.copy()
        self.server_proc = self._popen_with_pty(env)
        # Start new reader threads for new process
        self.stdout_thread = threading.Thread(target=self._read_stdout, daemon=True)
        self.stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
        self.stdout_thread.start()
        self.stderr_thread.start()
        # Initialize
        try:
            result = self._send_request("initialize", {
                "protocolVersion": 1,
                "clientInfo": {"name": "freely-bridge", "title": "Freely ACP Bridge", "version": "0.2"},
                "clientCapabilities": {"loadSession": True, "resumeSession": True},
            }, timeout=30)
            self.server_ready.set()
            self.log(f"re-initialize OK: {json.dumps(result)[:200]}")
        except Exception as e:
            self.log(f"re-initialize failed: {e}")
            raise

    def _restart_server(self):
        """Kill stale server process and start a fresh one.
        Does NOT create new threads — existing _read_stdout thread picks up
        the new process's stdout. Guarded against concurrent restarts."""
        with self.server_lock:
            if getattr(self, '_restarting', False):
                return  # another thread is already restarting
            self._restarting = True
        try:
            self._restart_server_locked()
        finally:
            self._restarting = False

    def _restart_server_locked(self):
        stale = self.server_proc
        if stale:
            try:
                stale.stdin.close()
            except OSError:
                pass
            _kill_descendants(stale.pid)
        self.server_proc = None
        self.server_ready.clear()
        _truncate_log(self.log_file)
        # Clear pending requests — their callers will get TimeoutError
        with self.server_lock:
            for req_id, slot in list(self.pending.items()):
                slot["event"].set()
                del self.pending[req_id]
        # Start new process (no initialize yet — lazy, done on first request)
        env = os.environ.copy()
        self.server_proc = self._popen_with_pty(env)
        self.log("server process restarted (initialize deferred to first request)")

    def _read_stdout(self):
        """Read newline-delimited JSON from server stdout (via PTY master fd)."""
        while self.running and self.server_proc and self._stdout_reader:
            try:
                line = self._stdout_reader.readline()
                if not line:
                    self.log("server stdout closed")
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    self.log(f"non-JSON stdout: {line[:200]}")
                    continue
                with self.activity_lock:
                    self.last_activity_ts = time.time()
                self._dispatch(msg)
            except (ValueError, OSError):
                break
            except Exception:
                self.log("unexpected error in stdout reader, shutting down bridge")
                self.running = False
                if self.server_proc and self.server_proc.poll() is None:
                    try:
                        self.server_proc.terminate()
                        self.server_proc.wait(timeout=2)
                    except Exception:
                        try:
                            self.server_proc.kill()
                        except OSError:
                            pass
                break

    def _read_stderr(self):
        """Log server stderr and detect fatal errors for stopReason normalization."""
        _fatal = ("fatal", "panic", "internal error", "segfault",
                  "out of memory", "cannot allocate", "unreachable",
                  "connection refused", "handshake failure", "broken pipe")
        while self.running and self.server_proc and self.server_proc.stderr:
            try:
                line = self.server_proc.stderr.readline()
                if not line:
                    break
                line_str = line.rstrip()[:500]
                self.log(f"server stderr: {line_str}")
                if any(p in line_str.lower() for p in _fatal):
                    self._fatal_detected = True
            except (ValueError, OSError):
                break

    def _dispatch(self, msg):
        msg_id = msg.get("id")
        if msg_id is not None and msg_id in self.pending:
            slot = self.pending[msg_id]
            slot["response"] = msg
            slot["event"].set()
            # Track context fill ratio + normalize stopReason
            if slot.get("method") == "session/prompt":
                result = msg.get("result", {})
                sr = result.get("stopReason", "")
                if sr == "end_turn" and self._fatal_detected:
                    result["stopReason"] = "error"
                elif sr == "end_turn" and self._idle_timeout_detected:
                    result["stopReason"] = "idle_timeout"
                self._track_context_ratio(result)
        elif "method" in msg:
            # Server→client request/notification (e.g. session/request_permission).
            # Broadcast to ALL connected clients so they can respond.
            method = msg.get("method", "")
            if method == "session/request_permission":
                self.log(f"permission requested (mode={ACP_PERMISSION_MODE}): {json.dumps(msg.get('params',{}))[:200]}")
            self._broadcast_notification(msg)
        elif msg_id is not None:
            # Response for unknown request — log for debugging
            self.log(f"response for unknown id: {msg_id}, result={str(msg.get('result',''))[:100]}")

    def _track_context_ratio(self, result):
        """Extract usage stats from session/prompt result and write to marker file."""
        usage = result.get("usage") or {}
        # Supports both Anthropic and DeepSeek cache field names
        total_tokens = usage.get("total_tokens") or 0
        if total_tokens <= 0:
            return
        # Context window: try model_context_window from usage, fall back to estimate
        context_window = usage.get("model_context_window") or 0
        if context_window <= 0:
            # If the result includes models info, try to locate it
            models = result.get("models") or {}
            available = models.get("availableModels") or []
            if available and isinstance(available, list) and len(available) > 0:
                context_window = (available[0].get("contextWindow")
                                  or available[0].get("model_context_window")
                                  or 0)
        if context_window <= 0:
            return
        ratio = total_tokens / context_window
        try:
            ratio_path = _context_ratio_file(self.project)
            os.makedirs(os.path.dirname(ratio_path), exist_ok=True)
            with open(ratio_path, "w") as f:
                f.write(f"{ratio:.4f}\n")
            self.log(f"context_ratio={ratio:.4f} ({total_tokens}/{context_window})")
        except OSError as e:
            self.log(f"failed to write context ratio: {e}")

    def _send_request(self, method, params, timeout=BRIDGE_TIMEOUT):
        """Send JSON-RPC request to server and wait for response.

        For session/prompt, uses activity-based idle timeout: the clock resets
        every time the AI produces output (tool calls, partial text, etc.).
        Only times out if the AI is completely silent for ACP_IDLE_TIMEOUT seconds.
        An absolute timeout (BRIDGE_TIMEOUT) still acts as a safety net.
        """
        with self.server_lock:
            self.request_counter += 1
            req_id = self.request_counter
            event = threading.Event()
            container = {}
            self.pending[req_id] = {"event": event, "response": container, "method": method}

            request = {
                "jsonrpc": "2.0",
                "id": req_id,
                "method": method,
                "params": params,
            }
            req_line = json.dumps(request, separators=(",", ":"))
            self.log(f"sending: {method} id={req_id}")

        # Write with stdin lock, then release ALL locks before waiting.
        # This allows concurrent threads to forward permission responses
        # to server stdin while we wait for the response.
        with self.stdin_write_lock:
            try:
                self.server_proc.stdin.write(req_line + "\n")
                self.server_proc.stdin.flush()
            except (BrokenPipeError, OSError) as e:
                with self.server_lock:
                    self.pending.pop(req_id, None)
                raise RuntimeError(f"server stdin write failed: {e}")

        if method == "session/prompt":
            poll_interval = min(ACP_IDLE_TIMEOUT // 2, 30)
            while True:
                if event.wait(timeout=poll_interval):
                    break
                with self.activity_lock:
                    idle_secs = time.time() - self.last_activity_ts
                if idle_secs > ACP_IDLE_TIMEOUT:
                    self._idle_timeout_detected = True
                    with self.server_lock:
                        self.pending.pop(req_id, None)
                    raise TimeoutError(
                        f"idle timeout: no AI activity for {idle_secs:.0f}s "
                        f"(limit={ACP_IDLE_TIMEOUT}s) waiting for {method}"
                    )
        else:
            if not event.wait(timeout=timeout):
                with self.server_lock:
                    self.pending.pop(req_id, None)
                raise TimeoutError(f"timeout waiting for {method}")

        with self.server_lock:
            slot = self.pending.pop(req_id, {"response": {}})
        response = slot.get("response", {})

        if "error" in response:
            err = response["error"]
            raise RuntimeError(f"server error: {err.get('message', str(err))}")

        return response.get("result", {})

    def _broadcast_notification(self, msg):
        """Forward server notification to all connected clients."""
        payload = json.dumps(msg, separators=(",", ":")) + "\n"
        data = payload.encode()
        with self.clients_lock:
            dead = []
            for sock in self.clients:
                try:
                    sock.send(data)
                except Exception:
                    dead.append(sock)
            for sock in dead:
                self.clients.remove(sock)

    @property
    def _is_claude_acp(self) -> bool:
        """session/set_mode is claude-agent-acp specific. opencode/codex don't support it."""
        return "claude-agent-acp" in self.acp_bin or self.acp_bin == "claude-agent-acp"

    def session_new(self, session_id=None, cwd=None):
        """Create a new ACP session."""
        params = {"cwd": cwd or self.project, "mcpServers": []}
        if session_id:
            params["sessionId"] = session_id
        result = self._send_request("session/new", params, timeout=30)
        sid = result.get("sessionId", "")
        if self._is_claude_acp:
            try:
                self._send_request("session/set_mode",
                    {"sessionId": sid, "modeId": ACP_PERMISSION_MODE}, timeout=10)
                self.log(f"session {sid[:12]}... mode set to {ACP_PERMISSION_MODE}")
                if ACP_PERMISSION_MODE != "bypassPermissions":
                    sys.stderr.write(f"[acp-bridge] WARNING: session {sid[:12]}... "
                                     f"permission mode is '{ACP_PERMISSION_MODE}', not 'bypassPermissions'. "
                                     f"Tool calls may require approval and could hang.\n")
                    sys.stderr.flush()
            except Exception as e:
                self.log(f"session/set_mode FAILED: {e}")
                sys.stderr.write(f"[acp-bridge] ERROR: session/set_mode failed for {sid[:12]}...: {e}. "
                                 f"Claude SDK will use default permission mode.\n")
                sys.stderr.flush()
        return sid

    def session_resume(self, session_id, cwd=None):
        """Resume an existing ACP session."""
        params = {"sessionId": session_id, "cwd": cwd or self.project, "mcpServers": []}
        result = self._send_request("session/resume", params, timeout=30)
        sid = result.get("sessionId", "")
        if self._is_claude_acp:
            try:
                self._send_request("session/set_mode",
                    {"sessionId": sid, "modeId": ACP_PERMISSION_MODE}, timeout=10)
            except Exception:
                pass
        return sid

    def session_ping(self, session_id, timeout=10):
        """Send session/ping to test AI liveness AND reset activity timer.
        If A2A workers are alive, call this periodically to prevent idle timeout.
        Returns True if pong received."""
        with self.activity_lock:
            self.last_activity_ts = time.time()  # reset idle timer
        try:
            result = self._send_request("session/ping", {"sessionId": session_id}, timeout=timeout)
            return result.get("status") == "ok" or "pong" in str(result).lower()
        except Exception:
            return False

    def session_prompt(self, session_id, prompt_text, timeout=900):
        """Send a prompt and wait for response. Returns (stop_reason, response_text)."""
        params = {
            "sessionId": session_id,
            "prompt": [{"type": "text", "text": prompt_text}],
        }
        result = self._send_request("session/prompt", params, timeout=timeout)
        stop_reason = result.get("stopReason", "unknown")
        # Normalize stopReason: detect fatal errors that AI tools mask as end_turn
        if stop_reason == "end_turn" and self._fatal_detected:
            stop_reason = "error"
        elif stop_reason == "end_turn" and self._idle_timeout_detected:
            stop_reason = "idle_timeout"
        # Collect text from response
        text = ""
        for item in result.get("message", []):
            if isinstance(item, dict) and item.get("type") == "text":
                text += item.get("text", "")
        return stop_reason, text

    def session_set_model(self, session_id, model_id):
        """Set model for session."""
        params = {"sessionId": session_id, "modelId": model_id}
        return self._send_request("session/set_model", params, timeout=10)

    def stop_server(self):
        """Gracefully stop the server and all descendant processes."""
        self.running = False
        if self.server_proc:
            try:
                self.server_proc.stdin.close()
            except OSError:
                pass
            # Kill entire process group to clean up orphaned Claude SDK children
            _kill_descendants(self.server_proc.pid)
        # Clean up PTY master fd
        if self._stdout_master_fd is not None:
            try:
                self._stdout_reader.close()
            except (OSError, AttributeError):
                try:
                    os.close(self._stdout_master_fd)
                except OSError:
                    pass
            self._stdout_master_fd = None
            self._stdout_reader = None
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
        pid_file = _pid_file(self.project)
        if os.path.exists(pid_file):
            os.unlink(pid_file)
        self.log("bridge stopped")


def handle_client(conn, bridge):
    """Generic JSON-RPC relay: forward client requests to ACP server, relay responses back."""
    buf = ""
    # Register for notification broadcast
    with bridge.clients_lock:
        bridge.clients.append(conn)
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            buf += data.decode("utf-8")
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    request = json.loads(line)
                except json.JSONDecodeError:
                    conn.send((json.dumps({"jsonrpc": "2.0", "id": 0, "error": {"code": -32700, "message": "parse error"}}) + "\n").encode())
                    continue

                method = request.get("method", "")
                params = request.get("params", {})
                req_id = request.get("id", 0)

                if "id" not in request:
                    # Client notification — forward to server without waiting for response
                    with bridge.stdin_write_lock:
                        bridge.server_proc.stdin.write(line + "\n")
                        bridge.server_proc.stdin.flush()
                    continue

                # Client-to-server RESPONSE (has id + result/error, no method):
                # Forward directly to server stdin without waiting for a server response.
                if "method" not in request and ("result" in request or "error" in request):
                    with bridge.stdin_write_lock:
                        bridge.server_proc.stdin.write(line + "\n")
                        bridge.server_proc.stdin.flush()
                    continue

                # initialize is connection-level; bridge already did it. Reply from cache.
                if method == "initialize":
                    response = {"jsonrpc": "2.0", "id": req_id, "result": {
                        "protocolVersion": 1,
                        "agentCapabilities": {"_meta": {"claudeCode": {"promptQueueing": True}}},
                    }}
                    conn.send((json.dumps(response, separators=(",", ":")) + "\n").encode())
                    continue

                try:
                    # Ensure server is alive before forwarding (lazy restart).
                    bridge._ensure_server_alive()
                    # Route session/new and session/resume through bridge methods
                    # so session/set_mode is called for claude-agent-acp.
                    if method == "session/new":
                        sid = bridge.session_new(
                            session_id=params.get("sessionId"),
                            cwd=params.get("cwd"),
                        )
                        result = {"sessionId": sid}
                    elif method == "session/resume":
                        sid = bridge.session_resume(
                            session_id=params.get("sessionId"),
                            cwd=params.get("cwd"),
                        )
                        result = {"sessionId": sid}
                    else:
                        result = bridge._send_request(method, params,
                            timeout=params.get("timeout", BRIDGE_TIMEOUT))
                    response = {"jsonrpc": "2.0", "id": req_id, "result": result}
                except TimeoutError as e:
                    response = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(e)}}
                except RuntimeError as e:
                    response = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(e)}}
                except Exception as e:
                    bridge.log(f"client request {method} failed: {e}")
                    response = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32603, "message": str(e)}}

                try:
                    conn.send((json.dumps(response, separators=(",", ":")) + "\n").encode())
                except Exception as e:
                    bridge.log(f"send response error: {e}")
                    break
    finally:
        with bridge.clients_lock:
            if conn in bridge.clients:
                bridge.clients.remove(conn)
        conn.close()


def run_socket_server(bridge):
    """Listen on Unix socket for client connections."""
    socket_path = bridge.socket_path
    if os.path.exists(socket_path):
        os.unlink(socket_path)

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(socket_path)
    sock.listen(8)
    sock.settimeout(1.0)  # allow checking running flag
    bridge.log(f"listening on {socket_path}")

    try:
        while bridge.running:
            try:
                conn, _ = sock.accept()
                t = threading.Thread(target=handle_client, args=(conn, bridge), daemon=True)
                t.start()
            except socket.timeout:
                continue
            except OSError as e:
                bridge.log(f"socket accept error: {e}")
                break
    finally:
        sock.close()
        if os.path.exists(socket_path):
            os.unlink(socket_path)


def cmd_start(args):
    project = args.project
    acp_bin = args.acp_bin or os.environ.get("FREELY_CLAUDE_ACP_BIN", "claude-agent-acp")
    log_file = args.log_file or _log_file(project)

    # Check if already running
    pid_file = _pid_file(project)
    if os.path.exists(pid_file):
        try:
            with open(pid_file) as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, 0)
            print(f"acp-bridge already running (PID {old_pid})")
            return 0
        except (OSError, ValueError):
            os.unlink(pid_file)

    # Resolve binary path
    if not os.path.isabs(acp_bin) and "/" not in acp_bin:
        import shutil
        resolved = shutil.which(acp_bin)
        if not resolved:
            print(f"[ERROR] ACP binary not found: {acp_bin}", file=sys.stderr)
            return 1
        acp_bin = resolved

    acp_args = args.acp_args.split() if args.acp_args else None
    bridge = AcpBridge(project, acp_bin, log_file, acp_args)

    # Daemonize: fork and run socket server in background.
    # start_server() writes the PID file — must happen AFTER fork so the
    # PID file contains the daemon child PID, not the short-lived parent.
    if not args.foreground:
        pid = os.fork()
        if pid > 0:
            # Parent: wait briefly to confirm child started, then exit
            time.sleep(0.5)
            if os.path.exists(_pid_file(bridge.project)):
                print(f"acp-bridge started (PID {pid})")
                print(f"{_pid_file(bridge.project)}")
                return 0
            else:
                print("[ERROR] bridge failed to start", file=sys.stderr)
                return 1

    # Child (or foreground): update PID file with real process PID,
    # start the ACP server, and run the socket server.
    os.makedirs(_runtime_dir(bridge.project), exist_ok=True)
    with open(_pid_file(bridge.project), "w") as f:
        f.write(str(os.getpid()))
    try:
        bridge.start_server()
    except Exception as e:
        print(f"[ERROR] failed to start ACP server: {e}", file=sys.stderr)
        return 1
    signal.signal(signal.SIGTERM, lambda *_: bridge.stop_server() or sys.exit(0))
    signal.signal(signal.SIGINT, lambda *_: bridge.stop_server() or sys.exit(0))
    run_socket_server(bridge)
    return 0


def cmd_stop(args):
    project = args.project
    pid_file = _pid_file(project)
    socket_path = _socket_path(project)

    if not os.path.exists(pid_file):
        print("acp-bridge not running")
        # Clean up stale socket
        if os.path.exists(socket_path):
            os.unlink(socket_path)
        return 0

    try:
        with open(pid_file) as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
        print(f"acp-bridge stopped (PID {pid})")
    except (OSError, ValueError) as e:
        print(f"failed to stop: {e}")
        if os.path.exists(pid_file):
            os.unlink(pid_file)
        if os.path.exists(socket_path):
            os.unlink(socket_path)
    return 0


def cmd_status(args):
    project = args.project
    pid_file = _pid_file(project)
    socket_path = _socket_path(project)

    if os.path.exists(pid_file):
        try:
            with open(pid_file) as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            print(f"running (PID {pid})")
            print(f"socket: {socket_path}")
            print(f"log: {_log_file(project)}")
            return 0
        except (OSError, ValueError):
            print("stale (PID file exists but process dead)")
            return 1
    else:
        print("not running")
        return 1


def main():
    parser = argparse.ArgumentParser(description="ACP bridge daemon for persistent claude-agent-acp")
    sub = parser.add_subparsers(dest="command")

    p_start = sub.add_parser("start")
    p_start.add_argument("--project", required=True)
    p_start.add_argument("--acp-bin")
    p_start.add_argument("--acp-args", help="Tool-specific ACP server arguments (space-separated, e.g. 'acp' for opencode)")
    p_start.add_argument("--log-file")
    p_start.add_argument("--foreground", action="store_true")

    p_stop = sub.add_parser("stop")
    p_stop.add_argument("--project", required=True)

    p_status = sub.add_parser("status")
    p_status.add_argument("--project", required=True)

    args = parser.parse_args()
    if args.command == "start":
        return cmd_start(args)
    elif args.command == "stop":
        return cmd_stop(args)
    elif args.command == "status":
        return cmd_status(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
