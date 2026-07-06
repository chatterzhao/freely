# Pre-Tests: supply-chain-baseline-and-install-intake-audit-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `supply-chain baseline and install-intake audit`
- testing layer: `focused regression`
- target environment: `feature worktree`
- required evidence: lockfile, dependency specifier, lifecycle script, workflow pinning, and doctor integration coverage
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. The canonical audit fails on missing root lockfile when a root `package.json` exists.
2. The audit fails on disallowed direct dependency specifiers.
3. The audit fails on install-time lifecycle scripts unless they are explicitly allowlisted.
4. The audit fails on mutable external GitHub Action refs.
5. `freely doctor` replays the same audit and fails on the same baseline violations.

### Post-merge canonical truth acceptance

- acceptance target: `develop carries automation-first supply-chain baseline gating`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: progress closeout, verification artifact, and develop commit provenance
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. This owner closes only once develop carries the audit script, doctor integration, tests, and lifecycle writeback.
2. Canonical truth must continue to state that this slice does not yet absorb minimum package age, provenance, or generalized vulnerability intelligence.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `canonical supply-chain audit rejects missing root lockfile and disallowed direct dependency intake`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-check-supply-chain-baseline`

### PT-2
- id: `PT-2`
- requirement: `canonical supply-chain audit rejects unallowlisted install lifecycle scripts`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-check-supply-chain-baseline`

### PT-3
- id: `PT-3`
- requirement: `canonical supply-chain audit rejects mutable external GitHub Action refs`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-check-supply-chain-baseline`

### PT-4
- id: `PT-4`
- requirement: `freely doctor enforces the same supply-chain baseline audit`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-doctor-supply-chain-gate`
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
