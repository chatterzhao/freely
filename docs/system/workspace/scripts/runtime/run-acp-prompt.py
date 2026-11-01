#!/usr/bin/env python3
"""run-acp-prompt.py: ACP JSON-RPC client for one-shot prompt execution.

Two transport modes:
  --bridge-socket <path>  Connect to persistent acp-bridge (server already running).
                          Bridge keeps claude-agent-acp alive across cycles.
  (default)               Spawn claude-agent-acp as subprocess, kill on exit.
                          DEPRECATED: use bridge mode for persistent sessions.

Session states (--launch-kind):
  fresh   → session/new
  resume  → session/resume <resume_target>  (correct; not session/load)
  prompt  → session/prompt (multi-turn, session already alive)
  fork    → session/new (worker gets own session, context from prompt)
"""

import argparse
import json
import os
import socket
import subprocess
import sys
import threading
import time
from abc import ABC, abstractmethod
from pathlib import Path


# ── Transport abstraction ───────────────────────────────────────────

class Transport(ABC):
    """Abstract bidirectional JSON-RPC transport."""

    @abstractmethod
    def send(self, line: str) -> None:
        """Send a newline-terminated JSON line."""

    @abstractmethod
    def recv(self) -> str:
        """Receive a newline-terminated JSON line (blocking)."""

    @abstractmethod
    def close(self) -> None:
        """Close transport. Bridge mode: disconnect only. Subprocess mode: kill server."""

    @abstractmethod
    def running(self) -> bool:
        """Whether transport is still viable."""


class SubprocessTransport(Transport):
    """Spawn claude-agent-acp as subprocess. DEPRECATED: use SocketTransport."""

    def __init__(self, agent_cmd):
        self.proc = subprocess.Popen(
            agent_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        if self.proc.stdin is None or self.proc.stdout is None:
            raise RuntimeError("failed to start ACP agent with piped stdio")
        # Stderr relay thread
        self._stderr_lines = []
        self._stderr_done = threading.Event()
        self._stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
        self._stderr_thread.start()

    def send(self, line: str) -> None:
        self.proc.stdin.write(line + "\n")
        self.proc.stdin.flush()

    def recv(self) -> str:
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise EOFError("ACP agent stdout closed")
            return line.rstrip("\n")

    def running(self) -> bool:
        return self.proc.poll() is None

    def close(self) -> None:
        try:
            if self.proc.stdin:
                self.proc.stdin.close()
        except OSError:
            pass
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=5)
        self._stderr_done.wait(timeout=1)

    def _read_stderr(self):
        try:
            for raw_line in self.proc.stderr:
                self._stderr_lines.append(raw_line)
                sys.stderr.write(raw_line)
                sys.stderr.flush()
        finally:
            self._stderr_done.set()


class SocketTransport(Transport):
    """Connect to persistent acp-bridge via Unix socket. Bridge keeps server alive."""

    def __init__(self, socket_path):
        if not os.path.exists(socket_path):
            raise RuntimeError(f"bridge socket not found: {socket_path}")
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(int(os.environ.get("ACP_PROMPT_SOCKET_TIMEOUT", "3600")))
        self.sock.connect(socket_path)
        self._file = self.sock.makefile("r", buffering=1)
        self._write_lock = threading.Lock()

    def send(self, line: str) -> None:
        with self._write_lock:
            self.sock.sendall((line + "\n").encode())

    def recv(self) -> str:
        line = self._file.readline()
        if not line:
            raise EOFError("bridge socket closed")
        return line.rstrip("\n")

    def running(self) -> bool:
        return True  # socket stays open until explicit close

    def close(self) -> None:
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.sock.close()


# ── ACP client ──────────────────────────────────────────────────────

