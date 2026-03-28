# PRD: live-status-current-runtime-state-reconciliation-governance

## Problem

`live-status` can mix current runtime PID truth with stale persisted `workcell-state.env` fields, producing an internally contradictory surface during active runtime execution.

## Product Goal

Keep `live-status` self-consistent as the current-state entrypoint without changing the runtime write-path or recovery ownership model.

## Requirements

1. Lift `last_supervisor_state` / `last_ai_state` to `up` only when project-owned live PIDs are confirmed.
2. Rewrite `last_exit_reason: starting` to `none` only when the AI PID is already confirmed live.
3. Do not mutate persisted state files during `live-status` reads.
4. Preserve watchdog-only and manager-recovery behavior.

## Non-Goals

1. No new JSON or watch surface.
2. No supervisor lifecycle rewrite.
3. No broad status-family redesign.

## Success Criteria

- `live-status` output is internally consistent during active runtime execution.
- The fix remains narrow and read-only.
- Existing focused recovery/status tests still pass.
