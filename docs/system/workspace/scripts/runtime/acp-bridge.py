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

BRIDGE_TIMEOUT = 900  # max seconds to wait for server response


def _runtime_dir(project):
    return os.path.join(project, ".freely", "run")


def _pid_file(project):
    return os.path.join(_runtime_dir(project), "acp-bridge.pid")


def _socket_path(project):
    return os.path.join(_runtime_dir(project), "acp-bridge.sock")


def _log_file(project):
    return os.path.join(_runtime_dir(project), "acp-bridge.log")


class AcpBridge:
    """Relays JSON-RPC between Unix socket clients and claude-agent-acp stdin/stdout."""

    def __init__(self, project, acp_bin="claude-agent-acp", log_file=None):
        self.project = project
        self.acp_bin = acp_bin
        self.log_file = log_file or _log_file(project)
        self.server_proc = None
        self.server_lock = threading.Lock()
        self.pending = {}  # request_id -> threading.Event + response
        self.request_counter = 0
        self.running = False
        self.socket_path = _socket_path(project)
        self.server_ready = threading.Event()
        self.clients = []  # connected client sockets for notification broadcast
        self.clients_lock = threading.Lock()

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
        self.log(f"starting ACP server: {self.acp_bin}")
        # Inherit environment but let explicitly-set vars (from alias settings) win
        env = os.environ.copy()
        self.server_proc = subprocess.Popen(
            [self.acp_bin],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )
        # Write PID file
        os.makedirs(_runtime_dir(self.project), exist_ok=True)
        with open(_pid_file(self.project), "w") as f:
            f.write(str(os.getpid()))

        # Start reader threads
        self.running = True
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
            self.log(f"initialize OK: {json.dumps(result)[:200]}")
        except Exception as e:
            self.log(f"initialize failed: {e}")
            raise

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
                self._dispatch(msg)
            except (ValueError, OSError):
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
            self.log(f"response for unknown id: {msg_id}, result={msg.get('result','')[:100]}")

    def _send_request(self, method, params, timeout=BRIDGE_TIMEOUT):
        """Send JSON-RPC request to server and wait for response."""
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

            try:
                self.server_proc.stdin.write(req_line + "\n")
                self.server_proc.stdin.flush()
            except (BrokenPipeError, OSError) as e:
                self.pending.pop(req_id, None)
                raise RuntimeError(f"server stdin write failed: {e}")

            if not event.wait(timeout=timeout):
                self.pending.pop(req_id, None)
                raise TimeoutError(f"timeout waiting for {method}")

            response = container.get("response", {})
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
        """Create a new ACP session."""
        params = {"cwd": cwd or self.project, "mcpServers": []}
        if session_id:
            params["sessionId"] = session_id
        result = self._send_request("session/new", params, timeout=30)
        return result.get("sessionId", "")

    def session_resume(self, session_id, cwd=None):
        """Resume an existing ACP session."""
        params = {"sessionId": session_id, "cwd": cwd or self.project, "mcpServers": []}
        result = self._send_request("session/resume", params, timeout=30)
        return result.get("sessionId", "")

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
        """Gracefully stop the server."""
        self.running = False
        if self.server_proc:
            try:
                self.server_proc.stdin.close()
            except OSError:
                pass
            try:
                self.server_proc.terminate()
                self.server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_proc.kill()
                self.server_proc.wait()
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
                    with bridge.server_lock:
                        bridge.server_proc.stdin.write(line + "\n")
                        bridge.server_proc.stdin.flush()
                    continue

                # Client-to-server RESPONSE (has id + result/error, no method):
                # Forward directly to server stdin without waiting for a server response.
                if "method" not in request and ("result" in request or "error" in request):
                    with bridge.server_lock:
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

    bridge = AcpBridge(project, acp_bin, log_file)
    try:
        bridge.start_server()
    except Exception as e:
        print(f"[ERROR] failed to start ACP server: {e}", file=sys.stderr)
        return 1

    # Daemonize: fork and run socket server in background
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

    # Child: run socket server
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
