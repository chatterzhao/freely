# Implementation Tasks: Manager keepalive kill -0 scanning

## Task summary

Add proactive `kill -0` scanning of launched worker PIDs to the manager keepalive loop. This ensures the manager detects dead worker processes within one keepalive cycle (~10–20s) instead of waiting 15+ minutes for the `mark_stale()` wall-clock timeout.

### Files to modify

| File | Change |
|------|--------|
| `docs/system/workspace/scripts/runtime/handoff.py` | Add `worker_pid` column migration; add `update_worker_pid` and bulk-fetch-launched CLI commands |
| `docs/system/workspace/scripts/runtime/freely` | Add `manager_scan_stale_worker_pids` function; integrate into keepalive loop; record PID at launch |

---

## T-1: Add `worker_pid` column to handoff DB schema

**File:** `docs/system/workspace/scripts/runtime/handoff.py`

**Change:**
1. In `init_db()` (line ~54–132), add `worker_pid` to the schema migration block:
   ```python
   ("worker_pid", "TEXT DEFAULT ''"),
   ```
   Add it alongside the existing migration columns (around line 103–113).

**Why:** The existing migration block already handles additive schema changes. No need to recreate the table.

**Acceptance:** After `init_db()`, `PRAGMA table_info(handoffs)` shows `worker_pid TEXT DEFAULT ''`.

---

## T-2: Add `update-worker-pid` CLI command to handoff.py

**File:** `docs/system/workspace/scripts/runtime/handoff.py`

**New function:**
```python
def update_worker_pid(handoff_id, worker_pid):
    """Record worker OS PID for kill -0 scanning."""
    conn = _connect()
    now = _now_utc()
    conn.execute(
        "UPDATE handoffs SET worker_pid=?, updated_at=? WHERE handoff_id=? AND status='launched'",
        (str(worker_pid), now, handoff_id))
    affected = cur.rowcount
    conn.commit()
    conn.close()
    return affected
```

**CLI subparser:**
```python
p_update_pid = sub.add_parser("update-worker-pid")
p_update_pid.add_argument("--handoff-id", required=True)
p_update_pid.add_argument("--worker-pid", required=True)
```

**Add to CLI dispatch:**
```python
elif args.cmd == "update-worker-pid":
    affected = update_worker_pid(args.handoff_id, args.worker_pid)
    print(f"ok affected={affected}")
```

**Acceptance:** `handoff.py update-worker-pid --handoff-id <id> --worker-pid 12345` updates the record.

---

## T-3: Add bulk-fetch-launched CLI command to handoff.py

**File:** `docs/system/workspace/scripts/runtime/handoff.py`

**New function:**
```python
def get_launched_workers_with_pids(raw_key=None):
    """Fetch all launched worker handoffs that have a worker_pid set."""
    conn = _connect()
    if raw_key:
        rows = conn.execute(
            "SELECT handoff_id, worker_pid, worktree, session_id, prompt_file FROM handoffs "
            "WHERE role='worker' AND status='launched' AND worker_pid != '' AND worker_pid IS NOT NULL "
            "AND raw_key=? ORDER BY created_at ASC",
            (raw_key,)).fetchall()
    else:
        rows = conn.execute(
            "SELECT handoff_id, worker_pid, worktree, session_id, prompt_file FROM handoffs "
            "WHERE role='worker' AND status='launched' AND worker_pid != '' AND worker_pid IS NOT NULL "
            "ORDER BY created_at ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
```

**CLI subparser:**
```python
p_launched = sub.add_parser("get-launched-pids")
p_launched.add_argument("--raw-key", default="")
```

**Add to CLI dispatch:**
```python
elif args.cmd == "get-launched-pids":
    rows = get_launched_workers_with_pids(args.raw_key or None)
    print(json.dumps(rows, indent=2, ensure_ascii=False))
```

**Acceptance:**
- Only returns `status='launched'` records with non-empty `worker_pid`
- With `--raw-key` filter, scoped to that key only
- Empty list when no matching records

---

## T-4: Record worker PID at launch time

**File:** `docs/system/workspace/scripts/runtime/freely`

**Location:** In `launch_worker_from_manager_prompt_if_needed`, after `_worker_pid` is captured and written to `ai.pid` (line ~11801–11811 for bridge launch, ~11774 for agent fallback).

