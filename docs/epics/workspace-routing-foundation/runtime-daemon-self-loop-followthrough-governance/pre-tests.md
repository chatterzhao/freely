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
8. Run `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-stale-target-worktree-blocked`.
9. Run `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`.
10. Run `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`.
11. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-invalid-forces-resume`.
12. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-stop-ai`.
13. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`.
14. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`.
15. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-blocks-stop-with-unresolved-worker`.
16. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-requires-launchable-prompt`.
17. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`.
18. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`.
19. Run `bash docs/system/workspace/scripts/tests/test-freely-cleanup-governance-retirement-worker-directive`.
20. Run `bash docs/system/workspace/scripts/tests/test-freely-retire-ready-merged-cleanup-handoff-not-reclaimed`.
21. Run `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-defers-codex-reconnect-until-retries-exhaust`.
22. Run `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`.
23. Run `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-429-rate-limit`.
24. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-runtime-cross-tool-recovery-remembers-failed-tools`.
25. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-avoids-initial-start`.
26. Run `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-ignores-codex-model-refresh-timeout`.
27. Run `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-pre-prompt-startup`.
28. Run `bash docs/system/workspace/scripts/tests/test-freely-runtime-failure-guidance`.
29. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-materialized-cleanup-worker-applies-selected-tool`.
30. Run `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`.
31. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-missing-resume-evidence-falls-back`.
32. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-stop-refreshes-manager-operator-boundary`.
33. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`.
34. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`.
35. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-ignores-pre-stop-delegated-continuation-after-operator-stop`.
36. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-ignores-pre-stop-delegated-intake-after-operator-stop`.
37. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autodelegates-cleanup-when-existing-prompt-is-nonlaunchable`.
38. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autodelegates-cleanup-from-worker-verification-truth`.
39. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reclaims-retained-merged-cleanup-self-intent`.
40. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-cleanup-queue-recorded-owner-from-verification-contract`.
41. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-queued-prompt`.
42. Run `bash docs/system/workspace/scripts/tests/test-freely-runtime-auth-failure-signal-filter`.
43. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reclaims-recorded-self-intent`.

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
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-daemon-recovery-verification.md`

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
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#5,tasks.md#6,tasks.md#7`
- case_design: `Use the guarded test-pre-merge lane to prove the owner carries explicit daemon-lifecycle adequacy into develop, then after protected replay observe canonical develop until Freely completes one task with lawful closeout and continues to the next task.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-startup-grace-verification.md`

### Guarded promote carries explicit daemon adequacy
- id: `daemon-self-loop-guarded-promote-proof`
- requirement: `The develop-bound replay is backed by an explicit premerge-integration evidence plan instead of feature-local daemon tests alone.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#5,tasks.md#6,tasks.md#19`
- case_design: `Replay the current blocker owner through the disposable protected test lane, including the reconnect-exhaustion 502 network-path regression set, rerun owner gates there, and use that bounded evidence to justify guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-reconnect-502-network-verification.md`

### Guarded promote carries fresh delegated-continuation stop-boundary evidence
- id: `guarded-promote-pre-stop-delegated-continuation-boundary-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving startup no longer re-consumes pre-stop delegated continuation handoffs after explicit operator stop.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#27`
- case_design: `Replay the stop-boundary delegated-continuation repair through the disposable protected lane, rerun the focused prompt/live-status regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-pre-stop-delegated-continuation-verification.md`

### Guarded promote carries fresh proxy/network diagnosis evidence
- id: `guarded-promote-proxy-guidance-proof`
- requirement: `The develop-bound replay includes fresh staged owner evidence for the current proxy/network diagnosis followthrough rather than relying only on older bounded runtime reviews.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#18`
- case_design: `Replay the current proxy-guidance repair through the disposable protected test lane, rerun the focused proxy/network regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-proxy-guidance-verification.md`

