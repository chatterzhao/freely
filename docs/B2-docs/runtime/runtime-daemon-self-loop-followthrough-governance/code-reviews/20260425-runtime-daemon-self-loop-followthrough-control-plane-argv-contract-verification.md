# Verification: runtime-daemon-self-loop-followthrough control-plane argv contract

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-25`
- verifier: `codex`
- source_branch: `feature/runtime-control-plane-child-argv-contract-20260425`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-feature-runtime-control-plane-child-argv-contract`

## Scope Verdict

- `FAIL`: canonical `develop` at merge commit `a63f37e1` no longer looped on worker runtime rebind, but a fresh `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely` still stalled before manager AI launch. Root evidence showed supervisor `11693` alive with child processes for `ensure-interruption-dispatch --watch` and `ensure-manager --watch`, yet runtime never emitted `interruption_dispatcher_relaunch_ready`, left `.freely/run/interruption-dispatcher.pid` and `.freely/run/manager-watchdog.pid` absent, and `live-status` reported `activity_state: stalled_without_runtime`.
- `PASS`: the root cause is a control-plane argv contract mismatch, not a dispatcher/watchdog launch failure. Background helpers were started as `bash .../docs/system/workspace/scripts/runtime/freely ensure-interruption-dispatch ...` and `bash ... ensure-manager ...`, while runtime readiness and pid validation only recognize commands that carry the `runtime/freely ...` argv prefix.
- `PASS`: `launch_interruption_dispatcher()`, `launch_manager_watchdog()`, and `launch_manager_control_plane_recheck()` now publish the same `exec -a 'runtime/freely ...'` contract used elsewhere by daemon-run and by runtime pid discovery, so startup readiness can see the helper processes it just launched.
- `PASS`: focused regressions passed for both the new launcher contract and nearby daemon-start command surfaces:
  1. `bash docs/system/workspace/scripts/tests/test-freely-control-plane-launch-argv-contract`
  2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
  3. `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
  4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-ignores-fake-supervisor-argv`
- `PENDING`: replay this repair through protected premerge, merge into canonical `develop`, restart `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`, and verify manager reaches `ai_launch_begin` instead of stalling after `interruption_dispatcher_relaunch_requested`.

## Implementation Decision Note

- decision: `Fix the launch contract to match existing pid discovery instead of widening discovery to accept multiple ambiguous helper command shapes.`
- why_this: `The helpers were already launching successfully, so changing discovery to accept every observed shell form would weaken runtime identity checks and make fake-process collisions easier. The narrow fix is to keep one authoritative process identity contract and make every launcher honor it.`
- alternatives_considered: `Loosen pid discovery to match any bash wrapper around the runtime script; bypass dispatcher/watchdog ready checks during startup; replace pid inspection with pid-file-only trust.`
- boundary_non_goals: `No change to manager/worker delegation semantics, no reduction in control-plane identity strictness, and no claim that canonical develop has fully recovered until real daemon replay advances past this startup seam.`
- residual_risk: `Canonical develop may still expose another bounded followthrough seam after startup reaches manager AI launch again, but helper-process invisibility due to argv mismatch should no longer be able to stall daemon start in place.`
