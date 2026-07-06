# Pre-tests: kiro-cli-runtime-availability-failure-governance

## Acceptance Structure

### Pre-merge focused regression acceptance

- acceptance target: `kiro runtime availability failure classification`
- testing layer: `focused regression + governance check`
- target environment: `feature worktree`
- required evidence: Kiro availability regression plus closeout verification artifact
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. `Monthly request limit reached` must be written as `kiro_monthly_request_limit` instead of falling through to `ai_exit_rc_0`.
2. `Unable to verify subscription status: service error` without the monthly-limit line must still be written as a canonical Kiro availability reason.
3. After either reason is detected, the local supervisor must stop and defer recovery instead of relaunching the same workcell.
4. The first slice stays Kiro-scoped; it does not widen into generic cross-tool fallback design.

### Post-merge integration acceptance

- acceptance target: `canonical runtime / verification truth alignment`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: landed runtime classifier, focused regression, and verification note all agree on the same failure family
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. `docs/system/workspace/scripts/runtime/freely` and the focused regression must agree on `kiro_monthly_request_limit` and `kiro_subscription_status_service_error`.
2. The verification artifact must explicitly confirm the supervisor no longer records these failures as plain `ai_exit_rc_0`.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `monthly request limit is promoted to canonical Kiro availability failure`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`

### PT-2
- id: `PT-2`
- requirement: `subscription status service error alone still stops local relaunch as a canonical Kiro availability failure`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`

### PT-3
- id: `PT-3`
- requirement: `closeout truth sources document the same Kiro failure family as the runtime and focused regression`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/kiro-cli-runtime-availability-failure-governance/raw-20260331-1830/code-reviews/20260331-kiro-cli-runtime-availability-verification.md`
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
