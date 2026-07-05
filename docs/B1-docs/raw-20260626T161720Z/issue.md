---
local_id: raw-20260626T161720Z20Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260626T161720Z-A
platform_ids:
  github:
    issue_id: '3567'
    url: https://github.com/chatterzhao/freely/issues/3567
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T16:17:43Z'
updated_at: '2026-06-26T16:17:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 现象

agent-table.toml 配置了 `manager_slot = "claude-apikey-ds-pro-auto"`，
但 daemon start 后 Manager 使用 `kiro-cli`（旧 `AI_TOOL` 残留 alias），
导致 slot 解析失败、ACP bridge 无法启动、supervisor 重启循环。

## 根因

`_ensure_acp_bridge_running` 和其他位置使用降级链：
```
AGENT_AI_TOOL → AI_TOOL → "claude"
```
`AI_TOOL` 是旧配置残留（`kiro-cli` alias），agent-table
已全面替代它，但降级逻辑让旧配置仍能生效，掩盖了 agent-table
未正确写入 `AGENT_AI_TOOL` 的问题。

## 修复

1. 删除所有 `AI_TOOL` 降级，只用 `AGENT_AI_TOOL`
2. daemon start 时从 agent-table 读取 Manager slot → 验证可用 → 写入 `AGENT_AI_TOOL`
3. 引用处改为硬错误而非静默降级

## 涉及位置

- `_ensure_acp_bridge_running`: `base_tool` 和 `tool_name` 的降级
- `sync_tooling`: 确保 Manager 自身的 `AGENT_AI_TOOL` 也被写入
- `tool_run_from_prompt_file`: tool 参数降级
