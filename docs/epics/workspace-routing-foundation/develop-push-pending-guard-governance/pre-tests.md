# Pre-Tests: develop-push-pending-guard-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `develop push followthrough truth`
- testing layer: `focused regression + governance checks`
- target environment: `feature worktree`
- required evidence: status-family regressions plus governance checks
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. Protected-branch push debt is modeled explicitly; it is not hidden behind “merge already happened locally”.
2. `develop` ahead of remote without a valid defer reason is surfaced as `push_pending`.
3. A valid defer reason downgrades the state to `push_deferred`, not silent success.
4. `live-status`, `fleet-status`, and `wt-fleet-status` all expose the new push state.
5. Manager patrol can consume the signal as standing-source followthrough drift without misclassifying explicit post-merge acceptance windows.
6. Existing push hooks still block illegal push patterns and do not auto-push.

### Post-merge canonical truth acceptance

- acceptance target: `develop carries push_pending and push_deferred truth`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: progress closeout, verification artifact, and live status on develop
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. This owner must close once canonical `develop` exposes push followthrough state and patrol truth.
2. `post_merge_acceptance` must remain a structured defer window rather than a hidden local-only state.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `live-status surfaces push_pending and push_deferred truth for develop`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`

### PT-2
- id: `PT-2`
- requirement: `fleet-status surfaces develop push followthrough drift`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-fleet-status-develop-push-pending`

### PT-3
- id: `PT-3`
- requirement: `wt-fleet-status surfaces develop push followthrough drift`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-wt-fleet-status-develop-push-pending`

### PT-4
- id: `PT-4`
- requirement: `governance gates remain green while push-followthrough truth is observational rather than global blocking`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/develop-push-pending-guard-governance/code-reviews/20260401-develop-push-pending-guard-verification.md`

1. `bash docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
2. `bash docs/system/workspace/scripts/tests/test-freely-fleet-status-develop-push-pending`
3. `bash docs/system/workspace/scripts/tests/test-wt-fleet-status-develop-push-pending`
4. `bash docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
5. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
