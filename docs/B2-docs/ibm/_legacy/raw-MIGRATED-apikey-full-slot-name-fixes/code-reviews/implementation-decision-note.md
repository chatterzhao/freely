- issue_id: I-20260522T042725Z-A
- issue_path: docs/issues/I-20260522T042725Z-A/issue.md
## Implementation Decision Note
- decision: Use full directory name (claude-apikey-xxx) as slot identity everywhere
- why_this: Eliminates partial/full name inconsistency. AI_TOOL=full name → alias=full name → type resolves correctly.
- alternatives_considered: Keep partial names with tool prefix reconstruction (fragile)
- residual_risk: Old active-slot files with partial names need manual fix