class ACPClient:
    def __init__(self, transport: Transport, mode: str = "auto"):
        self.transport = transport
        self.mode = mode
        self._next_id = 1
        self._pending = {}
        self._pending_lock = threading.Lock()
        self._recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
        self._recv_thread.start()

    def _send(self, message):
        payload = json.dumps(message, separators=(",", ":"))
        self.transport.send(payload)

    def _respond(self, request_id, *, result=None, error=None):
        response = {"jsonrpc": "2.0", "id": request_id}
        if error is not None:
            response["error"] = error
        else:
            response["result"] = result
        self._send(response)

    def request(self, method, params, timeout=300):
        request_id = self._next_id
        self._next_id += 1
        event = threading.Event()
        with self._pending_lock:
            self._pending[request_id] = {"event": event, "response": None}
        self._send(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params,
            }
        )
        if not event.wait(timeout):
            raise TimeoutError(f"timed out waiting for ACP response to {method}")
        with self._pending_lock:
            slot = self._pending.pop(request_id, None)
        if slot is None or slot["response"] is None:
            raise RuntimeError(f"missing ACP response for {method}")
        response = slot["response"]
        if "error" in response:
            raise RuntimeError(f"ACP {method} failed: {json.dumps(response['error'])}")
        return response.get("result", {})

    def _recv_loop(self):
        try:
            while self.transport.running():
                try:
                    raw_line = self.transport.recv()
                except EOFError:
                    break
                if not raw_line:
                    continue
                try:
                    message = json.loads(raw_line)
                except json.JSONDecodeError:
                    print(f"[WARN] non-JSON output: {raw_line[:200]}", flush=True)
                    continue
                self._handle_message(message)
        except Exception:
            pass

    def _handle_message(self, message):
        if "id" in message and ("result" in message or "error" in message):
            request_id = message["id"]
            with self._pending_lock:
                slot = self._pending.get(request_id)
            if slot is not None:
                slot["response"] = message
                slot["event"].set()
            return

        method = message.get("method")
        if method == "session/update":
            self._handle_session_update(message.get("params", {}))
            return
        if method == "session/request_permission":
            self._handle_permission_request(message)
            return

        if "id" in message and method:
            self._respond(
                message["id"],
                error={"code": -32601, "message": f"unsupported client method: {method}"},
            )

    def _handle_session_update(self, params):
        update = params.get("update", {})
        update_kind = update.get("sessionUpdate")
        if update_kind == "agent_message_chunk":
            content = update.get("content", {})
            if content.get("type") == "text":
                sys.stdout.write(content.get("text", ""))
                sys.stdout.flush()
        elif update_kind == "tool_call":
            title = update.get("title") or update.get("toolCallId") or "tool_call"
            status = update.get("status", "pending")
            print(f"\n[ACP tool_call] {title} ({status})", file=sys.stderr, flush=True)
        elif update_kind == "tool_call_update":
            tool_call_id = update.get("toolCallId", "unknown")
            status = update.get("status", "pending")
            print(f"\n[ACP tool_call_update] {tool_call_id} ({status})", file=sys.stderr, flush=True)

    def _handle_permission_request(self, message):
        request_id = message.get("id")
        params = message.get("params", {})
        options = params.get("options", [])
        if self.mode == "auto":
            preferred_kinds = ("allow_always", "allow_once")
        else:
            preferred_kinds = ("reject_once", "reject_always")

        selected_option_id = None
        for preferred_kind in preferred_kinds:
            for option in options:
                if option.get("kind") == preferred_kind:
                    selected_option_id = option.get("optionId")
                    break
            if selected_option_id:
                break

        if selected_option_id:
            self._respond(
                request_id,
                result={"outcome": {"outcome": "selected", "optionId": selected_option_id}},
            )
            return

        self._respond(request_id, result={"outcome": {"outcome": "cancelled"}})

    def close(self):
        self.transport.close()




# ── Delta extraction ------------------------------------------------------------------


# Section headers whose content is STATIC (agent def, governance, delegation
# workflow, fleet inventory, etc.) and should NOT be re-sent on subsequent
# turns in an existing ACP session -- the model already has them in context.
_STATIC_SECTION_PREFIXES = (
    "=== Agent 角色定义 ===",
    "## Worker Delegation",
    "## Fleet Inventory",
    "## Fleet Snapshot",
    "## Continuity Guard",
    "## Managed Surfaces",
    "## Current Worktree Inventory",
    "## Stale Runtime Refs",
    "## Summary Target Hint",
    "## Use",
    "## Repair Contract",
    "## Manager Bootstrap Recovery",
    "## 工位可写性",
)

# Section headers whose content is DYNAMIC (changes between turns).
# These are the sections we MUST include in the delta.
_DYNAMIC_SECTION_PREFIXES = (
    "=== 本轮 delta",
    "## Handoff 上下文",
    "### Worker 汇报",
    "### Worker 异常",
    "### 近期 Worker",
)


