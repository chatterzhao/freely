#!/usr/bin/env python3
"""acp-bridge.py: Persistent relay between claude-agent-acp and monitor clients.

Keeps claude-agent-acp alive across AI cycles. Each monitor invocation
connects via Unix socket, sends JSON-RPC, receives response, disconnects.
The bridge keeps the server process alive for session persistence.

Usage:
  acp-bridge.py start --project <path> [--acp-bin <path>] [--log-file <path>]
  acp-bridge.py stop --project <path>
  acp-bridge.py status --project <path>
"""

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
_perm = os.environ.get("CLAUDE_CODE_PERMISSION_MODE", "")
if not _perm:
    import sys
    print("[acp-bridge] WARNING: CLAUDE_CODE_PERMISSION_MODE not set. Permission mode defaults to empty. Check ~/.ai-auth/<tool>/settings.json", file=sys.stderr)
ACP_PERMISSION_MODE = _perm or "default"


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
        self.pending = {}  # request_id -> threading.Event + response
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

    def log(self, msg):
        ts = time.strftime("%Y-%m-%dT%H:%M:%S")
        line = f"[{ts}] {msg}\n"
        try:
            with open(self.log_file, "a") as f:
                f.write(line)
        except OSError:
            pass

    def start_server(self):
        """Launch claude-agent-acp and initialize handshake."""
        _truncate_log(self.log_file)
        self.log(f"starting ACP server: {self.acp_bin}")
        # Inherit environment but let explicitly-set vars (from alias settings) win
        env = os.environ.copy()
        # Bypass permissions in daemon mode — the ACP client handles
        # permission decisions via session/request_permission protocol.
        self.server_proc = subprocess.Popen(
            [self.acp_bin] + (self.acp_args if self.acp_args else ["--permission-mode", ACP_PERMISSION_MODE]),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )

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
            for req_id, (event, _container) in list(self.pending.items()):
                event.set(); del self.pending[req_id]
        # Restart
        env = os.environ.copy()
        self.server_proc = subprocess.Popen(
            [self.acp_bin] + (self.acp_args if self.acp_args else ["--permission-mode", ACP_PERMISSION_MODE]),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1, env=env,
        )
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
            for req_id, (event, _container) in list(self.pending.items()):
                event.set()
                del self.pending[req_id]
        # Start new process (no initialize yet — lazy, done on first request)
        env = os.environ.copy()
        self.server_proc = subprocess.Popen(
            [self.acp_bin] + (self.acp_args if self.acp_args else ["--permission-mode", ACP_PERMISSION_MODE]),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )
        self.log("server process restarted (initialize deferred to first request)")

    def _read_stdout(self):
        """Read newline-delimited JSON from server stdout."""
        while self.running and self.server_proc and self.server_proc.stdout:
            try:
                line = self.server_proc.stdout.readline()
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
        """Log server stderr."""
        while self.running and self.server_proc and self.server_proc.stderr:
            try:
                line = self.server_proc.stderr.readline()
                if not line:
                    break
                self.log(f"server stderr: {line.rstrip()[:500]}")
            except (ValueError, OSError):
                break

    def _dispatch(self, msg):
        msg_id = msg.get("id")
        if msg_id is not None and msg_id in self.pending:
            event, container = self.pending[msg_id]
            container["response"] = msg
            event.set()
        elif "method" in msg:
            # Server→client request/notification (e.g. session/request_permission).
            # Broadcast to ALL connected clients so they can respond.
            self._broadcast_notification(msg)
        elif msg_id is not None:
            # Response for unknown request — log for debugging
            self.log(f"response for unknown id: {msg_id}, result={str(msg.get('result',''))[:100]}")

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
            self.pending[req_id] = (event, container)

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
            deadline = time.time() + timeout
            while time.time() < deadline:
                if event.wait(timeout=poll_interval):
                    break
                with self.activity_lock:
                    idle_secs = time.time() - self.last_activity_ts
                if idle_secs > ACP_IDLE_TIMEOUT:
                    with self.server_lock:
                        self.pending.pop(req_id, None)
                    raise TimeoutError(
                        f"idle timeout: no AI activity for {idle_secs:.0f}s "
                        f"(limit={ACP_IDLE_TIMEOUT}s) waiting for {method}"
                    )
            if not event.is_set():
                with self.server_lock:
                    self.pending.pop(req_id, None)
                raise TimeoutError(
                    f"absolute timeout ({timeout}s) waiting for {method}"
                )
        else:
            if not event.wait(timeout=timeout):
                with self.server_lock:
                    self.pending.pop(req_id, None)
                raise TimeoutError(f"timeout waiting for {method}")

        response = container.get("response", {})
        with self.server_lock:
            self.pending.pop(req_id, None)

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

    def session_new(self, session_id=None, cwd=None):
        """Create a new ACP session and set bypassPermissions mode."""
        params = {"cwd": cwd or self.project, "mcpServers": []}
        if session_id:
            params["sessionId"] = session_id
        result = self._send_request("session/new", params, timeout=30)
        sid = result.get("sessionId", "")
        # Immediately set bypassPermissions to avoid interactive permission hangs
        try:
            self._send_request("session/set_mode", {"sessionId": sid, "modeId": ACP_PERMISSION_MODE}, timeout=10)
            self.log(f"session {sid[:12]}... mode set to bypassPermissions")
        except Exception as e:
            self.log(f"session/set_mode failed (non-fatal): {e}")
        return sid

    def session_resume(self, session_id, cwd=None):
        """Resume an existing ACP session and ensure bypassPermissions is active."""
        params = {"sessionId": session_id, "cwd": cwd or self.project, "mcpServers": []}
        result = self._send_request("session/resume", params, timeout=30)
        sid = result.get("sessionId", "")
        try:
            self._send_request("session/set_mode", {"sessionId": sid, "modeId": ACP_PERMISSION_MODE}, timeout=10)
        except Exception:
            pass
        return sid

    def session_prompt(self, session_id, prompt_text, timeout=900):
        """Send a prompt and wait for response. Returns (stop_reason, response_text)."""
        params = {
            "sessionId": session_id,
            "prompt": [{"type": "text", "text": prompt_text}],
        }
        result = self._send_request("session/prompt", params, timeout=timeout)
        stop_reason = result.get("stopReason", "unknown")
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
                    # Forward request to server via bridge's send/recv pipeline
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
