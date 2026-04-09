# Pre-Tests: verification-contract-and-premerge-adequacy-governance

## Acceptance Targets

### AT-001 issue-bound verification stays single-source

- acceptance target: `pre-tests.md` remains the only canonical verification truth for an owner issue
- testing layer: governance
- target environment: issue + IBM truth-source package
- required evidence: `issue package`
- blocker taxonomy: `definition_missing`

### AT-002 four required test sections always exist

- acceptance target: every `pre-tests.md` must explicitly contain `Unit`, `Integration`, `End-to-End`, and `Real-Environment`
- testing layer: governance
- target environment: IBM quality bar + issue materialization + skill truth
- required evidence: `pre-tests section contract`
- blocker taxonomy: `definition_missing`

### AT-003 section omission uses finite reviewable reasons

- acceptance target: when a section is not needed for the current change, the file still records a finite `not_applicable_reason` type plus a short explanation
- testing layer: governance
- target environment: `pre-tests.md` section skeleton
- required evidence: `not-applicable reason taxonomy`
- blocker taxonomy: `definition_missing`

### AT-004 handoff carries executable verification obligations

- acceptance target: manager / worker handoff carries enough machine-readable metadata to tell a worker which verification contract it must satisfy
- testing layer: governance
- target environment: manager continuity + worker prompt + runtime metadata parser
- required evidence: `prompt/runtime contract review`
- blocker taxonomy: `definition_missing`

### AT-005 adequacy gate diagnoses the missing layer

- acceptance target: the fallback gate can distinguish whether the failure is missing pre-tests, missing testcase derivation, missing execution, or missing completion/evidence state
- testing layer: focused regression
- target environment: `test-pre-merge-* -> develop` guarded merge design
- required evidence: `gate diagnostic contract`
- blocker taxonomy: `execution_pending_or_failed`

### AT-006 premerge and post-merge surfaces stay distinct

- acceptance target: premerge adequacy does not erase post-merge integration / real-environment / dogfood obligations
- testing layer: governance
- target environment: `pre-tests.md` schema + merge gate contract
- required evidence: `surface-boundary review`
- blocker taxonomy: `definition_missing`

## Pre-merge acceptance

1. `git diff --check`
   - expectation: new owner docs remain whitespace-clean
2. `./bin/governance-check`
   - expectation: candidate promotion, milestone writeback, and IBM package structure remain valid

## Post-merge acceptance

1. Freely can no longer hide verification failure behind a single vague message.
2. A future reviewer can see all four required test sections even when some are not applicable.
3. A future worker handoff can point to concrete required item ids / lanes / evidence level instead of only “please verify”.
4. A future guarded merge can tell whether the next fix is to write `pre-tests`, design cases from tasks, actually run the tests, or mark evidence/status.

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Issue-bound verification truth remains anchored in a single pre-tests file.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`

### AT-002
- id: `AT-002`
- requirement: `Pre-tests uses a mandatory four-section structure: Unit, Integration, End-to-End, and Real-Environment.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/prd.md`

### AT-003
- id: `AT-003`
- requirement: `Section omission is expressed through finite reason types rather than free-form skipping.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/brainstorms/b-verification-contract-and-premerge-adequacy-governance.md`

### AT-004
- id: `AT-004`
- requirement: `Worker handoff carries machine-readable verification obligations rather than scheduling metadata alone.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`

### AT-005
- id: `AT-005`
- requirement: `Fallback adequacy gate distinguishes pre-tests missing, testcase derivation missing, execution missing, and verification state missing.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/brainstorms/b-verification-contract-and-premerge-adequacy-governance.md`

### AT-006
- id: `AT-006`
- requirement: `Premerge adequacy keeps post-merge integration, real-environment, and dogfood as distinct surfaces.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/pre-brainstorms/20260408-1205--verification-contract-and-premerge-adequacy/brainstorms.md`
