# Pre-Tests: project-level-agents-bootstrap-and-management-contract-governance

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `workspace capability docs formally define project-level AGENTS bootstrap, read-order, preservation, and self-hosting semantics`
- evidence_level: `doc-read`
- status: `pass`
- artifact_ref: `docs/system/workspace/project-agents-contract.md`

### PT-2
- id: `PT-2`
- requirement: `freely init preserves an existing project-owned AGENTS.md instead of overwriting it`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-init-preserves-existing-agents-md`

### PT-3
- id: `PT-3`
- requirement: `existing init regressions still prove missing AGENTS.md is created`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-init-cc-config`

### PT-4
- id: `PT-4`
- requirement: `candidate, milestone, issue, progress, and verification artifacts form a lawful develop-bound chain`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `./bin/governance-check`

## Pre-merge Focused Regression / Smoke

1. acceptance target:
   - project-level `AGENTS.md` behavior is frozen as a reusable contract rather than implicit runtime trivia
2. testing layer:
   - focused runtime/doc regression
3. target environment:
   - feature worktree
4. required evidence:
   - `bash docs/system/workspace/scripts/tests/test-freely-init-preserves-existing-agents-md`
   - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
   - `bash docs/system/workspace/scripts/tests/test-freely-init-ai-default-precedence`
   - `./bin/governance-check`
5. blocker taxonomy:
   - `definition_missing`
   - `contract_drift`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - repair the capability contract or preserve-existing test without widening into richer template management

## Post-merge Integration Acceptance

1. acceptance target:
   - canonical `develop` preserves the same project-level AGENTS contract and test coverage
2. testing layer:
   - contract replay against `develop`
3. target environment:
   - `develop`
4. required evidence:
   - `bash docs/system/workspace/scripts/tests/test-freely-init-preserves-existing-agents-md`
   - `./bin/governance-check`
5. blocker taxonomy:
   - `execution_pending_or_failed`
   - `contract_drift`
6. failure handling / replay expectation:
   - reopen only if richer project-level AGENTS management behavior is needed beyond this first contract slice
