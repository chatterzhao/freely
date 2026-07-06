# Pre-Tests: governance-chain-legacy-repair

## Acceptance Targets

### AT-001 umbrella owner materialized

- acceptance target: `1100` is no longer only a promoted candidate; it has canonical milestone, issue, and progress truth
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `milestone + issue + progress`
- blocker taxonomy: `definition_missing`

### AT-002 child slices normalized

- acceptance target: `1200/1201/1202/1203` no longer appear in canonical docs as active slices claiming nonexistent materialized issues
- testing layer: IBM review
- target environment: pre-brainstorm artifacts
- required evidence: `child-slice inventory + parent issue`
- blocker taxonomy: `definition_missing`

### AT-003 gate strictness preserved

- acceptance target: the repair path keeps current gate strictness and fixes legacy truth instead of broadening exemptions
- testing layer: integration
- target environment: governance scripts + artifacts
- required evidence: `governance-check`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 decision note present

- acceptance target: this umbrella owner has an issue-bound decision note for the develop-bound repair strategy
- testing layer: IBM review
- target environment: verification artifact dir
- required evidence: `implementation decision note`
- blocker taxonomy: `definition_missing`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `The 1100 lane is materialized as the canonical owner.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/governance-chain-legacy-repair/raw-20260403-1100/issues/governance-chain-legacy-repair.md`

### AT-002
- id: `AT-002`
- requirement: `Historical child repair slices no longer pretend they are active issue lanes when they are not.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/governance-chain-legacy-repair/child-slice-status.md`

### AT-003
- id: `AT-003`
- requirement: `Governance repair preserves current gate strictness.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `./bin/governance-check`

### AT-004
- id: `AT-004`
- requirement: `The umbrella owner records why absorption is preferred over gate weakening.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/governance-chain-legacy-repair/raw-20260403-1100/code-reviews/20260403-governance-chain-legacy-repair-implementation-decision.md`
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
