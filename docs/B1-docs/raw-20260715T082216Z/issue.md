---
local_id: raw-20260715T082216Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260715T082216Z-A
platform_ids:
  github:
    issue_id: '3908'
    url: https://github.com/chatterzhao/freely/issues/3908
    synced_at: ''
  gitee:
    issue_id: IK18EE
    url: https://gitee.com/zhaoquan/freely/issues/IK18EE
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-15T08:22:40Z'
updated_at: '2026-07-15T08:22:40Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因

monitor-ai-acp.sh 的 _bridge_ensure_running (line 147) 直接 python3 acp-bridge.py start 启动 bridge，不传 ANTHROPIC_* 等凭证环境变量。

freely 脚本中的 _ensure_acp_bridge_running (line 14338) 正确调用 ai_cli_tool_with_auth_assemble work 读取 ~/.ai-auth/<slot>/settings.json 并通过 env KEY=VALUE 传入。但启动顺序导致 bridge 先被 monitor-ai-acp.sh 无凭证启动，然后 _ensure_acp_bridge_running 检测到 bridge 已在运行就复用，不再重启。

结果：claude-agent-acp 永远没有 ANTHROPIC_AUTH_TOKEN/ANTHROPIC_BASE_URL/ANTHROPIC_MODEL，session/new 无法创建 Claude Code 子进程。所有 AI cycle 都是 session_id=unavailable → tool_unproductive。

## 影响

daemon 在 auto 模式下无法启动 AI cycle。Manager agent 永远 tool_unproductive，scan 有 ready 任务但无法被处理。

## 修复方案

_bridge_ensure_running 中，在启动 bridge 前调用 ai_cli_tool_with_auth_assemble work 获取 slot 凭证，通过 env 传给 bridge subprocess。与 _ensure_acp_bridge_running 使用相同的 registry 驱动路径。
