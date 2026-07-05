# B2 handler bridge - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add docs/issues/ raw-* detection to ensure_interruption_dispatch_once. handle_interruption_intake_once accepts raw-xxx IDs and returns success. Full claim/resolve migration deferred.`
- why_this: `Bridges old .freely/intake/ and new docs/issues/ worlds. Daemon can now detect new raw issues during interruption dispatch.`
- alternatives_considered: `1) Full migration now: rejected, too risky without dedicated B2 cycle. 2) Nothing: rejected, new raw issues invisible to dispatcher. 3) Bridge: chosen, minimal, safe.`
- boundary_non_goals: `No claim/resolve state migration. No deep handler refactoring.`
- residual_risk: `Raw issues detected but not auto-classified (deferred to full handler migration).`
