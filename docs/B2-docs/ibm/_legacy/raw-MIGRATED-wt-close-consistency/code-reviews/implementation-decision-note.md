---
issue_id: I-20260625T235348Z-A
issue_path: docs/issues/I-20260625T235348Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260625T235348Z-A
- issue_path: docs/issues/I-20260625T235348Z-A/issue.md

## Implementation Decision Note

- decision: Phase 1.5 checks CWD safety + 4 consistency checks before any deletion
- why_this: local checks before platform ops, prevents silent data loss
- alternatives_considered: review-only guard → post-review manual edits still possible
- boundary_non_goals: not changing --force semantics (--force only for abandon)
- residual_risk: edge case where test worktree was deleted manually → skipped gracefully
