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
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-verification.md`

### AT-002
- id: `AT-002`
- requirement: `ai help output is clean and deterministic.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-verification.md`

### AT-003
- id: `AT-003`
- requirement: `auth-change wake regression behaves deterministically across equivalent worktrees.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/code-reviews/20260406-cli-wrapper-packaging-and-regression-surface-verification.md`
