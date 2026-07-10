---
local_id: raw-20260706T084817Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3774'
    url: https://github.com/chatterzhao/freely/issues/3774
    synced_at: ''
  gitee:
    issue_id: IJZ480
    url: https://gitee.com/zhaoquan/freely/issues/IJZ480
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-06T08:48:38Z'
updated_at: '2026-07-06T08:48:38Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed
absorbed_into: raw-20260710T005219Z---

\n\n## 根因
agent-table.toml 已是多 agent 唯一真源（manager→claude, worker→opencode, reviewer→cline），但代码中 181 处 AI_TOOL 引用形成降级链，绕过 agent-table。

## 影响
- AI_TOOL 降级链可能导致 agent 使用错误的 base tool
- 与 agent-table 的 per-role slot 分配冲突

## 修复方案
1. 把 181 处 AI_TOOL 引用改为 AGENT_AI_TOOL 或 agent-table 查询
2. 去掉硬编码 fallback（如 AI_TOOL:-codex）
3. _init_agent_table_slot_pin 覆盖所有 agent 类型
4. 保留 agent-table 为唯一真源
