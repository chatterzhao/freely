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

## Unit
- acceptance target: `opencode direct launcher`
- testing layer: `manual foreground`
- target environment: `feature worktree`
- required evidence: `syntax check, launch verification, session ID extraction`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `opencode launcher has no new logic units; it follows the existing direct adapter pattern. Automated unit tests for shell launch functions are out of scope for this absorbed contribution. Syntax validation (bash -n) passes for all modified files.`

## Integration
- acceptance target: `opencode direct adapter integration`
- testing layer: `runtime integration`
- target environment: `feature worktree daemon`
- required evidence: `daemon start, tool launch, lifecycle trace`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `opencode uses the existing direct adapter path with no new integration surface. Integration verified via daemon start: ai_launch_begin recorded with tool=opencode, tool_adapter=direct.`

## End-to-End
- acceptance target: `opencode full daemon lifecycle`
- testing layer: `end-to-end daemon`
- target environment: `real macOS host`
- required evidence: `full cycle trace, prompt build, model response`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `E2E validated via full daemon cycle: supervisor_started -> prompt build -> ai_launch_begin (tool=opencode, launch_kind=fresh) -> model response -> ai_cycle_finished -> lifecycle trace complete. OpenCode hit API error with default free model but deepseek-v4-pro confirmed working.`

## Real-Environment
- acceptance target: `opencode on real macOS host`
- testing layer: `real-environment daemon`
- target environment: `macOS with opencode v1.14.26`
- required evidence: `real daemon start, real AI model call, real session tracking`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: pass
- real_environment_reason: `Tested on real macOS host. opencode v1.14.26 launched via freely daemon with deepseek-v4-pro model. Session ID extracted (ses_233722117ffeOuUkPrDjl06elo). Lifecycle trace complete. The default free model (minimax-m2.5-free) hit API error but deepseek models work.`

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `generic tool login and switch create canonical slot inventory and current-slot truth`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-login-creates-slot-container`

### PT-2
- id: `PT-2`
- requirement: `cross-tool fallback still restarts from the leftmost configured priority entry`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-cross-tool-restarts-from-leftmost-priority`

### PT-3
- id: `PT-3`
- requirement: `non-codex tools perform slot-first recovery before cross-tool fallback`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-non-codex-slot-first-then-cross-tool`

### PT-4
- id: `PT-4`
- requirement: `all-tools-unavailable waiting truth preserves earliest tool plus slot`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-tool-slot`

### PT-5
- id: `PT-5`
- requirement: `live kiro failure plus dead codex slot still converge to a later usable codex slot before launch`
- evidence_level: `post_merge_dogfood`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/code-reviews/20260401-all-tools-unified-slot-contract-verification.md`

### PT-6
- id: `PT-6`
- requirement: `opencode direct launcher integration`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `runtime`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-1`
- case_design: `Launch opencode via direct adapter in auto mode, verify session ID extraction from print-logs output, verify tool validation passes.`
- artifact_ref: `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/code-reviews/20260401-all-tools-unified-slot-contract-verification.md`
