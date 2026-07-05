---
issue_id: I-20260624T155212Z-A
issue_path: docs/issues/I-20260624T155212Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260624T155212Z-A
- issue_path: docs/issues/I-20260624T155212Z-A/issue.md

## Implementation Decision Note

- decision: Add fallback scan of worktree pre-tests.md when workcell-state.env is missing, instead of immediately exiting with code 1
- why_this: Minimally invasive change (35 lines added, 2 removed). Preserves existing behavior when Worker metadata exists. Reuses the existing pretests-gate for validation. Eliminates the need for --force on manually-executed worktrees without degrading validation quality.
- alternatives_considered:
  - Remove the state_file check entirely (causes cascading failures from empty env dict)
  - Skip state-dependent checks when state_file missing (still needs to find issues to validate)
  - Check if worktree is on fix/ feature/ branch (branch-based logic doesn't determine if manual or Worker-executed)
- boundary_non_goals: Does not retroactively create workcell-state.env for existing worktrees. Does not change the validation logic of pretests-gate itself. Does not alter the Worker metadata recording process.
- residual_risk: If a worktree has pre-tests.md files that are not referenced by any issue file, the fallback reports empty scan and exits 1. This could be confusing for worktrees that have valid pre-tests but no owning issue with explicit pre_tests_path. However, this is consistent with the pretests-gate expectation that every pre-tests.md is owned by an issue.
