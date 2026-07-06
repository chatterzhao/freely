# Pre-tests: ai-auth-change-wake-command-lifecycle-governance

## Acceptance Structure

### Pre-merge acceptance

- acceptance target: `ai auth-change wake command lifecycle`
- testing layer: `focused regression + command replay`
- target environment: `feature worktree`
- required evidence: focused switch/login lifecycle regressions and verification artifact
- blocker taxonomy:
  - `definition_missing`
  - `repro_gap`
  - `reentrancy_gap`
  - `commands_only`
  - `execution_pending_or_failed`

1. `ai switch codex <current-slot>` 成功后必须及时退出。
2. `ai switch` success-path 不得被同步 `auth-change-wake` 长时间拖住。
3. watchdog-triggered slot handling 不得重新回流到同一 notify loop。
4. 修复不得要求真实 `login` 或 slot 删除。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `ai switch codex exits before auth-change wake completes`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-same-slot-switch-does-not-block-on-auth-change-wake`

### PT-2
- id: `PT-2`
- requirement: `successful login-path notify semantics no longer block the foreground command lifecycle`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-login-does-not-block-on-auth-change-wake`

### PT-3
- id: `PT-3`
- requirement: `watchdog-triggered slot handling suppresses the recursive auth-change wake loop`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-watchdog-switch-to-codex-slot-suppresses-auth-change-wake`

### PT-4
- id: `PT-4`
- requirement: `repair preserves adjacent auth inventory behavior without requiring real login or slot deletion`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/ai-auth-change-wake-command-lifecycle-governance/raw-20260329-2045/code-reviews/20260330-ai-auth-change-wake-command-lifecycle-verification.md`
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
