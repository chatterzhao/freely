# Pre-Tests: codex-current-live-apikey-bootstrap-without-saved-slot-governance

## Acceptance Targets

### AT-001 ai switch accepts usable current live apikey without saved-slot inventory

- acceptance target: `ai switch codex` preserves a bounded usable-current-live path when live Codex apikey auth exists but saved-slot inventory is empty
- testing layer: integration
- target environment: `ai-cli` current-live switch path
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-current-live-apikey-without-saved-slot`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 manager bootstrap accepts current-live apikey identity without saved-slot inventory

- acceptance target: watchdog/bootstrap can probe and assess readiness for a live current Codex apikey auth without requiring a pre-existing saved slot
- testing layer: integration
- target environment: watchdog bootstrap path
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-current-live-apikey-without-saved-slot`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 issue lane remains governance-clean

- acceptance target: the owner package and absorbed residual slice remain aligned with governance gates
- testing layer: governance
- target environment: dedicated feature worktree
- required evidence:
  - `./bin/governance-check`
  - `git diff --check`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `ai switch codex can accept a usable current live apikey auth when no saved slot inventory exists.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-switch-current-live-apikey-without-saved-slot`

### AT-002
- id: `AT-002`
- requirement: `manager bootstrap can accept and probe a usable current live apikey auth when no saved slot inventory exists.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-current-live-apikey-without-saved-slot`

### AT-003
- id: `AT-003`
- requirement: `The owner package remains governance-clean while absorbing the bounded residual slice.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-current-live-apikey-bootstrap-without-saved-slot-governance/raw-20260406-1829/code-reviews/20260406-codex-current-live-apikey-bootstrap-without-saved-slot-verification.md`
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
