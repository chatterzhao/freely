#!/usr/bin/env python3
"""Filter worker tasks from A2A list JSON stdin → tab-separated stdout.

Reads: {"rows": [{task_id, message, worktree, branch, raw_key, skill}, ...]}
Prints: task_id<TAB>message<TAB>worktree<TAB>branch<TAB>raw_key<TAB>skill

Used by consume_delegate_workers in freely runtime.
Replaces inline heredoc to avoid bash quoting issues in daemon context.
"""
import json
import sys

try:
    rows = json.load(sys.stdin)
    for r in rows.get("rows", []):
        tid = r.get("task_id", "")
        msg = r.get("message", "") or r.get("summary", "")
        wt = r.get("worktree", "")
        br = r.get("branch", "")
        rk = r.get("raw_key", "")
        sk = r.get("skill", "")
        if tid and msg:
            msg = msg.replace("\n", " ").replace("\r", "")
            print(f"{tid}\t{msg}\t{wt}\t{br}\t{rk}\t{sk}")
except Exception:
    pass
