---
local_id: raw-20260620T023657Z57Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T023657Z-A
platform_ids:
  github:
    issue_id: '3114'
    url: https://github.com/chatterzhao/freely/issues/3114
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T02:37:14Z'
updated_at: '2026-06-20T02:37:14Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

consume_delegate_workers already has _target_worktree from the A2A DB query. But it only passes _prompt_file to launch_worker_from_manager_prompt_if_needed, which then re-parses the worktree path from the prompt text using fragile awk patterns. The structured data is thrown away.

Fix: pass _target_worktree as an optional 3rd parameter. If provided, use it directly (test -d check). Only fall back to prompt text parsing if not provided (backward compat).
