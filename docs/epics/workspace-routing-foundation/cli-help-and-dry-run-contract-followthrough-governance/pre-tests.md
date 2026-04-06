# Pre-Tests: cli-help-and-dry-run-contract-followthrough-governance

## Acceptance Targets

### AT-001 help commands are explicit and side-effect free

- acceptance target: audited help invocations return a deliberate usage contract instead of entering create/merge/runtime command paths
- testing layer: integration
- target environment: repository CLI entrypoints and sourced worktree helpers
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-cli-help-contracts`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 ai dry-run output is bounded and machine-readable

- acceptance target: `ai switch codex --dry-run --format json` returns one stable JSON result that reflects saved-slot inventory without requiring the full probe/switch path
- testing layer: integration
- target environment: isolated ai-cli home fixture
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-dry-run-contract`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 issue lane remains governance-clean

- acceptance target: the owner package, code, and focused regressions remain aligned with governance gates
- testing layer: governance
- target environment: dedicated feature worktree
- required evidence:
  - `./bin/governance-check`
  - `git diff --check`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Audited help invocations are explicit, side-effect free, and success-returning for usage-only paths.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/code-reviews/20260406-cli-help-and-dry-run-contract-followthrough-verification.md`

### AT-002
- id: `AT-002`
- requirement: `ai switch codex dry-run output is stable and machine-consumable.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/code-reviews/20260406-cli-help-and-dry-run-contract-followthrough-verification.md`

### AT-003
- id: `AT-003`
- requirement: `Governance gates remain green for the bounded owner.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-help-and-dry-run-contract-followthrough-governance/code-reviews/20260406-cli-help-and-dry-run-contract-followthrough-verification.md`
