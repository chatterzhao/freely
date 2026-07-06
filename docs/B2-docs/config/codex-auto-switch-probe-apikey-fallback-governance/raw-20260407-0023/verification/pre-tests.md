# Pre-Tests: codex-auto-switch-probe-apikey-fallback-governance

## Acceptance Targets

### AT-001 auto switch keeps probing saved apikey slots after all-unavailable account sweep

- acceptance target: `ai switch codex` continues to exec-probe saved `apikey-*` slots when saved account slots are all unavailable in the OAuth inventory sweep
- testing layer: integration
- target environment: `ai-cli` auto-switch path
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-all-unavailable-falls-back-to-exec`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 watchdog recovery shares the same all-unavailable apikey fallback

- acceptance target: watchdog probing does not return early on `all_unavailable:*` when saved `apikey-*` slots still need exec-based probing
- testing layer: integration
- target environment: watchdog availability path
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 issue lane remains governance-clean

- acceptance target: the bounded follow-on owner remains promotion-ready after the focused replay
- testing layer: governance
- target environment: dedicated feature worktree
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
  - `./bin/governance-check`
  - `git diff --check`
  - `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-2138-feature-codex-auto-switch-probe-apikey-fallback --issue docs/B2-docs/config/codex-auto-switch-probe-apikey-fallback-governance/raw-20260407-0023/issues/codex-auto-switch-probe-apikey-fallback-governance.md`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Auto switch keeps probing saved apikey slots when the account OAuth sweep reports all_unavailable.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-auto-switch-probe-apikey-fallback-governance/raw-20260407-0023/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-verification.md`

### AT-002
- id: `AT-002`
- requirement: `Watchdog recovery follows the same all_unavailable-to-apikey-exec fallback contract.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-auto-switch-probe-apikey-fallback-governance/raw-20260407-0023/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-verification.md`

### AT-003
- id: `AT-003`
- requirement: `The bounded owner package stays governance-clean and premerge-ready.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-auto-switch-probe-apikey-fallback-governance/raw-20260407-0023/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-verification.md`
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
