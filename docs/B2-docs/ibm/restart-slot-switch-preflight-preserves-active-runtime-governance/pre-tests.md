# Pre-Tests: restart-slot-switch-preflight-preserves-active-runtime-governance

## Acceptance Targets

### AT-001 restart preflights before stop

- acceptance target: `freely restart` checks shared slot-switch readiness before stopping the current project runtime
- testing layer: integration
- target environment: runtime command semantics
- required evidence: `test-freely-project-command-semantics`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 active lock preserves running runtime

- acceptance target: an active shared slot-switch lock blocks restart without killing the already-running project supervisor or AI child
- testing layer: integration
- target environment: runtime script end-to-end restart flow
- required evidence: `test-freely-restart-preserves-runtime-on-active-slot-switch-lock`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 restart-adjacent durability regressions remain green

- acceptance target: the helper hardenings do not regress the adjacent runtime surfaces they touch
- testing layer: integration
- target environment: session rotation, checkpoint, auth-change wake, and switch serialization flows
- required evidence:
  - `test-freely-session-rotation`
  - `test-freely-ai-account-switch-serialization`
  - `test-ai-cli-login-triggers-auth-change-wake`
  - `test-ai-cli-login-does-not-block-on-auth-change-wake`
  - `test-freely-checkpoint-governance`
  - `test-freely-checkpoint-drift-escalation`
  - `test-freely-codex-current-slot-does-not-capture-switch-warning`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 issue-bound implementation decision note present

- acceptance target: the restart follow-on owner includes a decision note that explains why this is a new lifecycle instead of a reopen of the completed startup or project-command owners
- testing layer: IBM review
- target environment: verification artifact dir
- required evidence: `implementation decision note`
- blocker taxonomy: `definition_missing`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Restart preflight runs before any project-local stop.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

### AT-002
- id: `AT-002`
- requirement: `Active shared lock preserves the currently running project runtime.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-restart-preserves-runtime-on-active-slot-switch-lock`

### AT-003
- id: `AT-003`
- requirement: `Restart-adjacent durability changes do not regress the touched runtime surfaces.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/code-reviews/20260405-restart-slot-switch-preflight-verification.md`

### AT-004
- id: `AT-004`
- requirement: `Develop-bound runtime edits are backed by an issue-bound restart-specific decision note.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/code-reviews/20260405-restart-slot-switch-preflight-implementation-decision.md`
