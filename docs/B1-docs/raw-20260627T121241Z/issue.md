---
local_id: raw-20260627T121248Z41Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3592'
    url: https://github.com/chatterzhao/freely/issues/3592
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
absorbed_into: I-20260627T121241Z-A
absorbed_into: I-20260627T121241Z-A
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-27T12:13:01Z'
updated_at: '2026-06-27T12:13:01Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Bug
scan v3 Cat 3 reads `wt_path/.freely/run/agent-id.env` (per-worktree, never exists) instead of `develop/.freely/agent-id.env` (global binding table). Cat 3 always returns 3a_never_bound.

## Fix
Change agent-id.env path from `wt_path / ".freely" / "run" / "agent-id.env"` to project-global `.freely/agent-id.env`.
