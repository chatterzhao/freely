# Verification: runtime-daemon-self-loop-followthrough-governance

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-21`
- verifier: `codex`

## Scope Verdict

- `PASS`: the blocker reproduced as a runtime/control-plane seam, not as a generic scan or task-selection defect.
- `PASS`: `project_has_authoritative_runtime_processes_for_user_precheck()` now requires supervisor truth instead of lone dispatcher/watchdog residue.
- `PASS`: daemon supervisor now ignores unexpected `TERM` without `stop.marker` and still records explicit daemon stop correctly.
- `PASS`: current manager continuity files that use `## Worker Delegation` now expose worker prompt paths to runtime launch and live-status truth.
- `PASS`: current manager continuity followthrough stays anchored across `resume` and `fresh_with_handoff`, so context compaction does not devolve into rewriting the same continuity instead of executing queued manager-owned work.
- `PASS`: retire-ready merged-clean blocker worktrees are now treated as cleanup-followthrough retirement targets instead of recoverable edit workers, and cleanup can reclaim stale recorded ownership for those lanes.
- `PASS`: merged develop-absorbed blocker lanes that remain dirty only in owner evidence surfaces are now treated as retire-ready followthrough instead of relaunchable edit workers.
- `PASS`: never-started worker branches are no longer misclassified as absorbed merged lanes just because their branch tip still equals an ancestor of `develop`; runtime now requires recorded worker state before treating a merged lane as already absorbed.
- `PASS`: when manager writes a newer manager-owned continuity with no worker prompt, runtime now lets that continuity supersede stale queued worker-prompt state instead of keeping an older queued prompt as the consumed truth.
- `PASS`: manager worker-launch fallback now rechecks whether a prompt still targets a launchable lane before reviving it, so the latest generated continuity cannot bypass retire-ready merged guards.
- `PASS`: expected-running worker recovery and global restart selection now both exclude absorbed merged worker lanes, even if an earlier bad recovery already left ordinary dirty files behind in that old worktree.
- `PASS`: once canonical replay proves `kiro-cli` hit monthly request exhaustion, runtime now persists that tool-unavailable truth and later auto-switch / manager bootstrap selection skips Kiro instead of routing immediately back into the same exhausted tool.
- `PASS`: after a successful guarded `develop` push followthrough, runtime now refreshes the local upstream tracking ref to the pushed `HEAD`, so manager/live-status do not keep reporting false `push_pending` solely because the remote-tracking ref remained stale.
- `PASS`: untracked runtime-only Python cache residue under `docs/system/workspace/scripts/runtime/__pycache__/` no longer keeps canonical `develop` or disposable premerge lanes artificially dirty during manager hygiene judgement; runtime now auto-cleans that residue before dirty-state evaluation.
- `PASS`: Codex resume launches now omit `--add-dir`, matching the current `codex exec resume` CLI contract and preventing manager continuity resume loops from crashing with `ai_exit_rc_2`.
- `PASS`: worker bootstrap now rejects stale target paths outside the authoritative worktree fleet, requires missing-config `freely init` to succeed before any follow-on config mutation, and carries inherited `--accept-default-autonomy` through that runtime-owned bootstrap path.
- `PASS`: `sync-tooling` now also skips stale directories that still sit under the managed `*-worktrees` root but no longer belong to the authoritative worktree fleet, so runtime cannot rewrite `.freely/config.env` / `.githooks` into absorbed or deleted premerge lanes.
- `PASS`: manager and worker prompt builds now publish explicit structured exit-contract directives, so the role-specific closeout contract is no longer implicit free text.
- `PASS`: runtime now validates manager/worker exit contracts after `ai_exit_rc_0`, routes that handling through one unified dispatcher, and reuses the exact current resume target when it must repair a missing or malformed contract.
- `PASS`: manager `EXIT_KIND=stop_ai` is now rejected whenever authoritative supervision still shows a runtime-owned expected-running worker down/degraded; runtime writes a repair handoff instead of legally ending autonomy while recovery remains unresolved.
- `PASS`: `monitor-ai-cli` no longer treats pure `ERROR: Reconnecting... x/5` output as immediate network-failure kill evidence, so Codex keeps its own reconnect/backoff loop until the current process actually exits.
- `PASS`: post-exit runtime classification still maps pure reconnect evidence to bounded `execution_network_*` recovery, while hard failure evidence such as Codex 429 remains immediate monitor-level kill/switch-worthy.
- `PASS`: one bounded fallback episode now preserves attempted-tool memory and restores the episode origin tool after every configured fallback fails, instead of leaving project selection pinned to the last failed fallback.
- `PASS`: focused regressions cover manager-invalid repair, manager-stop, worker-invalid repair, worker-done stop, worker prompt directive injection, cleanup worker materialization, and retained-merged cleanup followthrough coexistence.
- `PASS`: cleanup-governance handoff workers that still have external cleanup surfaces are now explicitly protected from merged-lane reclaim/settle, and a focused regression proves runtime leaves them launchable instead of auto-closing them as `retire_ready_merged_worker`.
- `PASS`: the merged-lane guard now resolves that authoritative cleanup prompt through `worker-verification-contract.env` when the target worktree no longer has a local `prompt-*.txt`, which matches the canonical `develop` reproduction.
- `PASS`: the same guard now prefers `worker-verification-contract.env` `SOURCE_PROMPT_FILE` over a later worker-local reentry prompt, so bootstrap prompts cannot mask the real cleanup-handoff scope during merged-lane settle/reclaim.
- `PASS`: focused regressions and nearby daemon/live-status coverage passed on the guarded source lane, and the protected test lane replay still passed after the retirement followthrough repair.
- `PENDING`: the final protected-branch acceptance remains canonical `develop` self-host execution where Freely finishes one task to the current-project success standard, closes the worktree, and continues to the next task.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
6. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
10. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
11. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
12. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
13. `./bin/governance-check`
14. `bash docs/system/workspace/scripts/tests/test-freely-merged-clean-worker-handoff-guard`
15. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
16. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
17. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
18. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
19. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
20. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-retire-ready-merged-prompt`
21. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-absorbed-merged-dirty-worker`
22. `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
23. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-projection-without-state`
24. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
25. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-supersedes-queued-prompt-with-manager-continuity`
26. `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
27. `bash docs/system/workspace/scripts/tests/test-freely-tool-runtime-failure-skips-known-unavailable-kiro`
28. `bash docs/system/workspace/scripts/tests/test-freely-tool-runtime-failure-uses-unified-auto-recovery-path`
29. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
30. `bash docs/system/workspace/scripts/tests/test-freely-develop-push-attempt`
31. `bash docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
32. `bash docs/system/workspace/scripts/tests/test-freely-live-status-cleans-disposable-pycache-residue`
33. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
34. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-inherits-tool-adapter`
35. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-stale-existing-worktree-blocked`
36. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
37. `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-stale-target-worktree-blocked`
38. `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
39. `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`
40. `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-invalid-forces-resume`
41. `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-stop-ai`
42. `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-blocks-stop-with-unresolved-worker`
43. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
44. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`
45. `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`
46. `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`
47. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-retire-ready-merged-prompt`
48. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-governance-retirement-worker-directive`
49. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
50. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
51. `bash docs/system/workspace/scripts/tests/test-freely-retire-ready-merged-cleanup-handoff-not-reclaimed`
52. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-defers-codex-reconnect-until-retries-exhaust`
53. `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
54. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-429-rate-limit`
55. `bash docs/system/workspace/scripts/tests/test-freely-worker-runtime-cross-tool-recovery-remembers-failed-tools`

