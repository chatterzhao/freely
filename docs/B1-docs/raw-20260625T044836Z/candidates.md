---
candidate_id: C-20260625T044836Z-A
status: promoted
source_raw: raw-20260625T044836Z36Z
created_at: 2026-06-25
milestone: M-20260625T044836Z-A
---

## C-20260625T044836Z-A: legacy issue

- candidate_format_version: v2
- title: issue-sync batch 只处理不一致的 issue
- status: promoted
- decision_reason: 200+ issue 中已完成的大半 platform_state=closed，直接跳过
- next_action: 合并 → #3484 batch automation
- revisit_trigger: N/A
- acceptance_criteria:
  - cmd_batch 跳过 platform_state=closed 的 issue
  - 输出显示 skipped count
  - 功能正常：未同步的仍正常处理
- promotion_gate: 过滤逻辑正确
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260625T044836Z-A/issue.md
- milestone: M-20260625T044836Z-A
- session_refs: []
