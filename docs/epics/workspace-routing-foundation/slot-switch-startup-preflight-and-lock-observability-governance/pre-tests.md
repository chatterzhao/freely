# Pre-Tests: slot-switch-startup-preflight-and-lock-observability-governance

## Acceptance Targets

### AT-001 startup stale lock self-repair

- acceptance target: `freely start` auto-cleans a stale shared slot-switch lock and proceeds
- testing layer: integration
- target environment: feature worktree runtime script
- required evidence: `test-freely-start-cleans-stale-slot-switch-lock`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 startup active lock bounded failure

- acceptance target: `freely start` does not force-remove a live shared slot-switch lock and fails/defer clearly after bounded wait
- testing layer: integration
- target environment: feature worktree runtime script
- required evidence: `test-freely-start-times-out-on-active-slot-switch-lock`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 structured lock observability

- acceptance target: `doctor` and status output expose structured current slot-switch lock truth without raw `sed` noise
- testing layer: integration
- target environment: feature worktree status and doctor surfaces
- required evidence: `test-freely-slot-switch-lock-status-surface`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 implementation decision note present

- acceptance target: the issue has an implementation decision note that explains why shared helper taxonomy beats ad hoc start-only handling
- testing layer: IBM review
- target environment: verification artifact dir
- required evidence: `implementation decision note`
- blocker taxonomy: `definition_missing`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Stale shared slot-switch locks are auto-cleaned during startup preflight.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-slot-switch-lock`

### AT-002
- id: `AT-002`
- requirement: `Active shared slot-switch locks remain non-destructively handled by startup.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-start-times-out-on-active-slot-switch-lock`

### AT-003
- id: `AT-003`
- requirement: `Structured current lock truth is visible on status and doctor surfaces.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-slot-switch-lock-status-surface`

### AT-004
- id: `AT-004`
- requirement: `Develop-bound runtime edits are backed by an issue-bound decision note.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/code-reviews/20260404-slot-switch-startup-preflight-and-lock-observability-implementation-decision.md`
