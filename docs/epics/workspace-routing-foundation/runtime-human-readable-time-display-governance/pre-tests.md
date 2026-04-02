# Pre-Tests: runtime-human-readable-time-display-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `runtime human-readable time display surfaces`
- testing layer: `focused regression`
- target environment: `feature worktree`
- required evidence: runtime status, ai-cli, intake, and develop-push local-time rendering coverage
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. `freely live-status` renders human-facing timestamps in host-local time with timezone label.
2. `freely baseline-status` renders `activation_consent_recorded_at` in host-local time with timezone label.
3. `freely develop-push status` renders defer timestamps in host-local time with timezone label.
4. Intake status renders `created_at` in host-local time with timezone label.
5. `freely ai status` preserves raw truth and emits `refreshed_at_human`.
6. Watchdog cooldown human text remains host-local with timezone label.

### Post-merge canonical truth acceptance

- acceptance target: `develop carries the runtime human-readable time display contract`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: issue/progress/review writeback plus focused command evidence
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. This owner only closes once the runtime/status implementation, focused tests, and lifecycle writeback all land on `develop`.
2. Canonical truth must continue to state that machine truth and UTC naming are unchanged.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `freely ai status preserves refresh truth and adds host-local human-readable refresh output`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ai-account-switch`

### PT-2
- id: `PT-2`
- requirement: `baseline and live status surfaces render human-facing timestamps in host-local time with timezone label`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-baseline-status`

### PT-3
- id: `PT-3`
- requirement: `live-status renders runtime update and intake timestamps in host-local time without mutating stored truth`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-live-status`

### PT-4
- id: `PT-4`
- requirement: `develop-push and execution-boundary surfaces render local display timestamps`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`

### PT-5
- id: `PT-5`
- requirement: `direct develop-push status command renders defer timestamps in host-local time`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-develop-push-status-time-display`

### PT-6
- id: `PT-6`
- requirement: `intake status renders created_at in host-local time`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-human-chat-intake`
