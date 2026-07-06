# Pre-Tests: governance-merge-gate-review-aware-regression-alignment-governance

## Acceptance Targets

### AT-001 mixed unresolved-candidate fixture is review-aware

- acceptance target: the implementation-bearing mixed unresolved-candidate regression stages a complete owner review artifact and follows the current allowed path
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- required evidence: `focused regression`
- blocker taxonomy: `regression_missing`

### AT-002 same-file borrowed-owner bypass stays blocked

- acceptance target: directly touched same-file `promoted` / `absorbed` candidates still require their own canonical owner evidence and fail with the concrete owner diagnostic
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- required evidence: `focused regression`
- blocker taxonomy: `regression_missing`

### AT-003 closeout truth remains narrow

- acceptance target: completed lifecycle truth records the absorbed regression alignment without widening this owner into broader merge-gate policy redesign
- testing layer: governance
- target environment: issue/progress/milestone artifacts
- required evidence: `issue + progress + verification + governance-check`
- blocker taxonomy: `lifecycle_incomplete`

## Pre-merge acceptance

1. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
   - expectation: the mixed unresolved-candidate implementation case stages a complete review artifact and then passes, while same-file borrowed-owner regressions still fail
2. `git diff --check`
   - expectation: the refreshed fixture and lifecycle docs stay whitespace-clean
3. `./bin/governance-check`
   - expectation: the narrow reopen lifecycle is complete and merge-ready

## Post-merge acceptance

1. Canonical `develop` keeps `bash docs/system/workspace/scripts/tests/test-governance-merge-gate` green after replay.
2. The follow-on keeps merge-gate semantics aligned with existing law: unresolved metadata repairs remain allowed with same-line owner evidence, and same-file borrowed-owner regressions remain blocked.

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `The mixed unresolved-candidate implementation regression stages review evidence and passes on the current allowed path.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/governance-merge-gate-review-aware-regression-alignment-governance/raw-20260404-0232/code-reviews/20260404-governance-merge-gate-review-aware-regression-alignment-verification.md`

### AT-002
- id: `AT-002`
- requirement: `Same-file promoted or absorbed borrowed-owner regressions remain blocked by canonical owner binding.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/governance-merge-gate-review-aware-regression-alignment-governance/raw-20260404-0232/code-reviews/20260404-governance-merge-gate-review-aware-regression-alignment-verification.md`

### AT-003
- id: `AT-003`
- requirement: `The closeout lane keeps this owner completed and bounded on canonical develop.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/governance-merge-gate-review-aware-regression-alignment-governance/raw-20260404-0232/code-reviews/20260404-governance-merge-gate-review-aware-regression-alignment-verification.md`
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
