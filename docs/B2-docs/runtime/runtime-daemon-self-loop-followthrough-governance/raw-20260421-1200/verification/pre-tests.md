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
- blocker taxonomy: `pass`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`.
6. Run `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/issues/runtime-daemon-self-loop-followthrough-governance.md`.
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
44. Run `bash docs/system/workspace/scripts/tests/test-freely-worktree-summary-tolerates-closed-pipe`.
45. Run `bash docs/system/workspace/scripts/tests/test-freely-discover-supervisor-pid-sigpipe-guard`.
46. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-continuity-discovery-tolerates-closed-pipe`.
47. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-ignores-pre-stop-continuity`.
48. Run `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`.
49. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-failure-recovery-preserves-daemon`.
50. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`.
51. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`.
52. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`.
53. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-active-stall-recovery-from-manager-watchdog`.
54. Run `bash docs/system/workspace/scripts/tests/test-freely-delegated-worker-starting-stuck-reclaim`.
55. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-reclaims-stale-starting-worker-slot`.
56. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-collapses-terminal-handoff-worker-slot`.
57. Run `bash docs/system/workspace/scripts/tests/test-freely-runtime-effective-worker-role-from-contract`.
58. Run `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-between-rounds-relaunch-grace`.
59. Run `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-while-worker-active`.
60. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-autonomous-existing-worktree-review-merge-retire-next-task-loop`.
61. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-resume-cycle-does-not-reuse-stale-output-evidence`.

## End-to-End
- acceptance target: `Protected promotion must carry this owner chain and the final daemon acceptance must prove Freely can keep working instead of stopping after one patrol round.`
- testing layer: `end_to_end`
- target environment: `guarded feature -> test-pre-merge -> develop replay`
- required evidence: `merge receipts plus develop-side runtime observation`
- blocker taxonomy: `pass`
1. Merge `feature/runtime-daemon-self-loop-blocker-20260421` into `test-pre-merge-20260421-runtime-self-loop-blocker` via `freely pr-merge-guarded`.
2. Merge `test-pre-merge-20260421-runtime-self-loop-blocker` into `develop` via `freely pr-merge-guarded`.
3. On canonical `develop`, run `freely daemon start`.
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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260422-runtime-daemon-self-loop-followthrough-daemon-recovery-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260428-runtime-daemon-self-loop-state-closeout-verification.md`

### Canonical develop proves autonomous continuation
- id: `develop-self-host-daemon-continuation`
- requirement: `Canonical develop proves Freely can autonomously pick a task, finish it to the current-project success standard, close the temporary worktree, and proceed to another task.`
- surface_kind: `real_environment`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#5,tasks.md#6,tasks.md#7`
- case_design: `Use the guarded test-pre-merge lane to prove the owner carries explicit daemon-lifecycle adequacy into develop, then after protected replay observe canonical develop until Freely completes one task with lawful closeout and continues to the next task.`
- evidence_level: `integration`
- status: `not_applicable`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- not_applicable_reason: `covered_by_more_realistic_required_surface`
- not_applicable_explanation: `The truthful acceptance surface for this item only exists after guarded promote reaches canonical develop. Marking it pass before that replay would be false; premerge adequacy is instead anchored by the fresh protected replay artifact, and the immediate next step remains the post-merge canonical daemon replay.`
- replacement_evidence: `Fresh premerge-integration replay in test-pre-merge-runtime-target-worker-role-and-starting-stuck-recovery-20260425 plus the staged owner verification artifact prove guarded-merge adequacy without pretending canonical develop has already completed the full autonomous loop.`
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-control-plane-argv-contract-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-control-plane-argv-contract-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-pre-stop-delegated-continuation-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260422-runtime-daemon-self-loop-followthrough-proxy-guidance-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-auth-failure-timestamp-verification.md`

### Guarded promote carries fresh superseded-frozen prompt reclaim evidence
- id: `guarded-promote-superseded-frozen-prompt-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving runtime consumes the authoritative retained-lane prompt instead of queueing forever behind older same-lane frozen prompt history.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#28`
- case_design: `Replay the superseded-frozen prompt reclaim repair through the disposable protected lane, rerun the focused manager worker-launch regressions plus owner gates there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-superseded-frozen-prompt-premerge-verification.md`

