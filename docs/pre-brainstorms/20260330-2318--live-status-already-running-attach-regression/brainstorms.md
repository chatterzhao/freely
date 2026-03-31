# Brainstorms - 20260330-2318--live-status-already-running-attach-regression

## Context

- observed symptom on `develop`:
  - `./bin/freely fleet-status --project <root>` reports `develop | sup=none | ai=none`
  - `./bin/freely live-status --project <root>` simultaneously reports:
    - `activity_state: supervising_with_pending_intake`
    - `last_supervisor_state: up`
    - `last_ai_state: up`
    - `last_exit_reason: already_running_attach`
- current process truth:
  - only `ensure-manager --watch` and `ensure-interruption-dispatch --watch` are alive
  - there is no live `runtime/freely start --project <root>` process
  - `.freely/run/ai.pid` is absent
- current persisted state truth:
  - `.freely/run/workcell-state.env` keeps being rewritten to `running/up/up/already_running_attach`
  - `.freely/run/supervisor.pid` is rewritten with dead PIDs

## Why This Is Not The Same Old Bug

`20260328-0745--live-status-current-runtime-state-reconciliation` fixed one direction of stale mixing:

- active AI was real
- persisted `last_ai_state` was stale `down`
- `live-status` needed a read-time lift toward confirmed live PIDs

This regression is the inverse direction:

- no live supervisor/AI exists for the project runtime
- persisted `workcell-state.env` still claims `up/up`
- `live-status` now surfaces that stale optimistic state because there is no current PID to reconcile against

So this is not just a reopen of the old fix. It is a new regression family around false `already_running_attach` writeback and stale optimistic runtime truth.

## Frozen Evidence

### 1. Runtime event timeline stopped earlier than state writes

- `.freely/logs/runtime-events.log` last mtime: `2026-03-30 23:00:25 PDT`
- last event recorded:
  - `2026-03-31T06:00:25Z event=supervisor_cleanup ... desired_state=stopped exit_reason=operator_stop`

### 2. Persisted state changed later without matching runtime events

- `.freely/run/workcell-state.env` mtime: `2026-03-30 23:17:30 PDT`
- `.freely/run/supervisor.pid` mtime: `2026-03-30 23:17:30 PDT`
- content:
  - `DESIRED_RUNTIME_STATE="running"`
  - `LAST_SUPERVISOR_STATE="up"`
  - `LAST_AI_STATE="up"`
  - `LAST_EXIT_REASON="already_running_attach"`
- `.freely/run/supervisor.pid` currently contains a dead PID

### 3. Process truth disagrees with persisted truth

- live watcher processes:
  - `.freely/run/ensure-manager.pid` -> active `ensure-manager --watch`
  - `.freely/run/interruption-dispatch.pid` -> active `ensure-interruption-dispatch --watch`
- absent runtime processes:
  - no live `runtime/freely start --project <root>`
  - no live AI process for this project

### 4. Read surfaces disagree

- `fleet-status` derives `sup=none ai=none`
- `live-status` still surfaces `last_supervisor_state=up`, `last_ai_state=up`, `last_exit_reason=already_running_attach`

That means the problem is not just one bad output command. There is a write/read contract gap between:

- `ensure-manager` / `start_project_runtime`
- `workcell-state.env`
- `supervisor.pid`
- `live-status`
- `fleet-status`

## Narrow Suspected Path

`docs/system/workspace/scripts/runtime/freely` currently contains this write path:

- `start_project_runtime()`
- `ensure_no_active_supervisor_conflict(... allow_attach=1 )`
- if that returns `10`, write:
  - `write_workcell_state "$project" "running" "up" "up" "already_running_attach"`
  - then return without entering the normal supervisor loop

This is lawful only if a real project-owned supervisor is currently alive.

Current suspicion:

1. `ensure-manager --watch` repeatedly attempts manager bootstrap
2. one of those attempts decides `already_running_attach`
3. it rewrites `workcell-state.env` and `supervisor.pid`
4. the supervisor it attached to is already gone, or the detection was too weak / racy
5. no fresh `runtime-events.log` line is emitted for that attach-only writeback
6. `live-status` later trusts the optimistic persisted state because no current PID exists to reconcile downward

## Open Questions

1. Why is `already_running_attach` being written after the last recorded `supervisor_cleanup`?
2. Is `ensure_no_active_supervisor_conflict()` racing against a short-lived `freely start` child, or is `discover_supervisor_pid()` matching the wrong process window?
3. Should attach-only success be allowed to rewrite `last_ai_state=up` when there is no confirmed project AI PID?
4. Should attach-only state writes emit a runtime event so patrol can distinguish real supervisor loop activity from optimistic reuse?
5. Should `live-status` treat persisted `already_running_attach` as soft/stale unless a current supervisor or AI PID is still confirmed?

## Boundary

- do not patch yet
- first treat this as a focused status/control-plane regression
- avoid broadening into generic observability redesign
- likely same-family with the existing `live-status` / manager-stall / current-state contract cluster, but not yet proven to belong to one existing owner issue
