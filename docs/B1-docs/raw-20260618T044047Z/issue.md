---
local_id: raw-20260618T044047Z47Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T044047Z-A
platform_ids:
  github:
    issue_id: '2970'
    url: https://github.com/chatterzhao/freely/issues/2970
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T04:41:04Z'
updated_at: '2026-06-18T04:41:04Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## Bug

PR #2969 intended to add develop cleanliness check to pr-merge-guarded, but the fix was only applied to pr-create-guarded. The pr-merge-guarded python string replacement silently failed.

Additionally, pr-merge-guarded uses $PWD without explicit cd — if accidentally run from a worktree, it would check the wrong directory.

## Fix

1. Add explicit cd to PROJECT_ROOT (or git worktree primary path) at start
2. Add develop cleanliness check before merge
