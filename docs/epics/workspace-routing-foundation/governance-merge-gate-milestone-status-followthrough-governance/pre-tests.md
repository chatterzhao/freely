# Pre-Tests: governance-merge-gate-milestone-status-followthrough-governance

## Acceptance Targets

### AT-001 parser boundary narrowed

- acceptance target: `parse_milestones()` only captures milestone status from milestone-level fields
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/quality/governance-merge-gate`
- required evidence: `test-governance-merge-gate`
- blocker taxonomy: `regression_missing`

### AT-002 nested status no longer poisons active milestone

- acceptance target: nested `candidate_issues` item status does not downgrade an `active` milestone during replay validation
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- required evidence: `new replay-shaped fixture`
- blocker taxonomy: `regression_missing`

### AT-003 governance replay remains lawful

- acceptance target: same-line owner docs and verification stay complete for a develop-bound merge-gate followthrough
- testing layer: governance
- target environment: issue artifacts + repo checks
- required evidence: `issue + progress + review + governance-check`
- blocker taxonomy: `lifecycle_incomplete`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Milestone status parsing ignores nested queue item status lines.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`

### AT-002
- id: `AT-002`
- requirement: `An active milestone remains active even when a queue item carries status: needs_research.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`

### AT-003
- id: `AT-003`
- requirement: `The merge-gate followthrough carries lawful same-line lifecycle evidence.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/issues/governance-merge-gate-milestone-status-followthrough-governance.md`
