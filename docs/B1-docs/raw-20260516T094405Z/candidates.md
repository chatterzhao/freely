# Candidates — 20260516T094405Z--delegate-workers-exclusive-conflict

## C-20260516T094405Z-A: legacy issue

- candidate_format_version: v2
- title: delegate_workers 被 exclusive_fields_conflict 拒绝
- status: absorbed
- decision_reason: Runtime bug found via scan patrol: validate_manager_exit_contract_for_project reads `reason` field into `stop_reason`, causing exclusive_fields_conflict on delegate_workers. Fix merged directly into develop via fix/raw-20260516T014923Z* worktree. Absorbed as runtime fix without separate I-* materialization.
- next_action: None (already merged)
- revisit_trigger: If exclusive_fields_conflict pattern changes in handoff validation
- acceptance_criteria:
  - stop_reason only read for exit_kind=stop_ai
  - delegate_workers with reason field no longer blocked
- promotion_gate: N/A (absorbed as bug fix)
- open_questions: []
- acceptance_reviews: []
- promoted_issue_path: "docs/issues/I-20260516T094405Z-A/issue.md"
- milestone: M-20260516T094405Z-A
- session_refs: []
