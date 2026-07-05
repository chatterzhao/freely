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
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-switch-current-live-apikey-without-saved-slot`

### AT-002
- id: `AT-002`
- requirement: `manager bootstrap can accept and probe a usable current live apikey auth when no saved slot inventory exists.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-current-live-apikey-without-saved-slot`

### AT-003
- id: `AT-003`
- requirement: `The owner package remains governance-clean while absorbing the bounded residual slice.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/config/codex-current-live-apikey-bootstrap-without-saved-slot-governance/code-reviews/20260406-codex-current-live-apikey-bootstrap-without-saved-slot-verification.md`
