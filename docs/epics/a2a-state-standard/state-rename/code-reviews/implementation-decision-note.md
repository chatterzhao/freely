---
issue_id: I-20260630T021946Z-A
---
- issue_id: I-20260630T021946Z-A
## Implementation Decision Note
- decision: Remove PENDING_INPUT state, clean exit_kind refs, standardize on A2A states
- why_this: Align with Google A2A standard, no custom state names
- alternatives_considered: Keep PENDING_INPUT as alias — rejected, non-standard
- boundary_non_goals: Keep legacy STATE_ALIASES for backward compat
- residual_risk: Low. Old scripts using --exit-kind still work via backward compat aliases
