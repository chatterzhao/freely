---
local_id: raw-20260531T030328Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2358'
    url: https://github.com/chatterzhao/freely/issues/2358
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-31T03:03:43Z'
updated_at: '2026-05-31T03:03:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 修复

1. _assemble_slot_test_command: 根据 slot discovery 机制组装带授权的测试命令
   - alias_cli_arg (claude): --settings ~/.ai-auth/{slot}/settings.json
   - alias_env_var (codex): CODEX_HOME=~/.ai-auth/{slot}
   - alias_env_var (opencode): OPENCODE_CONFIG=~/.ai-auth/{slot}/settings.json

2. _resurrect_dead_tools_batch: 查 tool.failure-list-dead 获取所有 dead slot，逐个用对应授权测试
   - 通过则 _tool_failure_clear 清除该 slot 的失败记录
   - 失败/超时(30s)则保持 dead
   - 每次切槽事件只批量测一次，不重复

3. _tool_failure_clear 传入正确的 slot 名（之前传空字符串）
