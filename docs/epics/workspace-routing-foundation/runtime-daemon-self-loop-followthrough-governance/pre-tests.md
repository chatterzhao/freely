# Pre-Tests: runtime-daemon-self-loop-followthrough-governance

## Unit
- acceptance target: `Do not invent a fake unit seam for a runtime-control followthrough whose truth boundary is process lifecycle plus guarded promotion.`
- testing layer: `unit`
- target environment: `feature/runtime-daemon-self-loop-blocker-20260421`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The smallest truthful seam here is process-lifecycle integration, not an isolated pure unit.`
- replacement_evidence: `Focused runtime integration regressions plus guarded develop replay cover the bounded executable surface.`

## Integration
- acceptance target: `Repair repeated-start truth and daemon unexpected-signal handling without regressing explicit stop semantics.`
- testing layer: `integration`
- target environment: `feature/runtime-daemon-self-loop-blocker-20260421`
- required evidence: `focused runtime command output plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`.
6. Run `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`.
7. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `Protected promotion must carry this owner chain and the final daemon acceptance must prove Freely can keep working instead of stopping after one patrol round.`
- testing layer: `end_to_end`
- target environment: `guarded feature -> test-pre-merge -> develop replay`
- required evidence: `merge receipts plus develop-side runtime observation`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/runtime-daemon-self-loop-blocker-20260421` into `test-pre-merge-20260421-runtime-self-loop-blocker` via `./bin/merge-guarded`.
2. Merge `test-pre-merge-20260421-runtime-self-loop-blocker` into `develop` via `./bin/merge-guarded`.
3. On canonical `develop`, run `./bin/freely daemon start`.
4. Observe that Freely selects at least one task, completes it to the current-project success standard, closes the temporary worktree, and proceeds to another task instead of falling into `operator_stop`.

## Real-Environment
- acceptance target: `This bounded followthrough does not need a separate hosted environment before guarded replay; the executable runtime boundary is exercised directly on the local machine.`
- testing layer: `real_environment`
- target environment: `local runtime boundary`
- required evidence: `local daemon lifecycle replay plus verification artifact`
- blocker taxonomy: `definition_missing`
- real_environment_status: `pass`
- real_environment_reason: `The bounded executable seam repaired in this owner is the local daemon lifecycle boundary. Unexpected TERM handling, explicit stop preservation, and repeated-start residue truth were exercised directly in scripted local runtime replays before guarded promotion. Canonical develop self-host acceptance remains a separate end-to-end completion requirement for this owner and is recorded above instead of being faked as a pre-merge hosted-environment verdict.`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `There is no distinct hosted environment that meaningfully exercises this blocker before protected replay; the real executable surface is the local daemon lifecycle.`
- replacement_evidence: `Focused local daemon lifecycle replays plus the guarded develop replay provide the truthful acceptance surface for this bounded owner.`
1. Keep `freely` running on canonical `develop` until it completes at least one task and begins the next one.
2. Verify the completed task met the current-project success standard, including temporary worktree closeout.
3. Retire `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-daemon-self-loop-blocker`.
4. Delete branch `feature/runtime-daemon-self-loop-blocker-20260421`.
5. Delete branch `test-pre-merge-20260421-runtime-self-loop-blocker`.
6. Run `git worktree list` and confirm the temporary blocker worktree is gone.

## Acceptance Items

### Orphaned control-plane residue does not block lawful restart
- id: `orphaned-control-plane-precheck-clear`
- requirement: `User-facing start refusal requires an authoritative supervisor or explicit in-flight start lock, not lone dispatcher/watchdog residue.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#1,tasks.md#2`
- case_design: `Materialize stale dispatcher/watchdog pid files without a valid supervisor and verify precheck still clears.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`

### Unexpected daemon TERM does not fake operator stop
- id: `daemon-unexpected-term-ignored`
- requirement: `Daemon supervisor ignores unexpected external TERM without stop intent, but still honors explicit daemon stop.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#2,tasks.md#3`
- case_design: `Launch daemon mode, send TERM directly without writing stop.marker, confirm runtime survives and logs daemon_signal_ignored, then run explicit daemon stop and confirm operator stop still records correctly.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`

### Canonical develop proves autonomous continuation
- id: `develop-self-host-daemon-continuation`
- requirement: `Canonical develop proves Freely can autonomously pick a task, finish it to the current-project success standard, close the temporary worktree, and proceed to another task.`
- surface_kind: `real_environment`
- target_lane: `develop-self-host`
- promotion_gate: `completion`
- task_refs: `tasks.md#4,tasks.md#5`
- case_design: `Start Freely on canonical develop, observe one full task completion with lawful closeout, then confirm the daemon remains autonomous and moves on to a next task.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`
