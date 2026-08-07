---
local_id: raw-20260531T032813Z13Z
kind: raw
phase_state: dropped
platform_ids:
  github:
    issue_id: '2362'
    url: https://github.com/chatterzhao/freely/issues/2362
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-31T03:28:28Z'
updated_at: '2026-06-17T00:19:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 修复

1. _resurrect_dead_tools_batch: 查询 tool.failure-list-dead，按 slot 测试授权，批量复活
2. _assemble_slot_test_command: 根据 slot.discovery 组装带 ~/.ai-auth/{slot}/ 授权的测试命令
3. stall watchdog: 移除 bridge-dead 前提，120s 即可检测 AI 无响应
4. 取消 cooldown index-reset，单调前进
5. test_command 优化: --bare --system-prompt '' --max-tokens 50

## 验证
- codex 19s 失败 → opencode 132s stall → claude 正常工作
