# Issue: runtime-startup-self-healing-governance

- issue_id: `I-20260419-1630-A`
- title: `Runtime startup self-healing governance`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-startup-self-healing-governance`
- issue-name: `runtime-startup-self-healing-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260419T150500Z/candidates.md#c-20260419-1630-a`
- source_brainstorm: `docs/B1-docs/raw-20260419T150500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- prd_path: `docs/B2-docs/runtime/runtime-startup-self-healing-governance/prd.md`
- pre_tests_path: docs/B2-docs/runtime/runtime-startup-self-healing-governance/raw-20260419-1630/verification/pre-tests.md
- tasks_path: `docs/B2-docs/runtime/runtime-startup-self-healing-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-startup-self-healing-governance.md`
- verification_artifact_dir: docs/B2-docs/runtime/runtime-startup-self-healing-governance/raw-20260419-1630/code-reviews
- depends_on:
  - `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
  - `docs/B2-docs/ibm/freely-start-auto-recovery-rootcause-governance/issues/freely-start-auto-recovery-rootcause-governance.md`
- created_at: `2026-04-19`
- updated_at: `2026-04-23`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Protected-root replay on `2026-04-19` showed a narrower startup seam than the existing runtime owners cover:

1. `freely daemon start` left machine-owned truth claiming `desired_runtime_state=running`, `last_supervisor_state=up`, and `last_exit_reason=starting`.
2. The corresponding `supervisor.pid` and `interruption-dispatch.pid` files remained on disk even though no owned runtime processes were alive anymore.
3. Launch-state and continuity surfaces could still point to missing worktrees or stale continuity files from an already deleted feature lane.
4. This happened before a manager AI had a lawful continuity surface to read, so the system was already lying about startup liveness before manager-owned recovery began.

## Scope

1. Add startup-time self-heal that only repairs machine-provable stale runtime state.
2. Clear stale runtime pid files when project ownership cannot be validated and no unverified pid-hint exception remains.
3. Downgrade stale `running/up/starting` startup truth to canonical stopped/down state after a bounded grace window when no authoritative runtime processes exist.
4. Persist refreshed manager launch-state continuity/prompt references when read-time status repair discovers stale continuity anchors.
5. Treat equivalent on-disk project paths as the same runtime owner during pid and supervisor-identity validation so status readback does not clear a live daemon only because the recorded path spelling differs.
6. Keep startup/bootstrap grace aligned with runtime-published launch truth so a manager lane that has already recorded `ai_launch_in_flight` or `ai_launch_observed` is not torn down as fake runtime absence during the same bounded grace window.
7. Validate live AI pids against the configured supported-tool launcher signatures instead of stale hard-coded argv fragments, while still rejecting foreign same-tool processes.
8. Allow bounded project-scoped proxy self-heal for execution-time network failures without silently re-enabling tool or slot auto-switch when those controls are disabled.
9. Cover the repair with focused regressions and one protected-root replay.

## Non-Goals

1. Do not let startup scripts make semantic continuation or governance decisions.
2. Do not silently restore interrupted AI work during `restart`.
3. Do not redesign generic post-failure recovery, fleet sequencing, or manager routing.
4. Do not widen this owner into a broad runtime lifecycle rewrite.
5. Do not silently turn `AUTO_SWITCH_TOOL=false` or `AUTO_SWITCH_SLOT=false` back on.

## Acceptance

1. `start`, `daemon start`, `restart`, `ensure-manager`, and `live-status` all canonicalize stale startup machine state before they rely on it.
2. A stale startup state older than the bounded grace window, with no authoritative runtime processes or active start lock, is rewritten to `stopped/down/down/startup_self_heal_no_runtime`.
3. Stale `supervisor.pid`, `ai.pid`, `ensure-manager.pid`, and `interruption-dispatch.pid` files are removed only when project ownership cannot be validated and no unverified pid-hint exception remains.
4. `manager_worker_launch_state_refresh_for_status()` persists corrected continuity/prompt references even when worker-slot counts do not change.
5. If monitor/runtime has already recorded `LAST_EXIT_REASON="ai_launch_in_flight"` during startup, bootstrap grace keeps the supervisor in a retryable in-flight state instead of misclassifying it as missing AI runtime immediately after `L041 ai_launch_observed`.
6. AI pid validation follows the configured supported tool family and accepts lawful `claude` launcher processes for `cc` aliases while still rejecting foreign same-tool processes.
7. Network execution failures can attempt bounded project-scoped proxy self-heal, verified by a live `hi` probe, without changing tool or slot selection when those auto-switch controls are disabled.
8. `live-status` and related ownership checks keep a live daemon runtime authoritative when the recorded project root and the inspected project root resolve to the same on-disk directory even if the path spelling differs, and avoid heavy fleet refresh while a manager AI is already active.
9. `daemon start` launches `daemon-run` in a session-detached way that survives short-lived non-interactive caller teardown instead of depending on shell job control.
10. When `AUTO_SWITCH_SLOT=false`, startup/watchdog recovery paths do not inventory saved codex slots, do not probe candidate slots, and do not rewrite `~/.codex/auth.json` behind the operator's back.

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-keeps-daemon-runtime-across-case-variant-project-path`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-detach-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-runtime-state`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-launch-in-flight-state`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
- `bash docs/system/workspace/scripts/tests/test-freely-prompt-build-failure-keeps-supervisor-alive`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-persists-stale-continuity-rewrite`
- `bash docs/system/workspace/scripts/tests/test-freely-stale-manager-continuity-filter`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-bootstrap-keeps-supervisor-after-ai-launch-observed`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-pid-validation-supported-tools`
- `bash docs/system/workspace/scripts/tests/test-freely-proxy-self-heal`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-active-manager-skips-fleet-refresh`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-uses-status-signals-when-manager-idle`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-worker-count-fast-path`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `git diff --check`
- `./bin/governance-check`
- protected-root replay: `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely` then `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`

## Success Criteria

1. On the protected root, machine-owned startup truth no longer stays in fake `running/up/starting` after runtime processes are already gone.
2. Short-lived non-interactive AI tools remain compatible with attach/reuse, daemon cold-start, and existing after-failure recovery semantics because launch-in-flight state is recorded before child exit, `ai_launch_in_flight` stays inside the bounded bootstrap grace window, and prompt-build failure now stays retryable under a live supervisor.
3. Supported-tool PID matching, manager-active status fast paths, and proxy self-heal all preserve project-scoped truth without re-enabling disabled tool/slot auto-switch.
4. Verification evidence is written back in this owner, then the branch is merged to `develop`, pushed, and the dedicated worktree is retired.
5. Disabled slot auto-switch remains a hard stop for startup/watchdog recovery: no background codex slot probe or switch may touch live auth material until the operator explicitly re-enables it.
