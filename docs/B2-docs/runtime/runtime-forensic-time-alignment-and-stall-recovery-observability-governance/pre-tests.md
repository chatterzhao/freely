# Pre-Tests: runtime-forensic-time-alignment-and-stall-recovery-observability-governance

## Unit

- acceptance target: `No isolated unit seam is narrower than the existing focused runtime regressions for this owner`
- testing layer: `unit`
- target environment: `feature/fix-manager-continuity-gap-20260412`
- required evidence: `focused runtime regression coverage at the shell integration boundary`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The repaired behavior lives in the runtime shell entrypoint and stop/recovery orchestration rather than a separately importable unit seam.`
- replacement_evidence: `The focused runtime regressions in Integration cover the exact repaired control-flow boundaries.`

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

## End-to-End

- acceptance target: `Guarded promote from the authoritative test-pre-merge batch into develop carries artifact-backed evidence for the bounded runtime observability owner`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `fresh test-pre-merge batch receipt plus staged owner verification artifacts`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `protected_environment_only`
- not_applicable_explanation: `This owner reaches end-to-end verification only through the guarded test-pre-merge to develop promotion path, not through a separate standalone app surface before merge.`
- replacement_evidence: `The authoritative premerge-integration lane and guarded promotion receipt provide the closest truthful end-to-end evidence before develop absorption.`

## Real-Environment

- acceptance target: `After develop absorption, canonical runtime status and stop/recovery flows surface the bounded forensic-alignment evidence without reopening display-time policy`
- testing layer: `real_environment`
- target environment: `develop`
- required evidence: `post-merge followthrough on canonical develop runtime surfaces`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `This guarded premerge fixture does not require an additional real-environment test before merge; canonical develop followthrough remains the post-merge acceptance surface for this owner.`
- not_applicable_reason: `post_merge_only`
- not_applicable_explanation: `Real-environment verification for this owner only becomes lawful after guarded promote into canonical develop.`
- replacement_evidence: `Feature-lane focused regressions plus premerge-integration evidence establish merge readiness.`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `stall recovery leaves a visible runtime event trail`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `bash docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery; ./bin/governance-check`
- case_design: `Merge the bounded fix into a fresh authoritative test-pre-merge batch, rerun the stall-recovery regression there, and require the staged verification artifact before guarded promote to develop succeeds.`

### AT-002
- id: `AT-002`
- requirement: `freely stop materializes the missing manager continuity required by the latest prompt`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `bash docs/system/workspace/scripts/tests/test-freely-stop-materializes-missing-manager-continuity; bash docs/system/workspace/scripts/tests/test-freely-live-status-manager-continuity-gap-surface`
- case_design: `Use the same authoritative test-pre-merge batch to prove both the stop-time fallback artifact and the surfaced continuity-gap truth, then carry that staged artifact into guarded develop promotion.`

### AT-003
- id: `AT-003`
- requirement: `the owner keeps display-time governance and forensic-alignment governance separate`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-implementation-decision.md`

### AT-004
- id: `AT-004`
- requirement: `closeout writeback records merge 480d839a and moves the owner to completed lifecycle truth without reopening implementation scope`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/code-reviews/20260412-runtime-forensic-time-alignment-closeout-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `./bin/governance-check; git diff --check`
- case_design: `Stage a fresh owner closeout verification artifact alongside the lifecycle writeback, then require guarded premerge integration to see the owner as completed before develop promote can proceed.`
