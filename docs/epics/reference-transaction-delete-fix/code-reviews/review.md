# Code Review: reference-transaction delete fix
- issue_id: I-20260508T111130Z-A
## Implementation Decision Note
- decision: Skip aborted/no-op transactions in reference-transaction hook
- why_this: git sends aborted transactions with both oids zero, which falsely triggers the creation guard
- alternatives_considered: Check transaction state (rejected — reference-transaction hook doesn't expose state)
- boundary_non_goals: Other hook types, wt-create pull flow
- residual_risk: None — the fix only affects the zero/zero case
