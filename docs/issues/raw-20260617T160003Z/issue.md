---
local_id: raw-20260617T160003Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260617T160003Z-A
platform_ids:
  github:
    issue_id: '2934'
    url: https://github.com/chatterzhao/freely/issues/2934
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T16:00:19Z'
updated_at: '2026-06-21T18:28:02Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-06-17T16:06:32Z'
force_closed_reason: 'pr-merge-guarded: absorbed by merge'
platform_state: closed
---

## Bug

`2a72b794` (refactor: pr-merge-guarded absorbs wt-close frontmatter — develop never dirty) moved close frontmatter writing from wt-close to pr-merge-guarded. The merge commit now carries `phase_state=absorbed`, `force_closed_at`, and `absorbed_into`.

But wt-close Phase 3 (lines 292-306) still unconditionally writes `force_closed_at` and `force_closed_reason` when `--force` is used, overwriting what pr-merge-guarded already set. This leaves develop dirty with uncommitted frontmatter changes.

## Expected

Phase 3 should check if `phase_state` is already `absorbed` (pr-merge-guarded handled it). If so, skip the force-close trace write.

## Reproduce

1. pr-merge-guarded merge a fix branch → writes absorbed frontmatter to raw issue
2. wt-close --force the same branch → overwrites force_closed_reason with 'wt-close --force: worktree retired without completed phase_state'
3. develop is now dirty with inaccurate frontmatter
