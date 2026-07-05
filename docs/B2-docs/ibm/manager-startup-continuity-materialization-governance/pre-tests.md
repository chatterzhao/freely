# Pre-Tests: manager-startup-continuity-materialization-governance

## Unit
- acceptance target: `Runtime seeds a launch-bound startup continuity stub at the expected path when normal startup has not yet materialized manager continuity.`
- testing layer: `unit`
- target environment: `feature/manager-startup-continuity-materialization-governance-20260413`
- required evidence: `focused runtime startup-stub regression`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-startup-continuity-stub-materialization`.

## Integration
- acceptance target: `Status surfaces the bounded manager handoff states without redefining stop fallback or continuity-gap behavior.`
- testing layer: `integration`
- target environment: `feature/manager-startup-continuity-materialization-governance-20260413`
- required evidence: `focused runtime status regressions plus governance output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-manager-handoff-state-surface`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-stop-materializes-missing-manager-continuity`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-manager-continuity-gap-surface`.
4. Run `bash -n docs/system/workspace/scripts/runtime/freely`.
5. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `A bounded local runtime replay proves the startup path now creates the first handoff artifact before AI launch and that stop cleanup still leaves repair-only evidence distinct from startup seeding.`
- testing layer: `end_to_end`
- target environment: `local feature worktree runtime boundary`
- required evidence: `verification artifact records one foreground or daemon replay and one clean stop`
- blocker taxonomy: `execution_pending_or_failed`
1. Run a bounded local startup replay from this feature worktree.
2. Inspect `freely live-status --project <worktree>` while the runtime is up.
3. Stop the runtime and confirm no lingering freely runtime processes remain for the worktree.

## Real-Environment
- acceptance target: `The bounded self-host runtime in this feature worktree exhibits the same startup-handoff semantics that the focused tests assert.`
- testing layer: `real_environment`
- target environment: `local self-host runtime`
- required evidence: `verification artifact with exact commands and observed handoff-state outputs`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `This owner changes an executable runtime startup seam, and the bounded foreground plus daemon live replays were completed in the feature worktree without leaving residual freely runtime processes behind.`
- not_applicable_reason: `not_applicable`
- not_applicable_explanation: `none`
- replacement_evidence: `Focused regressions plus bounded local self-host replays cover the executable seam for this owner.`

## Acceptance Items

### Normal startup seeds the first handoff artifact
- id: `startup-seeds-first-handoff-artifact`
- requirement: `When the prompt-required continuity file is absent, runtime writes a startup stub on the normal path before AI launch.`
- surface_kind: `unit`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1,tasks.md#task-2`
- case_design: `Simulate a fresh startup path, inspect the expected continuity path, and verify the stub exists with startup writer metadata before any stop fallback runs.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews/20260413-manager-startup-continuity-materialization-verification.md`

### Handoff state is machine-readable
- id: `handoff-state-surfaced`
- requirement: `Runtime status exposes the manager handoff state and writer metadata distinctly from existing continuity-gap fields.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Seed a startup stub and inspect live-status and fleet-status for the bounded handoff state surface.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews/20260413-manager-startup-continuity-materialization-verification.md`

### Stop fallback stays repair-only
- id: `repair-fallback-stays-distinct`
- requirement: `Stop-time continuity repair remains distinguishable from normal startup seeding.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-3`
- case_design: `Run the existing stop fallback regression and verify the writer classification still reports repair fallback rather than seeded startup continuity.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews/20260413-manager-startup-continuity-materialization-verification.md`

### Guarded promote proves bounded adequacy
- id: `develop-promote-manager-handoff-proof`
- requirement: `A guarded test-pre-merge replay proves this owner carries explicit premerge adequacy before develop promotion.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-4,tasks.md#task-5`
- case_design: `Merge the feature lane into a disposable test-pre-merge batch, rerun the focused startup continuity and status regressions there, and record the replay in a closeout verification artifact for the develop gate.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews/20260413-manager-startup-continuity-materialization-closeout-verification.md`

### Real worker-lane replay stops cleanly
- id: `real-worker-lane-replay-clean-stop`
- requirement: `Bounded foreground and daemon replays on the feature worktree start and stop cleanly without leaving same-worktree freely runtime processes behind.`
- surface_kind: `real_environment`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-4,tasks.md#task-5`
- case_design: `Run one bounded foreground replay and one bounded daemon replay from the feature worktree, confirm the worker lane stays on worker semantics, and verify stop leaves the worktree at desired_runtime_state stopped with no residual same-worktree freely runtime process.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-startup-continuity-materialization-governance/code-reviews/20260413-manager-startup-continuity-materialization-verification.md`
