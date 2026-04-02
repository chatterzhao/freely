# Pre-Tests: runtime-loop-log-timezone-label-followthrough-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `loop log timezone label followthrough`
- testing layer: `focused regression`
- target environment: `feature worktree`
- required evidence: `loop.log` header includes a timezone label under a deterministic host timezone
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. `freely start` writes a `loop.log` header with a timezone label.
2. The regression observes `loop.log` directly rather than unrelated cycle logs.
3. Existing cooldown fallback behavior remains unchanged.

### Post-merge canonical truth acceptance

- acceptance target: `develop carries the loop log timezone-label followthrough`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: focused regression, verification artifact, and merge provenance
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. Canonical `develop` keeps the loop log header aligned with the host-local time-display policy.
2. The owner closes without reopening stored truth or naming truth scope.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `loop log header includes a timezone label in deterministic host-local time`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-rate-limit-cooldown-falls-back-to-active-slot`

### PT-2
- id: `PT-2`
- requirement: `governance lifecycle for the followthrough is valid for develop-bound replay`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-loop-log-timezone-label-followthrough-governance/code-reviews/20260402-runtime-loop-log-timezone-label-followthrough-verification.md`
