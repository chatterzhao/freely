# Pre-Tests: develop-push-followthrough-escalation-governance

## Acceptance Targets

### AT-001 timely push becomes the default followthrough

- acceptance target: after a lawful protected-branch merge, push is the default next step unless a lawful defer reason is active
- testing layer: governance
- target environment: laws + manager followthrough truth
- required evidence: `issue package`
- blocker taxonomy: `definition_missing`

### AT-002 lawful defer reasons stay finite and reviewable

- acceptance target: defer reasons use a bounded whitelist and record a concrete recovery point
- testing layer: governance
- target environment: status / patrol / manager continuity semantics
- required evidence: `defer taxonomy`
- blocker taxonomy: `definition_missing`

### AT-003 stale worktrees must resync before latest-develop-sensitive judgment

- acceptance target: active worktrees that need the newest protected truth for owner judgment, verification, cleanup, or absorption are marked `resync_required`
- testing layer: governance
- target environment: multi-worktree sequencing contract
- required evidence: `resync trigger contract`
- blocker taxonomy: `definition_missing`

### AT-004 auto-push stays out of scope

- acceptance target: the followthrough contract does not collapse into hidden hook/runtime network side effects
- testing layer: governance
- target environment: manager/runtime boundary
- required evidence: `boundary review`
- blocker taxonomy: `definition_missing`

## Pre-merge acceptance

1. `git diff --check`
   - expectation: new owner docs remain whitespace-clean
2. `./bin/governance-check`
   - expectation: candidate promotion, milestone writeback, and IBM package structure remain valid

## Post-merge acceptance

1. Future manager patrol can say whether push is immediately due or lawfully deferred.
2. Future active worktrees no longer continue latest-develop-sensitive judgment on stale upstream without an explicit resync check.
3. The project keeps explicit operator push semantics rather than silent auto-push.

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Timely push is the default followthrough after a lawful merge unless a lawful defer is active.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/develop-push-followthrough-escalation-governance/issues/develop-push-followthrough-escalation-governance.md`

### AT-002
- id: `AT-002`
- requirement: `Defer reasons are finite, reviewable, and recovery-bearing.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/develop-push-followthrough-escalation-governance/brainstorms/b-develop-push-followthrough-escalation-governance.md`

### AT-003
- id: `AT-003`
- requirement: `Stale active worktrees are required to resync before latest-develop-sensitive judgment.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/develop-push-followthrough-escalation-governance/prd.md`

### AT-004
- id: `AT-004`
- requirement: `The owner keeps auto-push out of scope.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/pre-brainstorms/20260408-1200--develop-push-followthrough-escalation/brainstorms.md`
