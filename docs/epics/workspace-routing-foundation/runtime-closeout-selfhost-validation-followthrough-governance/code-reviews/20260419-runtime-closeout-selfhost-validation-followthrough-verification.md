# Verification: runtime-closeout-selfhost-validation-followthrough-governance

- issue_id: `I-20260419-0333-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`
- verification_date: `2026-04-19`
- verifier: `codex`

## Scope Verdict

- `PASS`: the preserved checkpoint diff is now bound to one explicit owner instead of drifting as undocumented branch-local execution truth.
- `PASS`: focused regressions prove the daemon/start-lock half and the interruption-routing half still share one bounded closeout/self-host seam.
- `PASS`: the interruption-manager tests now explicitly cover both the new direct fast paths and the generic codex/cc fallback path, so the checkpoint no longer relies on stale pre-fast-path expectations.
- `PASS`: real self-host replay no longer relaunches a second supervisor on repeated `daemon start`; after the first start reaches `supervisor_pid=93757`, the second start is rejected as already running.
- `PASS`: a longer-delay replay reaches `ai_launch_begin` and `last_ai_state=up` without reopening the churn window; a second `daemon start` 12 seconds later still stops at `user_start_rejected_already_running` instead of replacing the active supervisor.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-start-lock-cleans-ambiguous-missing-state`
2. `bash docs/system/workspace/scripts/tests/test-freely-start-lock-acquires-with-missing-run-dir`
3. `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-worker-runtime-when-startup-truth-is-ready`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-releases-start-lock-when-launch-fails`
5. `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler`
6. `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler-cc`
7. `git diff --check`
8. `./bin/governance-check`
9. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260418-feature-runtime-closeout-selfhost-validation --issue docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`

## Real Replay Evidence

- First replay on `2026-04-19` exposed a true blocker: `freely daemon start --project <worktree>` could hang before `.freely/run` existed because project start-lock acquisition used `mkdir "$lock_dir"` without first creating the parent directory.
- After fixing the missing parent creation, replay showed first-start success with `supervisor_pid=93757` and `live-status` truth `desired_runtime_state=running`, `last_supervisor_state=up`, `last_ai_state=down`, `last_exit_reason=starting`.
- A repeated `freely daemon start --project <worktree>` no longer launched a replacement supervisor; the command now stops at the user precheck with `daemon start refused: project runtime is already running`.
- A guarded follow-up replay with a 12-second delay preserved the same no-relaunch behavior after runtime advance: first start returned `supervisor_pid=98716`, runtime events recorded `event=ai_launch_begin`, `live-status` reported `last_supervisor_state=up` and `last_ai_state=up`, and the second start still exited with code `2` at `user_start_rejected_already_running`.
- Added worker attach regression coverage for the narrower seam behind that replay: when a worker supervisor is authoritative and startup truth is already written, attach stays on the live runtime even if `ai.pid` has not landed yet.
- `./bin/pretests-gate` now passes for this owner after writing back the completed acceptance-item status and narrowing the real-environment surface to the truthful active checkpoint worktree replay.

## Implementation Decision Note

- decision: `Promote the runtime closeout/selfhost checkpoint as one bounded follow-on owner.`
- why_this: `The green focused regressions did not expose two independent seams. Daemon reuse, ambiguous start-lock cleanup, and closeout/self-host routing all arise from the same preserved checkpoint surface.`
- alternatives_considered: `Leave the checkpoint undocumented; split runtime and interruption routing into two new owners immediately; silently absorb the changes into the receipt-only followthrough lane.`
- boundary_non_goals: `This owner does not reopen receipt-ledger repair, generic interruption taxonomy redesign, or broader runtime startup architecture.`
- residual_risk: `Local replay now covers both startup-truth and post-ai-launch windows; the remaining risk is mainly promotion-path drift rather than an untested local relaunch window.`
