---
local_id: raw-20260617T040640Z40Z
kind: raw
phase_state: dropped
platform_state: closed
completed_at: '2026-08-07T06:00:00Z'
closeout_note: 'legacy raw closeout (platform closed)'
platform_ids:
  github:
    issue_id: '2884'
    url: https://github.com/chatterzhao/freely/issues/2884
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T04:06:56Z'
updated_at: '2026-06-17T04:06:56Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题
PR #2877 C5 和 PR #2879 G2 在后续 rebase 冲突中丢失：
1. a2a_server.py: streaming 仍为 True（应为 False）
2. freely: worktree_has_active_worker() 缺少 A2A state 查询（_a2a_state）
