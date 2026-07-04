---
candidate_id: C-20260704T080808Z-A
status: promoted
source_raw: raw-20260704T080808Z
created_at: 2026-07-04
milestone: M-20260704T080808Z-A
---

## C-20260704T080808Z-A: 多 ACP bridge 并行 — per-agent tool/slot

- candidate_format_version: v2
- title: 支持不同 agent 配置不同 slot — 多 ACP bridge 并行
- status: absorbed
- absorbed_into: I-20260704T080808Z-A
- decision_reason: |
  前置依赖 (raw-20260704T064539Z) 已合并，bridge 签名已预留 base_tool。
  本期启用: socket/pid 命名 per-tool, daemon 扫描 agent-table 启动所有 bridge,
  _resolve_bridge_socket 按 base_tool 路由。
  
  改动集中在 bridge infrastructure 层 (freely shell), session 管理层 (agent_working.py)
  和 agent logic 层 (watchdog) 无需改动——因为上期已通过 base_tool 参数穿透明。
- next_action: B2 设计 → dev 实现 → merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - agent-table 中有 N 个不同 base_tool → daemon 启动 N 个 bridge
  - socket 命名为 /tmp/freely-acp-{hash}-{base_tool}.sock
  - acp_session_connect 根据 slot 的 base_tool 连到正确的 bridge
  - 同 bridge 同 slot → fork ✅
  - 同 bridge 不同 slot → fork (尝试, 失败则 new)
  - 不同 bridge → session/new
  - base_tool 不可解析 → daemon 启动硬报错退出
  - daemon stop 清理所有 bridge
- promotion_gate: N 个 base_tool → N 个 bridge 正常启停, session 操作路由正确
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: plan-subagent
  - summary: 审查多 bridge 架构设计，确认 per-tool bridge 与 session 路由正确
  - verdict: pass
- promoted_issue_id: I-20260704T080808Z-A
- promoted_issue_path: docs/epics/{epic-name}/{story-name}/raw-20260704T080808Z/issues/I-20260704T080808Z-A.md
- milestone: M-20260704T080808Z-A
- session_refs: []
