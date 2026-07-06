# Pre-Tests: develop-guarded-merge-entrypoint-enforcement-governance

## Acceptance Targets

### AT-001 raw develop merge is blocked before downstream gates

- acceptance target: `develop` 上没有 canonical guarded handshake 的 merge commit 会被 `pre-merge-commit` 立即拒绝，并明确提示改用 `freely pr-merge-guarded`
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- required evidence: `raw merge blocked with pr-merge-guarded guidance`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 guarded handshake still reaches governance materialization gate

- acceptance target: 当 canonical guarded state 和 completion marker 存在时，`pre-merge-commit` 仍继续执行 governance materialization gate，而不是被入口 enforcement 提前短路
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- required evidence: `guarded-state positive control still surfaces no-candidate-driven lifecycle evidence`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 guarded handshake still reaches promotion ownership gate

- acceptance target: duplicate promotion ownership 仍在 guarded handshake 存在时被 `pre-merge-commit` 拦下
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- required evidence: `duplicate develop promotion ownership is already active`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 canonical pr-merge-guarded paths remain valid under real hooks

- acceptance target: `pr-merge-guarded` 正常初始 merge 与 break-glass completion 继续通过真实 hook
- testing layer: governance
- target environment: `docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt` plus `docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
- required evidence: `normal receipt path pass` and `break-glass completion pass`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Raw develop merge commits without the canonical guarded handshake fail closed and point to freely pr-merge-guarded.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`

### AT-002
- id: `AT-002`
- requirement: `Entrypoint enforcement does not suppress governance materialization gate execution once guarded state exists.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`

### AT-003
- id: `AT-003`
- requirement: `Entrypoint enforcement does not suppress promotion ownership gating once guarded state exists.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`

### AT-004
- id: `AT-004`
- requirement: `Canonical pr-merge-guarded initial merge and break-glass completion still pass under the real hook contract.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
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
