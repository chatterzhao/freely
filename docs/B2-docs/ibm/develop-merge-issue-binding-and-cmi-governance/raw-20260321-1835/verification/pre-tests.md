# Pre-tests: develop-merge-issue-binding-and-cmi-governance

## Acceptance Structure

### Pre-merge acceptance

1. standalone gate 会拒绝没有具体 issue/progress/review owner 的 develop merge
2. standalone gate 会拒绝 touched candidate 借 unrelated owner issue 过门禁
3. `absorbed` candidate 若 owner issue 不在同次 diff，会被拒绝
4. standalone gate 会放行 same-line direct issue touch
5. standalone gate 会放行 `promoted` candidate + canonical owner issue/progress
6. standalone gate 会放行 `absorbed` candidate + canonical owner issue/progress
7. standalone gate 会拒绝 `promoted` candidate 借不同 lifecycle 线的 progress owner
8. `pre-merge-commit` 真实 merge 路径仍会命中同一 gate

### Post-merge acceptance

1. develop 中的后续 issue-bound merge 会默认沿用这条更硬的 owner binding rule

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `governance-merge-gate rejects develop merges without issue-bound ownership`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`

### PT-2
- id: `PT-2`
- requirement: `governance-merge-gate rejects absorbed candidates that borrow an unrelated owner issue`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`

### PT-3
- id: `PT-3`
- requirement: `pre-merge-commit still invokes governance-merge-gate on real git merge`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`

### PT-4
- id: `PT-4`
- requirement: `governance-merge-gate allows same-line direct issue touches on a promoted lifecycle line`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`

### PT-5
- id: `PT-5`
- requirement: `governance-merge-gate allows promoted candidates that carry their canonical owner issue/progress in the same diff`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`

### PT-6
- id: `PT-6`
- requirement: `governance-merge-gate allows absorbed candidates that carry their canonical owner issue/progress in the same diff`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`

### PT-7
- id: `PT-7`
- requirement: `governance-merge-gate rejects promoted candidates that try to use a progress owner from a different lifecycle line`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`
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
