# Intake CRUD migration - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Migrate rewrite_existing_intake_item, cmd_intake_claim, cmd_intake_resolve to accept docs/issues/ IDs (raw-*, I-*). Frontmatter update for new model, meta.env fallback for legacy.`
- why_this: `Completes CHG 2.2. Claim/resolve can now process raw issues from docs/issues/ during interruption dispatch.`
- alternatives_considered: `1) Full removal of legacy path: rejected, risk of breaking in-flight intake. 2) Only new path: chosen with legacy fallback.`
- boundary_non_goals: `No cmd_intake_status migration (deferred). No handler deep refactoring beyond claim/resolve bridge.`
- residual_risk: `Python inline frontmatter update is simplistic; future: use proper YAML library.`
