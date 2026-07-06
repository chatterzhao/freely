# Pre-Tests: cli-wrapper-packaging-and-regression-surface-governance

## Acceptance Targets

### AT-001 runnable wrappers are directly executable

- acceptance target: audited runnable wrappers can be invoked directly from the shell without `bash ./bin/...`
- testing layer: integration
- target environment: repository CLI entrypoints
- required evidence:
  - `./bin/check-tauri-probe-host`
  - `./bin/test-freely-fleet-status`
  - `./bin/test-rust-toolchain-preflight`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 ai help output is clean

- acceptance target: `freely ai --help` prints usage without shell-evaluated noise before the help body
- testing layer: integration
- target environment: ai CLI help surface
- required evidence: `./bin/ai --help`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 auth-change wake regression is deterministic

- acceptance target: `test-ai-cli-switch-triggers-auth-change-wake` passes in both the dedicated feature worktree and the primary worktree
- testing layer: integration
- target environment: auth-change wake regression fixture
- required evidence: `./bin/test-ai-cli-switch-triggers-auth-change-wake`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Audited runnable wrappers are directly executable.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/cli-wrapper-packaging-and-regression-surface-governance/raw-20260405-2358/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-verification.md`

### AT-002
- id: `AT-002`
- requirement: `ai help output is clean and deterministic.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/cli-wrapper-packaging-and-regression-surface-governance/raw-20260405-2358/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-verification.md`

### AT-003
- id: `AT-003`
- requirement: `auth-change wake regression behaves deterministically across equivalent worktrees.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/cli-wrapper-packaging-and-regression-surface-governance/raw-20260405-2358/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-verification.md`
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
