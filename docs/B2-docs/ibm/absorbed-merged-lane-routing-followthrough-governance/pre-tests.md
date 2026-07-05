# Pre-Tests: absorbed-merged-lane-routing-followthrough-governance

## Unit
- acceptance target: `Do not invent a fake unit seam for a routing followthrough whose truthful boundary is CLI-visible scan/fleet behavior.`
- testing layer: `unit`
- target environment: `feature/absorbed-merged-scan-routing-fix-20260421`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The real seam is the runtime-facing CLI output and scan JSON, not an isolated pure unit.`
- replacement_evidence: `Focused CLI regressions plus guarded develop replay cover the actual executable boundary.`

## Integration
- acceptance target: `Absorbed merged lanes remain discoverable for cleanup but stop advertising themselves as edit-ready worker execution targets.`
- testing layer: `integration`
- target environment: `feature/absorbed-merged-scan-routing-fix-20260421`
- required evidence: `focused runtime command output plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`.
2. Run `bash docs/system/workspace/scripts/tests/test-wt-fleet-status-absorbed-merged-worker-role`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-routes-absorbed-merged-progress-to-cleanup`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-cleanup-governance-retirement-worker-directive`.
6. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `Guarded replay must carry the owner chain into develop before the final self-host daemon acceptance is trusted.`
- testing layer: `end_to_end`
- target environment: `guarded feature -> test-pre-merge -> develop replay`
- required evidence: `merge receipts plus develop-side runtime observation`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/absorbed-merged-scan-routing-fix-20260421` into `test-pre-merge-20260421-absorbed-merged-scan-routing-fix` via `freely pr-merge-guarded`.
2. Merge `test-pre-merge-20260421-absorbed-merged-scan-routing-fix` into `develop` via `freely pr-merge-guarded`.
3. On canonical `develop`, run `freely daemon start`.
4. Observe that Freely selects a real launchable task, completes it to the current-project success standard, closes the temporary worktree, and continues to another task.

## Real-Environment
- acceptance target: `The final truth surface is canonical develop self-host replay and temporary worktree closeout, not a synthetic premerge-only claim.`
- testing layer: `real_environment`
- target environment: `canonical develop`
- required evidence: `local daemon replay plus fleet closeout evidence`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `The bounded executable seam repaired in this owner is the scan/fleet routing surface, and that seam is already exercised truthfully by the focused CLI regressions on the source lane. Canonical develop self-host replay remains a separate end-to-end completion requirement for this owner and is recorded above instead of being faked as a premerge-only real-environment verdict.`
- not_applicable_reason: `post_merge_only`
- not_applicable_explanation: `The remaining canonical develop daemon replay can only be completed after guarded promotion, so premerge adequacy records the truthful local executable seam rather than pretending develop-side replay already happened.`
- replacement_evidence: `Focused scan/fleet CLI regressions plus guarded develop replay provide the truthful acceptance surface for this bounded owner.`
1. Keep `freely` running on canonical `develop` until it completes at least one task and starts another.
2. Verify the completed task met the current-project success standard, including temporary worktree closeout.
3. Retire `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-absorbed-merged-scan-routing-fix`.
4. Retire `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-test-pre-merge-absorbed-merged-scan-routing-fix`.
5. Re-run `git worktree list` and confirm both temporary worktrees are gone.

## Acceptance Items

### Fleet status downgrades absorbed merged worker lanes
- id: `fleet-status-absorbed-merged-lane-downgrade`
- requirement: `A merged-absorbed worker lane is visible for cleanup followthrough but not surfaced as role=worker execution capacity.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/code-reviews/20260421-absorbed-merged-lane-routing-followthrough-verification.md`

### Task-source scan routes absorbed merged progress to cleanup
- id: `task-source-scan-absorbed-merged-cleanup-routing`
- requirement: `A progress owner bound to an absorbed merged lane remains visible to scan, but its restart point becomes cleanup and manager-owned followthrough instead of verification execution.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/code-reviews/20260421-absorbed-merged-lane-routing-followthrough-verification.md`

### Guarded promote carries absorbed-lane routing evidence
- id: `absorbed-lane-routing-guarded-promote-proof`
- requirement: `The develop-bound replay is backed by an explicit premerge-integration evidence plan rather than by source-lane scan/fleet regressions alone.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#5,tasks.md#6`
- case_design: `Replay the source lane through the disposable test-pre-merge batch, rerun the focused scan/fleet regressions and owner gate there, and then guardedly replay that batch into develop so protected merge consumes concrete owner evidence instead of a raw code diff.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/code-reviews/20260421-absorbed-merged-lane-routing-followthrough-verification.md`

### Guarded replay keeps canonical self-host acceptance explicit
- id: `develop-self-host-after-absorbed-lane-downgrade`
- requirement: `This owner keeps canonical develop self-host replay as an explicit post-merge completion duty instead of pretending focused premerge scan/fleet coverage already proved it.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/code-reviews/20260421-absorbed-merged-lane-routing-followthrough-verification.md`
