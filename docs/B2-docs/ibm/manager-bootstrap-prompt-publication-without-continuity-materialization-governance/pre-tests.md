# Pre-Tests: manager-bootstrap-prompt-publication-without-continuity-materialization-governance

## Acceptance Targets

### AT-001 bootstrap survives first AI-launch window

- acceptance target: `freely start` no longer restarts the fresh manager during the `supervisor.pid`-before-`ai.pid` bootstrap window
- testing layer: integration
- target environment: canonical runtime scripts plus verification artifact
- required evidence: `verification note + focused runtime checks`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 worker-dispatch continuity is launchable

- acceptance target: manager continuity files that publish delegated prompts under `## Worker Dispatch` surface launchable worker prompt truth instead of `none`
- testing layer: integration
- target environment: runtime parser helpers plus canonical status surface
- required evidence: `verification note`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 closeout truth stays bounded

- acceptance target: completed lifecycle truth records the absorbed runtime fix without widening this owner into unrelated restart-churn followthrough
- testing layer: IBM review
- target environment: issue/progress/milestone artifacts
- required evidence: `issue + progress + milestone + implementation decision note`
- blocker taxonomy: `definition_missing`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `The bounded bootstrap grace fix is verified against the first AI-launch window.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/code-reviews/20260404-manager-bootstrap-prompt-publication-without-continuity-materialization-verification.md`

### AT-002
- id: `AT-002`
- requirement: `Worker prompts under the current ## Worker Dispatch continuity heading are visible as launchable manager handoff evidence.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/code-reviews/20260404-manager-bootstrap-prompt-publication-without-continuity-materialization-verification.md`

### AT-003
- id: `AT-003`
- requirement: `The closeout lane keeps this owner completed and bounded while leaving restart churn to a future owner.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/code-reviews/20260404-manager-bootstrap-prompt-publication-without-continuity-materialization-implementation-decision.md`
