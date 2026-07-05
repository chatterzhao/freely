---
local_id: raw-20260627T062554Z54Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3583'
    url: https://github.com/chatterzhao/freely/issues/3583
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
absorbed_into: I-20260627T062554Z-A
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-27T06:26:14Z'
updated_at: '2026-06-27T06:26:14Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Changes

Rewrite task-lifecycle-scan.py with three-category classification:

### Category 1 — 未开始
- 1a: Platform OPEN + no worktree + no `docs/B1-docs/raw-{key}/` → wt-create
- 1b: Platform OPEN + raw dir exists + phase=completed → reopen
- 1c: Chat inbox unconsumed + no worktree + no raw dir → AI 判断价值

### Category 2 — 已完成但状态/清理不对齐
- 2a: raw/I-* phase_state non-terminal on develop
- 2a: platform_state mismatch (local vs actual)
- 2a: platform_state missing
- 2b: worktree not cleaned after merge
- 2d: chat unconsumed while raw exists

### Category 3 — 进行中但 agent 死
- 3a: worktree exists, agent-id.env missing → never bound
- 3b: agent session dead

### Performance
- Platform API cache (5min TTL)
- HEAD-based incremental skip
- Cold: ~11s, Warm: 0.04s

### Fixes over old scan
- No more false push=176 (check local platform_state before classifying)
- No hardcoded platforms (detect from git remotes)
- Chat inbox now properly scanned (fixed PRAGMA table_info column bug)
- No duplicate keys from chat-inbox + chain_trace
