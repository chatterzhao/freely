---
local_id: raw-20260715T115327Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260715T115327Z-A
platform_ids:
  github:
    issue_id: '3910'
    url: https://github.com/chatterzhao/freely/issues/3910
    synced_at: ''
  gitee:
    issue_id: IK1AIT
    url: https://gitee.com/zhaoquan/freely/issues/IK1AIT
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-15T11:53:51Z'
updated_at: '2026-07-15T11:53:51Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因

freely 脚本 line 22757 判断 AI monitor 路径时使用 ${AGENT_AI_TOOL_ADAPTER:-direct}，该变量在 config.toml 中未设置，始终 fallback 到 "direct"。line 22720 已将 tool_adapter 正确解析为 "acp"（从 registry [claude.adapters].default=acp），但 line 22757 未使用该值。

结果：AI 永远通过已弃用的 monitor-ai-cli.sh (direct 模式) 启动，而非 monitor-ai-acp.sh (ACP 模式)。ACP bridge 虽然正常启动（_ensure_acp_bridge_running 走 registry 路径），但 prompt 从未被发送到 bridge。所有 cycle 都是 session_id=unavailable。

## 修复

line 22757: ${AGENT_AI_TOOL_ADAPTER:-direct} → ${tool_adapter:-acp}
确保使用从 tool-registry.toml 解析的默认 adapter，永不 fallback 到已弃用的 direct。
