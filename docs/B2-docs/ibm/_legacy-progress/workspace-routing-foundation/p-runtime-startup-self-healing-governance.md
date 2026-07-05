# Progress: runtime-startup-self-healing-governance

- issue_id: `I-20260419-1630-A`
- issue_path: `docs/B2-docs/runtime/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md`
- title: `Runtime startup self-healing governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/live-status-hang-root-cause-20260422`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260422-feature-live-status-hang-root-cause`
- updated_at: `2026-04-23`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Protected-root replay on `2026-04-22` exposed a narrower still-open startup seam on canonical `develop`: after `L041 ai_launch_observed`, watchdog still restarted the manager with `L223 trigger=supervisor_alive_ai_missing_after_grace` because bootstrap grace accepted `starting` but not the newer `ai_launch_in_flight` truth written by monitor/runtime.
- This continuation keeps the same owner boundary. The fix does not widen into generic recovery; it aligns bootstrap grace with runtime-published startup truth, strengthens supported-tool PID validation, and keeps manager-active status reads on the lightweight path.
- The current implementation now treats `LAST_EXIT_REASON="ai_launch_in_flight"` as lawful bootstrap in-flight state, so a just-observed AI launch is not torn down as fake absence before the grace window or startup lifecycle closes.
- Supported-tool PID validation now reads launcher fragments from configured tool support instead of stale hard-coded argv assumptions, including the lawful `claude` process behind `cc` aliases while still rejecting foreign same-tool processes.
- Execution-time network failure handling now supports bounded project-scoped proxy self-heal, verified by a `hi` probe, without silently re-enabling `AUTO_SWITCH_TOOL` or `AUTO_SWITCH_SLOT` when those settings are disabled.
- `live-status` no longer pays the heavy fleet-refresh cost while the manager AI is already active; it uses cached launch-state and lightweight intake/worker counters so status polling does not perturb the same startup window this owner is trying to stabilize.
- Continuation `2026-04-23`: a real operator report showed `AUTO_SWITCH_SLOT=false` still allowed startup/watchdog paths to inventory saved codex slots and eventually rewrite `~/.codex/auth.json`. The bounded repair now short-circuits startup preflight, watchdog entry selection, and watchdog full-sweep probing before any slot switch/probe happens when slot auto-switch is disabled.
- Focused regressions are green in both the feature lane and the disposable `test-pre-merge-20260422-live-status-hang-root-cause` lane; the remaining work is to land the owner docs, replay the guarded merge, and then re-run canonical root daemon validation on updated `develop`.

## Success Criteria

1. Protected-root stale startup truth is canonicalized before startup/status consumers rely on it.
2. Attach/reuse, daemon cold-start, and restart semantics remain intact.
3. Verification evidence is written back, then this lane merges to `develop`, pushes, and retires.

## Current Evidence

1. Real replay on `2026-04-19` recorded stale `supervisor.pid` and `interruption-dispatch.pid` under `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/` while no owned runtime processes remained.
2. The same protected-root state still showed `DESIRED_RUNTIME_STATE="running"`, `LAST_SUPERVISOR_STATE="up"`, and `LAST_EXIT_REASON="starting"`.
3. Continuity and prompt artifacts still referenced missing worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260413-feature-runtime-manager-startup-blocker-rootcause`.
4. Canonical protected-root history on `2026-04-22` still showed the defect before this fix landed: `L041 ai_launch_observed supervisor_pid=41480 child_pid=65227` at `02:46:31Z`, followed by `L223 manager_idle_supervisor_restart trigger=supervisor_alive_ai_missing_after_grace supervisor_pid=41480` at `02:46:43Z`. A second replay repeated the same pattern for supervisor `96217` at `02:51:45Z -> 02:52:04Z`.
5. `bash docs/system/workspace/scripts/tests/test-freely-manager-bootstrap-keeps-supervisor-after-ai-launch-observed` now passes and directly proves `project_bootstrap_launch_in_flight` accepts `LAST_EXIT_REASON="ai_launch_in_flight"` while the startup lifecycle is still in-flight.
6. `bash docs/system/workspace/scripts/tests/test-freely-ai-pid-validation-supported-tools` passes and proves configured supported-tool signatures accept lawful owner processes while rejecting foreign same-tool pids.
7. `bash docs/system/workspace/scripts/tests/test-freely-proxy-self-heal` passes and proves proxy self-heal rotates bounded proxy modes, honors `AUTO_SETUP_FREELY_PROXY`, and restores the original mode after exhaustion.
8. `bash docs/system/workspace/scripts/tests/test-freely-live-status-active-manager-skips-fleet-refresh`, `bash docs/system/workspace/scripts/tests/test-freely-live-status-uses-status-signals-when-manager-idle`, and `bash docs/system/workspace/scripts/tests/test-freely-live-status-worker-count-fast-path` all pass, so status polling now stays lightweight in the exact manager-active window that previously churned.
9. The feature lane and the disposable `test-pre-merge-20260422-live-status-hang-root-cause` lane both pass the focused regression set: `bash -n docs/system/workspace/scripts/runtime/freely`, `bash docs/system/workspace/scripts/tests/test-freely-manager-bootstrap-keeps-supervisor-after-ai-launch-observed`, `bash docs/system/workspace/scripts/tests/test-freely-startup-self-heal-keeps-codex-wrapper-ai-pid`, `bash docs/system/workspace/scripts/tests/test-freely-ai-pid-validation-supported-tools`, `bash docs/system/workspace/scripts/tests/test-freely-proxy-self-heal`, `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`, `bash docs/system/workspace/scripts/tests/test-freely-live-status-active-manager-skips-fleet-refresh`, `bash docs/system/workspace/scripts/tests/test-freely-live-status-uses-status-signals-when-manager-idle`, and `bash docs/system/workspace/scripts/tests/test-freely-live-status-worker-count-fast-path`.
10. The guarded `feature -> test-pre-merge` merge already succeeded for `feature/live-status-hang-root-cause-20260422`; the first `test-pre-merge -> develop` replay was blocked only because the merge diff lacked owner lifecycle artifacts, not because of code/test failure.
11. A separate bounded continuation lane `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-guard-disable-slot-switch-probe` now adds an explicit `AUTO_SWITCH_SLOT=false` guard to `preflight_codex_slot_recovery_before_start_or_fail()`, `ensure_codex_slot_ready_for_manager()`, `probe_any_usable_codex_slot_now()`, `probe_all_codex_slots_and_update_cooldown()`, and `switch_to_codex_slot()`.
12. The focused regressions `test-freely-start-skips-preflight-slot-recovery-when-auto-switch-slot-disabled`, `test-watchdog-manager-entry-skips-slot-selection-when-auto-switch-slot-disabled`, `test-watchdog-probe-all-skips-sweep-when-auto-switch-slot-disabled`, and baseline `test-ai-cli-switch-default-tool` all passed in both the feature lane and `test-pre-merge-20260423-guard-disable-slot-switch-probe`.

## Next Action

1. Re-run the guarded `test-pre-merge-20260423-guard-disable-slot-switch-probe -> develop` merge with this owner evidence in the diff.
2. After canonical `develop` carries the patch, restart `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely` under `AUTO_SWITCH_SLOT=false` and verify `~/.codex/auth.json` no longer changes from background startup/watchdog probing.
3. Once canonical replay is green, retire `test-pre-merge-20260423-guard-disable-slot-switch-probe` and `feature/guard-disable-slot-switch-probe`, then continue the broader protected-root daemon replay closeout for this owner.
