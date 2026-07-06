---
candidate_id: C-20260705T024320Z-A
status: absorbed
source_raw: raw-20260705T024320Z20Z
created_at: 2026-07-05
milestone: M-20260705T024320Z-A
---
## C-20260705T024320Z-A: legacy issue
- candidate_format_version: v2
- title: 支持不同 role agent 使用不同 base_tool 或同 base_tool 不同 slot
- status: absorbed
- decision_reason: 6 个 bug 根因一致——该传 base_tool/slot 处用了全局 AGENT_AI_TOOL 或不传参
- next_action: B2 设计 → dev 实现 → merge
- acceptance_criteria:
  - worker launch 从 agent-table 读 worker_slot，不再硬编码 --agent opencode
  - _acp_session_close 传 base_tool
  - bridge env 用对应 agent slot 而非全局 AGENT_AI_TOOL
  - _stop_acp_bridge 支持精准停，不杀无关 bridge
  - daemon stop 清理全部 bridge
  - sse-watchdog 传 base_tool
- promotion_gate: 全部修复通过 bash -n + Python AST
- promoted_issue_id: I-20260705T024320Z-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260705T024320Z-A/issue.md
- milestone: M-20260705T024320Z-A
