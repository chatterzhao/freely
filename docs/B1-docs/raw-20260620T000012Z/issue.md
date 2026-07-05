---
local_id: raw-20260620T000012Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T000012Z-A
platform_ids:
  github:
    issue_id: '3109'
    url: https://github.com/chatterzhao/freely/issues/3109
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T00:00:29Z'
updated_at: '2026-06-20T00:00:29Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problem

When Runtime cant launch a worker (worktree missing, raw issue missing),
it silently marks the task as 'rejected'. Manager never checks rejected tasks
→ dead end. All 65+ worker tasks accumulate as submitted, never launched.

The Runtime tried to auto-materialize worktrees via wt-create, but:
1. Missing --source parameter (not in A2A task struct)
2. Missing --raw-key in the wt-create call format (line 9926 uses wrong args)
3. Prompt text parsing is fragile

## Solution

### Runtime (freely script consume_delegate_workers):
- When worktree doesnt exist → update task state to 'input-required'
  with reason like: 'worktree_missing: raw_key=X branch=fix/X worktree=/path'
- Remove auto-materialize logic — Runtime shouldnt create worktrees without
  knowing --source
- Keep the check simple: test -d on worktree path from DB

### Manager (manager-agent.md):
- Add patrol step: query input-required worker tasks
- When found: run 'wt-create --help', construct correct command from raw_key
- If raw issue missing: run 'freely feedback --help', create it first
- After fix: update task state back to 'submitted' for Runtime to launch

This creates a self-healing loop: fail → report → AI reads help → fixes → retry.
