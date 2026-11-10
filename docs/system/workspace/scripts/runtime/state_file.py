#!/usr/bin/env python3
"""Safe state-file reader/writer (#4252, phase 1).

`runtime/freely` currently writes state as shell assignments
(`KEY="value"`) and reads it back with `source`. A value containing `"`,
`$()`, a backtick or a newline executes code in the daemon's context or kills
the supervisor loop under `set -e` — and AI-generated summaries / reasons /
branch names flow into those values.

This module is the single owner of the state-file protocol. It NEVER evaluates
a line. Two shapes are understood:

* new:  `KEY<TAB><json-encoded string>`  — no shell syntax at all
* legacy: `KEY=value` / `KEY="value"`   — split on the first `=`, strip one
  pair of quotes, keep the rest **verbatim** (no `$` expansion, no eval)

Unknown keys are rejected so a typo cannot silently become a new state field.
No third-party dependencies.

CLI:
  python3 state_file.py write  <path> --data '<json object>'
  python3 state_file.py read   <path>                # JSON dict to stdout
  python3 state_file.py to-shell <path>             # KEY='shlex-quoted' lines
  python3 state_file.py validate <path>
"""
from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

# Whitelist derived from a full scan of the state write sites in `runtime/freely`
# (develop ea9f5b38c). Adding a new state key requires registering it here —
# that is the point: state keys are a contract, not free-form shell variables.
ALLOWED_KEYS = frozenset("""
AUTO_RECOVERY_ATTEMPTED_TOOLS_CSV AUTO_RECOVERY_ORIGIN_TOOL AVAILABILITY_PHASE
BLOCKED_REASON CHECKPOINT_DRIFT_STREAK_CURRENT COOLDOWN_SWITCH_AT COOLDOWN_SWITCH_INDEX
CURRENT_TOOL_SLOT DESIRED_RUNTIME_STATE DEVELOP_PUSH_ATTEMPT_HEAD DEVELOP_PUSH_ATTEMPT_NOTE
DEVELOP_PUSH_ATTEMPT_REASON DEVELOP_PUSH_ATTEMPT_STATUS DEVELOP_PUSH_ATTEMPT_UPDATED_AT
DEVELOP_PUSH_DEFER_NOTE DEVELOP_PUSH_DEFER_REASON DEVELOP_PUSH_DEFER_UPDATED_AT
EARLIEST_RESET_HINT EXECUTION_NETWORK_FAILURE_COUNT EXECUTION_NETWORK_LAST_FAILURE_EPOCH
EXECUTION_NETWORK_NEXT_RETRY_EPOCH EXECUTION_NETWORK_REASON FREELY_ACP_FIRST_LAUNCH_DONE
LAST_ACTIVE_SLOT LAST_AI_STATE LAST_CLAUDE_JSONL_PATH LAST_CODEX_MCP_JSONL_PATH
LAST_CODEX_MCP_THREAD_ID LAST_CODEX_MCP_USED LAST_CONTEXT_COMPACTED LAST_CONTEXT_RATIO
LAST_CYCLE_DEBUG_LOG LAST_CYCLE_LOG LAST_DELEGATED_CONTINUATION_CONSUMED_AT
LAST_DELEGATED_CONTINUATION_CONSUMED_IDS LAST_DELEGATED_CONTINUATION_PENDING_COUNT
LAST_DELEGATED_CONTINUATION_PENDING_IDS LAST_ENTRYPOINT_MODE LAST_EXIT_REASON
LAST_LAUNCH_KIND LAST_PRIMARY_RATE_LIMIT_RESETS_AT LAST_PRIMARY_RATE_LIMIT_USED_PERCENT
LAST_PROBE_AT LAST_PROCESS_CHURN_PEAK LAST_PROJECT_DIRTY_ENTRIES LAST_PROMPT_FILE
LAST_RESTART_STORM_COUNT LAST_RESTART_STORM_ESCALATED_AT LAST_RESTART_STORM_ESCALATION_TARGET
LAST_RESTART_STORM_SIGNAL_AT LAST_RESTART_STORM_SIGNAL_REASON LAST_RESTART_STORM_WINDOW_SECS
LAST_ROLE_HINT LAST_ROTATION_REASON LAST_ROUTE_ONLY_HANDOFF
LAST_SECONDARY_RATE_LIMIT_RESETS_AT LAST_SECONDARY_RATE_LIMIT_USED_PERCENT
LAST_SLOT_SWITCH_AT LAST_SLOT_SWITCH_REASON LAST_STATE_UPDATED_AT LAST_SUPERVISOR_STATE
LAST_TASK_SOURCE_SCAN_ACTIVE_WORKERS LAST_TASK_SOURCE_SCAN_GENERATED_AT
LAST_TASK_SOURCE_SCAN_JSON LAST_TASK_SOURCE_SCAN_PROJECT_HEAD LAST_TASK_SOURCE_SCAN_REASON
LAST_TOOL_JSONL_PATH LAST_TOOL_RESUME_TARGET LAST_TOOL_SESSION_ID LAST_WORKTREE_SUMMARY_DIRTY
LAST_WORKTREE_SUMMARY_TOTAL RESUME_STREAK_CURRENT ROUTE_ONLY_STREAK_CURRENT
SESSION_PARENT_ID SESSION_PARENT_PROJECT TOOL_SESSION_ID_CURRENT TOOL_SESSION_ID_PREVIOUS
""".split())


