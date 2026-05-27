#!/usr/bin/env python3
"""stream-json-bridge.py: Claude stream-json adapter — no claude-agent-acp needed.

STATUS: PROTOTYPE — basic prompt/response works. NOT ready for production.
ON HOLD: 2026-05-01. Reason: no cross-process cache hits.
  ACP adapter confirmed cache hits (session/resume 60% speed improvement).
  stream-json spawns new claude process each cycle → system prompt varies
  → DeepSeek API cache cannot hit across cycles. Revisit when:
  a) Claude CLI supports persistent --session-id in -p mode, OR
  b) We implement session persistence at the bridge level (reuse process).

WHAT WORKS:
  - Spawn claude with stream-json protocol
  - Send prompt as JSON user message, read all output events
  - Extract session_id from system.init event
  - Extract assistant text from content_block_delta events
  - Persist session via session-store.py
  - Basic tool execution (Bash, Read, Write)

WHAT DOESN'T WORK:
  - Cross-process cache hits (inherent to -p mode)
  - --resume does not restore conversation context in -p mode
  - Large Chinese prompts (>30KB) may produce 0 output
  - Not integrated with freely's adapter system

Connects directly to `claude --output-format stream-json --input-format stream-json`.
Claude handles tool execution internally. Session persisted via session-store.py.

Usage:
  python3 stream-json-bridge.py run --project <path> --prompt-file <path> \\
      --session-id <uuid> --launch-kind fresh [--mode auto]
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(msg: str) -> None:
    print(f"[{_now_utc()}] {msg}", file=sys.stderr, flush=True)


def _persist_session(session_id: str, project: str, tool: str, launch_kind: str) -> None:
    """Persist session ID via freely-db daemon."""
    cli = os.path.join(os.path.dirname(__file__), "freely-db-cli")
    if not os.path.exists(cli):
        return
    subprocess.run(
        [sys.executable, cli, "--project", project, "session.upsert",
         "--session-id", session_id, "--project", project,
         "--tool", tool, "--role", os.environ.get("FREELY_ROLE_HINT", "manager"),
         "--launch-kind", launch_kind, "--tool_adapter", "stream-json"],
        capture_output=True, text=True,
    )


def run_prompt(
    project: str, prompt_file: str, session_id: str = "",
    launch_kind: str = "fresh", mode: str = "auto",
    model: str = "", tool: str = "claude",
) -> int:
    """Main: spawn claude, send prompt, read stream-json, return 0 on success."""
    with open(prompt_file, "r") as f:
        prompt_text = f.read()

    # Build command
    claude_bin = "claude"
    cmd = [
        claude_bin, "-p",
        "--output-format", "stream-json",
        "--input-format", "stream-json",
        "--include-partial-messages", "--verbose",
        "--dangerously-skip-permissions",
        "--permission-mode", "bypassPermissions" if mode == "auto" else "default",
        "--disallowed-tools", "AskUserQuestion",
    ]
    if model:
        cmd.extend(["--model", model])
    if session_id and launch_kind == "resume":
        cmd.extend(["--resume", session_id])

    # Clean env (don't inherit ANTHROPIC_MODEL from user shell)
    env = os.environ.copy()
    for k in ("ANTHROPIC_MODEL", "ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN"):
        env.pop(k, None)

    _log(f"starting: claude -p --output-format stream-json --model {model or 'default'} "
         f"launch={launch_kind} resume={'yes' if (session_id and launch_kind == 'resume') else 'no'}")

    proc = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, env=env,
    )

    detected_session_id = session_id
    stop_reason = "end_turn"

    try:
        # Send prompt as JSON user message, then close stdin to signal EOF
        msg = json.dumps({
            "type": "user",
            "message": {"role": "user", "content": [{"type": "text", "text": prompt_text}]},
        }, separators=(",", ":"))
        proc.stdin.write(msg + "\n")
        proc.stdin.flush()
        proc.stdin.close()

        # Read all stream-json output
        raw = proc.stdout.read()

        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                print(line, flush=True)
                continue

            t = event.get("type", "")

            # ── Session ID (from system.init event) ──
            if t == "system":
                sid = event.get("session_id", "")
                if sid and not detected_session_id:
                    detected_session_id = sid
                    print(sid, flush=True)  # line 1: clean UUID for session-store
                continue

            # ── Stream events (AI response) ──
            if t != "stream_event":
                continue

            inner = event.get("event", {})
            it = inner.get("type", "")

            if it == "content_block_delta":
                delta = inner.get("delta", {})
                if delta.get("type") == "text_delta":
                    print(delta.get("text", ""), end="", flush=True)

            elif it == "message_delta":
                sr = inner.get("delta", {}).get("stop_reason", "")
                if sr:
                    stop_reason = sr
                    if sr in ("end_turn", "stop_sequence"):
                        break

            elif it == "message_stop":
                break

        proc.wait()

    except Exception as e:
        _log(f"error: {e}")
        stop_reason = "error"
    finally:
        try:
            proc.stdin.close()
        except OSError:
            pass
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except (subprocess.TimeoutExpired, OSError):
            proc.kill()

    # Persist session for next cycle
    if detected_session_id and detected_session_id != session_id:
        _persist_session(detected_session_id, project, tool, launch_kind)

    # Timing/status
    print(f"\nstop_reason={stop_reason}", flush=True)
    return 0 if stop_reason in ("end_turn", "stop_sequence") else 1


def main() -> int:
    p = argparse.ArgumentParser(description="Claude stream-json adapter")
    sp = p.add_subparsers(dest="cmd")
    r = sp.add_parser("run")
    r.add_argument("--project", required=True)
    r.add_argument("--prompt-file", required=True)
    r.add_argument("--session-id", default="")
    r.add_argument("--launch-kind", default="fresh")
    r.add_argument("--mode", default="auto")
    r.add_argument("--model", default="")
    r.add_argument("--tool", default="claude")
    args = p.parse_args()
    if args.cmd != "run":
        p.print_help()
        return 1
    return run_prompt(args.project, args.prompt_file, args.session_id,
                      args.launch_kind, args.mode, args.model, args.tool)


if __name__ == "__main__":
    sys.exit(main())
