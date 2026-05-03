# Code Review: Enforce Test-Pre-Merge Gate (I-20260503T0915Z-enforce-test-pre-merge)

- issue_id: I-20260503T0915Z-enforce-test-pre-merge

## Implementation Decision Note
- decision: Block hotfix→develop direct merge, enforce test-pre-merge path
- why_this: Standardizes quality gate across all merge paths
- alternatives_considered: Break-glass on every hotfix (too manual)
- boundary_non_goals: Not changing release/main merge rules

## Verdict
APPROVED
