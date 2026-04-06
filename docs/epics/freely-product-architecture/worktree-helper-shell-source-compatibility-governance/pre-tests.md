# Pre-Tests: worktree-helper-shell-source-compatibility-governance

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `the owner is recorded as a narrow follow-on to the completed worktree helper/tooling family rather than an umbrella reopen`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/worktree-helper-shell-source-compatibility-governance/issues/worktree-helper-shell-source-compatibility-governance.md`

### PT-2
- id: `PT-2`
- requirement: `documented wt-add and wt-enter wrapper commands are source-safe in the default shell context`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-wt-wrapper-shell-source-compatibility`

### PT-3
- id: `PT-3`
- requirement: `wrapper-path regressions still preserve current worktree entry behavior`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-worktree-entry-flow`

### PT-4
- id: `PT-4`
- requirement: `candidate, milestone, issue, progress, and develop-bound artifacts stay internally consistent`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `./bin/governance-check`

## Pre-merge Focused Regression / Smoke

1. acceptance target:
   - documented worktree helper commands are callable from default shell context and preserve helper semantics
2. testing layer:
   - shell regression
3. target environment:
   - feature worktree
4. required evidence:
   - `bash docs/system/workspace/scripts/tests/test-worktree-entry-flow`
   - `bash docs/system/workspace/scripts/tests/test-wt-wrapper-shell-source-compatibility`
   - `./bin/governance-check`
5. blocker taxonomy:
   - `definition_missing`
   - `contract_drift`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - repair wrapper source-safety or wrapper-path tests without widening into helper redesign

## Post-merge Integration Acceptance

1. acceptance target:
   - canonical `develop` preserves the documented helper command contract in the default shell context
2. testing layer:
   - contract replay against `develop`
3. target environment:
   - `develop`
4. required evidence:
   - `bash docs/system/workspace/scripts/tests/test-worktree-entry-flow`
   - `bash docs/system/workspace/scripts/tests/test-wt-wrapper-shell-source-compatibility`
   - `./bin/governance-check`
5. blocker taxonomy:
   - `execution_pending_or_failed`
   - `contract_drift`
6. failure handling / replay expectation:
   - reopen only if documented sourced helper commands regress again or a broader wrapper family is proven broken
