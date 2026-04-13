# Pre-Tests: runtime-forensic-time-alignment-and-stall-recovery-observability-governance

## Integration

- acceptance target: `prove runtime stall recovery and missing manager continuity fallback now leave canonical observable evidence`
- testing layer: `integration`
- target environment: `feature/fix-manager-continuity-gap-20260412`
- required evidence: `focused regression output plus issue-bound verification artifacts`
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-stop-materializes-missing-manager-continuity`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-manager-continuity-gap-surface`.
4. Run `./bin/governance-check`.
5. Run `git diff --check`.

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `stall recovery leaves a visible runtime event trail`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-verification.md`

### AT-002
- id: `AT-002`
- requirement: `freely stop materializes the missing manager continuity required by the latest prompt`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-verification.md`

### AT-003
- id: `AT-003`
- requirement: `the owner keeps display-time governance and forensic-alignment governance separate`
- evidence_level: `review`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-implementation-decision.md`
