---
local_id: raw-20260711T083155Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260711T083155Z-A
platform_ids:
  github:
    issue_id: '3882'
    url: https://github.com/chatterzhao/freely/issues/3882
    synced_at: ''
  gitee:
    issue_id: IK0CRV
    url: https://gitee.com/zhaoquan/freely/issues/IK0CRV
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-11T08:32:17Z'
updated_at: '2026-07-11T08:32:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题

1. A2A Server messages handler 存储消息后不发送 SSE，watchdog_sse 不处理 message 事件。Manager→Worker 消息投递断裂。

2. a2a_tasks 表缺少 NOT NULL 约束，AI 写错格式时没有 DB 层拦截。

## 修复

### A2A Server
- messages handler: 存储后发送 SSE event (event_type=message_added)
- PATCH handler: 已有 SSE 推送，保持不变

### watchdog_sse  
- 新增 message_added 事件处理: 读 message → 查 agent_working → ACP session/prompt 投递
- 保留现有 input-required 状态路由

### a2a_tasks 表
- task_id, state, agent_id, raw_key 加 NOT NULL
- message 字段加非空校验
- DB 层拦截格式错误

## 验收
- Manager a2a_task.py prompt → Worker 收到 ACP session/prompt 消息
- AI 写错格式 → SQLite constraint violation 明确报错
