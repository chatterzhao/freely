# Code Review
- issue_id: I-20260508T232413Z-A
## Implementation Decision Note
- decision: merge error output guides AI through IBM self-diagnosis before fixing errors
- why_this: AI iterates merge→fail→fix without understanding IBM phases; structured guidance saves cycles
- alternatives_considered: (1) Put guidance in fix-execution skill only — rejected because AI may not read it before merge (2) Add gate check — rejected because it duplicates existing checks
- boundary_non_goals: Not changing gate validation logic; not adding new gate rules; not modifying IBM phases
- residual_risk: Unusual merge scenarios may not be covered by generic phase guidance