## 2026-04-21 23:12 PDT Manager Stop Guard Verification

- `FAIL`: canonical `develop` replay still allowed manager to legally emit `EXIT_KIND=stop_ai` even when authoritative supervision truth showed a runtime-owned expected-running worker had failed and remained unresolved, so autonomy could terminate before recovery/cleanup followthrough completed.
- `PASS`: manager exit-contract directives now surface the unresolved expected-running-worker count, and post-cycle runtime handling blocks `stop_ai` whenever that count is non-zero by writing a same-session repair handoff instead.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-blocks-stop-with-unresolved-worker`
- `PASS`: `./bin/governance-check`
- `PENDING`: absorb this stop-guard repair into canonical `develop`, then rerun daemon self-host acceptance until Freely completes one real task, lawfully closes the corresponding worktree, and advances to the next task instead of stopping at the first unresolved worker failure.

## 2026-04-21 18:15 PDT Worker Bootstrap Guard Followthrough

- `FAIL`: canonical self-host replay exposed one more bounded launcher seam after the Codex resume repair: a stale worker target could still enter missing-config bootstrap, call `freely init` without inherited default-autonomy consent, ignore that init failure, and continue mutating `config.env` for a path that no longer belonged to the authoritative fleet.
- `PASS`: runtime now gates worker bootstrap on authoritative worktree membership, requires missing-config init success before post-init config writes continue, and carries `--accept-default-autonomy` during that runtime-owned bootstrap path.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-inherits-tool-adapter`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-stale-existing-worktree-blocked`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-stale-target-worktree-blocked`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`
- `PENDING`: merge this same-owner followthrough into canonical `develop`, then rerun daemon self-host acceptance until one real task completes, the temporary worktree is lawfully retired, and the daemon advances to another task.

## 2026-04-21 08:45 PDT Kiro Availability Memory Followthrough

- `FAIL`: canonical `develop` self-host replay no longer stalled on stale manager continuity, but after a later `cc` `tool_runtime_failure` the active runtime still selected `kiro-cli` even though that same replay had already recorded `kiro_monthly_request_limit`; Kiro availability was classified correctly at failure time, but the candidate picker had no persisted memory of that unavailability.
- `PASS`: runtime now writes a Kiro tool-availability state file when monthly-limit truth is observed, preserves a reset hint from the CLI transcript when available, falls back to the next calendar-month boundary when the transcript omits the explicit reset line, and skips the cached-unavailable Kiro candidate during later cross-tool recovery.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-tool-runtime-failure-skips-known-unavailable-kiro`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-tool-runtime-failure-uses-unified-auto-recovery-path`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
- `PENDING`: replay the guarded merge into canonical `develop`, then resume self-host daemon validation until one real task completes, the corresponding worktree is lawfully closed, and the daemon proceeds to another task.

## 2026-04-21 09:25 PDT Develop Push Followthrough Tracking Refresh

- `FAIL`: canonical `develop` self-host replay showed the guarded merge push had already succeeded, but later manager patrols still surfaced `develop_push_followthrough_state=push_pending` because local `origin/develop` tracking truth stayed behind `HEAD`; this false gating fact kept protected push followthrough open and blocked later cleanup sequencing.
- `PASS`: `develop-push attempt` now refreshes the local upstream tracking ref to the pushed `HEAD` immediately after success, so later `develop_push_followthrough_snapshot_for_project()` returns `clean` instead of replaying stale ahead-count truth.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-develop-push-attempt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
- `PENDING`: replay the guarded merge into canonical `develop`, then resume daemon self-host validation until one real task completes, the relevant worktree is retired, and the daemon advances to another task.

## 2026-04-21 16:45 PDT Disposable Pycache Hygiene Followthrough

- `FAIL`: canonical `develop` self-host replay still looped after push truth cleared because manager kept treating untracked `docs/system/workspace/scripts/runtime/__pycache__/` residue in canonical `develop` and the disposable absorbed-merged premerge lane as durable cleanup blockers, so no real replay/closeout work ever started.
- `PASS`: runtime dirty-state and startup prompt hygiene now auto-clean untracked disposable Python cache residue (`__pycache__` / `.pyc`) before lane cleanliness is judged.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-live-status-cleans-disposable-pycache-residue`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-develop-push-attempt`
- `PENDING`: rerun canonical `develop` daemon self-host acceptance and confirm the repaired hygiene gate lets manager advance into a real task, retire the corresponding temporary worktree, and continue.

## 2026-04-21 05:25 PDT Recheck

- `PASS`: reran the full feature-local verification set in `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-daemon-self-loop-blocker` and the blocker did not reproduce.
- `PASS`: no source changes were required after the recheck; the lane remains guarded-promotion ready.
- `PENDING`: canonical `develop` replay is still the only remaining blocker to retire this lane.

## 2026-04-21 05:29 PDT Recheck

- `PASS`: reran every required feature-local command plus `./bin/pretests-gate` and `./bin/governance-check`; all passed in `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-daemon-self-loop-blocker`.
- `PASS`: the blocker still does not reproduce, and no additional source edits were needed in this lane.
- `PASS`: guarded promotion remains ready from the feature worktree evidence perspective.
- `PENDING`: canonical `develop` replay is still the only remaining blocker to retire this lane.

## 2026-04-21 05:33 PDT Fresh-Session Recheck

- `PASS`: reran the same feature-local verification set in a fresh session, including `./bin/pretests-gate` and `./bin/governance-check`; all passed again in `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-daemon-self-loop-blocker`.
- `PASS`: the blocker still does not reproduce, and no additional source edits were required.
- `PASS`: guarded promotion remains ready from the feature worktree evidence perspective.
- `PENDING`: canonical `develop` replay is still the only remaining blocker to retire this lane.

## 2026-04-21 05:36 PDT Failure Reproduction

- `FAIL`: a fresh-session rerun of `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch` reported `expected exactly one daemon-run process before reuse, found 2`.
- `FAIL`: this meant the earlier "already green" judgement was stale for current-session truth; the lane still needed a narrow repair before guarded promotion.

## 2026-04-21 05:42 PDT Narrow Fix Recheck

- `PASS`: hardened `docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch` so it waits for a stable single `daemon-run` snapshot before asserting reuse, instead of racing two separate `ps` snapshots during daemon bootstrap.
- `PASS`: reran that regression three consecutive times; each run showed `supervisor_attach_reuse` and no extra steady-state `daemon-run` process.
- `PASS`: reran the full feature-local verification set, including `./bin/pretests-gate` and `./bin/governance-check`; all passed in `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-daemon-self-loop-blocker`.
- `PASS`: guarded promotion is ready again from the feature-worktree evidence perspective.
- `PENDING`: canonical `develop` replay is still the only remaining blocker to retire this lane.

## 2026-04-21 05:47 PDT Fresh-Session Verification

- `PASS`: reran the same full feature-local verification chain in a new check window, including `./bin/pretests-gate` and `./bin/governance-check`; all commands passed again in `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-daemon-self-loop-blocker`.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch` still reports supervisor reuse without an extra steady-state `daemon-run` process, so the blocker does not reproduce on current-session truth.
- `PASS`: no additional source changes were required after the narrow regression hardening already present in this lane.
- `PASS`: guarded promotion remains ready from the feature-worktree evidence perspective.
- `PENDING`: canonical `develop` replay is still the only remaining blocker to retire this lane.

