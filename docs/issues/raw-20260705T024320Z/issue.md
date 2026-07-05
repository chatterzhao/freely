---
local_id: raw-20260705T024320Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260705T024320Z-A
platform_ids:
  github:
    issue_id: '3738'
    url: https://github.com/chatterzhao/freely/issues/3738
    synced_at: ''
  gitee:
    issue_id: IJYTV0
    url: https://gitee.com/zhaoquan/freely/issues/IJYTV0
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T02:43:44Z'
updated_at: '2026-07-05T02:43:44Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

AGENT_AI_TOOL 是 daemon 级全局变量，永远等于 manager 的 slot。所有 bridge 启动和 worker launch 都依赖它，导致多 tool 场景下：
- opencode/cline bridge 得不到自己的凭据 env
- worker 启动忽略 agent-table 的 worker_slot，硬编码 --agent opencode

## 审计发现

1. _ensure_acp_bridge_running:14133 — bridge env 用 AGENT_AI_TOOL 而非各 agent 的 slot
2. launch_worker:13179 — 无 base_tool socket 找不到 bridge，回退硬编码 opencode
3. session close/state 函数 — _acp_bridge_socket 不传 base_tool
4. acp_session_connect fork — 同 base_tool 不同 slot 时子 session 继承 manager 凭据

## 设计方向

AGENT_AI_TOOL 应从 agent-table 按 role 查询，每个 bridge/worker 用自己的 slot。
_ensure_acp_bridge_running 需接受 slot 参数或自行查询对应的 agent slot。
worker launch 需从 agent-table 读取 worker_slot 而非依赖全局变量。
