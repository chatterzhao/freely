---
local_id: raw-20260619T080231Z31Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T080231Z-A
platform_ids:
  github:
    issue_id: '3044'
    url: https://github.com/chatterzhao/freely/issues/3044
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T08:02:48Z'
updated_at: '2026-06-19T08:02:48Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

pr-merge-guarded and wt-close call issue-sync close without --project, causing guard to reject develop. Fix: revert the close exemption and instead make callers pass --project <worktree-path>.
