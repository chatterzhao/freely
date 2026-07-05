# Pre-Tests: manager-task-source-scan-idle-replan-boundary-governance

## Unit
- acceptance target: `Do not invent a fake lower-level seam when the patrol defect only becomes truthful across scan state, prompt composition, and runtime trigger handling together.`
- testing layer: `unit`
- target environment: `feature/startup-task-source-patrol-and-reconcile-20260420`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The bounded defect spans scan-generation, prompt-consumption, and continuity gating together; a fake narrower seam would miss the actual idle/replan contract.`
- replacement_evidence: `The focused patrol regressions plus owner verification artifact are the smallest truthful executable boundary for this owner.`

## Integration
- acceptance target: `Manager patrol regenerates or suppresses task-source scan only on the bounded idle/replan boundary while preserving current continuity truth.`
- testing layer: `integration`
- target environment: `feature/startup-task-source-patrol-and-reconcile-20260420`
- required evidence: `focused patrol regression output plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-includes-milestone-patrol-seed`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-suppresses-broad-patrol-while-worker-active`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-task-source-scan-ignores-pre-stop-continuity-anchor`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-provider-hints`.
6. Run `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-python-compat`.
7. Run `bash docs/system/workspace/scripts/tests/test-start-lead-agent-verification-metadata-contract`.
8. Run `bash -n docs/system/workspace/scripts/runtime/freely`.
9. Run `git diff --check`.
10. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `The authoritative premerge batch carries the idle/replan patrol owner chain and keeps manager startup autonomy bounded through guarded develop promote.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-20260420-autonomous-task-governance`
- required evidence: `guarded premerge replay plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Use `test-pre-merge-20260420-autonomous-task-governance` as the authoritative guarded batch for this owner.
2. Replay the focused patrol regressions plus `./bin/governance-check` there.
3. Stage the owner verification artifact in the same guarded develop-bound merge.

## Real-Environment
- acceptance target: `A bounded self-host replay proves startup manager rounds can keep autonomous patrol seed truth without letting stale delegated continuation or active-worker churn hijack the lane.`
- testing layer: `real_environment`
- target environment: `local self-host runtime plus recorded runtime evidence`
- required evidence: `runtime event log, worker continuity evidence, and owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `Current self-host replay already proved the truthful live seam for this owner: startup manager rounds consumed machine-readable patrol seed, active-worker rounds suppressed broad patrol, and idle followthrough regenerated scan only when continuity advanced without an active worker.`

## Acceptance Items

### Milestone patrol seed appears on idle startup
- id: `scan-seed-idle-startup`
- requirement: `Runtime publishes a machine-readable patrol seed that includes milestone unresolved work when startup enters an idle manager round.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-task-source-scan-idle-replan-boundary-governance/code-reviews/20260420-manager-task-source-scan-idle-replan-boundary-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1,tasks.md#task-2`
- case_design: `Start from the bounded patrol feature lane, generate the scan JSON, and verify milestone queue signals appear in the manager patrol seed without broadening raw-source families.`
- testcase_derivation: `The owner changed patrol-seed generation and milestone standing-surface exposure, so the narrowest truthful derivation is the milestone-seed regression paired with the owner verification artifact.`

### Active worker suppresses broad patrol
- id: `scan-suppressed-while-worker-active`
- requirement: `Manager prompt suppresses broad patrol scan regeneration while a stable active worker is already running.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-task-source-scan-idle-replan-boundary-governance/code-reviews/20260420-manager-task-source-scan-idle-replan-boundary-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Replay a manager round with an active worker and verify the prompt keeps continuity-first behavior instead of rerunning broad patrol.`
- testcase_derivation: `The exact regression being closed is broad patrol stealing focus from an active worker lane, so the direct derivation is the active-worker suppression regression anchored to the same owner review artifact.`

### Continuity advance regenerates scan only when idle
- id: `scan-regenerates-after-idle-continuity-advance`
- requirement: `Manager regenerates task-source scan after continuity advances only when there is no active worker and the round has truly re-entered idle/replan state.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-task-source-scan-idle-replan-boundary-governance/code-reviews/20260420-manager-task-source-scan-idle-replan-boundary-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1,tasks.md#task-3`
- case_design: `Advance manager continuity past the previous scan anchor, keep active workers at zero, and verify runtime regenerates the patrol scan instead of reusing stale seed data.`
- testcase_derivation: `This item derives from the owner's idle/replan trigger contract, which specifically froze continuity advance plus zero active workers as the first bounded regeneration trigger.`

### Guarded premerge replay carries develop adequacy
- id: `scan-guarded-promote-adequacy`
- requirement: `The authoritative premerge batch carries a staged pass owner review artifact proving idle/replan patrol regeneration remains bounded on the guarded develop path.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-task-source-scan-idle-replan-boundary-governance/code-reviews/20260420-manager-task-source-scan-idle-replan-boundary-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-3,tasks.md#task-4`
- case_design: `Use test-pre-merge-20260420-autonomous-task-governance as the authoritative guarded batch, rerun the focused patrol regressions there, and stage this owner review artifact with the same merge so develop consumes a real owner chain.`
- testcase_derivation: `The develop gate exposed the missing seam directly: this owner needed a premerge-integration/develop_merge adequacy item backed by a fresh staged review artifact under the owner verification directory.`

### Self-host replay proves the live patrol seam
- id: `scan-selfhost-live-seam`
- requirement: `Recorded self-host runtime evidence shows startup manager rounds consumed patrol seed truth, active-worker rounds suppressed broad patrol, and idle replan regenerated scan only on bounded triggers.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/manager-task-source-scan-idle-replan-boundary-governance/code-reviews/20260420-manager-task-source-scan-idle-replan-boundary-verification.md`
- surface_kind: `real_environment`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-4`
- case_design: `Review the runtime event log and worker continuity evidence from the bounded self-host replay and confirm the manager patrol seam behaves as the focused regressions claim.`
- testcase_derivation: `This owner changes a live runtime patrol seam, so one real-environment acceptance item must point back to concrete self-host evidence instead of relying only on synthetic fixture regressions.`
