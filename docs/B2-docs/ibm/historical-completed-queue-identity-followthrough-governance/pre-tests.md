# Pre-Tests: historical-completed-queue-identity-followthrough-governance

## Unit
- acceptance target: `This owner is a docs-only milestone identity writeback; no standalone executable unit boundary exists beyond deterministic governance parsing.`
- testing layer: `unit`
- target environment: `feature/watchdog-completed-identity-followthrough-20260412`
- required evidence: `lawful replacement evidence recorded in owner verification artifact`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The bounded repair only normalizes one historical milestone identity entry and does not introduce a separate executable unit harness.`
- replacement_evidence: `Focused governance-check plus guarded replay evidence are sufficient for this docs-only owner.`

## Integration
- acceptance target: `Milestone completed-queue truth now uses canonical issue identity while preserving the existing watchdog evidence chain.`
- testing layer: `integration`
- target environment: `feature/watchdog-completed-identity-followthrough-20260412`
- required evidence: `governance-check pass plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `A guarded feature -> test-pre-merge -> develop replay no longer emits the historical watchdog legacy-identity warning.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge completed-identity replay`
- required evidence: `guarded replay trace plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Replay one disposable `test-pre-merge-* -> develop` chain for this followthrough owner and confirm the old warning is gone.

## Real-Environment
- acceptance target: `This owner repairs repository governance truth only; no hosted or external real-environment surface is introduced.`
- testing layer: `real_environment`
- target environment: `local governance boundary`
- required evidence: `lawful replacement evidence recorded in owner verification artifact`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The bounded surface is canonical repo governance truth rather than a hosted runtime or external integration.`
- replacement_evidence: `Focused governance-check and guarded replay evidence are sufficient for this docs-only followthrough.`

## Acceptance Items

### Historical completed queue entry is canonicalized
- id: `historical-completed-queue-canonicalized`
- requirement: `The completed watchdog milestone entry uses canonical issue identity I-20260324-0405 and still points at the same existing owner evidence.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/progress/workspace-routing-foundation/p-historical-completed-queue-identity-followthrough-governance.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1,tasks.md#task-2`
- case_design: `Update the single historical completed-queue entry from the stale candidate identity to the canonical issue identity, then verify governance-check still resolves the original watchdog owner evidence chain.`

### Guarded develop replay clears the warning
- id: `guarded-develop-replay-clears-legacy-identity-warning`
- requirement: `Guarded develop replay no longer emits the historical watchdog legacy candidate identity warning after this owner lands.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/historical-completed-queue-identity-followthrough-governance/code-reviews/20260412-historical-completed-queue-identity-followthrough-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Replay a disposable guarded promote carrying only this narrow followthrough owner and confirm the earlier completed watchdog legacy-identity warning is absent from the develop-bound gate output.`
