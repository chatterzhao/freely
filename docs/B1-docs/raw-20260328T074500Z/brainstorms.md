# Brainstorms - 20260328-0745--live-status-current-runtime-state-reconciliation

## Context

- observed symptom: `live-status` could report `activity_state: ai_active` while still showing `last_ai_state: down` and `last_exit_reason: starting`
- current truth split:
  - `activity_state` comes from current PID discovery
  - `last_*` fields come from persisted `workcell-state.env`
- risk: users and manager patrol can misread an active runtime as degraded, even though the project-owned AI process is live

## Boundary

- this line is a narrow repair inside the status/observability family
- it does not add JSON/watch/scoring surfaces
- it does not change recovery ownership or write-path semantics
- it only reconciles the `live-status` read surface toward confirmed current runtime truth

## Decision

- materialize as a small same-family issue with a new compliant lifecycle id
- keep the repair read-only:
  - lift `last_supervisor_state` / `last_ai_state` to `up` only when project-owned live PIDs are confirmed
  - collapse `last_exit_reason: starting` to `none` only when AI is already confirmed live
  - do not rewrite persisted state files during status reads
