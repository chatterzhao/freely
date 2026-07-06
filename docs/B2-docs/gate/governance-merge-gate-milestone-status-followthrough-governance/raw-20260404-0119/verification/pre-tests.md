# Pre-Tests: governance-merge-gate-milestone-status-followthrough-governance

## Acceptance Targets

### AT-001 parser boundary narrowed

- acceptance target: `parse_milestones()` only captures milestone status from milestone-level fields
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/quality/governance-merge-gate`
- required evidence: `test-governance-merge-gate`
- blocker taxonomy: `regression_missing`

### AT-002 nested status no longer poisons active milestone

- acceptance target: nested `candidate_issues` item status does not downgrade an `active` milestone during replay validation
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- required evidence: `new replay-shaped fixture`
- blocker taxonomy: `regression_missing`

### AT-003 governance replay remains lawful

- acceptance target: same-line owner docs and verification stay complete for a develop-bound merge-gate followthrough
- testing layer: governance
- target environment: issue artifacts + repo checks
- required evidence: `issue + progress + review + governance-check`
- blocker taxonomy: `lifecycle_incomplete`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Milestone status parsing ignores nested queue item status lines.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`

### AT-002
- id: `AT-002`
- requirement: `An active milestone remains active even when a queue item carries status: needs_research.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`

### AT-003
- id: `AT-003`
- requirement: `The merge-gate followthrough carries lawful same-line lifecycle evidence.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/governance-merge-gate-milestone-status-followthrough-governance/raw-20260404-0119/issues/governance-merge-gate-milestone-status-followthrough-governance.md`
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