**Change:**
For bridge launch (line ~11801):
```bash
  echo "$_worker_pid" > "$(run_dir_for_project "$target_project")/ai.pid"

+ # Record worker PID in handoff DB for kill -0 scanning
+ manager_record_worker_pid_for_launch "$target_project" "$_worker_pid"
```

For agent fallback (line ~11776):
```bash
  echo "$_worker_pid" > "$(run_dir_for_project "$target_project")/ai.pid"
+ manager_record_worker_pid_for_launch "$target_project" "$_worker_pid"
```

**New helper function:**
```bash
manager_record_worker_pid_for_launch() {
  local target_project="$1" worker_pid="$2"
  local freely_db handoff_id
  freely_db="$(freely_db_for_project "$target_project" 2>/dev/null || true)"
  [[ -f "$freely_db" ]] || return 0
  # Find the pending handoff for this worker's prompt
  prompt_file="$(latest_prompt_file_for_project "$target_project" 2>/dev/null || true)"
  [[ -n "$prompt_file" && -f "$prompt_file" ]] || return 0
  handoff_id="$(python3 -c "
import sqlite3
conn = sqlite3.connect('$freely_db')
row = conn.execute(
  \"SELECT handoff_id FROM handoffs WHERE prompt_file=? AND role='worker' AND status IN ('pending','launched') ORDER BY created_at DESC LIMIT 1\",
  ('$prompt_file',)).fetchone()
conn.close()
print(row[0] if row else '')
" 2>/dev/null || true)"
  [[ -n "$handoff_id" ]] || return 0
  python3 "$SELF_ROOT/docs/system/workspace/scripts/runtime/handoff.py" \
    --db "$freely_db" update-worker-pid \
    --handoff-id "$handoff_id" \
    --worker-pid "$worker_pid" >/dev/null 2>&1 || true
}
```

**Acceptance:** After launching a worker, `handoffs.worker_pid` for the corresponding record equals the actual OS PID.

---

## T-5: Implement `manager_scan_stale_worker_pids` function

**File:** `docs/system/workspace/scripts/runtime/freely`

**New function:**
```bash
manager_scan_stale_worker_pids() {
  local project="$1" freely_db raw_key scanned_count=0 marked_count=0
  freely_db="$(freely_db_for_project "$project" 2>/dev/null || true)"
  [[ -f "$freely_db" ]] || return 0
  raw_key="$(raw_key_for_project "$project" 2>/dev/null || true)"
  [[ -n "$raw_key" ]] || return 0

  local result
  result="$(python3 -c "
import sqlite3, os
from datetime import datetime, timezone
conn = sqlite3.connect('$freely_db')
rows = conn.execute(
  \"SELECT handoff_id, worker_pid FROM handoffs \"
  \"WHERE role='worker' AND status='launched' AND worker_pid != '' AND worker_pid IS NOT NULL \"
  \"AND raw_key=? ORDER BY created_at ASC\",
  ('$raw_key',)
).fetchall()
marked = []
scanned = len(rows)
for hid, pid_str in rows:
  if not pid_str or not pid_str.strip().isdigit():
    continue
  pid = int(pid_str.strip())
  try:
    os.kill(pid, 0)
  except OSError:
    marked.append(hid)
if marked:
  now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
  for hid in marked:
    conn.execute(
      \"UPDATE handoffs SET status='blocked', exit_kind='stale_pid', \"
      \"reason='Worker PID kill -0 failed, marking stale_pid', \"
      \"next_action='Manager: check worker worktree and re-dispatch', \"
      \"completed_at=?, updated_at=? \"
      \"WHERE handoff_id=? AND status='launched'\",
      (now, now, hid)
    )
conn.commit()
conn.close()
print(f'{scanned},{len(marked)}')
" 2>/dev/null || echo "0,0")"

  scanned_count="${result%,*}"
  marked_count="${result#*,}"
  [[ "$scanned_count" =~ ^[0-9]+$ ]] || scanned_count=0
  [[ "$marked_count" =~ ^[0-9]+$ ]] || marked_count=0

  if (( marked_count > 0 )); then
    log_warn "manager stale-pid scan: marked $marked_count stale worker(s) out of $scanned_count scanned"
    append_lifecycle_trace "$project" "L225" "manager_stale_pid_scan" \
      "scanned=$scanned_count" \
      "marked_stale=$marked_count" \
      "trigger=kill_zero_failed" \
      "next=re_evaluate_keepalive"
  fi
  return 0
}
```

