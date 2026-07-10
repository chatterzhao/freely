---
local_id: raw-20260617T160807Z07Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260617T160807Z-A
platform_ids:
  github:
    issue_id: '2936'
    url: https://github.com/chatterzhao/freely/issues/2936
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T16:08:23Z'
updated_at: '2026-06-17T16:08:23Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-06-17T16:11:12Z'
force_closed_reason: 'pr-merge-guarded: absorbed by merge'
platform_state: closed
---

## Bug

Commit a80b3072 introduced a regression: wt-close Phase 3 declares `local _current_phase` at the script top level (not inside a function). Bash rejects this with:
`local: can only be used in a function`

This causes wt-close --force to crash, leaving worktrees unclosed.

## Fix

Remove `local` keyword from `_current_phase` declaration in Phase 3.
