# Pre-Tests: cc-acp-init-autonomy-consent-test-followthrough-governance

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `the owner is explicitly recorded as a completed-family followthrough of the tool autonomy policy materialization family`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/cc-acp-init-autonomy-consent-test-followthrough-governance/issues/cc-acp-init-autonomy-consent-test-followthrough-governance.md`

### PT-2
- id: `PT-2`
- requirement: `the cc:auto plus ACP init regression test passes only after carrying the canonical activation-consent flag`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-init-cc-config`

### PT-3
- id: `PT-3`
- requirement: `governance truth remains internally consistent after adding the narrow followthrough owner`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `./bin/governance-check`

## Pre-merge Focused Regression / Smoke

1. acceptance target:
   - the stale `cc:auto + adapter=acp` fixture is aligned with the canonical activation-consent contract
2. testing layer:
   - shell regression
3. target environment:
   - feature worktree
4. required evidence:
   - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
   - `./bin/governance-check`
5. blocker taxonomy:
   - `definition_missing`
   - `commands_only`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - keep the owner narrow and repair only the stale fixture or its lifecycle evidence

## Post-merge Integration Acceptance

1. acceptance target:
   - canonical `develop` absorbs the one-line test repair without reopening runtime semantics
2. testing layer:
   - contract replay against `develop`
3. target environment:
   - `develop`
4. required evidence:
   - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
5. blocker taxonomy:
   - `execution_pending_or_failed`
   - `evidence_plan_missing`
6. failure handling / replay expectation:
   - if additional stale fixtures appear, reopen as a new narrow owner instead of expanding this one

