---
candidate_id: C-20260720T055358Z-A
status: promoted
source_raw: raw-20260720T055358Z
created_at: 2026-07-20
milestone: M-20260720T055358Z-A
---

## C-20260720T055358Z-A: Prevent wt-create silent exit when issue.md lacks phase_state

- candidate_format_version: v2
- title: Prevent wt-create silent exit when issue.md lacks phase_state
- status: promoted
- decision_reason: Minimal fix (|| true), no behavioral change when phase_state is present
- next_action: Create I-* issue → PR → merge
- revisit_trigger: N/A (promoted)
- acceptance_criteria:
  - wt-create does not exit silently when issue.md lacks phase_state
- promotion_gate: PR created with I-* issue
- open_questions: []
- acceptance_reviews:
  - reviewer: patrol
  - mode: subagent
  - summary: Patrol discovered the bug; fix already applied on 2026-07-20
  - verdict: pass
- promoted_issue_id: I-20260720T055358Z-A
- promoted_issue_path: docs/B2-docs/git-worktree/wt-create/raw-20260720T055358Z/issues/I-20260720T055358Z-A.md
- milestone: M-20260720T055358Z-A
- session_refs: []
