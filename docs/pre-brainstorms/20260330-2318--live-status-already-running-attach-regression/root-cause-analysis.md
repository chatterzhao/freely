# Root Cause Analysis - Live-status Already-Running-Attach Regression

## Date
2026-03-31

## Status
Write/read mismatch identified; trigger mechanism still needs focused repro

## Summary

The regression family currently proven is narrower than the original draft. What is proven is:

1. `start_project_runtime()` can write optimistic `already_running_attach` state
2. that attach-only write does not emit a matching runtime event
3. `live-status` does not reconcile that optimistic state downward when no current project-owned PID exists

The still-unproven part is the exact trigger that caused the stale attach write observed on `develop`.

This creates a false-positive status scenario where:

1. A supervisor exits cleanly and writes `down/down` state
2. The `supervisor.pid` file is not cleaned up (or is rewritten later)
3. `ensure-manager --watch` attempts bootstrap
4. `resolve_active_supervisor_pid_for_start()` finds a PID (from file or discovery)
5. `ensure_no_active_supervisor_conflict()` returns 10 (attach success)
6. `start_project_runtime()` writes `running/up/up/already_running_attach` and returns
7. No runtime event is emitted for this attach-only case
8. `live-status` later trusts this optimistic state because no current PID exists to reconcile

## Code Path Analysis

### Entry Point: `start_project_runtime()` (line 5435)

```bash
start_project_runtime() {
  local project="$1"
  # ... setup ...
  
  local supervisor_conflict_rc=0
  ensure_no_active_supervisor_conflict "$project" "$sup_pid_file" "$child_pid_file" "1" || supervisor_conflict_rc=$?
  
  # PROBLEM: This writes optimistic state without verification
  if [[ "$supervisor_conflict_rc" -eq 10 ]]; then
    write_workcell_state "$project" "running" "up" "up" "already_running_attach"
    return 0  # Returns immediately, no supervisor loop entered
  fi
  # ...
}
```

### Detection: `ensure_no_active_supervisor_conflict()` (line 5394)

```bash
ensure_no_active_supervisor_conflict() {
  local project="$1" sup_pid_file="$2" child_pid_file="$3" allow_attach="${4:-0}"
  local old_pid=""
  old_pid="$(resolve_active_supervisor_pid_for_start "$project" "$sup_pid_file")"
  
  if [[ -n "$old_pid" ]]; then
    if [[ "$allow_attach" == "1" ]]; then
      # ... some checks ...
      
      # PROBLEM: Returns 10 if old_pid is found, assuming it's valid
      log_info "project runtime/control-plane already up; reusing supervisor pid=$old_pid"
      return 10
    fi
    # ...
  fi
  # ...
}
```

### PID Resolution: `resolve_active_supervisor_pid_for_start()` (line 5370)

```bash
resolve_active_supervisor_pid_for_start() {
  local project="$1" sup_pid_file="$2"
  local candidate_pid="" excluded_pids=""
  excluded_pids="${BASHPID:-$$},${PPID:-}"
  
  # First try: read from supervisor.pid file
  if [[ -f "$sup_pid_file" ]]; then
    candidate_pid="$(cat "$sup_pid_file" 2>/dev/null || true)"
    if valid_supervisor_pid_for_project "$project" "$candidate_pid"; then
      printf '%s\n' "$candidate_pid"
      return 0
    fi
    # ... cleanup stale pid ...
  fi

  # Second try: discover from process table
  candidate_pid="$(discover_supervisor_pid "$project" "$excluded_pids")"
  if valid_supervisor_pid_for_project "$project" "$candidate_pid"; then
    log_warn "recovered live project supervisor after supervisor.pid drift: $candidate_pid"
    printf '%s\n' "$candidate_pid" >"$sup_pid_file"
    printf '%s\n' "$candidate_pid"
  fi
}
```

## Root Causes

### 1. Optimistic State Write Without Verification

When `ensure_no_active_supervisor_conflict()` returns 10, `start_project_runtime()` immediately writes:
```bash
write_workcell_state "$project" "running" "up" "up" "already_running_attach"
```

This is optimistic because:
- It assumes the detected PID is a healthy supervisor
- It doesn't verify the supervisor is actually in its main loop
- It doesn't check if the supervisor's child AI process exists
- It doesn't emit a runtime event for observability

### 2. No Runtime Event for Attach-Only Case

The attach-only path returns immediately without emitting a runtime event:
```bash
if [[ "$supervisor_conflict_rc" -eq 10 ]]; then
  write_workcell_state "$project" "running" "up" "up" "already_running_attach"
  return 0  # No event emitted
fi
```

This breaks the observability contract where every state change should have a corresponding runtime event.

### 3. One-Way Read Reconciliation

`cmd_live_status()` only reconciles stale persisted state upward:

- if a current project-owned supervisor PID exists, it upgrades `last_supervisor_state` to `up`
- if a current project-owned AI PID exists, it upgrades `last_ai_state` to `up`
- absence of a PID does not downgrade previously persisted optimistic state

This means an optimistic attach write can outlive the real process truth on the status surface.

