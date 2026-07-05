# Code Review
- issue_id: I-20260513T075904Z-A
## Implementation Decision Note
- decision: pr-merge-guarded post-merge sync reads `phase_state` with `status` fallback
- why_this: I-* linked issues use `phase_state` as authoritative field since state refactoring (2026-05-05); `fm.get('status')` returns empty for all migrated issues, so `linked/completed` never matched
- alternatives_considered: (1) Only `phase_state` — breaks backward compat for legacy issues still using `status` (2) Only `status` — current broken behavior
- boundary_non_goals: Not changing issue-sync itself (it already handles both fields), not changing other pr-merge-guarded logic
- residual_risk: Issues with `phase_state` and `status` both set to different values — `phase_state` is preferred, which matches the state refactoring's intent
