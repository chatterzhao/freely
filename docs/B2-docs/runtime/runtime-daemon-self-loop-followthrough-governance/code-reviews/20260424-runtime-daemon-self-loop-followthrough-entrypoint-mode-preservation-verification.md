# Verification: runtime-daemon-self-loop-followthrough-governance daemon entrypoint mode preservation

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`
- source_branch: `feature/runtime-daemon-entrypoint-mode-preserve-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-runtime-daemon-entrypoint-mode-preserve`

## Scope Verdict

- `FAIL`: canonical daemon replay after merge commit `cd3e4675` fixed the earlier SIGPIPE seam but exposed a new ownership-drift seam in the same current start window. Runtime events from `2026-04-24T22:09:45Z` onward showed daemon supervisors `9148` and `39611`, then a watchdog-driven foreground `start` supervisor `54468` appeared at `2026-04-24T22:20:33Z event=user_start_command_received`.
- `PASS`: root cause is narrow and local to launch-state persistence. `monitor-ai-cli.sh` wrote launch-in-flight workcell truth without preserving `LAST_ENTRYPOINT_MODE`, and `project_control_plane_entrypoint_mode()` correctly falls back to `foreground` when that field is absent.
- `PASS`: preserving the prior entrypoint mode in the launch-state write keeps daemon recovery on `daemon-run --project` without altering foreground behavior.
- `PENDING`: guarded premerge replay and canonical `develop` replay still need to prove this ownership seam is gone under the full self-host loop.

## Current-Window Evidence

1. `2026-04-24T22:17:57Z event=ai_launch_begin supervisor_pid=39611 ...`
2. `2026-04-24T22:20:12Z seq=13729 checkpoint=L041 stage=ai_launch_observed supervisor_pid=39611 child_pid=40603`
3. `2026-04-24T22:20:23Z seq=13733 checkpoint=L223 stage=manager_idle_supervisor_restart supervisor_pid=39611`
4. `2026-04-24T22:20:33Z event=user_start_command_received force=0`
5. `.freely/run/workcell-state.env` captured after replay no longer contained `LAST_ENTRYPOINT_MODE`, matching the fallback-to-foreground diagnosis.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-failure-recovery-preserves-daemon`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-detach-contract`

## Implementation Decision Note

- decision: `Preserve previously recorded entrypoint ownership when monitor-ai-cli writes ai_launch_in_flight state.`
- why_this: `The bug was not in watchdog policy itself; the policy only degraded because launch-state persistence erased the daemon/foreground ownership discriminator that relaunch selection already consults.`
- alternatives_considered: `Special-case ensure-manager to remember daemon mode elsewhere; force every watchdog relaunch to daemon-run; widen the fix into ai.pid liveness policy before proving the ownership field loss first.`
- boundary_non_goals: `No broader watchdog redesign, no claim that ai.pid liveness is fully solved, and no claim that canonical self-host acceptance is complete before protected replay proves task completion plus next-task continuation.`
- residual_risk: `Canonical replay may still expose a separate ai.pid liveness seam after daemon ownership is preserved, but this repair removes the proven foreground-fallback cause from the current replay window.`
