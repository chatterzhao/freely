# Issue: runtime-daemon-self-loop-followthrough-governance

- issue_id: `I-20260421-1200-A`
- title: `Runtime daemon self-loop followthrough governance`
- phase_state: `done`
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
3. Keep current manager continuity formats runtime-consumable by parsing both direct `## Worker Delegation` handoffs and `## Queue State` `worker_prompts:` handoffs into concrete worker prompt launches.
4. Route `merged-clean` / `retire-ready` worker lanes to cleanup followthrough retirement instead of runtime recovery, and let cleanup reclaim stale recorded ownership for those lanes.
5. Treat merged develop-absorbed worker lanes that are dirty only in owner evidence surfaces as cleanup/promotion followthrough, not as relaunchable edit workers.
6. Add focused regressions for orphan precheck residue, unexpected daemon `TERM`, current-format continuity consumption, queue-state worker handoff consumption, and retire-ready merged-worker retirement routing.
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
27. Keep reconnect-in-progress runtime output on the bounded execution-network retry path until the current tool actually exits; `ERROR: Reconnecting... x/5` must not trigger monitor-level early kill or immediate cross-tool switch.
28. When one bounded cross-tool recovery episode exhausts every fallback tool, restore the original tool selection for the next retry instead of leaving the project pinned to the last failed fallback.
29. Preserve `manager_exit_contract_repair` / `worker_exit_contract_repair` relaunches across supervisor restarts and same-process relaunch loops, so repair rounds resume the same tool context instead of falling back to a fresh `initial_start` patrol.
30. Ignore the known benign Codex startup line `failed to refresh available models: timeout waiting for child process to exit` so monitor/runtime do not treat an otherwise successful manager patrol round as `tool_runtime_failure`.
31. Keep a newly started daemon manager alive while startup is still between `L010 supervisor_started` and `L020 prompt_build_begin`, so pre-prompt recovery/fleet work does not get misclassified as an idle supervisor restart.
32. When runtime classifies tool failures as network, proxy, auth, or subscription seams, log explicit operator guidance that points at relay/base_url reachability, proxy mode, and provider access rather than leaving canonical self-host replay with an opaque retry loop.
33. When Codex exits after exhausting its own reconnect loop with upstream `502 Bad Gateway` evidence, monitor/runtime must persist that outcome as execution-network failure truth instead of collapsing it into generic `tool_runtime_failure`.
34. Fresh startup patrol must treat the delegated-continuation freshness floor as the later of continuity truth and the explicit manager operator-stop boundary, so pre-stop delegated continuation handoffs stay historical after `daemon stop` while newer post-stop handoffs remain eligible.
34. When manager materializes a cleanup followthrough worker prompt from continuity rather than reusing an existing prompt file, it must carry the authoritative `selected_tool` so stale retained cleanup worktrees do not relaunch on obsolete local tool config.
35. Treat a Codex resume target as valid only when its rollout/session jsonl evidence is non-empty, so zero-byte persisted session files cannot send canonical cleanup followthrough back into `thread/resume failed: empty session file`.
36. When manager exit-contract replay resolves to `resume_manager` while continuity already targets cleanup followthrough, runtime must run that cleanup followthrough before relaunch so canonical replay cannot stay pinned on the same retained merged lane.
37. If cleanup followthrough fails on that `resume_manager` path, runtime must preserve exact blocker truth and same-owner repair handoff instead of silently degrading into another generic patrol/resume loop.
38. Treat Codex OAuth refresh request-send failures against `https://auth.openai.com/oauth/token` as bounded transport/network failures when the evidence is request delivery failure rather than explicit auth rejection, so runtime recovery stays on `execution_network_*` instead of widening to generic `tool_runtime_failure`.
39. Preserve the auth boundary for that same Codex OAuth refresh path: explicit auth denial such as `401 Unauthorized` remains non-network and must not enter the device-network recovery path.
40. When project proxy mode is `explicit`, resolve proxy fields with project-over-global precedence instead of treating blank project values as authoritative empties; an empty project explicit block must not mask valid global explicit proxy values and force false `proxy_config_invalid`.
41. Keep project-level worktree summary pipe-safe during daemon/live-status patrol so runtime hygiene and startup followthrough cannot fail just because a downstream consumer closes stdout early.
42. Treat explicit `daemon stop` as an operator-stop freshness boundary for startup patrol, so a new scan after restart can supersede pre-stop manager continuity instead of re-anchoring on stale cleanup queue truth.
43. Let manager delegation and launch treat a prompt-targeted missing sibling worktree as materializable when its branch/worktree headers stay within the governed `*-worktrees` root, and do not retire a merged-tip worker lane while authoritative continuity still carries active `edit` or `promotion` ownership for that lane.
44. Keep `## Queue State` `worker_prompts:` continuity launchable for the same runtime control plane that validated `delegate_workers`, so manager cannot consume a lawful handoff contract without ever materializing queued/launched worker state.
45. Preserve `LAST_ENTRYPOINT_MODE` when `monitor-ai-cli.sh` writes launch-in-flight workcell truth, so daemon-owned manager recovery cannot silently degrade into foreground `start --project`.
46. Derive the effective runtime role for a delegated target from authoritative worker verification-contract truth before falling back to branch/worktree role hints, so manager-launched worker lanes under `test-pre-merge-*` or other manager-default names do not relaunch as manager control planes.
47. Reclaim a delegated target that stays at `LAST_EXIT_REASON=starting` beyond the existing startup grace while no valid `ai.pid` ever appears, including clearing stale supervisor/watchdog residue so the parent manager can legally release and relaunch that worker slot.
48. Reconcile launched-worker liveness on the dispatch-critical path before manager concludes no launchable worker prompt remains, so stale `LAUNCHED_WORKER_PROMPTS` / `ACTIVE_RUNNING_WORKER_COUNT` state from dead or never-up targets cannot suppress the next lawful delegation.
49. Keep manager supervision alive while runtime is between-round relaunch grace or waiting on an expected-running worker, so a lawful manager/worker handoff loop is not misclassified as idle-supervisor drift and stopped prematurely.
50. Treat terminal worker exit-contract truth as authoritative for recovery/cleanup followthrough: terminal workers must not be relaunched, cleanup must record their terminal evidence, clear stale launch state, normalize authoritative worktree paths, and reset discovery caches before the next patrol/closeout decision.
51. When the latest authoritative worker prompt supersedes an older terminal `worker_handoff_needed` exit contract for the same lane, manager launch must absorb that terminal handoff and relaunch the current followthrough prompt instead of skipping the lane forever behind stale terminal truth.

