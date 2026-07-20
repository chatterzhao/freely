---
candidate_id: C-20260720T052921Z-A
status: promoted
source_raw: raw-20260720T052921Z
created_at: 2026-07-20
milestone: M-20260720T052921Z-A
---

## C-20260720T052921Z-A: Fix 15 I-* issue phase_state stuck in i_non_terminal

- candidate_format_version: v2
- title: Fix 15 I-* issue phase_state stuck in i_non_terminal
- status: promoted
- decision_reason: 15 I-* issues have non-terminal phase_state blocking scan; fix is to update to completed/absorbed
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - All 15 I-* issues have terminal phase_state (completed/absorbed/dropped)
- promotion_gate: scan no longer reports i_non_terminal for these 15 issues
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260720T052921Z-A
- promoted_issue_path: docs/issues/I-20260720T052921Z-A/issue.md
- milestone: M-20260720T052921Z-A
- session_refs: []
