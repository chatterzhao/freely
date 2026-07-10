---
local_id: raw-20260615T005743Z43Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2693'
    url: https://github.com/chatterzhao/freely/issues/2693
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-15T00:57:58Z'
updated_at: '2026-06-17T00:24:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-06-15T04:36:07Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
absorbed_into: raw-20260710T005219Z---

## 问题
Supervisor loop 在 worktree_has_active_worker 中通过 tail+extract 从 cycle log 文本解析 Worker 状态。
应该改为直接查询 a2a_tasks 表的 state 列。

## 修复
- freely bash: worktree_has_active_worker 函数中用 a2a_task.py get 替代 extract
- 移除对 cycle log 的 tail+extract 依赖
