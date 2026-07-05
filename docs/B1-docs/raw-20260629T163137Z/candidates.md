---
candidate_id: C-20260629T163137Z-A
status: promoted
source_raw: raw-20260629T163137Z37Z
milestone: M-20260629T163137Z-A
---
## C-20260629T163137Z-A: legacy issue
- candidate_format_version: v2
- title: pr-review-guarded path + ACP detection fixes
- status: promoted
- decision_reason: review 路径错误 + ACP 静默失败，两个 bug 影响所有 PR review
- acceptance_criteria:
  - 从 develop 或 fix 工位跑，review 路径都正确
  - ACP 不可用时显式报错并引导 skill:freely-tdd-review
  - freely-review 失败有 explicit error message
- promotion_gate: all AT green + merge
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260629T163137Z-A/issue.md
- milestone: M-20260629T163137Z-A
- session_refs: []