### Guarded promote carries fresh auth-failure classifier evidence
- id: `guarded-promote-auth-failure-timestamp-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving runtime no longer classifies timestamp-shaped non-auth errors as auth_failure before the retained cleanup followthrough can continue.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#28`
- case_design: `Replay the current auth-failure timestamp false-positive repair through the disposable protected lane, rerun the focused auth-classification regressions plus the real-log classifier check, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-auth-failure-timestamp-verification.md`

### Runtime exit contracts are machine-checkable and self-repairable
- id: `runtime-exit-contract-enforcement`
- requirement: `Every manager / worker AI round must leave exactly one valid structured exit contract, or runtime must resume that same role with the exact current resume target and repair handoff before broader work continues.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#9,tasks.md#10`
- case_design: `Exercise manager-invalid, manager-stop, manager-stop-blocked-by-unresolved-worker, manager-delegate-without-launchable-worker, worker-invalid, worker-done, and worker-prompt directive paths so runtime proves prompt injection, post-cycle validation, precise same-session repair behavior, and no premature autonomy stop while recovery-owned worker truth remains open.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`

### Cleanup handoff workers are not reclaimed before external cleanup surfaces run
- id: `cleanup-handoff-not-auto-settled`
- requirement: `A cleanup-governance worker that still carries external owner cleanup scope must remain launchable even if its branch is already merged into develop.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#12`
- case_design: `Construct a merged cleanup-handoff worktree with full verification metadata plus external cleanup write scope and verify runtime neither reclaims ownership nor auto-settles it as retire_ready_merged_worker.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`

### Reconnect retries stay local until the tool actually exits
- id: `reconnect-does-not-trigger-early-cross-tool-switch`
- requirement: `Reconnect-in-progress output must stay on the bounded execution-network retry path until the current tool exhausts its own retries and exits.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#13`
- case_design: `Emit a Codex transcript containing only ERROR: Reconnecting... x/5, verify monitor-ai-cli does not write the network-failure marker or kill the child early, then prove runtime classification still maps that log to execution_network_transient while 429 evidence still remains immediate kill/switch-worthy.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`

### Benign Codex model-refresh timeout noise does not trigger runtime failure
- id: `codex-model-refresh-timeout-noise-ignored`
- requirement: `Known benign Codex startup noise about model-refresh timeout must not write a runtime failure marker or trigger control-plane recovery.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#16`
- case_design: `Emit only the known Codex model-refresh timeout line, confirm monitor-ai-cli records no failure marker, then keep adjacent real-failure regressions green so 429 and reconnect handling still behave as designed.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-startup-grace-verification.md`

### Exhausted Codex reconnect 502 stays on the execution-network path
- id: `codex-reconnect-exhaustion-502-stays-network-scoped`
- requirement: `After Codex exhausts its own reconnect loop and exits with upstream 502 evidence, monitor/runtime must persist network failure truth rather than generic tool_runtime_failure.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#19`
- case_design: `Emit a Codex transcript with reconnect exhaustion plus upstream 502 Bad Gateway evidence, verify monitor-ai-cli writes only the network marker, then keep adjacent reconnect-defer and 429-kill regressions green.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-reconnect-502-network-verification.md`

### Manager bootstrap startup stays alive before prompt build begins
- id: `manager-pre-prompt-startup-grace-preserved`
- requirement: `A newly started manager supervisor must not be restarted as idle while startup is still lawfully between L010 supervisor_started and prompt build / ai launch.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#17`
- case_design: `Seed a running/starting manager with an old workcell timestamp but a fresh L010 lifecycle trace entry, and verify ensure-manager keeps the supervisor alive instead of relaunching before prompt build starts.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-startup-grace-verification.md`

### Exhausted fallback episodes restore the original tool
- id: `fallback-episode-restores-origin-tool`
- requirement: `A bounded cross-tool recovery episode must remember its origin tool and restore that tool selection once every configured fallback has failed.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#13`
- case_design: `Walk one recovery episode across codex -> cc -> iflow -> kiro-cli failures and verify the attempted-tool memory is preserved within the episode while project tool selection returns to codex after exhaustion.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`

