---
local_id: raw-20260715T142813Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260715T142813Z-A
platform_ids:
  github:
    issue_id: '3916'
    url: https://github.com/chatterzhao/freely/issues/3916
    synced_at: ''
  gitee:
    issue_id: IK1B54
    url: https://gitee.com/zhaoquan/freely/issues/IK1B54
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-15T14:28:41Z'
updated_at: '2026-07-15T14:28:41Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因
_init_agent_table_slot_pin 通过已废弃的 agent-id.env 文件解析当前 agent role。该文件不存在时 fallback 为 manager_01，导致所有 Worker/Reviewer daemon 拿到 manager 的 slot (claude-apikey-ds-flash-auto)，而非 agent-table.toml 中为该 role 配置的 slot。

已存在 _resolve_current_agent_id() 函数正确从 agent_working SQLite 表解析角色。应复用。

## 影响
Worker 无法以正确的 base tool (opencode/cline) 启动。跨 base tool 委派永远用 Claude。

## 修复
_init_agent_table_slot_pin 改用 _resolve_current_agent_id 读 agent_working 表，agent-id.env 作为 fallback。
