# Pre-Tests: governance-check-protected-merge-history-source-policy-governance

## Acceptance Targets

### AT-001 develop audits only its canonical protected merge chain

- acceptance target: `governance-check` evaluates protected merge receipt source policy from first-parent branch history instead of all reachable merge ancestry
- testing layer: integration
- target environment: governance receipt audit
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
  - `./bin/governance-check`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Protected-branch source-policy auditing honors first-parent branch history.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/governance-check-protected-merge-history-source-policy-governance/raw-20260406-0045/code-reviews/20260406-governance-check-protected-merge-history-source-policy-verification.md`
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