### Materialized cleanup worker prompts carry selected tool truth
- id: `materialized-cleanup-worker-selected-tool-truth`
- requirement: `When manager materializes a cleanup-governance worker prompt from continuity, that prompt must carry the authoritative selected_tool so stale retained cleanup worktrees are corrected before launch.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#20`
- case_design: `Seed continuity with selected_tool=codex and a retained cleanup worktree whose local config still says cc-use-codex-cli, then verify materialized worker prompt contains selected_tool and launch rewrites the stale worktree config before startup.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-materialized-cleanup-selected-tool-verification.md`

### Protected replay stages materialized cleanup selected-tool evidence
- id: `materialized-cleanup-worker-selected-tool-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the selected-tool cleanup materialization proof and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#20`
- case_design: `Replay the materialized cleanup selected-tool repair on the disposable protected lane, rerun the four focused selected-tool regressions plus owner gates there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-materialized-cleanup-selected-tool-verification.md`

### Empty Codex session files do not count as resume evidence
- id: `empty-codex-session-files-fall-back-from-resume`
- requirement: `Codex explicit resume targets must only survive when the persisted rollout/session jsonl is non-empty.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#21`
- case_design: `Seed Codex explicit resume state with a zero-byte rollout jsonl, then verify before-launch evidence checks, post-cycle persistence, and tool_has_resume_evidence all reject that state while non-empty jsonl evidence still remains resumable.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-empty-codex-session-resume-verification.md`

### Protected replay stages empty Codex session resume evidence
- id: `empty-codex-session-files-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the empty-session resume regression and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#21`
- case_design: `Replay the empty-session resume repair on the disposable protected lane, rerun the focused explicit-resume contract plus owner gates there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-empty-codex-session-resume-verification.md`

### Repair handoff relaunches stay on resume instead of restarting patrol
- id: `repair-handoff-does-not-regress-to-initial-start`
- requirement: `A manager or worker repair handoff created from an invalid exit contract must resume the recorded tool context even after supervisor restart, instead of re-entering fresh initial patrol.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#16`
- case_design: `Seed session-state plus a manager_exit_contract_repair handoff and verify launch-kind selection stays on resume rather than rotating to fresh/initial_start.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`

### Empty repair resume targets fall back before monitor preflight
- id: `empty-repair-resume-target-falls-back-before-launch`
- requirement: `Exit-contract repair continuity must not force Codex resume when the resolved resume target is empty or lacks verified rollout evidence.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#22`
- case_design: `Seed manager_exit_contract_repair continuity with empty Codex resume state and verify launch-kind selection downgrades to fresh_with_handoff with missing_resume_evidence, while verified resume evidence still preserves the existing repair resume path.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-empty-repair-resume-target-verification.md`

### Protected replay stages empty repair resume target evidence
- id: `empty-repair-resume-target-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the empty repair-resume-target regressions and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#22`
- case_design: `Replay the empty repair-resume-target fix on the disposable protected lane, rerun the focused repair-handoff and explicit-resume regressions plus owner gates there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-empty-repair-resume-target-verification.md`

### Cleanup followthrough runs before manager resume relaunch
- id: `cleanup-followthrough-precedes-resume-manager-relaunch`
- requirement: `When manager exit-contract replay resolves to resume_manager while continuity already targets cleanup governance, runtime must execute that cleanup followthrough before relaunch and must materialize exact blocker truth if the cleanup step fails.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#23`
- case_design: `Seed a resume_manager exit-contract with cleanup-followthrough continuity and verify runtime either runs cleanup before relaunch or records manager_exit_contract_cleanup_followthrough_failed plus repair handoff when that cleanup path fails.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260423-runtime-daemon-self-loop-followthrough-cleanup-followthrough-resume-verification.md`

### Protected replay stages cleanup followthrough resume evidence
- id: `cleanup-followthrough-resume-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the cleanup-followthrough resume regressions and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#23`
- case_design: `Replay the cleanup-followthrough resume repair on the disposable protected lane, rerun the focused cleanup-followthrough resume regressions plus owner gates there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260423-runtime-daemon-self-loop-followthrough-cleanup-followthrough-resume-premerge-verification.md`

