---
local_id: raw-20260708T110621Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3819'
    url: https://github.com/chatterzhao/freely/issues/3819
    synced_at: ''
  gitee:
    issue_id: IJZQPW
    url: https://gitee.com/zhaoquan/freely/issues/IJZQPW
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T11:06:43Z'
updated_at: '2026-07-08T11:06:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n## 4 个问题

### 1. SSE /tasks/stream 返回 500
A2A server SSE 端点崩溃，导致 watchdog 无法订阅事件。多 agent 事件驱动链路完全断开。

### 2. pool=1054 显示错误
读取废弃的 agent-id.env（1054 行）而非 agent-table.toml（pool=10）

### 3. A2A server stderr 未捕获
500 错误信息丢失，无法调试

### 4. Manager cycle log 缺失
AI session 输出未写入 cycle log，无法观察 Manager 行为
