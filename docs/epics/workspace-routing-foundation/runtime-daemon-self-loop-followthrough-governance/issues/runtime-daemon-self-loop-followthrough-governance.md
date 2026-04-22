# Issue: runtime-daemon-self-loop-followthrough-governance

- issue_id: `I-20260421-1200-A`
- title: `Runtime daemon self-loop followthrough governance`
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-daemon-self-loop-followthrough-governance`
- issue-name: `runtime-daemon-self-loop-followthrough-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260421-1200--runtime-daemon-self-loop-followthrough/candidates.md#c-20260421-1200-a`
- source_brainstorm: `docs/pre-brainstorms/20260421-1200--runtime-daemon-self-loop-followthrough/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
- reopen_reason: `real self-host dogfooding on 2026-04-21 showed one remaining daemon self-loop blocker after the broader runtime lifecycle owner landed: unexpected daemon TERM could be recorded as operator_stop, and orphan dispatcher/watchdog residue could block lawful restart`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/pre-tests.md`
- tasks_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-daemon-self-loop-followthrough-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/issues/three-loop-lifecycle-single-source-governance-followthrough.md`
- created_at: `2026-04-21`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

The blocker here is narrower than the surrounding scan/live-status architecture debate. Freely already knows how to patrol, choose a task source, and write continuity, but the runtime could not reliably remain in autonomous looping on canonical `develop`.

Two concrete causes were verified in real execution:

1. user-facing start precheck could treat orphaned dispatcher/watchdog residue as authoritative runtime truth even when no valid supervisor existed,
2. daemon supervisor could record an unexpected external `TERM` as `operator_stop`, which breaks autonomous looping after one patrol round.

This owner exists to carry the narrow fix through a lawful protected-branch path and then prove the final acceptance surface on `develop`, not just feature-local green tests.

## Scope

1. Keep `project_has_authoritative_runtime_processes_for_user_precheck()` authoritative-supervisor-only for user-facing repeated-start refusal.
2. Make daemon-mode supervisor ignore unexpected `INT`/`TERM` when no `stop.marker` exists, while preserving explicit stop semantics.
3. Keep current manager continuity formats runtime-consumable by parsing `## Worker Delegation` handoffs into concrete worker prompt launches.
4. Route `merged-clean` / `retire-ready` worker lanes to cleanup followthrough retirement instead of runtime recovery, and let cleanup reclaim stale recorded ownership for those lanes.
5. Treat merged develop-absorbed worker lanes that are dirty only in owner evidence surfaces as cleanup/promotion followthrough, not as relaunchable edit workers.
6. Add focused regressions for orphan precheck residue, unexpected daemon `TERM`, worker-delegation continuity consumption, and retire-ready merged-worker retirement routing.
7. Keep manager-owned continuity followthrough anchored across both `resume` and `fresh_with_handoff` launches so context compaction cannot devolve into rewriting the same continuity instead of performing the queued maintenance / retirement work.
8. Distinguish never-started worker branches from truly absorbed merged lanes so launch gating still starts real work while absorbed merged workers remain routed to retirement followthrough.
9. Replay the guarded promotion path with concrete owner evidence.
10. Ensure a newer manager-authored continuity can supersede stale queued worker-prompt state when the current truth has shifted to manager-owned cleanup / completion verification with no launchable worker prompt.
11. Prove on canonical `develop` that Freely self-starts, selects a task, completes it to the current-project success standard, closes the temporary worktree, and continues to another task.
12. When runtime learns that `kiro-cli` is unavailable due to monthly request exhaustion during canonical self-host replay, persist that tool-unavailable truth so later auto-switch / manager bootstrap decisions do not immediately route back into the same exhausted tool.
13. After guarded `develop` merge push followthrough succeeds, refresh local upstream tracking truth so manager/live-status do not keep treating canonical `develop` as `push_pending` purely because the local remote-tracking ref stayed stale.
14. Auto-clean untracked disposable Python cache residue (`__pycache__` / `.pyc`) before runtime hygiene judgement so canonical self-host replay does not spin forever on runtime-only cache dirt instead of advancing the selected cleanup / replay followthrough.
15. Keep Codex resume launches compatible with the current CLI contract: `codex exec resume` must not inherit `--add-dir`, otherwise manager continuity handoff chains crash with `ai_exit_rc_2` before followthrough can continue.
16. Only bootstrap worker runtime state for target paths that still belong to the authoritative `git worktree list --porcelain` fleet, and require missing-config worker init to succeed with inherited default-autonomy consent before any post-init config mutation proceeds.
17. Skip `sync-tooling` config and hook rewrites for stale directories that still sit under the managed `*-worktrees` root but no longer belong to the authoritative `git worktree list --porcelain` fleet, while preserving valid worktree sync and fresh-project bootstrap.
18. Require every manager AI round to leave exactly one machine-checkable exit contract artifact whose `EXIT_KIND` is one of `stop_ai`, `resume_manager`, or `delegate_workers`.
19. Require every worker AI round to leave exactly one machine-checkable exit contract artifact whose `EXIT_KIND` is one of `worker_done`, `worker_blocked`, or `worker_handoff_needed`.
20. When an exit contract is missing or malformed, reuse the exact current resume target for that role and force a same-session repair handoff before broader patrol, delegation, or closeout continues.
21. Do not reclaim or auto-settle a cleanup-handoff worker as `retire_ready_merged_worker` when its authoritative prompt still carries full verification metadata and external cleanup surfaces that must run before fleet retirement can close.
22. Resolve that cleanup-handoff authority from the worker verification contract when no local worker prompt artifact remains in the target worktree, so merged-lane settle/reclaim uses the same prompt truth runtime launched from.
23. Prefer the worker verification contract `SOURCE_PROMPT_FILE` over any later worker-local bootstrap/reentry prompt when deciding whether a merged lane is still a cleanup-handoff worker with external cleanup scope.
24. Refuse manager `EXIT_KIND=stop_ai` whenever authoritative supervision truth still shows any unresolved runtime-owned expected-running worker, so autonomy cannot legally terminate while recovery/cleanup followthrough remains open.
25. When a down expected-running worker is relaunched from fresh runtime state, reapply the delegated prompt's authoritative `selected_tool` from the worker verification contract instead of inheriting a stale fallback tool from the failed prior attempt.
26. Reject manager `EXIT_KIND=delegate_workers` unless the advertised `WORKER_PROMPTS_CSV` contains at least one prompt that the same runtime control plane would actually treat as launchable.