### 4. Trigger Mechanism Still Not Reproduced

The exact trigger that produced the observed stale attach write is still not pinned down.

Possible candidates:
- a same-project concurrent or delayed `start` / `ensure-manager` bootstrap window
- attach reuse of a short-lived supervisor process that soon exits
- a still-owned but no-longer-healthy process window

Not yet proven:
- generic unrelated PID reuse
- cleanup routinely leaving stale `supervisor.pid`

## Evidence from Production

From the frozen evidence in `brainstorms.md`:

1. **Runtime event timeline stopped earlier than state writes**
   - `.freely/logs/runtime-events.log` last mtime: `2026-03-30 23:00:25 PDT`
   - Last event: `supervisor_cleanup ... desired_state=stopped exit_reason=operator_stop`

2. **Persisted state changed later without matching runtime events**
   - `.freely/run/workcell-state.env` mtime: `2026-03-30 23:17:30 PDT` (17 minutes later!)
   - Content: `running/up/up/already_running_attach`

3. **Process truth disagrees with persisted truth**
   - No live `runtime/freely start --project <root>` process
   - `.freely/run/ai.pid` is absent
   - Only watcher processes are alive

4. **Read surfaces disagree**
   - `fleet-status` correctly reports `sup=none ai=none`
   - `live-status` incorrectly reports `last_supervisor_state=up last_ai_state=up`

## Design Directions

### Option 1: Make Attach Writes Less Optimistic (Conservative)

Before writing `already_running_attach`, verify:
1. The supervisor PID is alive
2. The supervisor is actually healthy enough to be reused
3. The supervisor owns the expected project path
4. If `last_ai_state=up` is going to be written, the AI child process exists and is valid

```bash
if [[ "$supervisor_conflict_rc" -eq 10 ]]; then
  # Verify supervisor is truly healthy before claiming attach success
  if ! verify_supervisor_health "$project" "$old_pid" "$child_pid_file"; then
    log_warn "supervisor pid=$old_pid detected but health check failed; falling back to fresh start"
    supervisor_conflict_rc=0
  else
    write_workcell_state "$project" "running" "up" "up" "already_running_attach"
    append_runtime_event "$project" "supervisor_attach_reuse" "supervisor_pid=$old_pid"
    return 0
  fi
fi
```

### Option 2: Downgrade Attach State to Soft/Stale (Defensive)

Treat `already_running_attach` as a soft hint rather than hard truth:
1. Write a different exit reason like `attach_pending_verification`
2. Let `live-status` reconcile this against current PIDs
3. If no current supervisor PID exists, downgrade to `down/down`

```bash
if [[ "$supervisor_conflict_rc" -eq 10 ]]; then
  write_workcell_state "$project" "running" "up" "up" "attach_pending_verification"
  append_runtime_event "$project" "supervisor_attach_attempt" "supervisor_pid=$old_pid"
  return 0
fi
```

Then in `live-status`:
```bash
if [[ "$LAST_EXIT_REASON" == "attach_pending_verification" ]]; then
  # Reconcile against current PIDs
  if ! current_supervisor_pid_exists; then
    LAST_SUPERVISOR_STATE="down"
    LAST_AI_STATE="down"
    LAST_EXIT_REASON="attach_verification_failed"
  fi
fi
```

### Option 3: Always Emit Runtime Event for Attach (Observability)

Ensure every state change has a corresponding runtime event:

```bash
if [[ "$supervisor_conflict_rc" -eq 10 ]]; then
  append_runtime_event "$project" "supervisor_attach_reuse" \
    "supervisor_pid=$old_pid" \
    "attach_time=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  write_workcell_state "$project" "running" "up" "up" "already_running_attach"
  return 0
fi
```

This allows patrol to distinguish:
- Real supervisor loop activity (has recent events)
- Optimistic attach reuse (has attach event but no subsequent activity)

### Option 4: Focused Trigger Repro Before Fix Selection

Before choosing between write-side hardening and read-side downgrade, reproduce one of these concrete triggers in a focused harness:

1. same-project concurrent `start` / attach race
2. attach to a still-live supervisor that has no live AI yet
3. attach to a soon-to-exit supervisor where no subsequent runtime event lands

## Recommended Fix

Current recommendation is to delay implementation choice until the trigger is reproduced.

The strongest currently supported conclusions are:

1. attach-only writes are too optimistic for their current observability contract
2. `live-status` intentionally avoids rewriting historical state downward, which makes this family visible
3. any fix must preserve the valid attach-reuse contract already covered by `test-freely-project-command-semantics`

## Next Steps

1. Build a focused repro that exercises the real `start_project_runtime()` attach path, not a hand-written symptom simulation
2. Distinguish "same-project short window attach" from "bad PID ownership match"
3. After the trigger is reproduced, decide whether repair belongs on write-side gating, read-side downgrade, or both
4. Keep existing valid attach semantics and stale-ownership protections passing
5. Update documentation for attach semantics

## Related Issues

- `I-20260328-0745-A`: Live-status current runtime state reconciliation (fixed the opposite direction)
- This regression is the inverse: persisted state is stale optimistic, not stale pessimistic
