---
issue_id: I-20260625T081835Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260625T081835Z-A
## Implementation Decision Note
- decision: use freely_config.py print instead of env var
- why_this: config.toml values are not auto-exported to shell env
- alternatives_considered: source_config (too heavy)
- boundary_non_goals: other commands unchanged
- residual_risk: none
