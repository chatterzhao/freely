# Pre-Tests: feature-owned-test-pre-merge-family-promotion-model-governance

## Acceptance Targets

### AT-001 promote model is frozen at the right abstraction level

- acceptance target: the owner freezes `feature/*`, `test-pre-merge-*`, and `develop` responsibilities without prematurely promising hook/script implementation
- testing layer: governance
- target environment: issue + brainstorm + `prd.md`
- required evidence: `owner doc package`
- blocker taxonomy: `definition_missing`

### AT-002 single-feature and explicit multi-bundle semantics are separated

- acceptance target: the owner distinguishes the default single-feature lane from the explicit multi-bundle lane and explains what remains unresolved for later enforcement owners
- testing layer: governance
- target environment: issue + brainstorm + `tasks.md`
- required evidence: `owner doc package`
- blocker taxonomy: `evidence_plan_missing`

### AT-003 follow-on owners are clearly sequenced

- acceptance target: the owner clearly routes later work into at least gate enforcement and lifecycle automation follow-ons instead of widening this owner into implementation
- testing layer: governance
- target environment: issue + milestone + candidate writeback
- required evidence: `owner doc package + milestone writeback`
- blocker taxonomy: `lifecycle_incomplete`

## Pre-merge acceptance

1. `./bin/governance-check`
   - expectation: candidate, milestone, and issue writeback are structurally consistent
2. `git diff --check`
   - expectation: the new IBM package and writebacks are whitespace-clean

## Post-merge acceptance

1. Active scans treat `I-20260405-1615-A` as the canonical owner for this promote-model design surface.
2. Later work on gate or lifecycle changes must cite this owner rather than reopening raw pre-brainstorm debate.

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `The owner freezes the promote model at governance level instead of prematurely implementing gate mechanics.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`

### AT-002
- id: `AT-002`
- requirement: `Single-feature and explicit multi-bundle lanes are distinguished and their remaining open edges are made explicit.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/brainstorms/b-feature-owned-test-pre-merge-family-promotion-model-governance.md`

### AT-003
- id: `AT-003`
- requirement: `The owner routes follow-on work into later enforcement and automation owners instead of widening itself.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/code-reviews/20260405-feature-owned-test-pre-merge-family-promotion-model-verification.md`
