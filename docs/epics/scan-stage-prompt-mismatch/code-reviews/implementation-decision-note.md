- issue_id: I-20260521T222919Z-A
## Implementation Decision Note
- decision: Replace hardcoded stage whitelist with dynamic stage_order from scan by_stage keys
- why_this: Scan and prompt builder stage names were completely mismatched. Dynamic iteration prevents future drift.
- alternatives_considered: Sync whitelist manually (fragile), use CHAIN_STATIONS as source of truth (coupling)
- residual_risk: Prompt may still be large with many stages; per-stage limit of 30 mitigates this