def extract_delta(text):
    '''Strip static sections from a prompt file.

    The ACP server already has the full system prompt, agent definition,
    governance rules and delegation workflow in its session context from
    the first turn.  On subsequent turns we MUST only send content that
    changes between turns - worker reports, scan data, turn instructions.

    Uses a simple line-oriented state machine keyed off ``## `` / ``=== ``
    section headers.  Unknown sections are PRESERVED (safe default).
    '''
    if "## " not in text and "=== " not in text:
        return text  # no section markers - assume already a delta

    out_lines = []
    in_static = False

    for line in text.split("\n"):
        stripped = line.strip()

        # Section header detection
        if stripped.startswith("## ") or stripped.startswith("=== "):
            is_static = any(stripped.startswith(p) for p in _STATIC_SECTION_PREFIXES)
            is_dynamic = any(stripped.startswith(p) for p in _DYNAMIC_SECTION_PREFIXES)

            if is_dynamic:
                in_static = False
            elif is_static:
                in_static = True
            else:
                in_static = False

        if not in_static:
            out_lines.append(line)

    result = "\n".join(out_lines)

    while result.endswith("\n\n"):
        result = result[:-1]

    if result.strip():
        return result
    return text



# ── CLI ─────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description="Run a one-shot ACP prompt against an agent.")
    parser.add_argument("--agent", default="", help="ACP agent executable (subprocess mode)")
    parser.add_argument("--bridge-socket", default="", help="Unix socket path for persistent acp-bridge")
    parser.add_argument("--cwd", required=True, help="Session cwd")
    parser.add_argument("--prompt-file", required=True, help="Prompt file path")
    parser.add_argument("--mode", choices=("auto", "step"), default="auto")
    parser.add_argument("--model", default="", help="Preferred model id when supported")
    parser.add_argument("--reasoning-effort", default="", help="Reasoning effort hint")
    parser.add_argument("--session-id", default="", help="Desired session UUID for new sessions")
    parser.add_argument("--resume", default="", help="Session ID to resume via session/resume")
    parser.add_argument("--launch-kind", choices=("fresh", "resume", "fork", "prompt"), default="fresh",
                        help="Session lifecycle state")
    parser.add_argument("--loop", action="store_true",
                        help="Loop mode: after prompt completes, check --next-prompt-file for the next prompt. Delete after reading. 'EXIT' in file stops the loop.")
    parser.add_argument("--next-prompt-file", default="",
                        help="Path to file that contains the next prompt file path (loop mode)")
    parser.add_argument("--delta", action="store_true",
                        help="Delta mode: strip static sections (agent def, governance) from prompt text. "
                             "Use on subsequent prompts in an existing ACP session to avoid re-sending "
                             "content the server already has in context.")
    return parser.parse_args()


