---
local_id: raw-20260617T023748Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2878'
    url: https://github.com/chatterzhao/freely/issues/2878
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T02:38:05Z'
updated_at: '2026-06-17T02:38:05Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 来源
Subagent 审查 #2873 后剩余的 5 个可修问题（H1, H3, C3, G1, G2）。

## 问题

### H1: _fatal_detected 从未设为 True
`acp-bridge.py:127` — `_read_stderr` 不检测 fatal 模式。修复：检测 "fatal","panic","internal error","segfault" 等关键词。

### H3: session_ping() 从未被调用
`acp-bridge.py:504` — 方法存在但零调用。修复：`monitor-ai-acp.sh` 监控循环每 60s 调用一次 ping。

### C3: A2A save() 仅在 SUBMITTED 调，WORKING/COMPLETED 不持久化
`a2a_server.py:240,268` — `FreelyAgentExecutor.execute()` 只在初始提交调 `save()`。修复：每次状态转换都调 `save()`。

### G1: _ai_shows_liveness() 不查 A2A task 状态
`freely:12922` — 只查进程/套接字/log。修复：增加 A2A Server 查询，有 alive worker 则延长超时。

### G2: Worker 完成检测是日志解析非 A2A 查询
`freely:12691` — `worktree_has_active_worker()` tail 日志 + extract 解析。修复：优先查 A2A Server TaskStore。

## C4 (db-cli task.* bypass) 分析
`freely-db-cli task.*` 是 WAL 持久化内部通道（A2A Server → SQLite），不应被外部直接调用。当前设计正确：A2A Server 内部通过 db-cli 落盘，外部（freely 脚本）通过 a2a_task.py → A2A Server 查询。**无需修改。**
