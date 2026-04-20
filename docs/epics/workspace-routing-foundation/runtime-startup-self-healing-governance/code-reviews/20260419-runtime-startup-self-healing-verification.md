# Verification: runtime-startup-self-healing-governance

- issue_id: `I-20260419-1630-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md`
- verification_date: `2026-04-19`
- branch: `feature/runtime-startup-self-healing-boundary-20260419`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-feature-runtime-startup-self-healing-boundary`
- verifier: `codex`

## Commands

1. `bash -n docs/system/workspace/scripts/runtime/freely`
2. `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-runtime-state`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-persists-stale-continuity-rewrite`
4. `bash docs/system/workspace/scripts/tests/test-freely-stale-manager-continuity-filter`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status`
6. `bash docs/system/workspace/scripts/tests/test-freely-daemon-command-semantics`
7. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
8. `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-live-supervisor-between-ai-cycles`
9. `git diff --check`
10. `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
11. `./bin/governance-check`
12. Protected-root replay:
   - `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
   - `./bin/freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`
   - wait about 70 seconds
   - `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`

## Results

1. All focused regressions above passed.
2. The protected root initially had stale machine-owned startup truth:
   - before replay, `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/workcell-state.env` still said `DESIRED_RUNTIME_STATE="running"`, `LAST_SUPERVISOR_STATE="up"`, `LAST_EXIT_REASON="starting"`
   - no authoritative runtime processes remained for the stale `supervisor.pid=10184` and `interruption-dispatch.pid=11099`
3. `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely` self-healed the stale startup machine state:
   - runtime events logged `startup_self_heal_stale_pid_cleared` for `supervisor` and `interruption_dispatcher`
   - runtime events logged `startup_self_heal_runtime_state_cleared trigger=live_status reason=no_runtime_processes_after_startup_grace`
   - resulting protected-root status became `desired_runtime_state: stopped`, `last_supervisor_state: down`, `last_ai_state: down`, `last_exit_reason: startup_self_heal_no_runtime`
4. A fresh `daemon start` then launched `supervisor_pid: 48674` and `interruption_dispatcher_relaunch_ready dispatcher_pid=49310`.
5. After roughly 70 seconds, protected-root `live-status` no longer claimed fake runtime liveness:
   - status again self-healed to `startup_self_heal_no_runtime` after the new startup attempt stopped
   - `manager_handoff_state: missing` and `manager_continuity_gap_state: active` surfaced the downstream continuity failure explicitly instead of leaving startup in fake `running/up/starting`
6. `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills` passed after adding a retired-target regression for `unparseable_subject_ancestry`.
7. `./bin/governance-check` passed once the retired-target ancestry path was treated as still auditable through its canonical absorbing protected merge.

## Verdict

`AT-001`, `AT-002`, and `AT-003` are satisfied for this bounded owner: startup now canonicalizes stale machine-owned truth and exposes the remaining failure as continuity-gap truth rather than fake runtime liveness.

## Implementation Decision Note

- decision: `Keep startup self-heal scoped to machine-provable stale state and repair the separate retired-target receipt-gap audit path only far enough to let this owner close under the existing governance gate.`
- why_this: `The protected-root replay showed the user-visible failure happens before manager-owned semantic recovery starts, so startup must canonicalize stale pid/state truth itself. The receipt-gap follow-on is deliberately narrower than a governance redesign: it only restores auditability for already absorbed unparseable-subject entries after their target batch branch is lawfully deleted.`
- alternatives_considered: `Leave stale startup truth for manager recovery; widen restart into implicit continuity restoration; delete the stale receipt-gap entries by hand; broaden governance-check into a generic ancestry audit redesign.`
- boundary_non_goals: `This note does not let startup repair semantic continuation, does not change attach/reuse or restart semantics, and does not reopen the broader protected-merge receipt policy beyond the retired-target false negative needed for closeout.`
- residual_risk: `The remaining risk is downstream manager continuity failure after startup truth is corrected; that failure now surfaces explicitly as continuity-gap state instead of fake runtime liveness.`

## Remaining Closeout

1. Merge, push, and retire the dedicated feature worktree after recording the closeout commit on this lane.
