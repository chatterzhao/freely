# Pre-Tests: build-artifact-exposure-and-release-allowlist-audit-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `build artifact exposure audit and release allowlist`
- testing layer: `focused regression`
- target environment: `feature worktree`
- required evidence: forbidden artifact rejection, allowlist enforcement, and doctor/build integration
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. The audit rejects forbidden artifacts such as `.map` and `.env*`.
2. The audit rejects build outputs that are not explicitly allowlisted.
3. `freely doctor` fails on dirty build output and passes on clean, allowlisted output.
4. Existing hook/doc gate truth remains green after the doctor audit is added.

### Post-merge canonical truth acceptance

- acceptance target: `develop carries automation-first artifact exposure gating`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: progress closeout, verification artifact, and develop commit provenance
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. This owner closes only once develop carries the audit script, doctor enforcement, allowlist truth, and build-path integration.
2. Canonical truth must continue to state that the first slice is narrow and does not yet absorb broader supply-chain or full secret-scanning work.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `forbidden build artifacts are rejected by the canonical audit`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-build-artifact-exposure-audit`

### PT-2
- id: `PT-2`
- requirement: `non-allowlisted build output files are rejected`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-build-artifact-exposure-audit`

### PT-3
- id: `PT-3`
- requirement: `freely doctor enforces build artifact audit when build output exists`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-doctor-build-artifact-exposure-gate`

### PT-4
- id: `PT-4`
- requirement: `doctor hook/doc gate behavior remains green after adding the build artifact audit`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/build-artifact-exposure-and-release-allowlist-audit-governance/raw-20260401-2245/code-reviews/20260401-build-artifact-exposure-and-release-allowlist-verification.md`
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
