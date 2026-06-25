---
candidate_id: C-20260625T222357Z-A
status: promoted
source_raw: raw-20260625T222357Z
created_at: 2026-06-25
milestone: M-20260625T222357Z-A
---

## C-20260625T222357Z-A: Review in test-pre-merge

- candidate_format_version: v2
- title: pr-review-guarded review in test-pre-merge + three-layer review
- status: promoted
- decision_reason: evidence 在现场才能验证，code sync 防止 test-pre-merge 丢弃后丢代码
- next_action: 合并
- acceptance_criteria:
  - pr-review-guarded: 找 test-pre-merge + 检查 clean + 检查 sync
  - TDD review SKILL.md: 三层 + pass/fail
- promotion_gate: 逻辑正确
- promoted_issue_path: docs/issues/I-20260625T222357Z-A/issue.md
- milestone: M-20260625T222357Z-A
- session_refs: []
