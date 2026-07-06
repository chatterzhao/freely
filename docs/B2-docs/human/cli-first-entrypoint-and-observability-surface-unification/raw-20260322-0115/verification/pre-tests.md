# Pre-Tests: cli-first-entrypoint-and-observability-surface-unification

1. `freely tui` 提交消息后，与 `freely chat` 一样能够触发 dispatcher ensure。
2. `freely tui` 在 worker continuation 场景下，也能触发允许的 runtime reactivation。
3. 真源明确 CLI-first backend contract，未来 TUI/GUI 只复用，不另造语义。

## Acceptance Items

### shared-submit-chain
- id: `shared-submit-chain`
- requirement: freely tui must enter the same high-level submit helper and dispatcher ensure path that freely chat uses.
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/raw-20260322-0115/code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`

### tui-worker-reactivation-gate
- id: `tui-worker-reactivation-gate`
- requirement: freely tui must trigger the same allowed worker runtime reactivation gate as freely chat during continuation flows.
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/raw-20260322-0115/code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`

### cli-first-contract-preserved
- id: `cli-first-contract-preserved`
- requirement: canonical truth must continue to state that freely is the only front-door command and that TUI/GUI are render layers over the same backend contract.
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/raw-20260322-0115/code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`
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
