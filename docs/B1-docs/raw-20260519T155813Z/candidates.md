# Candidates — 20260519T155813Z--launchable-check-reason

## C-20260519T155813Z-A: legacy issue

- candidate_format_version: v2
- title: launchable check failed reason too vague
- status: absorbed
- decision_reason: Runtime bug: worker_prompt_launchable_for_manager_project multiple failure paths don't set LAUNCH_REJECT_REASON. Fix merged via hotfix/cleanup-worker-launchable. Absorbed as runtime bug fix without separate I-* materialization.
- next_action: None (already merged)
- revisit_trigger: If new launchable failure paths are added without LAUNCH_REJECT_REASON
- acceptance_criteria:
  - Each return 1 before setting LAUNCH_REJECT_REASON
  - Rejection messages include why it failed and suggested fix command
- promotion_gate: N/A (absorbed as bug fix)
- open_questions: []
- acceptance_reviews: []
- promoted_issue_path: "docs/issues/I-20260519T155813Z-A/issue.md"
- milestone: M-20260519T155813Z-A
- session_refs: []
