# Code Review: merge-guarded fix/* whitelist

- issue_id: `raw-20260506T1400Z`
- issue_path: `docs/issues/raw-20260506T1400Z/issue.md`

## Implementation Decision Note
- decision: Add fix/* to merge-guarded whitelist
- why_this: fix-execution skill produces fix/* branches that need to merge to test-pre-merge
- alternatives_considered: None — fix/* branches must be supported
- boundary_non_goals: Other merge directions unchanged
- residual_risk: None — one-line change in 3 places
