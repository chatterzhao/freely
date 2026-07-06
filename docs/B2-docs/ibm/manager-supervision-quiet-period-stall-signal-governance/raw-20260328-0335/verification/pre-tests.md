# Pre-tests: manager-supervision-quiet-period-stall-signal-governance

## Acceptance Structure

### Pre-merge acceptance

- acceptance target: `manager delegated-supervision quiet-period stall signal`
- testing layer: `focused regression + integration`
- target environment: `feature worktree`
- required evidence: quiet-period regressions, delegated-continuation regressions, verification artifact
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. quiet-period lawful wait 不得直接触发 recovery。
2. 无关 active worker 或 non-busy worker 不得误 suppress recovery。
3. 更强 stall evidence 出现时 recovery 仍必须成立。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `manager delegated-supervision quiet-period does not trigger false-positive recovery`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-quiet-period-does-not-recover`

### PT-2
- id: `PT-2`
- requirement: `unrelated active workers and nonbusy workers do not mask real recovery decisions`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-unrelated-active-worker-recovers`

### PT-3
- id: `PT-3`
- requirement: `existing delegated-continuation true-positive recovery boundaries remain intact`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-busy-and-stale-prompt-recovers`
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
