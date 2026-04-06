# Pre-Tests: milestone-completed-queue-closeout-governance

## Acceptance Targets

### AT-001 completed owner queue drift is rejected

- acceptance target: `governance-check` fails when a milestone leaves a `phase_state=completed` issue in `committed_issues`
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-milestone-phase-queue-alignment`
- required evidence: `failure fixture plus repaired pass path`
- blocker taxonomy: `regression_missing`

### AT-002 candidate v2 audit still passes beside the new queue audit

- acceptance target: existing candidate v2 governance coverage still passes after the queue/phase audit lands
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
- required evidence: `existing v2 candidate regression remains green`
- blocker taxonomy: `regression_missing`

### AT-003 canonical baseline no longer carries queue drift

- acceptance target: canonical repo truth passes `./bin/governance-check` once completed owners are moved to `completed_issues`
- testing layer: governance baseline audit
- target environment: dedicated owner worktree
- required evidence: `repaired milestone truth plus green governance-check`
- blocker taxonomy: `lifecycle_incomplete`

### AT-004 patch is whitespace-clean

- acceptance target: the closeout patch remains free of diff formatting errors
- testing layer: static patch validation
- target environment: dedicated owner worktree
- required evidence: `git diff --check`
- blocker taxonomy: `commands_only`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `A completed issue referenced from docs/milestones.md fails governance-check unless it lives only in completed_issues.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/code-reviews/20260406-milestone-completed-queue-closeout-verification.md`

### AT-002
- id: `AT-002`
- requirement: `The milestone queue audit does not regress existing v2 candidate governance coverage.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/code-reviews/20260406-milestone-completed-queue-closeout-verification.md`

### AT-003
- id: `AT-003`
- requirement: `Canonical milestone truth and the new queue/phase audit pass together on the owner worktree.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/code-reviews/20260406-milestone-completed-queue-closeout-verification.md`

### AT-004
- id: `AT-004`
- requirement: `The owner patch remains free of diff-formatting defects before promotion.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/code-reviews/20260406-milestone-completed-queue-closeout-verification.md`