class StateFileError(ValueError):
    pass


def _check_key(key: str) -> str:
    if key not in ALLOWED_KEYS:
        raise StateFileError(f"unknown state key: {key!r}")
    return key


def _strip_legacy_value(raw: str) -> str:
    """Remove one surrounding quote pair. NEVER expand anything."""
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        value = value[1:-1]
    return value


def read_state(path: str | Path) -> dict[str, str]:
    """Read a state file into a dict without executing any line."""
    p = Path(path)
    if not p.is_file():
        return {}
    result: dict[str, str] = {}
    for number, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        if "\t" in line:
            key, encoded = line.split("\t", 1)
            key = _check_key(key)
            try:
                value = json.loads(encoded)
            except json.JSONDecodeError as exc:
                raise StateFileError(f"{p}:{number}: invalid encoded value: {exc}") from exc
            if not isinstance(value, str):
                raise StateFileError(f"{p}:{number}: state values must be strings")
            result[key] = value
            continue
        if "=" not in line:
            raise StateFileError(f"{p}:{number}: not a state assignment")
        key, raw = line.split("=", 1)
        result[_check_key(key.strip())] = _strip_legacy_value(raw)
    return result


def write_state(path: str | Path, values: dict[str, str]) -> None:
    """Write the non-executable TAB + JSON format, rejecting unknown keys."""
    for key, value in values.items():
        _check_key(key)
        if not isinstance(value, str):
            raise StateFileError(f"state values must be strings: {key}")
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(f"{key}\t{json.dumps(value, ensure_ascii=False)}\n"
                   for key, value in values.items())
    p.write_text(body, encoding="utf-8")


def to_shell(path: str | Path) -> str:
    """Render safe shell assignments for the migration period.

    Values are quoted with shlex.quote, so even a value containing `$(...)`
    stays a literal. Callers must still source ONLY this generated text, never
    the original state file.
    """
    return "".join(f"{key}={shlex.quote(value)}\n"
                   for key, value in sorted(read_state(path).items()))


def main() -> int:
    ap = argparse.ArgumentParser(description="safe state-file reader/writer")
    sub = ap.add_subparsers(dest="command", required=True)
    p_write = sub.add_parser("write")
    p_write.add_argument("path")
    p_write.add_argument("--data", required=True, help="JSON object of string values")
    p_read = sub.add_parser("read")
    p_read.add_argument("path")
    p_shell = sub.add_parser("to-shell")
    p_shell.add_argument("path")
    p_validate = sub.add_parser("validate")
    p_validate.add_argument("path")
    args = ap.parse_args()
    try:
        if args.command == "write":
            data = json.loads(args.data)
            if not isinstance(data, dict):
                raise StateFileError("--data must be a JSON object")
            write_state(args.path, data)
        elif args.command == "read":
            print(json.dumps(read_state(args.path), ensure_ascii=False, sort_keys=True))
        elif args.command == "to-shell":
            sys.stdout.write(to_shell(args.path))
        else:
            read_state(args.path)
            print("ok")
    except (StateFileError, json.JSONDecodeError, OSError) as exc:
        print(f"[state-file] ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
