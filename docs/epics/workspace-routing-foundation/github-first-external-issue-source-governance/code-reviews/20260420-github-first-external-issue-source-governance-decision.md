# Decision Review: github-first-external-issue-source-governance

- owner_issue: `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/issues/github-first-external-issue-source-governance.md`
- decision: `Materialize a bounded GitHub-first external-source governance owner now, land the first consumer-facing truth in context-source routing docs, and defer runtime/API automation to a later implementation owner.`
- rationale:
  - pre-research already froze raw scan, canonical metadata, publication reuse, and closeout rules strongly enough for a bounded owner
  - the immediate product gap is contract drift in source-routing truth, not missing API calls
  - landing the family term and source semantics in `context-source-skill` reduces the risk that later implementation bakes old `github issue` assumptions back into runtime
- alternatives_considered:
  - `leave everything in pre-brainstorm until runtime implementation begins`
  - `open a wider multi-platform issue-publication owner immediately`
  - `skip owner materialization and change only context-source docs ad hoc`
- rejected_because:
  - leaving the work in pre-brainstorm keeps the source-family boundary too soft for follow-on implementation
  - multi-platform widening is premature before the GitHub-first slice is proven
  - ad hoc doc edits without an owner would reintroduce lifecycle drift
- residual_risk:
  - runtime implementation may still discover that a dedicated local mapping artifact is needed sooner than expected
  - `human interruption` and `external issue` shared scan infrastructure may still need a narrower umbrella owner later
