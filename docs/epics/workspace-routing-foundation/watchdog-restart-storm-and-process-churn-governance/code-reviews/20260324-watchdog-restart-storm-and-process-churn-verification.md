# Code Review: watchdog-restart-storm-and-process-churn-governance
- issue_id: `I-20260324-0405`

## Result

- verification passed
- restart storm / process churn signal is now persisted in `session-state.env`, surfaced by `live-status` / `fleet-status`, and kept out of `workcell-state.env`
- watchdog no longer blind-relaunches through a short restart storm window; it emits a manager bootstrap handoff and enters low-frequency observation
- manager/auto-loop remains the owner of dead-loop or thrash judgement; runtime only emits signal and escalation context

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-restart-storm-defers-blind-relaunch`
- `bash docs/system/workspace/scripts/tests/test-freely-restart-storm-status-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
- `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-log-defers-to-watchdog`
- `./bin/governance-check`

## What Changed

1. `runtime/freely` now tracks restart storm windows in a run-dir window file instead of fragile in-memory counters.
2. `session-state.env` now persists restart storm window, count, peak, signal time, signal reason, escalation time, and escalation target.
3. watchdog signal hits now write a `manager_bootstrap_handoff`, reset blind relaunch pressure, and enter low-frequency observation.
4. `live-status` / `fleet-status` now expose restart storm summaries for supervisor patrol and human interruption.
5. `workcell-state.env` intentionally remains free of restart storm counters to preserve the contract that it only mirrors workcell lifecycle state.

## Remaining Lifecycle

- the issue is complete for this batch
- this worktree is not delete-ready until merge, cleanup evidence, and retirement gating are finished
