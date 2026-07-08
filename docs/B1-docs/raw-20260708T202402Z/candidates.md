---
candidate_id: C-20260708T202402Z-A
status: promoted
source_raw: raw-20260708T202402Z
milestone: M-20260708T202402Z-A
---
## C-20260708T202402Z-A: scan station chain + two-level delegation + batch dedup
- status: promoted
- milestone: `M-20260708T202402Z-A`
- decision_reason: 恢复旧scan优秀设计，保留新scan改进
- promoted_issue_id: I-20260708T202402Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260708T202402Z/issues/I-20260708T202402Z-A.md
- acceptance_criteria:
  - 所有item有 [manager]/[worker] 两级 next_action
  - sync batch 跨scan去重
  - wt-create 带完整参数
