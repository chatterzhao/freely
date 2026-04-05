# Pre-Tests: agents-cli-output-style-experiment-governance

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `the change is recorded as an AGENTS-only experiment rather than a Freely capability materialization`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/agents-cli-output-style-experiment-governance/issues/agents-cli-output-style-experiment-governance.md`

### PT-2
- id: `PT-2`
- requirement: `AGENTS.md freezes concise plain Chinese as the current default and explicitly rejects classical Chinese as the default style`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `AGENTS.md`

### PT-3
- id: `PT-3`
- requirement: `AGENTS.md states that project-level AGENTS.md is the first governance surface, and this remains aligned with the current runtime/init contract`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/runtime/freely`

### PT-4
- id: `PT-4`
- requirement: `candidate, milestone, issue, progress, and verification artifacts form a lawful develop-bound chain`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `./bin/governance-check`

## Pre-merge Focused Regression / Smoke

1. acceptance target:
   - the output-style experiment plus project-AGENTS entry contract are recorded as developer-entrypoint governance rather than unowned candidate-only drift
2. testing layer:
   - governance/document verification
3. target environment:
   - feature worktree
4. required evidence:
   - `./bin/governance-check`
5. blocker taxonomy:
   - `definition_missing`
   - `commands_only`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - repair the lifecycle writeback or AGENTS experiment wording without widening into capability materialization

## Post-merge Integration Acceptance

1. acceptance target:
   - canonical `develop` still presents the change as an `AGENTS.md` experiment and keeps governance consistency
2. testing layer:
   - contract replay against `develop`
3. target environment:
   - `develop`
4. required evidence:
   - `./bin/governance-check`
5. blocker taxonomy:
   - `execution_pending_or_failed`
   - `evidence_plan_missing`
6. failure handling / replay expectation:
   - if canonical `develop` requires a stronger product or capability contract, reopen as a new narrow follow-on instead of silently widening this owner
