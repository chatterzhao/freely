# Pre-Tests: tasks-closeout-completion-and-adequacy-gate-governance

## Unit
- acceptance target: `No separate unit harness is required; the smallest executable boundary is the shell gate behavior itself.`
- testing layer: `unit`
- target environment: `feature/tasks-closeout-gate-20260413`
- required evidence: `focused shell gate regression output`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The bounded change lives inside shell gate flow, so focused gate regressions are the smallest useful executable boundary.`
- replacement_evidence: `Focused shell regressions and syntax validation cover this owner's executable surface.`

## Integration
- acceptance target: `Owner completion and guarded adequacy both consume bound tasks closeout truth from the same pretests-gate owner line.`
- testing layer: `integration`
- target environment: `feature/tasks-closeout-gate-20260413`
- required evidence: `command output plus owner review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash -n docs/system/workspace/scripts/quality/pretests-gate`.
2. Run `bash docs/system/workspace/scripts/tests/test-pretests-gate`.
3. Run `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`.
4. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `Guarded merge delegation still respects the new tasks closeout blocker without creating a second parser in governance-merge-gate.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge owner replay via delegated pretests-gate`
- required evidence: `delegated merge-gate regression output plus owner review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Stage owner `tasks.md` in the delegated merge-gate fixture and verify the inherited path stays green.

## Real-Environment
- acceptance target: `This owner hardens local governance closure and does not introduce a separate hosted environment before canonical develop promote.`
- testing layer: `real_environment`
- target environment: `local governance gate boundary`
- required evidence: `lawful replacement evidence recorded in owner review artifact`
- blocker taxonomy: `definition_missing`
- real_environment_status: `pass`
- real_environment_reason: `This owner changes a local governance gate boundary, and the executable surface is already exercised directly by the focused pretests-gate and delegated governance-merge-gate regressions. Canonical develop promotion remains the post-merge acceptance surface rather than a missing pre-merge environment.`
- not_applicable_reason: `post_merge_only`
- not_applicable_explanation: `No separate hosted environment exists before guarded develop promote; the real-environment boundary for this owner is the canonical protected-branch replay itself.`
- replacement_evidence: `Focused shell regressions and governance-check are sufficient for this narrow owner.`

## Acceptance Items

### Completed owners require tasks closeout
- id: `completed-owners-require-tasks-closeout`
- requirement: `pretests-gate rejects phase_state=completed owners when bound tasks.md is missing or still contains unchecked task boxes.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/code-reviews/20260413-tasks-closeout-completion-and-adequacy-gate-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1,tasks.md#task-2,tasks.md#task-3`
- case_design: `Run the focused pretests-gate regression where a completed owner retains unchecked tasks and confirm the gate fails on task closeout rather than passing on pre-tests evidence alone.`

### Guarded adequacy requires tasks closeout
- id: `guarded-adequacy-requires-tasks-closeout`
- requirement: `pretests-gate --require-adequacy applies the same tasks.md closeout blocker before returning an owner-bound pass verdict.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/code-reviews/20260413-tasks-closeout-completion-and-adequacy-gate-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-2,tasks.md#task-3,tasks.md#task-4`
- case_design: `Run the focused pretests-gate adequacy regression and confirm unchecked tasks block guarded promote even when the owner otherwise has adequacy metadata.`

### Delegated merge gate stays aligned
- id: `delegated-merge-gate-stays-aligned`
- requirement: `governance-merge-gate inherits the owner tasks closeout contract through pretests-gate delegation without adding a second parser.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/code-reviews/20260413-tasks-closeout-completion-and-adequacy-gate-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-3,tasks.md#task-4`
- case_design: `Run delegated merge-gate regression coverage with a staged owner tasks.md fixture and confirm the inherited path remains green without merge-gate-local tasks parsing.`
