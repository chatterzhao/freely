- issue_id: I-20260521T230423Z-A
## Implementation Decision Note
- decision: Guard moved from function body to parameter; only prompt path passes skip_if_active
- why_this: Original backlog≥5 design was over-constrained by active_running_workers>0
- alternatives_considered: Remove guard entirely (risks overwhelming prompt path), time-based guard (adds complexity)
- residual_risk: None — fresh always shows scan, prompt can still skip when workers busy
