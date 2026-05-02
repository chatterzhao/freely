# Pre-Tests: manager-startup-continuity-contract-governance

## Unit
- acceptance target: `The contract freeze makes the startup-handoff boundary explicit enough that a future implementation owner has one bounded seam to follow.`
- testing layer: `unit`
- target environment: `feature/manager-startup-continuity-contract-governance-20260413`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner freezes contract and routing only; it does not add an executable runtime change in the current lane.`
- replacement_evidence: `The owner issue, contract brainstorm, decision note, and verification review together are the smallest useful unit for this documentation-only contract freeze.`

## Integration
- acceptance target: `Canonical docs freeze the normal-path continuity contract without claiming implementation has already landed.`
- testing layer: `integration`
- target environment: `feature/manager-startup-continuity-contract-governance-20260413`
- required evidence: `governance/test command output plus owner review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-pretests-gate`.
2. Run `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`.
3. Run `./bin/governance-check`.
4. Run `git diff --check`.

## End-to-End
- acceptance target: `A guarded feature -> test-pre-merge -> develop chain accepts the owner as bounded contract truth instead of candidate-only follow-on research.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-20260413-manager-startup-continuity-contract`
- required evidence: `guarded merge replay trace plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Replay the bounded `feature/manager-startup-continuity-contract-governance-20260413 -> test-pre-merge-20260413-manager-startup-continuity-contract -> develop` chain after the owner is materialized.

## Real-Environment
- acceptance target: `Canonical develop still exposes real startup-handoff evidence that justifies freezing this owner before implementation.`
- testing layer: `real_environment`
- target environment: `develop`
- required evidence: `artifact-backed canonical runtime evidence plus current live-status readability`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `The owner is documentation-only, but the bounded contract freeze is justified by real canonical startup evidence already reproduced on develop and by current live-status inspection remaining readable on the canonical project.`
- not_applicable_reason: `post_merge_only`
- not_applicable_explanation: `No new runtime behavior is being validated before merge; the real-environment obligation here is to keep the canonical evidence trail visible and tied to this owner.`
- replacement_evidence: `The source brainstorm and verification artifact anchor the real self-host startup evidence that motivates this contract freeze.`

## Acceptance Items

### Startup layers are distinct
- id: `startup-layers-distinct`
- requirement: `Canonical docs distinguish launch bootstrapping from manager handoff materialization.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/code-reviews/20260413-manager-startup-continuity-contract-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1,tasks.md#task-2`
- case_design: `Review the owner issue, brainstorm, and PRD together and confirm they freeze two startup layers instead of folding manager handoff back into generic startup readiness.`

### Normal-path handoff artifact is required
- id: `normal-path-handoff-required`
- requirement: `Canonical docs freeze that the first handoff artifact must appear on the normal startup path and that stop fallback remains repair-only.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/code-reviews/20260413-manager-startup-continuity-contract-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Audit the owner docs and confirm they require normal-path continuity materialization while explicitly rejecting stop fallback as normal success.`

### Implementation seam stays bounded
- id: `bounded-stub-state-seam`
- requirement: `Canonical docs choose the runtime-seeded continuity stub plus machine-readable handoff state seam without widening this owner into implementation.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/code-reviews/20260413-manager-startup-continuity-contract-decision.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Review the decision note and verify the chosen seam is runtime-seeded continuity claim/stub plus handoff state, while runtime code changes remain explicitly deferred to a later owner.`

### Canonical evidence justifies the freeze
- id: `canonical-handoff-gap-evidence-visible`
- requirement: `Canonical develop still carries real startup-handoff evidence strong enough to justify freezing the manager continuity contract before implementation.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-startup-continuity-contract-governance/code-reviews/20260413-manager-startup-continuity-contract-verification.md`
- surface_kind: `real_environment`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-1,tasks.md#task-2,tasks.md#task-4`
- case_design: `In the disposable test-pre-merge batch, review the canonical develop startup evidence from the root-cause packet together with a current live-status inspection and confirm the missing first-handoff contract is still a real product/runtime problem rather than candidate-only theory.`