### Protected replay stages Codex OAuth refresh network-classification evidence
- id: `codex-oauth-refresh-network-classification-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the focused Codex OAuth refresh network-classification regressions and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#13`
- case_design: `Replay the Codex OAuth refresh transport-classification repair on the disposable protected lane, rerun the focused OAuth request-send network classification regressions plus owner gate there, and stage the refreshed owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`

### Worker materialization and pipe-safe summary hold on feature lane
- id: `worker-materialization-and-summary-feature-proof`
- requirement: `Daemon patrol must tolerate closed-pipe worktree summary consumers, and manager launch must be able to materialize a governed missing sibling worker lane without reclaiming active authoritative edit ownership as retire-ready cleanup.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#24`
- case_design: `Run the focused worktree-summary broken-pipe regressions together with worker materialization / authoritative-edit ownership regressions on the writable owner lane and record the bounded followthrough evidence under the owner review directory.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260423-runtime-daemon-self-loop-followthrough-worker-materialization-and-summary-verification.md`

### Protected replay stages worker materialization and pipe-safe summary evidence
- id: `worker-materialization-and-summary-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the bounded worker-materialization / summary regressions plus owner gates and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#24`
- case_design: `Replay the pipe-safe worktree-summary and missing-worktree materialization repair on the disposable protected lane, rerun the focused summary and worker-materialization regressions plus owner gates there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260423-runtime-daemon-self-loop-followthrough-worker-materialization-and-summary-verification.md`

### Explicit daemon stop invalidates pre-stop patrol continuity
- id: `daemon-stop-refreshes-pre-stop-boundary`
- requirement: `An explicit daemon stop must refresh the manager operator-stop boundary so the next startup patrol treats older manager continuity as stale history instead of current queue truth.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#25`
- case_design: `Seed a manager continuity newer than the previous boundary, run stop handling with operator_daemon_stop, and verify the refreshed boundary makes that continuity pre-stop on the next patrol.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260423-runtime-daemon-self-loop-followthrough-daemon-stop-boundary-verification.md`

### Queue-state worker handoffs stay launchable through delegate_workers
- id: `queue-state-worker-handoff-launches-worker`
- requirement: `When manager continuity uses the current ## Queue State shape with worker_prompts:, runtime must still extract the prompt, record launch-state truth, and start the worker after delegate_workers.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#26`
- case_design: `Replay the queue-state handoff repair on a disposable protected test lane, rerun the continuity parsing and post-AI-cycle launch regressions there, and stage a fresh owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-queue-state-worker-prompt-premerge-verification.md`

### Protected replay stages explicit daemon-stop boundary evidence
- id: `daemon-stop-boundary-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the explicit daemon-stop boundary regression plus owner gates and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#25`
- case_design: `Replay the explicit daemon-stop boundary repair on the disposable protected lane, rerun the focused daemon-stop boundary regression plus owner gates there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260423-runtime-daemon-self-loop-followthrough-daemon-stop-boundary-premerge-verification.md`

### Blocked cleanup workers retain authoritative recorded ownership
- id: `blocked-cleanup-recorded-owner-retained`
- requirement: `When a cleanup worker exits blocked, runtime must derive current blocking ownership from the authoritative verification-contract prompt source rather than a later worker-local AI prompt that may omit dispatch headers.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#28`
- case_design: `Simulate a blocked cleanup worker whose verification contract still points at the delegated source prompt while the latest worker AI prompt no longer carries machine-readable Worktree/Branch headers, then verify duplicate cleanup launch requests queue behind the recorded owner instead of relaunching the lane.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-cleanup-blocked-recorded-owner-verification.md`

### Protected replay stages blocked cleanup ownership evidence
- id: `blocked-cleanup-recorded-owner-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the blocked-cleanup recorded-owner regression together with adjacent ownership guards and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#28`
- case_design: `Replay the blocked-cleanup ownership repair on a disposable protected lane, rerun the duplicate-cleanup, stale-target, and duplicate-promotion recorded-owner regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-cleanup-blocked-recorded-owner-premerge-verification.md`

