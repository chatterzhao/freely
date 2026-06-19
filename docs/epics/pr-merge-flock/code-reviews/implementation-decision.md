---
issue_id: I-20260619T045626Z-A
issue_path: docs/issues/I-20260619T045626Z-A/issue.md
phase_state: done_b2_ibm
---
- issue_id: I-20260619T045626Z-A
- issue_path: docs/issues/I-20260619T045626Z-A/issue.md

## Implementation Decision Note
- decision: Add flock-based merge lock + EXIT trap for MERGE_HEAD cleanup in do_initial_merge
- why_this: Prevents stale MERGE_HEAD from blocking subsequent merge attempts. Industry standard for single-manager serial merge.
- alternatives_considered: Merge queue (overkill for single-manager), lock file without cleanup (leaves residue on crash)
- boundary_non_goals: Not implementing full merge queue, not changing merge strategy
- residual_risk: flock timeout (300s default) might need tuning for very slow CI runs