## 2026-04-21 05:54 PDT Worker Continuation Verification

- `PASS`: reran the owner-required feature-local regression and gate set from this worker continuation, including the daemon reuse regression, continuity-consumption regressions, retirement followthrough regressions, `./bin/pretests-gate`, and `./bin/governance-check`; all commands passed in `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-daemon-self-loop-blocker`.
- `PASS`: the blocker still does not reproduce on current worktree truth; `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch` again reported supervisor reuse without an extra steady-state `daemon-run` process.
- `PASS`: no additional implementation edits were required during this continuation beyond the already-present regression hardening in `docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`.
- `PASS`: guarded promotion remains ready now from the feature-worktree evidence perspective.
- `PENDING`: canonical `develop` replay is still the remaining blocker before retirement / cleanup closeout.

## 2026-04-21 06:12 PDT Worker Continuation Verification

- `PASS`: reran the full owner-required feature-local regression and gate chain again from this worker continuation, including the daemon reuse regression, orphaned precheck guard, daemon detach/status replay, unexpected TERM replay, watchdog survival, continuity-consumption regressions, retirement followthrough regressions, `./bin/pretests-gate`, and `./bin/governance-check`; all commands passed in `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-daemon-self-loop-blocker`.
- `PASS`: the blocker still does not reproduce on current worktree truth; `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch` again reported supervisor reuse without an extra steady-state `daemon-run` process.
- `PASS`: no additional implementation edits were required during this continuation beyond the already-present regression hardening in `docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`.
- `PASS`: guarded promotion remains ready now from the feature-worktree evidence perspective.
- `PENDING`: canonical `develop` replay remains the only blocker before retirement / cleanup closeout.

