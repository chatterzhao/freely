---
local_id: raw-20260701T085407Z
kind: raw
phase_state: absorbed
absorbed_into: C-20260701T085407Z-A
platform_ids:
  github:
    issue_id: '3697'
    url: https://github.com/chatterzhao/freely/issues/3697
    synced_at: ''
  gitee:
    issue_id: IJY4DB
    url: https://gitee.com/zhaoquan/freely/issues/IJY4DB
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T08:54:28Z'
updated_at: '2026-07-01T08:54:28Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n
## 审查发现 (Phase 1 reviewer agent PR #3694)

### CRITICAL: A2A server _restore_tasks() operator precedence
L403: `state == 'working' and worker_prefix or reviewer_prefix`
Python `and` binds tighter than `or`, reviewer tasks enter wrong handler.

### MEDIUM: reviewer lacks _restore_tasks recovery path
- worker 有 working→alive check→恢复
- manager 有 submitted→stale check→恢复  
- reviewer: 无专属路径，需新增

### MEDIUM: _ensure_reviewer_agent() is a stub
只解析 slot 输出 log，不启动任何 session。
需支持 reviewer_manager_01 和 reviewer_worker_NN。

## 修复
全面梳理 runtime→ACP→A2A→agent(manager/worker/reviewer) 交互链路，
补全 reviewer agent 在 _restore_tasks 和 session 启动中的缺失。