### Guarded promote carries fresh daemon entrypoint ownership evidence
- id: `guarded-promote-daemon-entrypoint-mode-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving daemon-owned recovery preserves entrypoint ownership while ai launch is in flight, so watchdog relaunch cannot silently fall back to foreground start semantics.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#29`
- case_design: `Replay the daemon entrypoint-mode preservation repair through the disposable protected lane, rerun the focused monitor/daemon recovery regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-entrypoint-mode-preservation-verification.md`

### Guarded promote carries fresh resume-cycle evidence-boundary proof
- id: `guarded-promote-resume-incremental-output-evidence-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving a reused Codex resume session cannot satisfy manager success using stale historical output from an earlier cycle.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#20,tasks.md#35,tasks.md#36`
- case_design: `Replay the resume evidence-boundary repair through the disposable protected lane, rerun the focused manager exit-contract regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-resume-incremental-output-evidence-verification.md`

### Guarded promote carries fresh queued-owner self-block evidence
- id: `guarded-promote-queued-owner-self-block-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving runtime no longer lets the retained authoritative prompt block itself as queued-owner while preserving real earlier queued-owner explainability.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#28`
- case_design: `Replay the queued-owner self-block repair through the disposable protected lane, rerun the focused worker-delegation, active-authoritative, and duplicate queued-owner regressions plus owner gates there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-queued-owner-self-block-premerge-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260428-runtime-daemon-self-loop-state-closeout-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260428-runtime-daemon-self-loop-state-closeout-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260428-runtime-daemon-self-loop-state-closeout-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260422-runtime-daemon-self-loop-followthrough-startup-grace-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260422-runtime-daemon-self-loop-followthrough-reconnect-502-network-verification.md`

### Cached discovery producers survive closed-pipe consumers
- id: `cached-discovery-producers-survive-closed-pipe`
- requirement: `Closed-pipe exits from early-return consumers must not abort manager or worker supervision while runtime is scanning continuity, worktrees, or PID inventories.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#33`
- case_design: `Exercise worktree-summary, supervisor-discovery, and manager continuity discovery paths under set -euo pipefail with downstream consumers that return as soon as they find the first needed record.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-sigpipe-closeout-verification.md`

### Guarded promote carries fresh SIGPIPE closeout evidence
- id: `guarded-promote-sigpipe-closeout-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving cached discovery producers no longer strand supervisor closeout when downstream consumers exit early.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#33`
- case_design: `Replay the SIGPIPE closeout repair through the disposable protected lane, rerun the focused closed-pipe regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-sigpipe-closeout-premerge-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260422-runtime-daemon-self-loop-followthrough-startup-grace-verification.md`

### Resumed manager round stays alive while the next prompt is still building
- id: `manager-resume-prompt-build-startup-grace-preserved`
- requirement: `After ai_cycle_finished and resume_manager handoff, ensure-manager must keep the same supervisor alive while that resumed round has already re-entered L020/L021/L022 startup lifecycle truth and has not yet relaunched AI.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#36`
- case_design: `Seed a running manager whose between-rounds grace is already expired, but whose lifecycle trace has a newer L020 prompt_build_begin after the last L042 ai_cycle_finished, and verify ensure-manager keeps the same supervisor alive instead of triggering manager_idle_supervisor_restart.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-resume-prompt-build-grace-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260428-runtime-daemon-self-loop-state-closeout-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260422-runtime-daemon-self-loop-followthrough-materialized-cleanup-selected-tool-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260422-runtime-daemon-self-loop-followthrough-materialized-cleanup-selected-tool-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260422-runtime-daemon-self-loop-followthrough-empty-codex-session-resume-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260422-runtime-daemon-self-loop-followthrough-empty-codex-session-resume-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260428-runtime-daemon-self-loop-state-closeout-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260422-runtime-daemon-self-loop-followthrough-empty-repair-resume-target-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260422-runtime-daemon-self-loop-followthrough-empty-repair-resume-target-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260423-runtime-daemon-self-loop-followthrough-cleanup-followthrough-resume-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260423-runtime-daemon-self-loop-followthrough-cleanup-followthrough-resume-premerge-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260428-runtime-daemon-self-loop-state-closeout-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260423-runtime-daemon-self-loop-followthrough-worker-materialization-and-summary-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260423-runtime-daemon-self-loop-followthrough-worker-materialization-and-summary-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260423-runtime-daemon-self-loop-followthrough-daemon-stop-boundary-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-queue-state-worker-prompt-premerge-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260423-runtime-daemon-self-loop-followthrough-daemon-stop-boundary-premerge-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-cleanup-blocked-recorded-owner-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-cleanup-blocked-recorded-owner-premerge-verification.md`