## 2026-04-21 07:18 PDT Direct Worker Delegation Followthrough

- `FAIL`: canonical `develop` self-host replay wrote `manager-continuity-20260421-070449.md` with the current direct `## Worker Delegation` handoff shape, but runtime parsed zero generated worker prompts from that continuity and therefore relaunched manager instead of consuming the delegated worker prompt.
- `PASS`: narrowed the parser so direct `prompt_path` entries under `## Worker Delegation` are treated as launchable by default rather than requiring an intermediate `launchable_queue` subsection.
- `PASS`: updated the current-format continuity-consumption and manager worker-launch regressions to use the same direct handoff shape that canonical self-host just produced.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
- `PENDING`: replay the guarded promote and rerun canonical `develop` self-host acceptance to prove the worker now launches and the lane can actually advance toward completion / retirement.

## Implementation Decision Note

- decision: `Keep the owner narrow: preserve the runtime/control-plane repair, harden the daemon reuse regression around stable steady-state truth, and teach runtime to consume the manager's current direct Worker Delegation handoff shape instead of requiring an older subsection wrapper.`
- why_this: `Fresh-session evidence first showed the lane was not honestly green because the reuse regression could fail on a transient process-count race even when runtime attach/reuse behavior was correct. Canonical self-host replay then showed one more bounded seam: the manager wrote a direct Worker Delegation prompt_path, but the parser only recognized prompt_path after an explicit launchable_queue subsection, so post-cycle worker launch treated the continuity as prompt-empty. Tightening the regression and aligning parser consumption with the manager-written handoff shape fixes the real blocker without reopening broader architecture.`
- alternatives_considered: `Treat the transient duplicate snapshot as a proven product relaunch defect without first proving steady-state duplication; weaken the daemon reuse assertion to stop checking daemon-run cardinality at all; force the manager to keep emitting the older launchable_queue wrapper instead of consuming the current direct handoff shape; reopen scan/live-status architecture instead of fixing the bounded continuity-consumption seam.`
- boundary_non_goals: `No scan-architecture rewrite, no live-status redesign, no reduction in Freely's autonomous execution authority.`
- residual_risk: `The remaining risk is only the final canonical develop self-host acceptance, which still must prove end-to-end autonomous continuation after one completed task and lawful worktree retirement.`

