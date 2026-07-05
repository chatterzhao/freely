# Pre-Tests: test-pre-merge-family-promotion-gate-enforcement-governance

## Acceptance Targets

### AT-001 truth sources and gates change together

- acceptance target: the owner updates constitutional truth and directly coupled gate semantics in the same lifecycle
- testing layer: governance
- target environment: issue + `CONSTITUTION` + `LAWS` + references + gate package
- required evidence: `doc and gate package`
- blocker taxonomy: `definition_missing`

### AT-002 develop source-branch semantics are enforced

- acceptance target: `develop` accepts `test-pre-merge-*` family and `hotfix/*`, and blocks `feature/*` as the normal path
- testing layer: focused regression
- target environment: `pr-merge-guarded` plus related hook/gate tests
- required evidence: `source-branch regression`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 lifecycle automation stays out of scope

- acceptance target: the owner does not widen into stale automation, manifest generation, or batch-create UX
- testing layer: governance
- target environment: issue + tasks + milestone writeback
- required evidence: `owner scope remains narrow`
- blocker taxonomy: `lifecycle_incomplete`

## Pre-merge acceptance

1. `./bin/governance-check`
   - expectation: new candidate, milestone, and owner writeback remain structurally valid
2. `git diff --check`
   - expectation: new IBM package and writeback stay whitespace-clean

## Post-merge acceptance

1. Follow-on execution can update truth sources and gates in one owner without reopening the promote-model debate.
2. Later lifecycle automation work no longer needs to redefine who may promote into `develop`.

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Truth-source update and directly coupled gate enforcement are owned by the same lifecycle.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/test-pre-merge-family-promotion-gate-enforcement-governance/issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`

### AT-002
- id: `AT-002`
- requirement: `The owner targets develop source-branch enforcement around test-pre-merge family promotion semantics.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-pr-merge-guarded`

### AT-003
- id: `AT-003`
- requirement: `Lifecycle automation remains a later owner.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/test-pre-merge-family-promotion-gate-enforcement-governance/code-reviews/20260405-test-pre-merge-family-promotion-gate-enforcement-verification.md`
