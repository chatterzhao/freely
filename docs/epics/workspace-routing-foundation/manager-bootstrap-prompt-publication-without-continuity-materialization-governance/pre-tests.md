# Pre-Tests: manager-bootstrap-prompt-publication-without-continuity-materialization-governance

## Acceptance Targets

### AT-001 bootstrap no longer self-restarts during first AI launch window

- acceptance target: `freely start` keeps the fresh manager supervisor alive while `LAST_EXIT_REASON=starting` and `ai.pid` has not appeared yet
- testing layer: focused runtime regression
- target environment: `docs/system/workspace/scripts/runtime/freely`
- required evidence: `test-freely-manager bootstrap replay + live-status verification`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 current continuity format surfaces worker dispatch prompt truth

- acceptance target: manager continuity that records delegated prompts under `## Worker Dispatch` is parsed as launchable worker evidence instead of `none`
- testing layer: focused parser regression
- target environment: `docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- required evidence: `focused parser fixtures + live-status replay`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 completed lifecycle keeps canonical evidence aligned

- acceptance target: milestone, issue, progress, and review artifacts all point to the absorbed `develop` result without reopening implementation scope
- testing layer: governance
- target environment: issue artifacts + repo checks
- required evidence: `governance-check + closeout docs`
- blocker taxonomy: `lifecycle_incomplete`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Bootstrap survives the first AI-launch window without a false watchdog restart.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/code-reviews/20260404-manager-bootstrap-prompt-publication-without-continuity-materialization-verification.md`

### AT-002
- id: `AT-002`
- requirement: `Current-format Worker Dispatch continuity surfaces generated worker prompts through runtime parser helpers and live-status.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`

### AT-003
- id: `AT-003`
- requirement: `Completed lifecycle truth is canonical and auditable on current develop.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/progress/workspace-routing-foundation/p-manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
