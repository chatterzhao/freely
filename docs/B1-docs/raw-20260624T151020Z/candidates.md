---
candidate_id: C-20260624T151020Z-A
status: promoted
source_raw: raw-20260624T151020Z
created_at: 2026-06-24
milestone: M-20260624T151020Z-A
promoted_issue_path: docs/issues/I-20260624T151020Z-A/issue.md
---

## C-20260624T151020Z-A: wt-close gate 传参修复

- candidate_format_version: v2
- title: wt-close 传递正确的 pretests-retirement-gate 参数
- status: promoted
- decision_reason: 一行修复，改 wt-close 传参而非 gate 接口
- next_action: pr-create → pr-merge → wt-close
- acceptance_criteria:
  - wt-close 调用 pretests-retirement-gate 时传递 --project 和 --worktree-path
- promotion_gate: 代码 review 通过
- open_questions: []
- acceptance_reviews: []
- promoted_issue_path: docs/issues/I-20260624T151020Z-A/issue.md
- milestone: M-20260624T151020Z-A
