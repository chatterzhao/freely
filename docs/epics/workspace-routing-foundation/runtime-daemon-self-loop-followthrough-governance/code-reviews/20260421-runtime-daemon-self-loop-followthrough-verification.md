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

## Implementation Decision Note

- decision: `Keep the runtime fix narrow but extend both recovery and fallback manager-launch paths so they recheck whether a worker prompt is still launchable before reviving it, while treating merged-clean blocker worktrees plus owner-evidence-only merged followthrough lanes as cleanup-only followthrough lanes instead of edit workers to auto-recover.`
- why_this: `The develop-side blockers were followthrough seams, not scan selection defects. Manager continuity had already picked a worker lane, but runtime first treated the current continuity format as prompt-empty; after that repair it still misread a develop-absorbed blocker worktree as recoverable worker capacity; and after that it still had one fallback seam where latest-generated continuity could relaunch a now-retire-ready prompt without checking launchability. Fixing these narrow launch/recovery seams restores autonomy without adding a durable index, making scan heavier, or weakening cleanup lifecycle invariants.`
- alternatives_considered: `Treat the unlaunched lane as a scan-selection failure; add a separate prompt lifecycle index; redesign live-status before fixing runtime continuity parsing; hardcode that any merged worktree can never be revisited under any circumstance instead of encoding the narrower retire-ready cleanup invariant; keep requiring a fully clean merged worktree even though develop-bound owner evidence writeback legitimately leaves progress / verification files dirty during closeout; let latest-generated continuity fallback bypass launchability checks and hope human interruption closes the lane in time.`
- boundary_non_goals: `No scan-architecture rewrite, no live-status redesign, no reduction in Freely's autonomous execution authority.`
- residual_risk: `The remaining risk is only the final canonical develop self-host acceptance, which still must prove end-to-end autonomous continuation after one completed task and lawful worktree retirement.`
