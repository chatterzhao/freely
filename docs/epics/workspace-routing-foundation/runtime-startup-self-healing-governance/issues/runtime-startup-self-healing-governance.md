# Issue: runtime-startup-self-healing-governance

- issue_id: `I-20260419-1630-A`
- title: `Runtime startup self-healing governance`
- phase_state: `in_dev`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-startup-self-healing-governance`
- issue-name: `runtime-startup-self-healing-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260419-1630--runtime-startup-self-healing-boundary/candidates.md#c-20260419-1630-a`
- source_brainstorm: `docs/pre-brainstorms/20260419-1630--runtime-startup-self-healing-boundary/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- prd_path: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/prd.md`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/pre-tests.md`
- tasks_path: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-startup-self-healing-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
  - `docs/epics/workspace-routing-foundation/freely-start-auto-recovery-rootcause-governance/issues/freely-start-auto-recovery-rootcause-governance.md`
- created_at: `2026-04-19`
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
5. Cover the repair with focused regressions and one protected-root replay.

## Non-Goals

1. Do not let startup scripts make semantic continuation or governance decisions.
2. Do not silently restore interrupted AI work during `restart`.
3. Do not redesign generic post-failure recovery, fleet sequencing, or manager routing.
4. Do not widen this owner into a broad runtime lifecycle rewrite.

## Acceptance

1. `start`, `daemon start`, `restart`, `ensure-manager`, and `live-status` all canonicalize stale startup machine state before they rely on it.
2. A stale startup state older than the bounded grace window, with no authoritative runtime processes or active start lock, is rewritten to `stopped/down/down/startup_self_heal_no_runtime`.
3. Stale `supervisor.pid`, `ai.pid`, `ensure-manager.pid`, and `interruption-dispatch.pid` files are removed only when project ownership cannot be validated and no unverified pid-hint exception remains.
4. `manager_worker_launch_state_refresh_for_status()` persists corrected continuity/prompt references even when worker-slot counts do not change.
5. Protected-root replay proves Freely can cold-start from a stale machine-owned state and reach a canonical self-healed startup surface instead of remaining self-contradictory.

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-runtime-state`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-persists-stale-continuity-rewrite`
- `bash docs/system/workspace/scripts/tests/test-freely-stale-manager-continuity-filter`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `git diff --check`
- `./bin/governance-check`
- protected-root replay: `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely` then `./bin/freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`

## Success Criteria

1. On the protected root, machine-owned startup truth no longer stays in `running/up/starting` after runtime processes are already gone.
2. Any startup self-heal remains compatible with attach/reuse, daemon cold-start, and existing after-failure recovery semantics.
3. Verification evidence is written back in this owner, then the branch is merged to `develop`, pushed, and the dedicated worktree is retired.
