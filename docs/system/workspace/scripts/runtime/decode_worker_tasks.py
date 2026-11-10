#!/usr/bin/env python3
"""Decode JSON Lines worker tasks into a NUL-separated field stream.

Reads:  one JSON object per line (consume_worker_tasks.py output)
Writes: for each record, six fields separated by NUL bytes:
        task_id \\0 message \\0 worktree \\0 branch \\0 raw_key \\0 skill \\0

NUL is the only byte that cannot appear in a bash variable or a JSON string
value, so `IFS= read -r -d ''` in the runtime can consume AI-generated text
without any quoting, escaping or tab-splitting. A malformed line is reported
to stderr, counted, and skipped — it must never look like "no pending tasks".

Exit 0 on success (including an all-malformed input), 1 on unusable input.
"""
from __future__ import annotations

import json
import sys

FIELDS = ("task_id", "message", "worktree", "branch", "raw_key", "skill")


def main() -> int:
    skipped = 0
    emitted = 0
    out = sys.stdout.buffer
    for lineno, raw in enumerate(sys.stdin, 1):
        line = raw.strip()
        if not line:
            continue
        try:
            task = json.loads(line)
        except Exception as exc:
            skipped += 1
            print(f"[decode_worker_tasks] skipping malformed line {lineno}: {exc}",
                  file=sys.stderr)
            continue
        if not isinstance(task, dict):
            skipped += 1
            print(f"[decode_worker_tasks] skipping non-object line {lineno}",
                  file=sys.stderr)
            continue
        for field in FIELDS:
            value = task.get(field, "")
            out.write(str(value).encode("utf-8", errors="replace"))
            out.write(b"\0")
        out.flush()
        emitted += 1
    if skipped:
        print(f"[decode_worker_tasks] skipped={skipped} emitted={emitted}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
