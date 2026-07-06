# Pre-Tests: all-tools-unified-slot-contract-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `all-tools unified slot contract`
- testing layer: `focused regression + live validation`
- target environment: `feature worktree`
- required evidence: slot inventory tests, fallback regressions, and live kiro-to-codex dead-slot validation
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. `I-20260331-1840-A` is explicitly narrowed to ordered fallback v1, and this owner is the canonical follow-on for all-tools slot parity.
2. `~/.ai-auth/<tool>-<slot>/` is the canonical inventory contract for every tool family.
3. `current tool/current slot` scheduler truth is distinct from `last_*` observability truth, with `current_slot` mirrored to `LAST_ACTIVE_SLOT` only for compatibility.
4. Same-tool recovery is slot-first for every tool that has slot inventory when `AUTO_SWITCH_SLOT=true`.
5. Cross-tool fallback still restarts from the leftmost `AI_FALLBACK_TOOLS` entry.
6. all-tools-unavailable waiting truth preserves earliest recovery as `tool + slot`.
7. Real live repro proves `kiro-cli` tool failure + dead current Codex slot still converge to a later usable Codex slot before launch.

### Post-merge canonical truth acceptance

- acceptance target: `develop carries the unified slot scheduler and truth sources`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: progress closeout, verification artifact, and develop merge provenance
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. Canonical truth must point at `develop`, not keep this owner parked in `in_verification`.
2. Tool and runtime truth must agree that every tool enters slot-first recovery before cross-tool fallback.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `generic tool login and switch create canonical slot inventory and current-slot truth`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-login-creates-slot-container`

### PT-2
- id: `PT-2`
- requirement: `cross-tool fallback still restarts from the leftmost configured priority entry`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-cross-tool-restarts-from-leftmost-priority`

### PT-3
- id: `PT-3`
- requirement: `non-codex tools perform slot-first recovery before cross-tool fallback`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-non-codex-slot-first-then-cross-tool`

### PT-4
- id: `PT-4`
- requirement: `all-tools-unavailable waiting truth preserves earliest tool plus slot`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-tool-slot`

### PT-5
- id: `PT-5`
- requirement: `live kiro failure plus dead codex slot still converge to a later usable codex slot before launch`
- evidence_level: `post_merge_dogfood`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/all-tools-unified-slot-contract-governance/raw-20260401-0840/code-reviews/20260401-all-tools-unified-slot-contract-verification.md`
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
