# Implementation Decision: github-first-external-issue-source-governance

- issue_id: `I-20260407-1042-A`
- issue_path: `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/issues/github-first-external-issue-source-governance.md`

## Implementation Decision Note

- decision: `Materialize a bounded GitHub-first external-source governance owner now, land the first consumer-facing truth in context-source routing docs, and defer runtime/API automation to a later implementation owner.`
- why_this:
  - Pre-research already froze raw scan, canonical metadata, publication reuse, and closeout rules strongly enough for a bounded owner.
  - The immediate product gap is contract drift in source-routing truth, not missing API calls.
  - Landing the family term and source semantics in `context-source-skill` reduces the risk that later implementation bakes old `github issue` assumptions back into runtime.
- alternatives_considered:
  - `Leave everything in pre-brainstorm until runtime implementation begins`: rejected because the source-family boundary would remain too soft for follow-on implementation.
  - `Open a wider multi-platform issue-publication owner immediately`: rejected because widening before the GitHub-first slice is proven would blur the first stable contract.
  - `Skip owner materialization and change only context-source docs ad hoc`: rejected because ad hoc doc edits would reintroduce lifecycle drift.
- boundary_non_goals:
  - No GitHub or Gitee API create/sync automation in this owner
  - No generic multi-platform abstraction or publication redesign
  - No reopening of `human interruption` family semantics from this owner
- residual_risk:
  - Runtime implementation may still discover that a dedicated local mapping artifact is needed sooner than expected.
  - Shared scan infrastructure across `human interruption` and `external issue` may still need a narrower umbrella owner later.
