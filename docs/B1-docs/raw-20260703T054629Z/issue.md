---
local_id: raw-20260703T054629Z29Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260703T054629Z-A
platform_ids:
  github:
    issue_id: '3703'
    url: https://github.com/chatterzhao/freely/issues/3703
    synced_at: ''
  gitee:
    issue_id: IJYKE5
    url: https://gitee.com/zhaoquan/freely/issues/IJYKE5
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-03T05:46:50Z'
updated_at: '2026-07-03T05:46:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## Bug
wt-close passes fix worktree path to pretests-retirement-gate. test-gate.env only exists in test-pre-merge — fix worktrees never have it. Gate always fails.

## Fix
Find companion test-pre-merge (same raw key) and pass that path. Block if test wt not found.
