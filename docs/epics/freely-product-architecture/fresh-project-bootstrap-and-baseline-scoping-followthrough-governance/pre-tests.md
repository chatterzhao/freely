# Pre-Tests: fresh-project-bootstrap-and-baseline-scoping-followthrough-governance

## Acceptance Targets

### AT-001 sync-tooling retargets fresh-project config truth

- acceptance target: `sync-tooling` rewrites target `.freely/config.env` so project/intent/constitution point at the target project rather than the source repo
- testing layer: integration
- target environment: fresh git project bootstrap path
- required evidence: `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 sync-tooling rematerializes hook assets for follow-on init

- acceptance target: a fresh project that just ran `sync-tooling` no longer needs manual `.githooks` copying before `freely init`
- testing layer: integration
- target environment: fresh git project bootstrap path
- required evidence: `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 baseline and status baseline stay pinned to the target project

- acceptance target: `baseline-status` and `status --view baseline` both report the requested target project after sync/init instead of drifting to the source project
- testing layer: integration
- target environment: fresh git project bootstrap path
- required evidence:
  - `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`
  - `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-status-family`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `sync-tooling retargets fresh-project config truth to the target project.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance/code-reviews/20260406-fresh-project-bootstrap-and-baseline-scoping-followthrough-verification.md`

### AT-002
- id: `AT-002`
- requirement: `sync-tooling rematerializes hook assets so follow-on init does not require manual .githooks copying.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance/code-reviews/20260406-fresh-project-bootstrap-and-baseline-scoping-followthrough-verification.md`

### AT-003
- id: `AT-003`
- requirement: `baseline-status and status baseline stay pinned to the target project after sync/init.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance/code-reviews/20260406-fresh-project-bootstrap-and-baseline-scoping-followthrough-verification.md`