## Non-Goals

1. Do not redesign scan architecture or live-status semantics in this owner.
2. Do not weaken Freely's freedom of action or task autonomy.
3. Do not reopen unrelated runtime/watchdog architecture owners.
4. Do not stop at "daemon process stayed alive once"; the final acceptance remains autonomous end-to-end self-work on `develop`.

## Acceptance

1. Focused regressions cover the orphaned precheck residue and unexpected daemon `TERM` seams.
2. Focused regressions also prove runtime consumes current `## Worker Delegation` and `## Queue State` continuity handoffs, then retires merged-clean blocker worktrees instead of re-recovering them.
3. `./bin/pretests-gate` and `./bin/governance-check` pass for this owner.
4. Guarded replay from `feature/runtime-daemon-self-loop-blocker-20260421` through `test-pre-merge-20260421-runtime-self-loop-blocker` into `develop` succeeds lawfully.
5. On canonical `develop`, `freely daemon start` selects at least one task, completes it to the current-project success standard, closes the corresponding temporary worktree, and proceeds to another task.
6. The temporary blocker worktree and disposable test-pre-merge branch are retired after canonical `develop` absorbs the fix.
7. Manager prompt build, worker prompt build, and post-cycle runtime handling all agree on the same structured exit-contract contract, so manager/worker intent is machine-checkable instead of inferred from free text.
8. Cleanup-governance handoff workers selected on canonical `develop` remain launchable until they finish or explicitly hand back the external cleanup surfaces named in their worker prompt, rather than being auto-settled immediately after launch.
9. Canonical `develop` no longer accepts manager `stop_ai` as a lawful terminal outcome while any runtime-owned expected-running worker is still down/degraded; runtime must continue with repair/recovery until that worker is resolved or explicitly reclassified.
10. Canonical `develop` no longer loops on fresh worker restarts that inherit a stale fallback tool; a relaunched expected-running worker must recover with the delegated `selected_tool` and continue the same owner followthrough.
11. Canonical `develop` no longer accepts `delegate_workers` as a lawful manager outcome when every advertised worker prompt is already non-launchable; runtime must force same-session repair instead of recording an impossible delegation.
12. Canonical `develop` no longer treats `ERROR: Reconnecting... x/5` as sufficient evidence to live-kill Codex or switch tools before the tool exhausts its own retry loop; pure reconnect evidence stays on the bounded execution-network retry path.
13. Canonical `develop` restores the original tool after one bounded fallback episode exhausts every configured fallback, so the next retry starts from truthful project preference instead of stale last-fallback state.
14. Canonical `develop` no longer re-enters `initial_start` after `manager_exit_contract_invalid`; repair handoff rounds must reuse the recorded resume target and stay on the same repair contract path until a valid exit contract exists.
15. Canonical `develop` surfaces explicit runtime diagnostics for execution-network, proxy-config, auth, and Kiro subscription failures, including the effective proxy mode and the relevant config-file path, so supervision can distinguish network-path bugs from provider/quota misconfiguration during self-host replay.
16. Canonical `develop` no longer routes exhausted Codex reconnect `502 Bad Gateway` exits into `tool_runtime_failure`; the bounded execution-network retry path remains authoritative for that failure family.
17. Canonical `develop` no longer materializes cleanup followthrough worker prompts without `selected_tool`; retained cleanup worktrees with stale local config must be corrected to the continuity-selected tool before launch.
18. Canonical `develop` no longer attempts `codex exec resume` against a zero-byte persisted rollout file; empty-session resume evidence must fall back to fresh launch/handoff so cleanup governance can keep progressing.
19. Canonical `develop` no longer lets `EXIT_KIND=resume_manager` bypass an already-selected cleanup followthrough; retained cleanup closeout must run before manager relaunch.
20. Canonical `develop` now records `manager_exit_contract_cleanup_followthrough_failed` plus repair-handoff truth whenever that cleanup-followthrough resume path breaks, so self-host replay stops on exact blocker evidence instead of an opaque relaunch loop.
21. Canonical `develop` no longer collapses Codex OAuth refresh request-send failures into `tool_runtime_failure`; those transport failures stay on the bounded `execution_network_transient` / `execution_network_persistent` path.
22. Canonical `develop` still keeps explicit Codex OAuth refresh auth denial such as `401 Unauthorized` off the network path, so auth noise does not masquerade as device-network instability.
23. Canonical `develop` no longer loops on `proxy_config_invalid` when project config sets `FREELY_NETWORK_PROXY_MODE="explicit"` but leaves proxy values blank while global config still carries valid explicit proxy settings; field-level resolution must preserve the usable global proxy and let daemon self-work continue.
24. Canonical `develop` no longer risks aborting patrol/log consumers with `printf: write error: Broken pipe` while computing multi-worktree summary during daemon/live-status followthrough.
25. Canonical `develop` can take a scan/continuity-selected worker prompt that points at a missing governed sibling worktree, materialize that worktree lawfully, launch the worker, and keep a merged-tip authoritative `edit` lane out of retire-ready cleanup until its prompt ownership is actually settled.
26. Canonical `develop` no longer records `EXIT_KIND=delegate_workers` while `manager-worker-launch-state.env` still shows `generated/queued/launched=none` just because the selected continuity used `## Queue State` `worker_prompts:` instead of a direct `## Worker Delegation` block.
27. Canonical `develop` no longer re-consumes a pre-stop delegated continuation after fresh restart just because the stale continuity anchor was discarded; operator-stop freshness still fences off older delegated handoffs until newer post-stop continuity or newer post-stop delegated continuation arrives.
28. Canonical `develop` can recover cleanup followthrough from current-shape continuity that exposes only top-level `route_kind` plus inline `worker_prompt:` references, by inheriting authoritative verification metadata from the retained target worker lane instead of looping on a nonlaunchable hygiene prompt.
29. Canonical `develop` no longer loses daemon control-plane ownership while AI launch is in flight; if watchdog must relaunch after that state write, it still chooses `daemon-run --project` rather than materializing a foreground `start --project`.
30. Canonical `develop` can also recover cleanup followthrough when the latest continuity exposes retained-lane prompt truth only through `## Dispatch State` `worker_prompt_paths:` and the retained worker has no authoritative local prompt left, by materializing a fresh cleanup prompt from the continuity-carried source prompt metadata without treating the merged-lane `edit` prompt itself as still launchable.
31. Canonical `develop` no longer lets delegated worker targets under manager-default worktree names boot manager-mode control planes just because branch/worktree role hints say `manager`; authoritative worker verification truth now decides the effective runtime role for that lane.
32. Canonical `develop` now reclaims delegated targets that stay stuck in `starting` past startup grace without ever producing `ai.pid`, releases their recorded launch slot, and allows manager to relaunch or advance instead of rewriting the same worker prompt forever.
33. Canonical `develop` now performs target-liveness reconciliation before delegation/no-launchable-worker decisions, so stale launched-worker state from dead or never-up targets cannot keep `ACTIVE_RUNNING_WORKER_COUNT` pinned and block the next lawful worker dispatch.
34. Canonical `develop` keeps manager supervision alive while runtime is waiting on an expected-running worker or inside between-round relaunch grace, so manager does not stop in the middle of an otherwise-correct manager/worker loop.
35. Canonical `develop` treats terminal worker exit-contract truth plus cleanup followthrough as authoritative closeout state, which prevents stale terminal workers from being relaunched and lets cleanup clear launch/discovery residue before the next patrol and retirement decision.
36. Canonical `develop` no longer lets a stale terminal `worker_handoff_needed` contract suppress the same lane's newer authoritative followthrough prompt; runtime must absorb that terminal handoff, clear the stale contract, and relaunch the current lane so review/cleanup/retirement can keep progressing.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-ignores-pre-stop-delegated-continuation-after-operator-stop`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-ignores-pre-stop-delegated-intake-after-operator-stop`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-supersedes-queued-prompt-with-manager-continuity`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
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
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autodelegates-cleanup-from-worker-verification-truth`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-defers-codex-reconnect-until-retries-exhaust`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-ignores-codex-model-refresh-timeout`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-pre-prompt-startup`
- `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
- `bash docs/system/workspace/scripts/tests/test-freely-runtime-failure-guidance`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-classifies-codex-reconnect-exhaustion-as-network-failure`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-classifies-codex-oauth-refresh-request-error-as-network-failure`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-ignores-codex-apikey-oauth-refresh-401`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-429-rate-limit`
- `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-resolver`
- `bash docs/system/workspace/scripts/tests/test-freely-worktree-summary-multi-worktree`
- `bash docs/system/workspace/scripts/tests/test-freely-worktree-summary-tolerates-closed-pipe`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-allows-materializable-missing-worktree`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-repairs-existing-stale-worktree`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-materializes-missing-worktree`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-keeps-fresh-materialized-worker-with-authoritative-edit-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-runtime-cross-tool-recovery-remembers-failed-tools`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-avoids-initial-start`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-blocks-stop-with-unresolved-worker`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-restart-reapplies-selected-tool-from-verification-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-materialized-cleanup-worker-applies-selected-tool`
- `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-triggers-cleanup-followthrough`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-cleanup-followthrough-failure-materializes-blocker`
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
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-failure-recovery-preserves-daemon`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-active-stall-recovery-from-manager-watchdog`
- `bash docs/system/workspace/scripts/tests/test-freely-delegated-worker-starting-stuck-reclaim`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-reclaims-stale-starting-worker-slot`
- `bash docs/system/workspace/scripts/tests/test-freely-runtime-effective-worker-role-from-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-between-rounds-relaunch-grace`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-while-worker-active`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-workers-absorbs-terminal-handoff-followthrough`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-absorbs-terminal-handoff-followthrough`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-autonomous-existing-worktree-review-merge-retire-next-task-loop`
- `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `./bin/governance-check`
- canonical `develop` self-host replay: `freely daemon start`
- `git worktree list`

## 2026-04-25 Continuation Note: Post-L042 Followthrough Keepalive

- Real canonical `develop` replay advanced past the earlier `post-L041/pre-L042` finalize seam and started recording `L042 ai_cycle_finished`, but watchdog could still classify the same live manager supervisor as idle and emit `L223 manager_idle_supervisor_restart` before that supervisor finished exit-contract replay or wrote later terminal/followthrough truth.
- This remains inside `I-20260421-1200-A`. The architecture boundary is unchanged: manager/worker intent stays artifact-driven, runtime remains the middleman, and the defect is still watchdog lifecycle classification rather than task-selection policy or role taxonomy.
- The bounded fix is to treat same-supervisor `L042` as post-cycle followthrough-in-flight for a short authoritative grace window unless later `L090|L091|L092` truth has already been written.

## Completion

- `docs/pre-brainstorms/20260421-1200--runtime-daemon-self-loop-followthrough/brainstorms.md`
- `docs/pre-brainstorms/20260421-1200--runtime-daemon-self-loop-followthrough/candidates.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-runtime-daemon-self-loop-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260422-runtime-daemon-self-loop-followthrough-empty-codex-session-resume-verification.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-terminal-handoff-followthrough-absorb-verification.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-terminal-handoff-followthrough-absorb-premerge-verification.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-post-l042-followthrough-keepalive-verification.md`
- `docs/system/workspace/hooks/commit-msg.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
- `docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
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
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-defers-codex-reconnect-until-retries-exhaust`
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-ignores-codex-model-refresh-timeout`
- `docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
- `docs/system/workspace/scripts/tests/test-freely-runtime-failure-guidance`
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-classifies-codex-reconnect-exhaustion-as-network-failure`
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-429-rate-limit`
- `docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
- `docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`
- `docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-blocks-stop-with-unresolved-worker`
- `docs/system/workspace/scripts/tests/test-freely-worker-runtime-cross-tool-recovery-remembers-failed-tools`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`
- `docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`
- `docs/system/workspace/scripts/tests/test-freely-worker-active-stall-recovery-from-manager-watchdog`
- `docs/system/workspace/scripts/tests/test-freely-delegated-worker-starting-stuck-reclaim`
- `docs/system/workspace/scripts/tests/test-freely-manager-launch-path-reclaims-stale-starting-worker-slot`
- `docs/system/workspace/scripts/tests/test-freely-runtime-effective-worker-role-from-contract`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-between-rounds-relaunch-grace`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-while-worker-active`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-post-ai-cycle-finalize-grace`
- `docs/system/workspace/scripts/tests/test-freely-daemon-autonomous-existing-worktree-review-merge-retire-next-task-loop`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-worker-self-loop-recovery-verification.md`
