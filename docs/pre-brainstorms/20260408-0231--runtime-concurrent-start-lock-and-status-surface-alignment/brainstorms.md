# Brainstorms - 20260408-0231--runtime-concurrent-start-lock-and-status-surface-alignment

## Context

- Observed dogfood truth on `2026-04-08 01:23:58 PDT`: the research worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260407-060440-feature-runtime-evidence-provenance-and-canonical-absorption-gate` emitted three same-second `supervisor_started` events for the same project (`81547`, `81933`, `81935`).
- Root cause evidence is runtime-level, not just stale docs:
  - `start_workcell_supervisor_async()` blindly `nohup`s `freely start --project ...` with no project-local launch serialization.
  - `start_project_runtime()` checks `supervisor.pid` and process discovery before writing the new supervisor pid, but concurrent `start` invocations can all pass that check before any one writes durable ownership.
- A separate but adjacent status-surface defect is also present:
  - `live-status` refreshes `latest_manager_continuity_generated` from disk and intentionally allows `generated != consumed`.
  - `status` and `fleet-status` still surface stale `manager_intent` / generated prompt truth from `manager-worker-launch-state.env`, even when a newer continuity file exists on disk.
- These two problems should stay separate in reasoning:
  - concurrent worker start is a runtime correctness / ownership bug
  - stale generated surface is a status alignment bug

## 2026-04-10 Followthrough Check

- The status-surface half is no longer open research:
  - commit `3ef222ec` on `develop` already landed the baseline/fleet generated-truth refresh
  - `bash docs/system/workspace/scripts/tests/test-freely-status-latest-generated-manager-continuity-surface` now passes on the current base
- The remaining unfinished worktree task is narrower than the original two-part packet:
  - keep attach/reuse behavior when a same-project supervisor is still inside bootstrap grace, even if process inspection is degraded
  - ensure `freely stop --project <same-project>` kills every discovered same-project supervisor rather than only the pid-file owner
  - preserve the stop marker correctly while another same-project supervisor is still cleaning up
- This means the active lane is now a runtime start/stop followthrough, not another status-surface alignment repair.

## Boundaries

- Keep this lane narrow:
  - do not redesign worker recovery policy
  - do not widen into generic restart-storm governance
  - do not reopen runtime evidence provenance / canonical absorption gate research
  - do not change the existing meaning of `generated != consumed` in `live-status`
- Safe scope:
  - add a per-project start serialization guard so concurrent `freely start --project <same-project>` calls cannot materialize multiple supervisors
  - keep later callers attach/reuse-friendly once the first start has acquired ownership
  - align `status` / `fleet-status` generated worker-prompt surface with the latest valid continuity file on disk, without pretending that consumption advanced

## Why Existing Owners Do Not Absorb This

- `20260330-2318--live-status-already-running-attach-regression` only covered false optimistic attach truth after manager attach reuse with missing AI.
- `20260328-0745--live-status-current-runtime-state-reconciliation` only covered read-time reconciliation of current live PIDs in `live-status`.
- `20260407-0603--runtime-evidence-provenance-and-canonical-absorption-gate` is explicitly research-only and does not own runtime start serialization.
- `watchdog-restart-storm-and-process-churn` surfaces churn but does not prevent same-project duplicate supervisor bootstrap.

## Candidate Shape

- One focused candidate is enough if its acceptance remains split:
  1. same-project concurrent `start` calls cannot create duplicate supervisors
  2. later same-project attach/stop cleanup paths do not reintroduce duplicate-supervisor churn once the start lock and generated-truth repair already exist on `develop`

## Preferred Fix Direction

- Add a project-local start lock rooted in `.freely/run/` and acquired before `ensure_no_active_supervisor_conflict()` plus `supervisor.pid` write.
- Lock must be robust against stale owners:
  - stale lock can be cleared if the recorded pid is dead or clearly unrelated
  - otherwise later start callers should wait briefly, then retry supervisor discovery / attach instead of racing into a second launch
- After the lock lands, `start_workcell_supervisor_async()` may stay simple; the correctness boundary belongs in `freely start`.
- The followthrough repair should stay narrow:
  - prefer bootstrap-in-flight attach before degraded dispatcher/watchdog repair tears down the hinted supervisor
  - on `freely stop`, discover and terminate all same-project supervisors, not just the first matching pid
  - only clear the stop marker when no other same-project supervisor is still alive

## Risks

- Over-eager stale-lock clearing could kill legitimate in-flight starts.
- Preserving a stale stop marker after the last supervisor exits could leave the project falsely stuck in stop mode.
- Killing only the pid-file owner while leaving sibling same-project supervisors alive would keep the original duplicate-supervisor incident operationally unresolved.
- Tests must prove the narrow invariant:
  - one `supervisor_started` event under concurrent same-project starts
  - degraded bootstrap grace prefers attach/reuse over partial-control-plane repair
  - stop terminates all discovered same-project supervisors for the project
