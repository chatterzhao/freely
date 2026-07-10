---
local_id: raw-20260626T171144Z44Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260626T171144Z-A
platform_ids:
  github:
    issue_id: '3569'
    url: https://github.com/chatterzhao/freely/issues/3569
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T17:12:04Z'
updated_at: '2026-06-26T17:12:04Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 现象

Daemon 启动后不断切换 slot。slot 发现逻辑扫 ~/.ai-auth/ 目录按字母序选第一个，
不知道 agent-table 给当前角色配置的 slot（manager_slot/worker_slot）。

## 根因

slot 切换用 runtime_current_or_first_tool_slot → runtime_list_tool_slots
→ ls ~/.ai-auth/claude-* 按字母序。agent-table 的 per-role slot 赋值未被写入
current-slot 文件。

## 修复

启动时添加 _init_agent_table_slot_pin:
1. 从 agent-id.env 解析当前 agent 角色
2. 查 agent-table 获取该角色的 slot
3. 写入 ~/.ai-auth/.${tool}-current-slot

这样 slot 切换优先使用 agent-table 配置的 slot，切换时再找其他同工具 slots。
