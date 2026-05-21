# PRD: Manager keepalive kill -0 scanning for stale worker PIDs

## Problem

When a worker AI process dies silently (e.g., segfault, OOM, SIGKILL, bridge disconnect without clean handoff), the manager's keepalive loop does not detect the death. The handoff DB retains the worker record as `status='launched'`, the manager's worker count cache remains positive, and the supervisor waits indefinitely for worker completion. Only the 15-minute wall-clock `mark_stale()` timeout (based on `last_activity_at`) eventually resolves the blockage.

This causes cascading fleet stalls: workers that should be replaced are not, pending delegations are queued but never retried, and closeout worktrees block.

### Root cause

Worker liveness is checked via two mechanisms, both with gaps:

1. **Process inspection path** (`process_inspection_available` = true): `count_active_running_workers_for_manager_project` iterates worktrees and does `kill -0` on each worker's `ai.pid`/`supervisor.pid`. *But* this only produces a count — it does NOT update the handoff DB when a stale PID is discovered.

2. **Degraded path** (`process_inspection_available` = false): `manager_active_running_worker_count_hint_for_project` reads a cached count from `manager-worker-launch-state.env`. This cache is never invalidated by PID death — it only changes via `manager_worker_launch_state_reconcile_prompt_liveness` reconciliation, which can detect terminal workers but does not propagate to the handoff DB.

In both paths: the handoff DB record (`handoffs` table) stays at `status='launched'` forever when a worker dies without producing an exit contract. The `mark_stale()` function only uses `last_activity_at` wall-clock timeout (15 min default) — it does not perform active `kill -0` scanning.

## Scope

### In scope (sub-problem 1)

- Add `worker_pid` column to the `handoffs` table to track the OS PID of launched workers
- Record worker PID in the handoff DB at launch time in `launch_worker_from_manager_prompt_if_needed`
- Add a `manager_scan_stale_worker_pids` function that queries all `status='launched'` worker handoffs for the current raw_key and performs `kill -0` on each worker PID
- `kill -0` fails (process not found) → update handoff to `status='blocked'`, `exit_kind='stale_pid'`, with a descriptive `reason` field
- `kill -0` succeeds → no action (the existing `mark_stale()` soft-timeout handles inactivity)
- Integrate the scan into the manager's keepalive decision loop, called before `manager_supervisor_waiting_on_active_workers`
- Compatible with `consumed`, `blocked`, `completed` handoff states — only `launched` records are scanned

### Out of scope (sub-problem 2, deferred)

- Worker ACP init timeout self-healing (to C-20260519T015638Z-A coordination)

## Design

### 1. handoffs table: add `worker_pid` column

```sql
ALTER TABLE handoffs ADD COLUMN worker_pid TEXT DEFAULT '';
```

Migrated via the existing schema migration block in `handoff.py`'s `init_db()`.

### 2. Record PID at worker launch time

In `launch_worker_from_manager_prompt_if_needed` (freely, ~line 11801–11811), after the worker process is started and `_worker_pid` is captured:

```bash
# Record worker PID in handoff DB for kill -0 scanning
python3 "$SELF_ROOT/docs/system/workspace/scripts/runtime/handoff.py" \
  --db "$freely_db" update-worker-pid \
  --handoff-id <handoff_id> \
  --worker-pid "$_worker_pid"
```

The handoff_id is obtained from the worker handoff created when the prompt was delegated. The function must resolve the prompt_file to the handoff record.

### 3. New scanning function `manager_scan_stale_worker_pids`

```bash
manager_scan_stale_worker_pids() {
  local project="$1" freely_db
  freely_db="$(freely_db_for_project "$project")"
  [[ -f "$freely_db" ]] || return 0

  # Query launched worker handoffs where worker_pid is set
  python3 -c "
import sqlite3, os
conn = sqlite3.connect('$freely_db')
rows = conn.execute(
  \"SELECT handoff_id, worker_pid, worktree FROM handoffs \"
  \"WHERE role='worker' AND status='launched' AND worker_pid != ''\"
).fetchall()
stale_ids = []
for hid, pid, wt in rows:
  pid_int = int(pid) if pid.isdigit() else 0
  if pid_int == 0:
    continue
  try:
    os.kill(pid_int, 0)  # kill -0
  except OSError:
    stale_ids.append((hid, pid, wt))
for hid, pid, wt in stale_ids:
  conn.execute(
    \"UPDATE handoffs SET status='blocked', exit_kind='stale_pid', \"
    \"reason=?, completed_at=?, updated_at=? \"
    \"WHERE handoff_id=? AND status='launched'\",
    (f'Worker PID {pid} is dead (kill -0 failed). worktree={wt}',
     datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
     datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
     hid)
  )
conn.commit()
conn.close()
" 2>/dev/null || true
}
```

### 4. Integration point

Inject the scan into the manager keepalive loop. The most natural location is within `manager_supervisor_waiting_on_active_workers` (before the count check) OR as a new `elif` guard in the main keepalive chain (~line 16472), immediately before the current `manager_supervisor_waiting_on_active_workers` check:

```bash
elif manager_scan_stale_worker_pids "$project"; then
  # Some stale PIDs were found and marked; re-evaluate this cycle
  # (fall through to let the next checks see the updated state)
```

Alternatively, integrate the scan inside `manager_supervisor_waiting_on_active_workers` so that stale workers are flushed from the count before the keepalive decision.

### 5. Compatibility

- `consumed`/`blocked`/`completed` handoffs: `WHERE status='launched'` ensures no effect
- `mark_stale()` soft-timeout: remains active as a complementary check (catches workers where process is alive but stuck)
- `mark_stale_as_failed()` in `worker-store.py` : not changed, still uses wall-clock timeout as before
- The scan is idempotent: if a handoff is already `blocked`, the query skips it

## Dependencies

- None. The `os.kill(pid, 0)` call is Python standard library (POSIX `kill -0`).
- Requires that the manager process has permission to signal the worker process. Under normal operation (same user, same session), this holds.
- For cross-container scenarios (future), the scan will return `OSError` and mark stale — which is the correct behavior since if we can't reach the PID, it's effectively dead.

## Open Questions

- **handoff_id resolution at launch**: The exact mechanism to link the launched worker process to the correct handoff_id needs verification. Currently, the worker prompt is delegated and a handoff record is inserted before `launch_worker_from_manager_prompt_if_needed` is called. The prompt_file identifies the delegation, and the handoff DB can be queried by `prompt_file` + `status='pending'` to find the correct record.
- **`worker_pid` vs existing `session_id` field**: The `session_id` field in `handoffs` stores the Claude session ID, not the OS PID. A new `worker_pid` column is cleaner than repurposing `session_id`.
