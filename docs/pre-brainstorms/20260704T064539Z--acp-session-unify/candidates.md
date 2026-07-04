---
candidate_id: C-20260704T064539Z-A
status: promoted
source_raw: raw-20260704T064539Z
created_at: 2026-07-04
milestone: M-20260704T064539Z-A
---

## C-20260704T064539Z-A: 统一 ACP session 管理 + Bridge 解耦

- candidate_format_version: v2
- title: 统一 ACP session 管理方法 — acp_session_connect + bridge 解耦 + slot 检测
- status: promoted
- decision_reason: |
  12 个分散的 session 调用点 → 1 个 acp_session_connect()。
  7 处 bridge 耦合 → 签名预留 base_tool，三层解耦。
  主动检测 slot 变化，回退兜底安全网。

  设计原则: active detection (主路径) + fallback safety net (兜底)
    - slot 变了 → 主动 new + log，不浪费时间 resume
    - resume/fork 意外失败 → 降级 new + log，兜底保证不阻塞
- next_action: B2 设计 → dev 实现 → merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - agent_working 新增 slot 列
  - agent_working.py 新增 acp_session_connect() + acp_session_register()
  - _ensure_acp_bridge_running 接受显式 base_tool 参数
  - _acp_bridge_socket 接受 base_tool 参数（本期忽略）
  - 3 处 agent 逻辑 (Manager/Worker/Reviewer) 改为调用 acp_session_connect
  - 删除 watchdog 6 个分散函数 (~140行)
  - CLAUDE_SESSION_ID_CURRENT → TOOL_SESSION_ID_CURRENT
- promotion_gate: 所有 session 操作经统一入口，bridge 签名预留，slot 检测生效
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: plan-subagent
  - summary: 审查 session 统一 + bridge 解耦方案，确认三层架构合理
  - verdict: pass
- promoted_issue_id: I-20260704T064539Z-A
- promoted_issue_path: docs/epics/{epic-name}/{story-name}/raw-20260704T064539Z/issues/I-20260704T064539Z-A.md
- milestone: M-20260704T064539Z-A
- session_refs: []
