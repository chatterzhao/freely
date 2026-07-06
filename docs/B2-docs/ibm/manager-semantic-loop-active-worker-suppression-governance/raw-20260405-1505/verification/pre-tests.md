# Pre-Tests: manager-semantic-loop-active-worker-suppression-governance

## Acceptance Targets

### AT-001 active worker execution suppresses semantic-loop suspicion

- acceptance target: the semantic-loop regression still detects the zero-worker loop shape, but clears once worker supervisor and AI execution are already active
- testing layer: integration
- target environment: feature worktree runtime scripts plus focused regression
- required evidence: `semantic-loop regression replay`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 adjacent status surfaces stay stable

- acceptance target: `live-status` and `fleet-status` keep their current runtime/status surfaces healthy while the suppression fallback is active
- testing layer: integration
- target environment: feature worktree runtime scripts
- required evidence: `status regression replay`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 closeout stays bounded to semantic-loop suppression

- acceptance target: lifecycle truth records the new follow-on owner without reopening completed `I-20260322-0445` or widening into unrelated stall recovery
- testing layer: IBM review
- target environment: issue/progress/milestone artifacts
- required evidence: `issue + progress + milestone + implementation decision note`
- blocker taxonomy: `definition_missing`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Semantic-loop monitoring clears once active worker execution is already present while preserving the zero-worker signal path.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/manager-semantic-loop-active-worker-suppression-governance/raw-20260405-1505/code-reviews/20260405-manager-semantic-loop-active-worker-suppression-verification.md`

### AT-002
- id: `AT-002`
- requirement: `Adjacent live-status and fleet-status regressions remain green after the suppression fallback lands.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/manager-semantic-loop-active-worker-suppression-governance/raw-20260405-1505/code-reviews/20260405-manager-semantic-loop-active-worker-suppression-verification.md`

### AT-003
- id: `AT-003`
- requirement: `The closeout lane materializes a new bounded owner instead of reopening completed I-20260322-0445.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/manager-semantic-loop-active-worker-suppression-governance/raw-20260405-1505/code-reviews/20260405-manager-semantic-loop-active-worker-suppression-implementation-decision.md`
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
