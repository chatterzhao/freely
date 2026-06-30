---
issue_id: I-20260629T122254Z-A
---
- issue_id: I-20260629T122254Z-A
## Implementation Decision Note
- decision: Add case entries + exec functions for 8 commands in main freely script
- why_this: Uniform freely xxx entry for all workflow [cmd] nodes + [CMD] log consistency
- alternatives_considered: Python CLI rewrite — rejected, too large scope
- boundary_non_goals: Internal scripts (governance-merge-gate, freely-review) stay as ./bin/
- residual_risk: Low. Only adding dispatch, no logic changes