def main():
    args = parse_args()
    t_start = time.time()
    prompt_path = Path(args.prompt_file)
    prompt_text = prompt_path.read_text(encoding="utf-8")
    try:
        from prompt_manifest import record_manifest
        record_manifest(Path(args.cwd), prompt_text, session_id=getattr(args, "session_id", ""))
    except Exception as _manifest_error:
        print(f"[manifest] skipped: {_manifest_error}", file=sys.stderr)
    cwd = str(Path(args.cwd))

    # ── Transport selection ──────────────────────────────────────
    if args.bridge_socket:
        transport = SocketTransport(args.bridge_socket)
    elif args.agent:
        agent_cmd = args.agent.split()
        transport = SubprocessTransport(agent_cmd)
    else:
        print("[ERROR] must specify --bridge-socket or --agent", flush=True)
        sys.exit(1)
    t_transport = time.time()

    client = ACPClient(transport=transport, mode=args.mode)
    stop_reason = "error"  # prevent UnboundLocalError in finally block
    try:
        # Handshake
        client.request(
            "initialize",
            {
                "protocolVersion": 1,
                "clientInfo": {"name": "freely", "title": "Freely ACP", "version": "0.2"},
                "clientCapabilities": {"loadSession": True, "resumeSession": True},
            },
            timeout=30,
        )

        # ── Session management (fresh | resume | fork) ──────────
        launch_kind = args.launch_kind
        resume_target = args.resume

        if launch_kind == "resume" and resume_target:
            # Resume existing session → cache hit.
            # If session was lost (bridge restart), fall back to session/new.
            try:
                session_result = client.request(
                    "session/resume",
                    {"sessionId": resume_target, "cwd": cwd, "mcpServers": []},
                    timeout=30,
                )
                session_id = session_result["sessionId"]
                print(session_id, flush=True)                                # line 1: clean UUID for machine parsing
                print(f"session id: {session_id} (resumed)", flush=True)     # line 2: human log
            except Exception as e:
                print(f"[WARN] session/resume failed ({e}), falling back to session/new", flush=True)
                new_params = {"cwd": cwd, "mcpServers": []}
                if args.session_id:
                    new_params["sessionId"] = args.session_id
                session_result = client.request("session/new", new_params, timeout=30)
                session_id = session_result["sessionId"]
                print(session_id, flush=True)                                             # line 1: clean UUID
                print(f"session id: {session_id} (fresh after resume failure)", flush=True) # line 2: human log

        elif launch_kind == "prompt" and resume_target:
            # Multi-turn within same session: session already exists from fresh/resume.
            # If session was lost (bridge restart), send_prompt() will fall back to session/new.
            session_id = resume_target
            print(session_id, flush=True)                                    # line 1: clean ID for machine parsing
            print(f"session id: {session_id} (prompt)", flush=True)          # line 2: human log
            # session_result for prompt-mode multi-turn
            session_result = {"sessionId": session_id}

        elif launch_kind == "fork":
            # Worker/reviewer forks from parent: creates independent session
            # while inheriting parent conversation history for cache hits.
            # Uses session/fork (ACP official spec) when supported — Claude and
            # OpenCode support it; Cline and Codex fall back to session/new.
            new_params = {"cwd": cwd, "mcpServers": []}
            if args.session_id:
                new_params["sessionId"] = args.session_id
            try:
                session_result = client.request("session/fork",
                    {"sessionId": resume_target or args.session_id, "cwd": cwd, "mcpServers": []},
                    timeout=30)
            except Exception:
                session_result = client.request("session/new", new_params, timeout=30)
            session_id = session_result["sessionId"]
            if resume_target:
                print(session_id, flush=True)
                print(f"session id: {session_id} (fork from {resume_target})", flush=True)
            else:
                print(session_id, flush=True)
                print(f"session id: {session_id} (fork)", flush=True)

        else:
            # fresh launch
            new_params = {"cwd": cwd, "mcpServers": []}
            if args.session_id:
                new_params["sessionId"] = args.session_id
            session_result = client.request("session/new", new_params, timeout=30)
            session_id = session_result["sessionId"]
            print(session_id, flush=True)                         # line 1: clean UUID
            print(f"session id: {session_id}", flush=True)       # line 2: human log

        t_session = time.time()

        # Ensure bypassPermissions is active for this session.
        # In bridge mode, the bridge already handles this after session/new
        # and session/resume. Only needed for subprocess (--agent) mode.
        if not args.bridge_socket:
            _perm_mode = os.environ.get("CLAUDE_CODE_PERMISSION_MODE", "")
            if not _perm_mode:
                print("[run-acp-prompt] WARNING: CLAUDE_CODE_PERMISSION_MODE not set", file=sys.stderr)
                _perm_mode = "default"
            try:
                client.request(
                    "session/set_mode",
                    {"sessionId": session_id, "modeId": _perm_mode},
                    timeout=10,
                )
            except Exception:
                pass

        # Model selection
        if args.reasoning_effort:
            print(
                f"[WARN] ACP reasoning_effort='{args.reasoning_effort}' not mapped yet",
                file=sys.stderr, flush=True,
            )

        if args.model:
            models_state = session_result.get("models") or {}
            available_models = models_state.get("availableModels") or []
            if any(m.get("modelId") == args.model for m in available_models):
                client.request(
                    "session/set_model",
                    {"sessionId": session_id, "modelId": args.model},
                    timeout=10,
                )
            else:
                print(
                    f"[WARN] model '{args.model}' not advertised; using agent default",
                    file=sys.stderr, flush=True,
                )

        # ── Prompt loop (one-shot or loop mode) ────────────────────
        def send_prompt(prompt_text, t_start, t_session, launch_kind, use_delta=False):
            if use_delta:
                orig_len = len(prompt_text)
                prompt_text = extract_delta(prompt_text)
                if len(prompt_text) != orig_len:
                    print(f"[DELTA] stripped {orig_len - len(prompt_text)} bytes of static sections "
                          f"(original={orig_len}b -> delta={len(prompt_text)}b)", flush=True)
            t_before = time.time()
            prompt_timeout = int(os.environ.get("ACP_PROMPT_TIMEOUT", "3600"))
            prompt_result = client.request(
                "session/prompt",
                {"sessionId": session_id, "prompt": [{"type": "text", "text": prompt_text}]},
                timeout=prompt_timeout,
            )
            t_done = time.time()
            stop_reason = prompt_result.get("stopReason", "unknown")
            print()  # ensure newline before stop_reason marker
            print(f"stop_reason={stop_reason}", flush=True)

            prompt_kb = len(prompt_text.encode("utf-8")) / 1024
            print(f"[TIMING] transport_connect={(t_session - t_start):.1f}s session_new={0:.1f}s prompt_wait={(t_done - t_before):.1f}s total={(t_done - t_start):.1f}s prompt_size={prompt_kb:.1f}kb", flush=True)

            usage = prompt_result.get("usage") or {}
            prompt_bytes = len(prompt_text.encode('utf-8'))
            # Supports both Anthropic and DeepSeek cache field names
            cache_hit = usage.get("cache_read_input_tokens") or usage.get("prompt_cache_hit_tokens") or 0
            cache_miss = usage.get("cache_creation_input_tokens") or usage.get("prompt_cache_miss_tokens") or 0
            input_tokens = usage.get("input_tokens") or usage.get("prompt_tokens") or 0
            output_tokens = usage.get("output_tokens") or usage.get("completion_tokens") or 0
            total_tokens = usage.get("total_tokens", 0)
            # Workaround: if no usage data, estimate from bytes (4 bytes ≈ 1 token for mixed CN/EN)
            if total_tokens == 0 and input_tokens == 0:
                input_tokens = prompt_bytes // 4
                total_tokens = input_tokens  # lower bound estimate
            cache_msg = f"[CACHE] session_id={session_id} launch_kind={launch_kind} prompt_bytes={prompt_bytes} input={input_tokens} cache_hit={cache_hit} cache_miss={cache_miss} output={output_tokens} total={total_tokens}"
            print(cache_msg, flush=True)
            print(cache_msg, flush=True)  # also to stdout (cycle log) for easy inspection

            if stop_reason != "end_turn":
                print(f"[WARN] ACP prompt finished with stopReason={stop_reason}", flush=True)
            return stop_reason

        try:
            stop_reason = send_prompt(prompt_text, t_start, t_session, launch_kind,
                                      use_delta=(launch_kind == "prompt" or args.delta))
        except Exception as prompt_exc:
            # session/prompt failed — session may have been closed by the AI
            # (e.g. opencode closes sessions after stop_reason=end_turn).
            # Try session/resume first to re-activate the closed session
            # before falling all the way back to session/new.
            # session/resume preserves context history and enables cache hits.
            print(f"[WARN] session/prompt failed ({prompt_exc}), trying session/resume", flush=True)
            _exc_msg = str(prompt_exc)
            if "idle timeout" in _exc_msg:
                print(f"[FATAL] idle timeout: AI unresponsive, not retrying. Let runtime recover.", flush=True)
                sys.exit(1)
            try:
                resume_result = client.request(
                    "session/resume",
                    {"sessionId": session_id, "cwd": cwd, "mcpServers": []},
                    timeout=30,
                )
                resumed_id = resume_result["sessionId"]
                print(resumed_id, flush=True)
                print(f"session id: {resumed_id} (resumed after prompt failure)", flush=True)
                session_id = resumed_id
                t_session = time.time()
                launch_kind = "resume"
                stop_reason = send_prompt(prompt_text, t_start, t_session, launch_kind,
                                          use_delta=True)
            except Exception as resume_exc:
                # session/resume also failed — bridge may have restarted.
                # Fall back to session/new as last resort.
                print(f"[WARN] session/resume also failed ({resume_exc}), falling back to session/new", flush=True)
                new_params = {"cwd": cwd, "mcpServers": []}
                if args.session_id:
                    new_params["sessionId"] = args.session_id
                session_result = client.request("session/new", new_params, timeout=30)
                session_id = session_result["sessionId"]
                print(session_id, flush=True)
                print(f"session id: {session_id} (fresh after prompt failure)", flush=True)
                t_session = time.time()
                launch_kind = "fresh"
                stop_reason = send_prompt(prompt_text, t_start, t_session, launch_kind,
                                          use_delta=False)

        # Loop mode: keep session alive, wait for next prompt via control file
        if args.loop and args.next_prompt_file:
            next_file = Path(args.next_prompt_file)
            while True:
                if next_file.exists():
                    try:
                        line = next_file.read_text(encoding="utf-8").strip()
                        next_file.unlink()  # consume the signal
                    except Exception:
                        time.sleep(0.5)
                        continue
                    if not line:
                        time.sleep(0.5)
                        continue
                    if line == "EXIT":
                        break
                    try:
                        next_text = Path(line).read_text(encoding="utf-8")
                    except Exception as e:
                        print(f"[WARN] cannot read next prompt file: {line} ({e})", flush=True)
                        continue
                    stop_reason = send_prompt(next_text, t_start, t_session, launch_kind,
                                              use_delta=True)
                    t_start = time.time()
                else:
                    time.sleep(0.5)  # poll interval
    finally:
        if stop_reason == "end_turn" and not args.loop:
            time.sleep(2)  # grace period for bridge to finish sending notifications
        if args.loop:
            try:
                client.request("session/close", {"sessionId": session_id}, timeout=10)
            except Exception:
                pass
        client.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[ERROR] {exc}", flush=True)
        sys.exit(1)
