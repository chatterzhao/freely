---
candidate_id: C-20260720T032133Z-A
status: promoted
source_raw: raw-20260720T032133Z
created_at: '2026-07-20'
milestone: M-20260720T032133Z-A
---

## C-20260720T032133Z-A: Manager prompt 委派决策规则

- candidate_format_version: v2
- title: Manager prompt 委派 vs 插话决策规则
- status: promoted
- decision_reason: 参照 Routa 设计——不硬编码去重，通过 prompt 让 AI 自行判断。agent_working + a2a_tasks 提供完整视图，Manager 据此决定 delegate vs prompt vs escalate
- next_action: merge → clear DB → restart → 观察 Manager 是否正确使用 prompt
- revisit_trigger: N/A
- acceptance_criteria:
  - Manager prompt 对已委派 raw_key 明确引导使用 prompt 而非 submitted
  - 表格包含 task_id 供 prompt --task-id 使用
  - 决策规则覆盖：跟进/继续、失败重试、全新委派
- promotion_gate: prompt 模板修改完成
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: subagent
  - summary: Routa 验证无硬编码去重，纯语义 AI 决策
  - verdict: pass
- promoted_issue_id: I-20260720T032133Z-A
- promoted_issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260720T032133Z/issues/I-20260720T032133Z-A.md
- milestone: M-20260720T032133Z-A
- session_refs: []
