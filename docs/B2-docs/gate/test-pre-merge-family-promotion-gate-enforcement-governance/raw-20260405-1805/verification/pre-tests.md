# Pre-Tests: test-pre-merge-family-promotion-gate-enforcement-governance

## Acceptance Targets

### AT-001 truth sources and gates change together

- acceptance target: the owner updates constitutional truth and directly coupled gate semantics in the same lifecycle
- testing layer: governance
- target environment: issue + `CONSTITUTION` + `LAWS` + references + gate package
- required evidence: `doc and gate package`
- blocker taxonomy: `definition_missing`

### AT-002 develop source-branch semantics are enforced

- acceptance target: `develop` accepts `test-pre-merge-*` family and `hotfix/*`, and blocks `feature/*` as the normal path
- testing layer: focused regression
- target environment: `pr-merge-guarded` plus related hook/gate tests
- required evidence: `source-branch regression`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 lifecycle automation stays out of scope

- acceptance target: the owner does not widen into stale automation, manifest generation, or batch-create UX
- testing layer: governance
- target environment: issue + tasks + milestone writeback
- required evidence: `owner scope remains narrow`
- blocker taxonomy: `lifecycle_incomplete`

## Pre-merge acceptance

1. `./bin/governance-check`
   - expectation: new candidate, milestone, and owner writeback remain structurally valid
2. `git diff --check`
   - expectation: new IBM package and writeback stay whitespace-clean

## Post-merge acceptance

1. Follow-on execution can update truth sources and gates in one owner without reopening the promote-model debate.
2. Later lifecycle automation work no longer needs to redefine who may promote into `develop`.

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Truth-source update and directly coupled gate enforcement are owned by the same lifecycle.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805/issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`

### AT-002
- id: `AT-002`
- requirement: `The owner targets develop source-branch enforcement around test-pre-merge family promotion semantics.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-pr-merge-guarded`

### AT-003
- id: `AT-003`
- requirement: `Lifecycle automation remains a later owner.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805/code-reviews/20260405-test-pre-merge-family-promotion-gate-enforcement-verification.md`
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
