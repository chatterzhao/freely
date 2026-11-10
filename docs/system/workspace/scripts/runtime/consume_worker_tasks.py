#!/usr/bin/env python3
"""Filter worker tasks from A2A list JSON stdin -> JSON Lines stdout.

Reads:  {"rows": [{task_id, message, worktree, branch, raw_key, skill}, ...]}
Prints: one compact JSON object per task (one line per task).

Why JSON Lines instead of TSV (raw-20261109T085539Z / #4246):
  AI-generated prompts routinely contain tabs (code block indentation). In a
  tab-separated row that silently shifts every following field, so `worktree`
  becomes part of the message and `[[ ! -d ]]` marks the task
  "worktree_missing" forever. JSON keeps field boundaries explicit and
  survives tabs, newlines, quotes and shell metacharacters unchanged.

Malformed rows are reported to stderr and counted; they are never swallowed
as "no pending tasks". Decode side: decode_worker_tasks.py.
"""
from __future__ import annotations

import json
import sys


def main() -> int:
    skipped = 0
    emitted = 0
    try:
        payload = json.load(sys.stdin)
    except Exception as exc:
        print(f"[consume_worker_tasks] invalid input payload: {exc}", file=sys.stderr)
        return 1
    rows = payload.get("rows", []) if isinstance(payload, dict) else []
    if not isinstance(rows, list):
        print("[consume_worker_tasks] 'rows' is not a list", file=sys.stderr)
        return 1
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            skipped += 1
            print(f"[consume_worker_tasks] skipping malformed row {index}: not an object",
                  file=sys.stderr)
            continue
        tid = str(row.get("task_id", ""))
        msg = row.get("message", "") or row.get("summary", "")
        if not tid or not msg:
            skipped += 1
            print(f"[consume_worker_tasks] skipping incomplete row {index}: "
                  f"task_id={tid!r}", file=sys.stderr)
            continue
        record = {
            "task_id": tid,
            "message": str(msg),
            "worktree": str(row.get("worktree", "")),
            "branch": str(row.get("branch", "")),
            "raw_key": str(row.get("raw_key", "")),
            "skill": str(row.get("skill", "")),
        }
        print(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
        emitted += 1
    if skipped:
        print(f"[consume_worker_tasks] skipped={skipped} emitted={emitted}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