## 2026-04-21 07:47 PDT Implementation Decision Note

- decision: `Keep the same owner and harden the manager followthrough execution contract instead of opening a new scan/live-status architecture lane.`
- why_this: `Canonical develop replay proved the next blocker was not task selection itself. Manager already picked the right followthrough, but after context compaction the runtime prompt lost its anchor to the current continuity and rewrote continuity again. The same repair lane also showed launch gating was using a pure git-ancestry shortcut that treated never-started worker branches as already absorbed merged lanes. Extending the current continuity anchor to `fresh_with_handoff` and requiring recorded worker state before classifying a merged worker as absorbed fixes the real control-plane seams without weakening autonomy.`
- alternatives_considered: `Teach Freely to rescan broadly after every compaction instead of honoring the current continuity anchor; keep the old absorbed-merged shortcut and special-case individual tests; add a new lifecycle index or prompt registry just to recover the current followthrough anchor.`
- boundary_non_goals: `No broad scan-architecture rewrite, no live-status redesign, no hardcoded task picking, and no reduction in Freely's freely working behavior.`
- residual_risk: `Canonical develop still has to prove the repaired manager can finish one task to the current-project success standard, close the temporary worktree, and continue to the next task before this owner can be closed.`

## 2026-04-21 08:31 PDT Implementation Decision Note

- decision: `Let manager-authored no-worker continuity supersede stale queued prompt state, but keep the older prompt-preservation exception only for runtime-seeded startup stubs and runtime fallback continuity.`
- why_this: `Canonical develop replay showed the previous repair was still not enough: manager chose the correct cleanup-only followthrough and wrote a new continuity, but `manager_worker_launch_state.env` kept an older queued worker prompt and older consumed continuity. The next `fresh_with_handoff` round therefore re-entered startup patrol semantics instead of advancing the already-selected manager-owned task. The true boundary is not “newer continuity with no prompt” in general; runtime-seeded startup stubs are intentionally allowed to preserve older unconsumed prompts, while manager-authored completion/cleanup continuity must advance the consumed truth.`
- alternatives_considered: `Always preserve the older launchable prompt whenever a newer continuity has no worker prompt; always supersede older prompts for any newer no-worker continuity including startup stubs; add a separate index file just to track manager continuity supersession.`
- boundary_non_goals: `No new index layer, no broad scan redesign, and no weakening of the existing startup-stub prompt-preservation behavior.`
- residual_risk: `The remaining risk is still only the final canonical develop daemon replay: Freely must now prove it can consume the manager-owned cleanup continuity, finish a task to the current-project success standard, and continue to the next task.`

