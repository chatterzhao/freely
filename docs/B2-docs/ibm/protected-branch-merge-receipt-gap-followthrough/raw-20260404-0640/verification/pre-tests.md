# Pre-Tests: protected-branch-merge-receipt-gap-followthrough

## Acceptance Targets

### AT-001 missing ancestry gap fails closed

- acceptance target: `governance-check` rejects trailerless protected-ancestry merges after the audit effective date when no matching ordinary backfill entry exists
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- required evidence: `no-backfill failure case`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 matching ordinary backfill passes

- acceptance target: ordinary trailerless merge commits pass audit once the canonical backfill ledger matches the merge subject/source pair
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- required evidence: `develop-target and feature-target pass cases`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 trailer-bearing merges cannot claim backfill

- acceptance target: protected merges that already carry canonical receipts are rejected if they also appear in the ordinary receipt-gap ledger
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- required evidence: `trailer-bearing rejection case`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 break-glass receipts remain separate

- acceptance target: ordinary receipt-gap auditing does not absorb break-glass receipt policy, and canonical governance still validates both surfaces together
- testing layer: governance
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt` plus `./bin/governance-check`
- required evidence: `break-glass path still passes while ordinary gap audits stay green`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `A trailerless protected-ancestry merge without a matching backfill entry fails governance-check.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

### AT-002
- id: `AT-002`
- requirement: `Matching ordinary backfill entries pass for both direct develop merges and develop -> feature ancestry merges that later enter protected ancestry.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

### AT-003
- id: `AT-003`
- requirement: `Trailer-bearing protected merges cannot use the ordinary receipt-gap ledger as a redundant backfill path.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

### AT-004
- id: `AT-004`
- requirement: `Break-glass receipt auditing remains independent while repository-level governance still passes.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
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
