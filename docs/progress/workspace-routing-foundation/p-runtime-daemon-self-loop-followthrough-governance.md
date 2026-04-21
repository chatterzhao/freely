# Progress: runtime-daemon-self-loop-followthrough-governance

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- title: `Runtime daemon self-loop followthrough governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-daemon-self-loop-blocker-20260421`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-daemon-self-loop-blocker`
- updated_at: `2026-04-21 06:05 PDT`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Real self-host observation showed Freely could patrol once but fail to sustain autonomous looping because daemon-mode `TERM` could become a false `operator_stop`.
- A second restart blocker also existed: a lone same-project dispatcher/watchdog residue could cause `start` or `daemon start` to refuse even though no authoritative supervisor was alive.
- The runtime fix and focused regressions are complete in the blocker worktree.
- Canonical `develop` then exposed one more followthrough seam: runtime was reading the new `## Worker Delegation` continuity shape as if no worker prompts existed, so freshly generated worker lanes could not launch even though manager continuity had already selected them.
- The continuity parser and worker-launch consumption path are now updated to read that current handoff shape.
- Guarded replay then exposed one more same-owner retirement seam: an already merged-clean blocker worktree could still be treated as a recoverable active worker. Runtime now settles those lanes toward cleanup followthrough, and cleanup can reclaim stale recorded ownership for retire-ready merged worktrees.
- Canonical `develop` then exposed a narrower replay seam after guarded absorption: if the merged blocker lane only stayed dirty in owner progress / verification evidence, runtime still treated it as a relaunchable edit worker because the old guard only recognized fully clean merged worktrees. This followthrough now treats owner-evidence-only dirty merged lanes as retirement/promotion followthrough instead of active edit capacity.
- Canonical `develop` then exposed one more fallback seam in the manager launcher: when no launchable continuity remained, runtime could fall back to the latest generated continuity and relaunch a worker prompt without rechecking whether that prompt now targeted a retire-ready merged lane.
- This followthrough now makes the fallback launcher respect the same `worker_prompt_launchable_for_manager_project()` gate and settle retire-ready merged targets instead of reviving them.
- The protected test lane replay now passes again; the remaining completion work is develop absorption, real self-host task completion, and temporary lane retirement.

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
14. `bash docs/system/workspace/scripts/tests/test-freely-merged-clean-worker-handoff-guard`
15. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
16. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
17. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
18. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
19. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
20. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
21. `./bin/governance-check`
22. `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`
23. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-retire-ready-merged-prompt`

## Next Action

1. Replay the narrowed manager-launch fallback guard through guarded promotion into `develop`, then rerun canonical self-host acceptance.
2. On canonical `develop`, run `./bin/freely daemon start` until one task completes to the current-project success standard, its temporary worktree closes lawfully, and the daemon proceeds to the next task.
3. Retire the temporary blocker worktree and disposable test-pre-merge branch.