### Existing stale worker worktree bootstrap repair holds on feature lane
- id: `existing-stale-worker-worktree-bootstrap-feature-proof`
- requirement: `If a manager-selected worker worktree directory already exists with .freely/config.env already present but managed tooling or .freely/run/workcell-state.env still missing, runtime must repair that same worktree before delegation instead of treating it as already launch-ready.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#34`
- case_design: `Run test-freely-manager-worker-launch-repairs-existing-stale-worktree by seeding an authoritative worker prompt that targets an already-existing sibling worktree containing only copied .freely/config.env, then verify manager launch syncs tooling, recreates runtime baseline state, and starts the worker instead of stalling on the half-materialized directory.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-existing-stale-worker-bootstrap-verification.md`

### Protected replay stages existing stale worker worktree bootstrap repair
- id: `existing-stale-worker-worktree-bootstrap-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the bounded stale-existing-worktree bootstrap regressions together with adjacent worker-materialization/tooling checks and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#34`
- case_design: `Replay the stale-existing-worktree bootstrap repair on the disposable protected lane, rerun the focused stale-worktree launch repair regression plus missing-worktree materialization and sync-tooling regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-existing-stale-worker-bootstrap-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-nonlaunchable-cleanup-autofill-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-nonlaunchable-cleanup-autofill-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-current-shape-cleanup-autofill-premerge-verification.md`

### Dispatch-state cleanup continuity recovers from source prompt fallback
- id: `cleanup-dispatch-state-source-prompt-fallback`
- requirement: `When cleanup-governance continuity exposes retained-lane prompt truth only through dispatch-state worker prompt paths and legacy issue-truth is absent, runtime must still materialize a fresh launchable cleanup prompt from the continuity-carried source prompt metadata for that same retained merged lane.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#36`
- case_design: `Seed cleanup-governance continuity with dispatch-state worker prompt paths, no legacy issue-truth, and only a merged-lane nonlaunchable edit prompt carrying verification metadata for the same retained worker; verify manager exit-contract autofill writes a fresh cleanup prompt, rebases owner metadata into the retained worker worktree, and keeps the nonlaunchable launchability guard intact.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-dispatch-state-cleanup-source-prompt-fallback-premerge-verification.md`

### Protected replay stages dispatch-state cleanup source-prompt fallback evidence
- id: `cleanup-dispatch-state-source-prompt-fallback-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must rerun the dispatch-state source-prompt fallback regression together with the adjacent cleanup-governance launchability guard and stage a fresh owner review artifact under the owner code-reviews directory.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#36`
- case_design: `Replay the dispatch-state retained-lane cleanup prompt repair on a disposable protected lane, rerun the source-prompt fallback regression together with the delegate-workers launchability guard, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-dispatch-state-cleanup-source-prompt-fallback-premerge-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-retained-cleanup-self-intent-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-retained-cleanup-self-intent-premerge-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-recorded-self-intent-verification.md`

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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-recorded-self-intent-premerge-verification.md`

### Protected replay stages active authoritative worker prompt consumption evidence
- id: `active-authoritative-worker-prompt-consumption-premerge-proof`
- requirement: `Before guarded develop merge, the protected test lane must prove manager consumes an already-active worker's exact authoritative prompt instead of keeping that prompt queued and spinning another manager round.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#34`
- case_design: `Replay the active-authoritative worker prompt consumption repair on a disposable protected lane, rerun the focused active-authoritative, delegated-busy queue, and launch-state refresh regressions there, then stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-active-authoritative-worker-prompt-premerge-verification.md`

### Guarded promote carries worker exit contract network-transient precedence evidence
- id: `guarded-promote-worker-exit-contract-network-transient-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving a valid retained-worker exit contract stops the lane even if the same AI cycle is also classified as reconnect/network transient, while malformed contracts still stay on bounded recovery.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#9,tasks.md#10`
- case_design: `Replay the worker exit-contract network-transient precedence repair through the disposable protected lane, rerun the focused worker_done, network-transient override, malformed-contract recovery, and owner gates there, then stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-worker-exit-contract-network-transient-premerge-verification.md`

