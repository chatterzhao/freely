# Progress: runtime-daemon-self-loop-followthrough-governance

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- title: `Runtime daemon self-loop followthrough governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-daemon-self-loop-blocker-20260421`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-daemon-self-loop-blocker`
- updated_at: `2026-04-21 06:12 PDT`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Real self-host observation showed Freely could patrol once but fail to sustain autonomous looping because daemon-mode `TERM` could become a false `operator_stop`.
- A second restart blocker also existed: a lone same-project dispatcher/watchdog residue could cause `start` or `daemon start` to refuse even though no authoritative supervisor was alive.
- The runtime fix and focused regressions are complete in the blocker worktree.
- Canonical `develop` then exposed one more followthrough seam: runtime was reading the new `## Worker Delegation` continuity shape as if no worker prompts existed, so freshly generated worker lanes could not launch even though manager continuity had already selected them.
- The continuity parser and worker-launch consumption path are now updated to read that current handoff shape.
- Guarded replay then exposed one more same-owner retirement seam: an already merged-clean blocker worktree could still be treated as a recoverable active worker. Runtime now settles those lanes toward cleanup followthrough, and cleanup can reclaim stale recorded ownership for retire-ready merged worktrees.
- A fresh-session verification at `2026-04-21 05:36 PDT` disproved the previous "already green" claim: `test-freely-daemon-start-reuses-live-supervisor-without-relaunch` failed before reuse because its `ps`-count assertion could observe a transient duplicate `daemon-run` snapshot.
- A narrow same-lane fix then hardened that regression to wait for a stable single `daemon-run` process snapshot before asserting reuse, instead of treating a startup race between separate `ps` calls as a product failure.
- As of `2026-04-21 05:42 PDT`, the refreshed feature worktree verification passes every required feature-local regression and gate again with that repair in place.
- A second fresh-session recheck at `2026-04-21 05:47 PDT` passed the same full feature-local verification chain without any additional source edits, so the lane remains green on current-session truth.
- A third same-session verification at `2026-04-21 05:54 PDT` reran the owner-required feature-local regression and gate set from this worker continuation; every command still passed, and no additional implementation edits were needed beyond the already-present regression hardening in this worktree.
- A fourth worker-continuation verification at `2026-04-21 06:12 PDT` reran the full owner-required feature-local chain, including the daemon lifecycle regressions, continuity/retirement regressions, `./bin/pretests-gate`, and `./bin/governance-check`; every command passed again with no further source edits.
- Canonical `develop` self-host replay then exposed a remaining continuity-consumption seam: manager wrote the current direct `## Worker Delegation` handoff with a bare `prompt_path`, but runtime only parsed `prompt_path` after an explicit `launchable_queue`/`queue` subsection, so post-cycle worker launch treated the continuity as prompt-empty and restarted manager instead.
- The runtime parser now treats direct `## Worker Delegation` `prompt_path` entries as launchable by default, matching the manager-written continuity shape that self-host dogfooding is actually producing.
- The current-format continuity-consumption and manager worker-launch regressions now exercise that direct handoff shape, and a post-AI-cycle launch regression passes against the same parser path.
- The remaining completion work is guarded promotion into `develop`, canonical `develop` self-host task completion, and temporary lane retirement.

## Verification Evidence

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
14. `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`
15. `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`

## 2026-04-21 05:29 PDT Recheck Commands

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

All commands passed in the feature worktree on this recheck.

## 2026-04-21 05:33 PDT Fresh-Session Recheck Commands

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

All commands passed again in the feature worktree during this fresh session.

## 2026-04-21 05:36 PDT Failure Reproduction

1. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`

Observed result:

- `FAIL`: `expected exactly one daemon-run process before reuse, found 2`
- Interpretation: the lane was not honestly promotion-ready at the start of this session because the fresh-session reuse regression still had a startup-window race.

## 2026-04-21 05:42 PDT Narrow Fix And Recheck Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
4. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
5. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
6. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
7. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
8. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
9. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
10. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
11. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
12. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
13. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
14. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
15. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
16. `./bin/governance-check`

All commands above passed after the narrow test hardening.

## 2026-04-21 05:47 PDT Fresh-Session Verification Commands

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

All commands passed again in the feature worktree during this fresh-session verification.

## 2026-04-21 05:54 PDT Worker Continuation Verification Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
2. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
6. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
10. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
11. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
12. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
13. `./bin/governance-check`

All commands passed in the feature worktree during this worker continuation verification. No new source edits were required after these reruns.

## 2026-04-21 06:12 PDT Worker Continuation Verification Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
2. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
6. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
10. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
11. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
12. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
13. `./bin/governance-check`

All commands passed again in the feature worktree during this worker continuation verification. No further source edits were required.

## Current Lane Judgement

 - lane_state: `feature-local green after a narrow regression hardening fix`
- blocker_reproduction: `no`
- guarded_promotion_ready: `yes`
- remaining_blocker: `canonical develop replay is still required before retirement`

## Next Action

1. Replay `feature/runtime-daemon-self-loop-blocker-20260421 -> test-pre-merge-20260421-runtime-self-loop-blocker -> develop` through `./bin/merge-guarded` with this refreshed evidence included.
2. On canonical `develop`, run `./bin/freely daemon start` until one task completes to the current-project success standard, its temporary worktree closes lawfully, and the daemon proceeds to the next task.
3. Retire the temporary blocker worktree and disposable test-pre-merge branch after canonical replay succeeds.