**Acceptance:**
- Scans all launched handoffs with non-empty worker_pid for the project's raw_key
- `os.kill(pid, 0)` failure → marks `status='blocked'`, `exit_kind='stale_pid'`
- Skips records with empty worker_pid
- Skips non-launched statuses
- Returns 0 (never blocks keepalive chain)

---

## T-6: Integrate stale PID scan into keepalive loop

**File:** `docs/system/workspace/scripts/runtime/freely`

**Location:** In the manager keepalive decision chain, immediately before `manager_supervisor_waiting_on_active_workers` (line ~16472).

**Change:**
```bash
+ elif manager_supervisor_scan_stale_worker_pids "$project"; then
+   # Stale PIDs were detected and marked; fall through to re-evaluate
+   # (the function already marked handoffs as blocked/stale_pid;
+   #  subsequent keepalive checks will see updated active worker count)
+   :
  elif manager_supervisor_waiting_on_active_workers "$project" "$current_pid" "$current_ai_pid"; then
```

Wait — the scan function doesn't return useful exit codes. Better to restructure: call the scan unconditionally before the keepalive chain, not as a guard in the chain.

**Better approach:** Insert at the top of the keepalive block, after `same_tool_blocked` check and before the first `elif`:
```bash
+ # Scan launched workers for stale PIDs before keepalive decisions
+ manager_scan_stale_worker_pids "$project" || true
```

This is simpler and ensures the scan always runs regardless of which keepalive branch fires.

**Alternatively:** Keep the scan as a separate call near the start of the supervisor loop (after `load_session_state_or_defaults`, before the keepalive decision). This is even simpler:

In the supervisor while loop (~line 18974+), add:
```bash
+     # Scan for stale worker PIDs before keepalive decisions
+     if [[ "$(effective_runtime_role_for_project "$project")" == "manager" ]]; then
+       manager_scan_stale_worker_pids "$project" || true
+     fi
```

**Acceptance:** Stale PIDs are detected and marked within one keepalive cycle of the worker process dying.

---

## T-7: Write test scripts (see pre-tests.md)

Implement all P0 test scripts as standalone bash files and verify they pass:

1. `test-stale-pid-keepalive-worker-pid-column` — TC-1
2. `test-stale-pid-keepalive-record-worker-pid` — TC-2 (manual/integration)
3. `test-stale-pid-keepalive-kill-zero-detection` — TC-3
4. `test-stale-pid-keepalive-scan-marks-blocked` — TC-4
5. `test-stale-pid-keepalive-scan-isolates-completed` — TC-5
6. `test-stale-pid-keepalive-scan-idempotent` — TC-6
7. `test-stale-pid-keepalive-integration` — TC-7 (manual/integration)
8. `test-stale-pid-keepalive-live-worker-untouched` — TC-8
9. `test-stale-pid-keepalive-degraded-mode` — TC-9
10. `test-stale-pid-keepalive-mark-stale-complement` — TC-10
11. `test-stale-pid-keepalive-pid-persistence` — TC-11

---

## Task dependencies

```
T-1 (schema) → T-2 (CLI) → T-4 (record PID)
                    ↓
T-1 (schema) → T-3 (bulk fetch) → T-5 (scan function)
                                      ↓
T-4 + T-5 → T-6 (integration)
T-1 through T-5 → T-7 (tests)
```

T-1 (schema) is the single dependency for all downstream tasks. T-2 and T-3 are independent once T-1 is done. T-4 and T-5 are independent of each other. T-6 requires both T-4 and T-5.

## Effort estimate

| Task | Est. time | Complexity |
|------|-----------|------------|
| T-1: Schema migration | 5 min | Trivial |
| T-2: update-worker-pid CLI | 10 min | Low |
| T-3: bulk-fetch-launched CLI | 10 min | Low |
| T-4: Record PID at launch | 20 min | Medium (needs handoff_id resolution) |
| T-5: Manager scan function | 30 min | Medium |
| T-6: Integrate into keepalive | 10 min | Low |
| T-7: Test scripts | 45 min | Medium |
| **Total** | **~2 hours** | |
