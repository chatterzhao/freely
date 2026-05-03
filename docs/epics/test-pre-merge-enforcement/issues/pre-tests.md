# Pre-Tests: Enforce Test-Pre-Merge Gate

## Acceptance Targets

### AT-001 merge-guarded enforces correct merge direction

- acceptance target: `merge-guarded` rejects invalid merge directions (feature→develop, hotfix→develop, feature→main) and allows valid ones (feature→test-pre-merge, test-pre-merge→develop)
- testing layer: integration
- target environment: isolated temp git repo
- required evidence: `bash docs/system/workspace/scripts/tests/test-merge-guarded`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 merge-guarded records guarded merge receipts

- acceptance target: each guarded merge produces a commit with canonical `Freely-Merge-Path`, `Freely-Bypass-Mode`, and `Freely-Source-Branch` trailers
- testing layer: integration
- target environment: isolated temp git repo
- required evidence: `bash docs/system/workspace/scripts/tests/test-merge-guarded`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 merge-guarded supports controlled conflict completion

- acceptance target: textual merge conflicts leave the merge state intact and `merge-guarded complete` finishes the merge with correct receipt trailers
- testing layer: integration
- target environment: isolated temp git repo
- required evidence: `bash docs/system/workspace/scripts/tests/test-merge-guarded`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 merge-guarded supports break-glass completion

- acceptance target: hotfix→develop break-glass merge produces `Freely-Break-Glass-Reason`, `Freely-Evidence-Ref`, and `Freely-Follow-On-Issue` trailers
- testing layer: integration
- target environment: isolated temp git repo
- required evidence: `bash docs/system/workspace/scripts/tests/test-merge-guarded`
- blocker taxonomy: `execution_pending_or_failed`

### AT-005 governance-merge-gate validates C/M/I lifecycle chain

- acceptance target: `governance-merge-gate` blocks merges that lack proper candidate→milestone→issue lifecycle evidence
- testing layer: unit
- target environment: feature worktree with governance artifacts
- required evidence: `./bin/governance-merge-gate --range develop..HEAD`
- blocker taxonomy: `execution_pending_or_failed`

### AT-006 governance-check verifies repo-wide governance consistency

- acceptance target: `./bin/governance-check` reports governance artifacts consistent, with no errors specific to the feature branch
- testing layer: integration
- target environment: feature worktree
- required evidence: `./bin/governance-check`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `merge-guarded rejects invalid merge directions and allows valid ones.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`

### AT-002
- id: `AT-002`
- requirement: `Each guarded merge produces canonical Freely-* trailers in the merge commit.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`

### AT-003
- id: `AT-003`
- requirement: `merge-guarded handles conflict completion with correct receipt trailers.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`

### AT-004
- id: `AT-004`
- requirement: `merge-guarded break-glass path produces correct break-glass trailers.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`

### AT-005
- id: `AT-005`
- requirement: `governance-merge-gate validates C/M/I lifecycle.`
- evidence_level: `unit`
- status: `pass`
- artifact_ref: `docs/epics/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`

### AT-006
- id: `AT-006`
- requirement: `governance-check verifies repo-wide governance consistency.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/test-pre-merge-enforcement/code-reviews/rev-20260503-enforce-test-pre-merge.md`