## 2026-04-21 23:10 PDT Ordinary Manager Stall Recovery Verification

- `FAIL`: canonical `develop` self-host replay moved beyond the retired absorbed-cleanup lane, but a fresh ordinary manager `codex` prompt could still hang indefinitely with no delegated continuation, no pending intake, and no new runtime artifacts; the existing recovery contract only recognized pending-intake and delegated-continuation stall shapes, so the manager could remain active without making autonomous progress.
- `PASS`: added a narrow third manager stall classification for ordinary prompts that show no pending intake, no delegated continuation handoff, and no cycle-log progress past the existing stall threshold; recovery still reuses the same local continuation reentry path rather than inventing a new repair flow.
- `PASS`: kept the delegated-supervision boundary intact by excluding delegated-continuation prompts and pending-intake prompts from the new classifier, so active-worker quiet periods still remain idle-safe.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery-without-runtime-progress`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-stall-recovery`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-quiet-period-does-not-recover`
- `PENDING`: guarded promote into canonical `develop`, then rerun the daemon self-host acceptance until Freely proves it can complete one task, retire that temporary lane, and continue to a second task without hanging on an ordinary manager prompt.

## 2026-04-21 23:35 PDT Worker Restart Selected-Tool Verification

- `FAIL`: canonical `develop` self-host replay relaunched the down cleanup worker from fresh runtime state, but the new worker inherited `tool=cc-use-codex-cli` from fallback state instead of the delegated prompt's `selected_tool=codex`; that immediately reproduced `tool_runtime_failure` and prevented the same owner followthrough from completing.
- `PASS`: runtime now resolves the authoritative delegated tool from `worker-verification-contract.env` `SOURCE_PROMPT_FILE` and reapplies that `selected_tool` before a fresh worker restart launches.
- `PASS`: the new restart path preserves the delegated prompt contract across failure recovery instead of reviving whichever fallback tool the previous failed attempt left behind.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-restart-reapplies-selected-tool-from-verification-contract`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-applies-selected-tool`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-tool-runtime-failure-uses-unified-auto-recovery-path`
- `PASS`: `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-manager-exit-contract-expected-worker-guard --issue docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `PASS`: `./bin/governance-check`
- `PENDING`: guarded promotion into canonical `develop` and final self-host replay still remain required before this owner can close.

## 2026-04-22 00:44 PDT Non-Launchable Delegate Contract Verification

- `FAIL`: canonical `develop` self-host replay showed one more exit-contract/control-plane mismatch: manager generated only a cleanup prompt for an already absorbed `retire_ready` merged worker lane, wrote `EXIT_KIND=delegate_workers`, and runtime accepted that contract even though the subsequent worker-launch gate would refuse to launch the same prompt.
- `PASS`: `validate_manager_exit_contract_for_project()` now treats `delegate_workers` as invalid unless at least one prompt in `WORKER_PROMPTS_CSV` is actually launchable under `worker_prompt_launchable_for_manager_project()`.
- `PASS`: runtime now records `WORKER_PROMPTS_NOT_LAUNCHABLE` and forces same-session manager repair via `resume_invalid` instead of silently accepting an impossible delegate outcome.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-requires-launchable-prompt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-invalid-forces-resume`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-blocks-stop-with-unresolved-worker`
- `PASS`: `./bin/governance-check`

## 2026-04-22 09:35 PDT Reconnect Deferral And Origin-Tool Recovery Verification

- `FAIL`: canonical `develop` replay showed `monitor-ai-cli` could treat Codex `ERROR: Reconnecting... x/5` as immediate live network-failure evidence, so runtime switched tools before Codex exhausted its own retry loop even though Codex itself was still usable.
- `FAIL`: the same bounded recovery path could also leave `AI_TOOL` pinned to the last failed fallback after `codex -> cc -> iflow -> kiro-cli` exhaustion, so the next retry no longer started from the truthful origin tool.
- `PASS`: `monitor-ai-cli` now ignores reconnect-in-progress output as a live-kill signal and lets the tool exit naturally; post-exit runtime classification still routes pure reconnect evidence through `execution_network_transient` / `execution_network_persistent`.
- `PASS`: hard failures such as Codex 429 remain immediate monitor-level kill signals, so the reconnect deferral does not weaken rate-limit handling.
- `PASS`: runtime auto-recovery now remembers the origin tool for one fallback episode and restores that tool once every configured fallback has failed.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-defers-codex-reconnect-until-retries-exhaust`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-429-rate-limit`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-runtime-cross-tool-recovery-remembers-failed-tools`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-network-failure-blocks-fallback`
- `PENDING`: carry this same-owner reconnect/fallback repair through guarded `feature -> test-pre-merge -> develop` promotion, then rerun canonical `develop` self-host acceptance until Freely finishes one real task, lawfully closes that temporary worktree, and advances to the next task.
- `PASS`: replayed the same regression trio plus `./bin/governance-check` on protected lane `test-pre-merge-20260421-manager-exit-contract-expected-worker-guard-v2`; all passed before the first `develop` merge attempt.
- `FAIL`: the first guarded `develop` merge attempt was blocked by the develop-bound governance materialization gate because this followthrough's owner issue/progress/review evidence was not yet present in the merge diff, even though the code/test patch itself was ready.
- `PENDING`: rerun guarded `develop` merge with the refreshed owner evidence, then restart canonical `develop` runtime and continue self-host replay until Freely completes one task with lawful closeout and advances to the next task.

## 2026-04-23 08:05 PDT Codex OAuth Refresh Transport Classification Verification

- `FAIL`: latest runtime truth still showed a real Codex transport failure being widened into generic runtime failure: worker prompt evidence included `Failed to refresh token: error sending request for url (https://auth.openai.com/oauth/token)`, while live-status still reported `last_exit_reason=tool_runtime_failure`.
- `PASS`: `monitor-ai-cli` and runtime classification now treat that request-send failure family as bounded network evidence, so the same device-network recovery path used for reconnect exhaustion can also cover OAuth refresh transport failures.
- `PASS`: explicit auth rejection remains outside that path; the existing `401 Unauthorized` OAuth refresh noise test still passes and guards the auth/network boundary.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-ignores-codex-apikey-oauth-refresh-401`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-classifies-codex-oauth-refresh-request-error-as-network-failure`
- `PASS`: `./bin/governance-check`
- `PENDING`: replay protected promotion with this refreshed owner evidence, then re-run canonical `develop` daemon self-host acceptance and verify the same Codex OAuth request-send failure family now lands on `execution_network_*` rather than `tool_runtime_failure`.

## 2026-04-22 03:15 PDT Repair Handoff Relaunch Verification

- `FAIL`: canonical `develop` self-host replay progressed to `manager_exit_contract_invalid`, but the next manager round relaunched as `fresh rotation_reason=initial_start`; that violated the repair handoff contract, reopened broad patrol, and let newer intake supersede the repair round before a valid exit contract existed.
- `PASS`: `select_launch_kind()` now recognizes persisted `manager_exit_contract_repair` / `worker_exit_contract_repair` handoffs as resume-only relaunches and refuses to treat a supervisor restart with existing handoff/resume evidence as a true first launch.
- `PASS`: the supervisor loop now flips `FIRST_ROUND=false` immediately after the first AI cycle, so same-process `resume_invalid` / `resume_manager` loops cannot regress into `initial_start`.
- `PASS`: `tool_has_resume_evidence()` now evaluates resume evidence against the actual project root instead of an unbound local `project` variable, which keeps repair-handoff launch-kind selection shell-safe.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-avoids-initial-start`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-invalid-forces-resume`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-new-intake-reentry`
- `PASS`: replayed the same regressions plus `bash -n docs/system/workspace/scripts/runtime/freely` on protected lane `test-pre-merge-20260422-manager-repair-handoff-intake-supersede`.
- `PENDING`: rerun guarded `develop` merge with the refreshed owner evidence, then restart canonical `develop` runtime and verify the repair handoff stays on same-context resume until the daemon can complete one task, retire that temporary lane, and advance to another task.
