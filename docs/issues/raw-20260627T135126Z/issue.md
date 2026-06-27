---
local_id: raw-20260627T135126Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3596'
    url: https://github.com/chatterzhao/freely/issues/3596
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
absorbed_into: I-20260627T135126Z-A
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-27T13:51:46Z'
updated_at: '2026-06-27T13:51:46Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problem
git merge develop into worktree pulls in already-merged files from other worktrees, exceeding MAX_SCOPE_COUNT=4. This blocks legitimate pre-PR conflict resolution.

## Fix
Add _is_merge_commit check: when MERGE_HEAD exists, skip scope_count_threshold. Merge commits bring in committed develop changes, not new worktree work.