### Guarded promote carries manager-owned worker runtime source rebind evidence
- id: `guarded-promote-manager-worker-runtime-source-rebind-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving retained active worker control planes are rebound from stale worktree-local runtime code to the canonical manager/source runtime before closeout continues.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#34`
- case_design: `Replay the manager-owned worker runtime source-rebind repair on a disposable protected lane, rerun the focused source-runtime launch and stale-active-runtime rebind regressions plus owner governance there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260424-runtime-daemon-self-loop-followthrough-manager-worker-runtime-source-rebind-premerge-verification.md`

### Guarded promote carries manager/worker self-loop recovery evidence
- id: `guarded-promote-manager-worker-self-loop-recovery-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving delegated-worker effective role, starting-stuck reclaim, terminal-worker closeout handling, and manager keepalive now preserve the full manager/worker/runtime handoff loop instead of stopping after the first dispatch.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#34`
- case_design: `Replay the manager/worker self-loop recovery repair on the disposable protected lane, rerun the focused delegated-worker role, starting-stuck reclaim, manager keepalive, and autonomous existing-worktree loop regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-worker-self-loop-recovery-verification.md`

### Guarded promote carries terminal followthrough materialization evidence
- id: `guarded-promote-manager-worker-terminal-followthrough-materialization-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving manager empty-success rounds no longer auto-resume from input-only Codex sessions, terminal worker exit contracts are materialized into manager-consumable delegated continuation truth, and advisory live-status helpers cannot abort followthrough state inspection early.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#34`
- case_design: `Replay the manager/worker terminal followthrough materialization repair on the disposable protected lane, rerun the focused explicit-resume, empty-success, terminal-worker materialization, idempotence, and live-status advisory regressions there, then stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-worker-terminal-followthrough-materialization-verification.md`

### Guarded promote carries post-ai-cycle finalize keepalive evidence
- id: `guarded-promote-manager-post-ai-cycle-finalize-grace-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving ensure-manager does not restart a live manager supervisor during the narrow post-L041 finalize window before ai_cycle_finished or other terminal lifecycle checkpoints are recorded.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#35`
- case_design: `Replay the manager post-ai-cycle finalize keepalive repair on the disposable protected lane, rerun the focused finalize-grace and adjacent empty-success / exit-contract regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-post-ai-cycle-finalize-grace-verification.md`

### Guarded promote carries terminal handoff followthrough absorb evidence
- id: `guarded-promote-terminal-handoff-followthrough-absorb-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving manager launch absorbs stale terminal worker_handoff_needed truth when the same lane already has a newer authoritative followthrough prompt, instead of suppressing that lane forever.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#35`
- case_design: `Replay the terminal-handoff followthrough absorb repair on the disposable protected lane, rerun the focused absorb, runtime-recovery, and terminal-slot-collapse regressions plus owner governance there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-terminal-handoff-followthrough-absorb-premerge-verification.md`

### Delegated continuation session state clears absorbed pending backlog
- id: `delegated-continuation-session-state-clears-absorbed-pending-backlog`
- requirement: `When the active manager prompt already carries a Delegated continuation handoff block, runtime must persist those delegated IDs as consumed and must not keep the same IDs exposed as pending session-state backlog.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#36`
- case_design: `Seed delegated pending ids, build an active prompt that already contains the delegated continuation handoff block, write session-state, and verify the same ids move to consumed while pending ids/count collapse to empty/zero so resume focus can execute the current followthrough instead of treating it as still-pending backlog.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-delegated-continuation-pending-state-verification.md`

### Guarded promote carries delegated continuation pending-state evidence
- id: `guarded-promote-delegated-continuation-pending-state-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving delegated continuation ids already absorbed into the active manager prompt are cleared from pending session-state, so consumed-continuity resume cannot stall behind contradictory backlog truth.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#36`
- case_design: `Replay the delegated-continuation pending-state repair on the disposable protected lane, rerun the focused pending-state and consumed-continuity resume-focus regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-delegated-continuation-pending-state-verification.md`

### Guarded promote carries resumed prompt-build keepalive evidence
- id: `guarded-promote-manager-resume-prompt-build-grace-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving ensure-manager does not restart a live manager supervisor after resume_manager once the same supervisor has already re-entered L020/L021/L022 startup lifecycle truth for the next round.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#37`
- case_design: `Replay the resumed prompt-build keepalive repair on the disposable protected lane, rerun the focused resumed-prompt-build, between-rounds, pre-prompt, and post-finalize keepalive regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-resume-prompt-build-grace-verification.md`

