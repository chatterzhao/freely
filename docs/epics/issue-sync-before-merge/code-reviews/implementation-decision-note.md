---
issue_id: I-20260626T155612Z-A
issue_path: docs/issues/I-20260626T155612Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260626T155612Z-A
- issue_path: docs/issues/I-20260626T155612Z-A/issue.md

## Implementation Decision Note

- decision: Move _sync_issues_changed_in_merge before git merge, add auto-commit + push. Change diff comparison from post-merge (HEAD vs HEAD^) to pre-merge (source vs target).
- why_this: issue-sync after merge dirties source worktree → blocks wt-close. Moving before merge + auto-commit mirrors pr-review-guarded pattern (commit → push → merge). Works for all source branch types.
- alternatives_considered: (A) Write to develop instead — violates protected branch. (B) wt-close --force bypass — papers over symptom. (C) Move before merge + auto-commit — correct fix, chosen.
- boundary_non_goals: Not changing issue-sync logic itself (phase_state transitions remain same). Not changing _sync_prs_across_platforms.
- residual_risk: Diff comparison now uses source vs target which may find different issue files than post-merge comparison. However, issue-sync is idempotent (re-running on already-synced issues is safe). The fetch after push ensures merge uses the latest source branch ref.
