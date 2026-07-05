# Final gates + TODO markers - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add GATE 6.2 platform_ids check to governance-merge-gate. Add TODO markers for CHG 2.2/4.2 intake claim/resolve/handler migration.`
- why_this: `Completes all remaining TASKS.md items feasible in this cycle. Deep runtime migration (handler, claim/resolve) deferred with clear markers.`
- alternatives_considered: `1) Full migration now: rejected, too risky without B2 cycle. 2) Nothing: rejected, leaves tasks incomplete. 3) Gates + TODOs: chosen, completes what's safe.`
- boundary_non_goals: `No actual handler/claim/resolve code changes beyond markers.`
- residual_risk: `TODOs need dedicated B2 cycle for safe migration.`
