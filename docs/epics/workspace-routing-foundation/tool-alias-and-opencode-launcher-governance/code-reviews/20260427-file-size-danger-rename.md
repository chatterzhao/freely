# File size DANGER rename - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Rename TIP to DANGER, raise threshold from 300 to 750. Reorder checks: WARN → DANGER → ERROR.`
- why_this: `TIP at 300 nagged too early and lacked urgency. DANGER at 750 sits between WARN (500) and ERROR (1000), giving a clearer escalation path for files that need splitting before they hit the hard limit.`
- alternatives_considered: `1) TIP at 300 (current): rejected, too noisy at low line counts. 2) REFACTOR: rejected, sounds mandatory. 3) DANGER at 750: chosen, urgent word + meaningful threshold.`
- boundary_non_goals: `SKIP behavior unchanged. WARN and ERROR thresholds unchanged.`
- residual_risk: `Existing scripts that parse [TIP] output will need updating.`

## Verification
- bash -n: `pass`
- execution: `pass` (4 WARNs at 500+, 2 DANGERs at 750+, 0 ERRORs, 1 SKIP)
- threshold order: `pass` (WARN < DANGER < ERROR, reordered check cascade)
- SKIP unchanged: `pass`