### Cleanup governance autofills nonlaunchable retained-lane prompts
- id: `cleanup-nonlaunchable-prompt-autofill`
- requirement: `When cleanup_governance continuity already carries an AI-written worker prompt for a retained merged lane, runtime must materialize an authoritative verification-bound cleanup prompt if that existing prompt is not launchable.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#29`
- case_design: `Seed canonical cleanup continuity with a retained merged cleanup lane plus an AI-written hygiene prompt that lacks verification metadata, then verify manager exit-contract autofill appends a launchable authoritative cleanup prompt instead of looping on WORKER_PROMPTS_NOT_LAUNCHABLE.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-nonlaunchable-cleanup-autofill-verification.md`

### Cleanup governance current-shape continuity recovers from worker verification truth
- id: `cleanup-current-shape-worker-verification-autofill`
- requirement: `When cleanup_governance continuity exposes only top-level route kind plus inline worker_prompt references, runtime must still resolve the retained cleanup lane and inherit authoritative verification metadata from that worker's existing prompt/contract.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#29`
- case_design: `Seed current-shape cleanup continuity with top-level route_kind, inline Worker Dispatch prompt references, and a retained merged cleanup lane whose authoritative verification truth already exists on the target worker; verify manager exit-contract autofill rewrites the nonlaunchable hygiene prompt into a launchable authoritative cleanup prompt.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-nonlaunchable-cleanup-autofill-verification.md`

### Protected replay stages current-shape cleanup autofill evidence
- id: `cleanup-current-shape-worker-verification-autofill-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the current-shape cleanup autofill regression together with the adjacent cleanup-governance launchability guard and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#29`
- case_design: `Replay the current-shape retained-lane cleanup prompt repair on a disposable protected lane, rerun the worker-verification-truth autofill regression together with the adjacent nonlaunchable-prompt launchability guard plus owner gates there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-current-shape-cleanup-autofill-premerge-verification.md`

### Retained cleanup self-intent relaunch stays launchable
- id: `retained-cleanup-self-intent-relaunch`
- requirement: `When manager relaunches a retained merged cleanup lane from authoritative verification-bound prompt truth, runtime must let that lane reclaim its own recorded cleanup intent instead of self-queuing forever.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#32`
- case_design: `Seed a retained merged cleanup lane whose current recorded cleanup signature matches the authoritative delegated prompt, then verify manager launches that prompt while adjacent duplicate-owner and stale-queue guards remain intact.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-retained-cleanup-self-intent-verification.md`

### Protected replay stages retained cleanup self-intent relaunch evidence
- id: `retained-cleanup-self-intent-relaunch-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the retained cleanup self-intent relaunch regression together with adjacent queue/ownership guards and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#32`
- case_design: `Replay the retained cleanup self-intent relaunch repair on a disposable protected lane, rerun the focused retained-self-reclaim, duplicate-owner, stale-queue, and post-ai-cycle launch regressions plus owner gates there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-retained-cleanup-self-intent-premerge-verification.md`

### Recorded self-intent worker relaunch stays launchable
- id: `recorded-self-intent-worker-relaunch`
- requirement: `When manager re-delegates a stopped worker lane whose target worktree still advertises the same soft-stale recorded intent signature, runtime must relaunch that exact lane instead of queueing it behind its own recorded ownership.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#33`
- case_design: `Seed a stopped worker lane whose latest prompt leaves an `edit@<target_worktree>` recorded signature behind, delegate the same lane again from manager continuity, and verify launch selection reclaims that self-intent while leaving other queued/frozen holders blocked.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-recorded-self-intent-verification.md`

### Protected replay stages recorded self-intent relaunch evidence
- id: `recorded-self-intent-worker-relaunch-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the recorded self-intent relaunch regression together with adjacent ownership queue guards and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#33`
- case_design: `Replay the recorded-self-intent relaunch repair on a disposable protected lane, rerun the focused relaunch, retained-cleanup reclaim, duplicate-owner queue, and stale-queue regressions there, then stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260424-runtime-daemon-self-loop-followthrough-recorded-self-intent-premerge-verification.md`
