---
local_id: raw-20260626T173930Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260626T173930Z-A
absorbed_into: I-20260627T020240Z-A
absorbed_into: I-20260626T173930Z-A
platform_ids:
  github:
    issue_id: '3571'
    url: https://github.com/chatterzhao/freely/issues/3571
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T17:39:50Z'
updated_at: '2026-06-27T00:40:10Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 现象

slot 切换依赖 shell alias 来测试可用性。用户不再配置 alias 后，
slot 测试无法工作。slot 切换写 ~/.ai-auth/.{tool}-current-slot，
不更新 agent-table.toml 的 {role}_slot。

## 需要的行为

1. agent slot 不可用 → 同工具 ~/.ai-auth/{tool}-* 找其他 slot
2. 同工具全不可用 → AI_FALLBACK_TOOLS 顺序试下一个工具
3. 每个候选 slot 用 tool-registry test_command + 直接拼接 slot 路径测试
   （不依赖 alias，内部组装：--settings /path 或 ENV_VAR=/path）
4. 找到可用 slot → Python 更新 agent-table.toml {role}_slot = 新slot
5. recover 成功后使用新 slot 继续

## 需要改的函数

- _assemble_slot_test_command: 去掉 alias 发现，直接用 slot 路径 + config_file
- _test_slot_availability: 新增，测试单个 slot 是否可用
- runtime_list_tool_slots: 保持扫描 ~/.ai-auth/ 逻辑
- attempt_local_same_tool_slot_recovery: 改成用 _test_slot_availability
- attempt_runtime_auto_recovery_after_failure: 改成更新 agent-table.toml
- 新增 _update_agent_table_slot: Python 写 agent-table.toml {role}_slot