### Feature-local post-L042 followthrough keepalive evidence is develop-bound adequate
- id: `feature-local-post-l042-followthrough-keepalive-develop-adequacy`
- requirement: `Before protected promote, the owner must carry explicit feature-local develop-bound adequacy evidence that same-supervisor L042 is treated as followthrough-in-flight keepalive instead of idle restart truth.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#38`
- case_design: `Run the focused post-L042 helper, ensure-manager top-level keepalive, resume-manager cleanup-followthrough, and network-transient override regressions in the writable owner worktree, then record the owner-linked verification artifact that explains why this seam belongs to the runtime middleman rather than task-selection or role-taxonomy design.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-post-l042-followthrough-keepalive-verification.md`

### Guarded promote carries post-L042 followthrough keepalive evidence
- id: `guarded-promote-post-l042-followthrough-keepalive-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving watchdog does not restart a live manager supervisor after L042 while the same supervisor is still finishing exit-contract replay or delegated followthrough.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#38`
- case_design: `Replay the post-L042 keepalive repair on the disposable protected lane, rerun the focused post-L042 helper, ensure-manager top-level keepalive, cleanup-followthrough, and network-transient override regressions there, and stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-post-l042-followthrough-keepalive-verification.md`

### Feature-local manager exit-contract repair prompt narrowing is develop-bound adequate
- id: `feature-local-manager-exit-contract-repair-prompt-narrowing-develop-adequacy`
- requirement: `Before protected promote, the owner must carry explicit feature-local develop-bound adequacy evidence that manager repair rounds downgraded to fresh_with_handoff on missing resume evidence no longer re-enter broad startup patrol before writing continuity and exit-contract artifacts.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#39`
- case_design: `Run the focused manager repair prompt narrowing regression plus the adjacent empty-success, missing-resume-evidence fallback, worker repair prompt, and consumed-continuity resume-focus regressions in the writable owner worktree, then stage the owner-linked verification artifact that explains why this seam belongs to the runtime prompt contract rather than scan choice or role taxonomy.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-exit-contract-prompt-narrowing-verification.md`

### Guarded promote carries manager exit-contract repair prompt narrowing evidence
- id: `guarded-promote-manager-exit-contract-repair-prompt-narrowing-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving a manager exit-contract repair round relaunched as fresh_with_handoff on missing resume evidence receives a bounded continuity-first / exit-contract-second prompt instead of broad startup patrol.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#39`
- case_design: `Replay the manager exit-contract repair prompt narrowing on the disposable protected lane, rerun the focused manager repair prompt narrowing, empty-success, missing-resume-evidence fallback, worker repair prompt, consumed-continuity resume-focus regressions, and governance gate there, then stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-exit-contract-prompt-narrowing-verification.md`

### Feature-local manager repair handoff survives missing-resume downgrade
- id: `feature-local-manager-exit-contract-repair-handoff-preservation-develop-adequacy`
- requirement: `Before protected promote, the owner must carry explicit feature-local develop-bound adequacy evidence that a manager exit-contract repair handoff downgraded to fresh_with_handoff on missing resume evidence is not overwritten by a generic rotation handoff before prompt build.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#39`
- case_design: `Run the chain-level manager repair handoff preservation regression together with the prompt narrowing, missing-resume-evidence fallback, worker repair prompt, and empty-success adjacency regressions in the writable owner worktree, then stage the owner-linked verification artifact that pins the failure to the runtime handoff/prompt control plane seam.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-exit-contract-repair-handoff-preservation-verification.md`

### Guarded promote carries manager repair handoff preservation evidence
- id: `guarded-promote-manager-exit-contract-repair-handoff-preservation-proof`
- requirement: `The develop-bound replay includes a fresh staged owner artifact proving that a manager exit-contract repair round downgraded to fresh_with_handoff on missing resume evidence preserves the repair handoff through prompt build instead of rewriting it into a generic rotation handoff.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#39`
- case_design: `Replay the manager repair handoff preservation fix on the disposable protected lane, rerun the chain-level preservation regression plus the adjacent prompt narrowing, empty-success, missing-resume-evidence fallback, worker repair prompt, and governance regressions there, then stage the resulting owner review artifact before guarded promote into develop.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/raw-20260421-1200/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-exit-contract-repair-handoff-preservation-verification.md`
