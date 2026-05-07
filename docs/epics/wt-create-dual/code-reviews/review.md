# Code Review: wt-create Dual Worktree Creation

- issue_id: `raw-20260506T1230Z`
- issue_path: `docs/issues/raw-20260506T1230Z/issue.md`

## Implementation Decision Note
- decision: wt-create creates two worktrees at once — test-pre-merge from develop, fix/feature from test-pre-merge
- why_this: Makes fix→test-pre-merge a fast-forward merge, eliminating merge commit and conflict risk
- alternatives_considered: Keep two separate wt-create calls (current behavior) — rejected because it creates independent branches requiring real merge
- boundary_non_goals: Source 2 platform API scan (#233), B1_IBM/B2_IBM skill rename (#239)
- residual_risk: None — pure script change, legacy interface preserved
