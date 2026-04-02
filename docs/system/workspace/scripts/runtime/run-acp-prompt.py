#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import threading
from pathlib import Path


class ACPClient:
    def __init__(self, agent_cmd, mode):
        self.mode = mode
        self._next_id = 1
        self._pending = {}
        self._pending_lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._stdout_done = threading.Event()
        self._stderr_done = threading.Event()
        self._stderr_lines = []
        self.proc = subprocess.Popen(
            agent_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        if self.proc.stdin is None or self.proc.stdout is None or self.proc.stderr is None:
            raise RuntimeError("failed to start ACP agent with piped stdio")
        self._stdout_thread = threading.Thread(target=self._read_stdout, daemon=True)
        self._stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
        self._stdout_thread.start()
        self._stderr_thread.start()

    def _send(self, message):
        payload = json.dumps(message, separators=(",", ":"))
        with self._write_lock:
            self.proc.stdin.write(payload + "\n")
            self.proc.stdin.flush()

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

    def _read_stdout(self):
        try:
            for raw_line in self.proc.stdout:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    print(f"[WARN] non-JSON ACP output: {line}", file=sys.stderr, flush=True)
                    continue
                self._handle_message(message)
        finally:
            self._stdout_done.set()

    def _read_stderr(self):
        try:
            for raw_line in self.proc.stderr:
                self._stderr_lines.append(raw_line)
                sys.stderr.write(raw_line)
                sys.stderr.flush()
        finally:
            self._stderr_done.set()

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
            print(f"\n[ACP tool_call] {title} ({status})", flush=True)
        elif update_kind == "tool_call_update":
            tool_call_id = update.get("toolCallId", "unknown")
            status = update.get("status", "pending")
            print(f"\n[ACP tool_call_update] {tool_call_id} ({status})", flush=True)

    def _handle_permission_request(self, message):
        request_id = message.get("id")
        params = message.get("params", {})
        options = params.get("options", [])
        if self.mode == "auto":
            preferred_kinds = ("allow_once", "allow_always")
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
        self._stdout_done.wait(timeout=1)
        self._stderr_done.wait(timeout=1)


def parse_args():
    parser = argparse.ArgumentParser(description="Run a one-shot ACP prompt against an agent.")
    parser.add_argument("--agent", required=True, help="ACP agent executable")
    parser.add_argument("--cwd", required=True, help="Session cwd")
    parser.add_argument("--prompt-file", required=True, help="Prompt file path")
    parser.add_argument("--mode", choices=("auto", "step"), default="auto")
    parser.add_argument("--model", default="", help="Preferred model id when supported")
    parser.add_argument("--reasoning-effort", default="", help="Reasoning effort hint")
    return parser.parse_args()


def main():
    args = parse_args()
    prompt_path = Path(args.prompt_file)
    prompt_text = prompt_path.read_text(encoding="utf-8")
    agent_cmd = [args.agent]

    client = ACPClient(agent_cmd=agent_cmd, mode=args.mode)
    try:
        init_result = client.request(
            "initialize",
            {
                "protocolVersion": 1,
                "clientInfo": {"name": "freely", "title": "Freely ACP bridge", "version": "0.1"},
                "clientCapabilities": {},
            },
        )

        session_result = client.request(
            "session/new",
            {
                "cwd": str(Path(args.cwd)),
                "mcpServers": [],
            },
        )
        session_id = session_result["sessionId"]
        print(f"session id: {session_id}", flush=True)

        if args.reasoning_effort:
            print(
                f"[WARN] ACP fresh-path prototype does not map reasoning_effort='{args.reasoning_effort}' yet",
                file=sys.stderr,
                flush=True,
            )

        if args.model:
            models_state = session_result.get("models") or init_result.get("models")
            available_models = []
            if isinstance(models_state, dict):
                available_models = models_state.get("availableModels") or []
            if any(model_info.get("modelId") == args.model for model_info in available_models):
                client.request(
                    "session/set_model",
                    {
                        "sessionId": session_id,
                        "modelId": args.model,
                    },
                )
            else:
                print(
                    f"[WARN] ACP agent did not advertise requested model '{args.model}'; continuing with agent default",
                    file=sys.stderr,
                    flush=True,
                )

        prompt_result = client.request(
            "session/prompt",
            {
                "sessionId": session_id,
                "prompt": [{"type": "text", "text": prompt_text}],
            },
            timeout=900,
        )
        if prompt_result.get("stopReason") != "end_turn":
            print(
                f"\n[WARN] ACP prompt finished with stopReason={prompt_result.get('stopReason')}",
                file=sys.stderr,
                flush=True,
            )
    finally:
        client.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr, flush=True)
        sys.exit(1)
