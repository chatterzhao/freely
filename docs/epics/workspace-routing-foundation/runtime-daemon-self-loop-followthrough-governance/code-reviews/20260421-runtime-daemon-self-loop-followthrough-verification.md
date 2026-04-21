# Verification: runtime-daemon-self-loop-followthrough-governance

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-21`
- verifier: `codex`

## Scope Verdict

- `PASS`: the blocker reproduced as a runtime/control-plane seam, not as a generic scan or task-selection defect.
- `PASS`: `project_has_authoritative_runtime_processes_for_user_precheck()` now requires supervisor truth instead of lone dispatcher/watchdog residue.
- `PASS`: daemon supervisor now ignores unexpected `TERM` without `stop.marker` and still records explicit daemon stop correctly.
- `PASS`: current manager continuity files that use `## Worker Delegation` now expose worker prompt paths to runtime launch and live-status truth.
- `PASS`: retire-ready merged-clean blocker worktrees are now treated as cleanup-followthrough retirement targets instead of recoverable edit workers, and cleanup can reclaim stale recorded ownership for those lanes.
- `PASS`: merged develop-absorbed blocker lanes that remain dirty only in owner evidence surfaces are now treated as retire-ready followthrough instead of relaunchable edit workers.
- `PASS`: manager worker-launch fallback now rechecks whether a prompt still targets a launchable lane before reviving it, so the latest generated continuity cannot bypass retire-ready merged guards.
- `PASS`: expected-running worker recovery and global restart selection now both exclude absorbed merged worker lanes, even if an earlier bad recovery already left ordinary dirty files behind in that old worktree.
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
12. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
13. `./bin/governance-check`
14. `bash docs/system/workspace/scripts/tests/test-freely-merged-clean-worker-handoff-guard`
15. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
16. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
17. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
18. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
19. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
20. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-retire-ready-merged-prompt`
21. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-absorbed-merged-dirty-worker`

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
