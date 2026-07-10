---
local_id: raw-20260703T080443Z43Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260703T080443Z-A
platform_ids:
  github:
    issue_id: '3705'
    url: https://github.com/chatterzhao/freely/issues/3705
    synced_at: ''
  gitee:
    issue_id: IJYMGG
    url: https://gitee.com/zhaoquan/freely/issues/IJYMGG
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-03T08:05:04Z'
updated_at: '2026-07-03T08:05:04Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n## Design Defect
__manager__ record only written lazily by _handle_needs_manager (watchdog_sse.py).
Should be written at daemon startup — manager exists from the moment daemon starts.

## Current (broken)
- Daemon starts → no __manager__ in agent_working
- First needs-manager event → _handle_needs_manager → creates __manager__ row
- Gap: fork unavailable until first worker event

## Fix
At daemon startup (supervisor ready), UPSERT __manager__ row:
- raw_key: __manager__
- worktree: project root (develop)
- branch: develop
- manager_id: manager_01 (fixed, pool=1)
- On restart: existing row → get session_id → resume session

## Reference
Residual risk documented in: docs/B2-docs/a2a/reviewer-agent/raw-20260701T085407Z07Z/code-reviews/implementation-decision-note.md:15
  (1) __manager__首次自举依赖_handle_needs_manager触发
