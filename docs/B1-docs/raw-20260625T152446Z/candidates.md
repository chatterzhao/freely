---
candidate_id: C-20260625T152446Z-A
status: promoted
source_raw: raw-20260625T152446Z
created_at: 2026-06-25
milestone: M-20260625T152446Z-A
---

## C-20260625T152446Z-A: legacy issue

- candidate_format_version: v2
- title: pr-review-guarded 接入 ACP TDD Reviewer agent
- status: promoted
- decision_reason: 独立 session 确保他检，TDD 四问覆盖 RED/GREEN/ADEQUACY/REFACTOR
- next_action: 合并到 develop
- revisit_trigger: N/A
- acceptance_criteria:
  - pr-review-guarded 通过 ACP 启动 Reviewer session
  - TDD 四问 JSON 输出解析
  - 多轮循环 + escalate
  - 保留 --verdict override 旁路
- promotion_gate: ACP bridge 可用时正常评审
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260625T152446Z-A/issue.md
- milestone: M-20260625T152446Z-A
- session_refs: []
