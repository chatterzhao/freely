# Pre-Tests: codex-interactive-login-and-apikey-input-flow-governance

## Acceptance Targets

### AT-001 interactive login mode selection routes Codex auth flow

- acceptance target: `freely ai login codex` exposes a bounded interactive mode selector that can route into `account` or `apikey`
- testing layer: integration
- target environment: `ai-cli` login flow
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-interactive-mode-selection`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 interactive apikey prompts materialize Codex bundle and saved slot

- acceptance target: `freely ai login codex apikey` collects provider/base-url/api-key interactively and saves the resulting Codex slot
- testing layer: integration
- target environment: `ai-cli` login flow
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-interactive`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 direct args preserve interactive API-key login parity

- acceptance target: `freely ai login codex apikey --name --url --key` preserves the same bounded Codex API-key login contract without prompts
- testing layer: integration
- target environment: `ai-cli` login flow
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-direct-args`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 empty required input fails without mutating auth state

- acceptance target: empty interactive API-key input exits with bounded failure and does not mutate live auth/config or saved-slot state
- testing layer: integration
- target environment: `ai-cli` login flow
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-empty-input-fails`
- blocker taxonomy: `execution_pending_or_failed`

### AT-005 issue lane remains governance-clean

- acceptance target: the owner package and interactive login implementation stay aligned with governance gates
- testing layer: integration
- target environment: dedicated feature worktree
- required evidence:
  - `./bin/governance-check`
  - `git diff --check`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `freely ai login codex can route interactively between account and apikey modes.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-login-codex-interactive-mode-selection`

### AT-002
- id: `AT-002`
- requirement: `Interactive Codex API-key login collects provider/base-url/api-key and saves a slot.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-interactive`

### AT-003
- id: `AT-003`
- requirement: `Direct-arg Codex API-key login preserves the same bounded login contract as the interactive path.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-direct-args`

### AT-004
- id: `AT-004`
- requirement: `Empty required input fails without mutating live auth/config or saved-slot state.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-empty-input-fails`

### AT-005
- id: `AT-005`
- requirement: `The owner package remains governance-clean while absorbing the bounded interactive login patch.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/code-reviews/20260406-codex-interactive-login-and-apikey-input-flow-verification.md`
