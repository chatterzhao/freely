# Pre-Tests: worktree-tool-boundary-bootstrap-governance

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `the owner is recorded as a narrow follow-on of the completed tool materialization family rather than a reopened umbrella`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/issues/worktree-tool-boundary-bootstrap-governance.md`

### PT-2
- id: `PT-2`
- requirement: `explicit sync tooling can rematerialize managed local tool boundaries into a fresh sibling worktree even when local tool directories are ignored`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`

### PT-3
- id: `PT-3`
- requirement: `managed worktree entrypoints call the rematerialization path automatically`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-wt-create-syncs-tooling`

### PT-4
- id: `PT-4`
- requirement: `protected-branch post-checkout auto-worktree creation also rematerializes managed tool boundaries`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-post-checkout-syncs-tooling`

### PT-5
- id: `PT-5`
- requirement: `tools that require launch-time writable-root extension include the sibling worktrees root in their launch contract`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-tool-launchers-iflow-add-dir`

### PT-6
- id: `PT-6`
- requirement: `governance truth remains internally consistent after adding the follow-on owner and standardizing the managed worktree path`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `./bin/governance-check`

## Pre-merge Focused Regression / Smoke

1. acceptance target:
   - sibling worktree creation no longer strands managed tool boundaries in the project root
2. testing layer:
   - shell regression
3. target environment:
   - feature worktree
4. required evidence:
   - `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
   - `bash docs/system/workspace/scripts/tests/test-wt-create-syncs-tooling`
   - `bash docs/system/workspace/scripts/tests/test-post-checkout-syncs-tooling`
   - `bash docs/system/workspace/scripts/tests/test-tool-launchers-iflow-add-dir`
   - `bash docs/system/workspace/scripts/tests/test-worktree-entry-flow`
5. blocker taxonomy:
   - `definition_missing`
   - `commands_only`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - repair the boundary bootstrap contract or managed entrypoint guidance without widening into generic runtime redesign

## Post-merge Integration Acceptance

1. acceptance target:
   - canonical `develop` and future sibling worktrees use the same managed tool boundary bootstrap contract
2. testing layer:
   - contract replay against `develop`
3. target environment:
   - `develop`
4. required evidence:
   - `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
   - `bash docs/system/workspace/scripts/tests/test-wt-create-syncs-tooling`
   - `bash docs/system/workspace/scripts/tests/test-post-checkout-syncs-tooling`
   - `./bin/governance-check`
5. blocker taxonomy:
   - `execution_pending_or_failed`
   - `evidence_plan_missing`
6. failure handling / replay expectation:
   - if additional tool surfaces still lack a managed boundary, reopen as another narrow tool-boundary follow-on instead of widening this owner