## Non-Goals

1. Do not redesign scan architecture or live-status semantics in this owner.
2. Do not weaken Freely's freedom of action or task autonomy.
3. Do not reopen unrelated runtime/watchdog architecture owners.
4. Do not stop at "daemon process stayed alive once"; the final acceptance remains autonomous end-to-end self-work on `develop`.

## Acceptance

1. Focused regressions cover the orphaned precheck residue and unexpected daemon `TERM` seams.
2. Focused regressions also prove runtime consumes current `## Worker Delegation` continuity and retires merged-clean blocker worktrees instead of re-recovering them.
3. `./bin/pretests-gate` and `./bin/governance-check` pass for this owner.
4. Guarded replay from `feature/runtime-daemon-self-loop-blocker-20260421` through `test-pre-merge-20260421-runtime-self-loop-blocker` into `develop` succeeds lawfully.
5. On canonical `develop`, `freely daemon start` selects at least one task, completes it to the current-project success standard, closes the corresponding temporary worktree, and proceeds to another task.
6. The temporary blocker worktree and disposable test-pre-merge branch are retired after canonical `develop` absorbs the fix.
7. Manager prompt build, worker prompt build, and post-cycle runtime handling all agree on the same structured exit-contract contract, so manager/worker intent is machine-checkable instead of inferred from free text.
8. Cleanup-governance handoff workers selected on canonical `develop` remain launchable until they finish or explicitly hand back the external cleanup surfaces named in their worker prompt, rather than being auto-settled immediately after launch.
9. Canonical `develop` no longer accepts manager `stop_ai` as a lawful terminal outcome while any runtime-owned expected-running worker is still down/degraded; runtime must continue with repair/recovery until that worker is resolved or explicitly reclassified.
10. Canonical `develop` no longer loops on fresh worker restarts that inherit a stale fallback tool; a relaunched expected-running worker must recover with the delegated `selected_tool` and continue the same owner followthrough.
11. Canonical `develop` no longer accepts `delegate_workers` as a lawful manager outcome when every advertised worker prompt is already non-launchable; runtime must force same-session repair instead of recording an impossible delegation.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-supersedes-queued-prompt-with-manager-continuity`
- `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- `bash docs/system/workspace/scripts/tests/test-freely-tool-runtime-failure-skips-known-unavailable-kiro`
- `bash docs/system/workspace/scripts/tests/test-freely-develop-push-attempt`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-cleans-disposable-pycache-residue`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-inherits-tool-adapter`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-stale-existing-worktree-blocked`
- `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-stale-target-worktree-blocked`
- `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
- `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-invalid-forces-resume`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-stop-ai`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-requires-launchable-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-blocks-stop-with-unresolved-worker`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-restart-reapplies-selected-tool-from-verification-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-governance-retirement-worker-directive`
- `bash docs/system/workspace/scripts/tests/test-freely-retire-ready-merged-cleanup-handoff-not-reclaimed`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-projection-without-state`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-retire-ready-merged-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-absorbed-merged-dirty-worker`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
- `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `./bin/governance-check`
- canonical `develop` self-host replay: `./bin/freely daemon start`
- `git worktree list`

## Completion

- `docs/pre-brainstorms/20260421-1200--runtime-daemon-self-loop-followthrough/brainstorms.md`
- `docs/pre-brainstorms/20260421-1200--runtime-daemon-self-loop-followthrough/candidates.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-runtime-daemon-self-loop-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
- `docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
- `docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
- `docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
- `docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
- `docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
- `docs/system/workspace/scripts/tests/test-freely-sync-tooling-stale-target-worktree-blocked`
- `docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-invalid-forces-resume`
- `docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-stop-ai`
- `docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-requires-launchable-prompt`
- `docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
- `docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`
- `docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-blocks-stop-with-unresolved-worker`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`
- `docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`
