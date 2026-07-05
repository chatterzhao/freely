# Implementation Decision: runtime-blocked-intake-and-continuity-truth-governance

- issue_id: `I-20260404-1545-A`
- issue_path: `docs/B2-docs/runtime/runtime-blocked-intake-and-continuity-truth-governance/issues/runtime-blocked-intake-and-continuity-truth-governance.md`

## Implementation Decision Note

- decision: `Materialize prompt-visible blocked supervision by reusing delegated-continuation intake semantics plus a blocked resolution artifact, instead of introducing a brand-new intake lifecycle.`
- why_this:
  - The owner boundary only required truthful writeback after prompt visibility, not a generic runtime-state redesign.
  - Existing `delegated` plus `handoff://continuation` semantics already integrate with manager continuation absorption and local reentry handling.
  - Reusing that contract keeps the first implementation slice bounded to truth writeback and status observability without widening CLI or intake-state semantics.
- alternatives_considered:
  - `add a brand-new blocked intake lifecycle`: rejected because it widens change surface across intake CLI, status rendering, and neighboring owners before the bounded truth gap is proven closed.
  - `leave intake at new and rely only on logs or prompt text`: rejected because it preserves the misleading false-active surface that triggered this owner.
  - `fold the work into generic watchdog or network recovery redesign`: rejected because this owner only needed prompt-visible blocked truth and should not absorb broader orchestration policy.
- boundary_non_goals:
  - No generic network retry or cooldown redesign
  - No full watchdog or worker-stall orchestration rewrite
  - No new GitHub issue automation or unrelated lifecycle expansion
- residual_risk:
  - Future field evidence could prove blocked supervision needs a distinct intake lifecycle rather than reused delegated-continuation semantics.
  - Broader network-policy or watchdog follow-on owners may still need to refine how blocked reasons are classified, but they should not reopen this bounded truth contract unless the current surface regresses.
