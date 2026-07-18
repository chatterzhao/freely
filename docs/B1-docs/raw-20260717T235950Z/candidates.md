---
candidate_id: C-20260717T235950Z-A
status: promoted
source_raw: raw-20260717T235950Z
created_at: 2026-07-17
milestone: M-20260717T235950Z-A
---

# Candidates

## C-20260717T235950Z-A: commands.md wt-close --force 文案同步

- candidate_format_version: v2
- title: commands.md wt-close --force 描述与 autonomous gate 语义同步
- status: promoted
- decision_reason: usage() 为真源已随 #3984 合入，commands.md 引用面滞后造成语义缺失，一行同步即闭环
- next_action: N/A（已 promote）
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - commands.md --force 行含"自治门禁"且语义与 wt-close --help 一致
- promotion_gate: 文案落地 + grep 断言通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - summary: 范围确认为 L193 单行；L35/L182 场景行不涉判定语义不动
  - verdict: pass
- promoted_issue_id: I-20260717T235950Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T235950Z/issues/I-20260717T235950Z-A.md
- milestone: M-20260717T235950Z-A
- session_refs: []
