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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`

### AT-002
- id: `AT-002`
- requirement: `Single-feature and explicit multi-bundle lanes are distinguished and their remaining open edges are made explicit.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/brainstorms/b-feature-owned-test-pre-merge-family-promotion-model-governance.md`

### AT-003
- id: `AT-003`
- requirement: `The owner routes follow-on work into later enforcement and automation owners instead of widening itself.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/raw-20260405-1615/code-reviews/20260405-feature-owned-test-pre-merge-family-promotion-model-verification.md`
## Unit
- acceptance_target: 历史 issue，已完成验证
- testing_layer: unit
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成，当时不要求这些 section。原始测试证据在 issue 开发过程中已验证。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Integration
- acceptance_target: 历史 issue，已完成验证
- testing_layer: integration
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## End-to-End
- acceptance_target: 历史 issue，已完成验证
- testing_layer: end-to-end
- target_environment: develop merge chain (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 此 issue 在 pre-tests v2 标准引入前完成并已合并，原始实现已通过真实环境验证。
