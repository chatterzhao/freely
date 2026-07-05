---
local_id: raw-20260619T133131Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T133131Z-A
platform_ids:
  github:
    issue_id: '3083'
    url: https://github.com/chatterzhao/freely/issues/3083
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T13:31:49Z'
updated_at: '2026-06-19T13:31:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Root cause

Manager's worker prompt format: 'Worktree: /path' (single line, colon+space)
Runtime parsers expect: 'Worktree:' (alone) + '- /path' (next line)

All 3 parsers affected:
- worker_prompt_target_worktree (line 10894): /^Worktree:$/ → misses Worktree: /path
- worker_prompt_target_branch (line 9741): /^Branch:$/ → misses Branch: name
- worker_prompt_target_branch line 9734: /^- branch: / → misses Branch: name (no - prefix)

## Impact

All 32 worker tasks silently skipped. worker_prompt_target_worktree returns empty
→ materialize_worker_prompt_worktree_if_needed fails → launch_worker_from_manager_prompt_if_needed
logs 'worker launch BLOCKED: worktree does not exist' (but this message is also suppressed
by >/dev/null — fixed in PR #3074)

## Fix

Add single-line patterns to both parsers:
- worker_prompt_target_worktree: /^Worktree: / { sub(...); print; exit }
- worker_prompt_target_branch: /^Branch: / { sub(...); print; exit }
