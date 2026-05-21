# Pre-implementation Test Plan: Manager keepalive kill -0 scanning

## Test Infrastructure

Tests are standalone bash scripts under `docs/system/workspace/scripts/tests/`. They directly call Python functions or the shell functions being tested, using `set -euo pipefail` and manual pass/fail tallying.

## Test Cases

### TC-1: handoff DB schema migration adds `worker_pid` column

| Field | Value |
|-------|-------|
| **Type** | Unit (handoff.py `init_db`) |
| **Priority** | P0 (blocking) |
| **File** | `test-stale-pid-keepalive-worker-pid-column` |

**Steps:**
1. Create a temp SQLite DB with `handoff.py init`
2. Verify `worker_pid` column exists via `PRAGMA table_info(handoffs)`
3. Insert a handoff record
4. Update `worker_pid` to a test value
5. Verify readback matches

**Expected:**
- Column exists with `TEXT DEFAULT ''` type
- INSERT/UPDATE on `worker_pid` succeeds without affecting other columns

---

### TC-2: worker PID recorded at launch time

| Field | Value |
|-------|-------|
| **Type** | Integration (freely `launch_worker_from_manager_prompt_if_needed`) |
| **Priority** | P0 (blocking) |
| **File** | `test-stale-pid-keepalive-record-worker-pid` |

**Steps:**
1. Set up a minimal manager project with a prompt_file delegation
2. Insert a `pending` worker handoff in the handoff DB
3. Mock `launch_worker_from_manager_prompt_if_needed` to capture the `_worker_pid`
4. After launch, query the handoff DB for `worker_pid`

**Expected:**
- `worker_pid` in the handoff DB matches the actual OS PID of the launched background process
- `status` remains `launched`

---

### TC-3: kill -0 detects dead worker PID

| Field | Value |
|-------|-------|
| **Type** | Unit (Python `os.kill(pid, 0)`) |
| **Priority** | P0 (blocking) |
| **File** | `test-stale-pid-keepalive-kill-zero-detection` |

**Steps:**
1. Spawn a background child process, capture its PID
2. Verify `os.kill(pid, 0)` succeeds (process alive)
3. Kill the child process
4. Verify `os.kill(pid, 0)` raises `OSError` (EPERM or ESRCH)
5. Confirm the error is caught and handled (returns False)

**Expected:**
- Alive PID → `os.kill(pid, 0)` returns None (no error)
- Dead PID → OSError raised, caught by function → returns False

---

### TC-4: scan marks stale PID handoffs as blocked

| Field | Value |
|-------|-------|
| **Type** | Unit (handoff.py + Python scanning logic) |
| **Priority** | P0 (blocking) |
| **File** | `test-stale-pid-keepalive-scan-marks-blocked` |

**Steps:**
1. Create a temp handoff DB with multiple `launched` worker records:
   - Record A: `worker_pid=12345` (valid PID of a process that will be killed)
   - Record B: `worker_pid=` (empty — should be skipped)
   - Record C: `worker_pid=$$` (PID of the test process itself — alive)
2. Kill process with PID 12345 (or use 1 as a guaranteed-inaccessible PID for non-root)
3. Run the `manager_scan_stale_worker_pids` scanning logic
4. Query handoff records

**Expected:**
- Record A: `status='blocked'`, `exit_kind='stale_pid'`, `reason` contains "kill -0 failed"
- Record B: unchanged (empty worker_pid skipped)
- Record C: unchanged (PID is alive)

---

### TC-5: scan does NOT touch `consumed`, `completed`, `blocked` handoffs

| Field | Value |
|-------|-------|
| **Type** | Unit (isolation) |
| **Priority** | P1 |
| **File** | `test-stale-pid-keepalive-scan-isolates-completed` |

**Steps:**
1. Create a temp handoff DB with non-launched records, each having worker_pid=1 (inaccessible):
   - Record A: `status='completed'`, `worker_pid=1`
   - Record B: `status='blocked'`, `worker_pid=1`
   - Record C: `status='consumed'`, `worker_pid=1`
2. Run the scanning logic
3. Query all records

**Expected:**
- All records remain unchanged — `WHERE status='launched'` guard works

---

### TC-6: scan idempotent — already-blocked records not re-marked

| Field | Value |
|-------|-------|
| **Type** | Unit (idempotency) |
| **Priority** | P1 |
| **File** | `test-stale-pid-keepalive-scan-idempotent` |

**Steps:**
1. Create a handoff DB with a `blocked` stale_pid record (already marked)
2. Run scanning logic
3. Verify no UPDATE count for the already-blocked record

**Expected:**
- No changes; `updated_at` unchanged

---

### TC-7: keepalive chain integration — stale workers don't block supervisor stop

| Field | Value |
|-------|-------|
| **Type** | Integration (freely keepalive loop) |
| **Priority** | P0 (blocking) |
| **File** | `test-stale-pid-keepalive-integration` |

**Steps:**
1. Set up a manager project with a delegated worker handoff in `launched` status
2. Set `worker_pid` to a dead PID
3. Run the manager keepalive decision chain (`manager_should_keep_supervisor`)
4. Verify the stale PID is detected and the supervisor is NOT kept alive for "waiting on active workers"
5. Verify the handoff DB is updated with `stale_pid` before the decision returns

**Expected:**
- `manager_supervisor_waiting_on_active_workers` returns 1 (because scan was integrated or called first)
  Wait — actually the opposite: after scanning, the stale worker is marked, so `active_worker_count` becomes 0, and `waiting_on_active_workers` returns 1 (no active workers), meaning the supervisor can stop.
  
  Let me re-describe:
  
- After scan marks the stale PID, `manager_supervisor_waiting_on_active_workers` returns 1 (not waiting)
- The supervisor moves to the next keepalive check or stop decision
- The handoff DB shows `status='blocked'`, `exit_kind='stale_pid'`

---

### TC-8: live worker not mis-marked by scan

| Field | Value |
|-------|-------|
| **Type** | Integration (false positive prevention) |
| **Priority** | P0 (blocking) |
| **File** | `test-stale-pid-keepalive-live-worker-untouched` |

**Steps:**
1. Create a handoff DB with a `launched` worker whose `worker_pid` is the test script's own PID (alive)
2. Run scanning logic
3. Verify the record remains `launched` with no exit_kind

**Expected:**
- Record unchanged: `status='launched'`, `exit_kind=''`

---

### TC-9: scan with process_inspection_available=false (degraded mode)

| Field | Value |
|-------|-------|
| **Type** | Integration (degraded path) |
| **Priority** | P1 |
| **File** | `test-stale-pid-keepalive-degraded-mode` |

**Steps:**
1. Set `process_inspection_available` to return false (or simulate via `ps` unavailability)
2. Create a handoff DB with a launched worker whose `worker_pid` is dead
3. Verify the scanning function still works (it uses Python `os.kill`, not `ps`)

**Expected:**
- Scanning succeeds regardless of `process_inspection_available`
- Stale PID is marked correctly
- The `kill -0` approach is independent of the `/proc` filesystem availability

---

### TC-10: mark_stale() soft-timeout still works after kill -0 scan

| Field | Value |
|-------|-------|
| **Type** | Verification (complementary check) |
| **Priority** | P1 |
| **File** | `test-stale-pid-keepalive-mark-stale-complement` |

**Steps:**
1. Create a handoff DB with a `launched` worker whose PID is alive (alive)
2. Set `last_activity_at` to 30 minutes ago
3. Run `mark_stale()` with 15-minute threshold
4. Verify the record is marked `blocked` by the timeout mechanism

**Expected:**
- `mark_stale()` continues to catch "process alive but stuck" workers
- No regression from the new kill -0 scan

### TC-11: worker_pid survives handoff re-entry / re-launch

| Field | Value |
|-------|-------|
| **Type** | Integration (state persistence) |
| **Priority** | P1 |
| **File** | `test-stale-pid-keepalive-pid-persistence` |

**Steps:**
1. Create handoff DB with a worker record
2. Set `worker_pid` to a test value
3. Simulate a session rotation (write/read handoff file)
4. Verify `worker_pid` is still present after re-load

**Expected:**
- `worker_pid` column value preserved across normal handoff operations

---

## Test execution

Run all tests:

```bash
for t in docs/system/workspace/scripts/tests/test-stale-pid-keepalive-*; do
  echo "=== $(basename "$t") ==="
  bash "$t" || true
done
```

Exit on failure: P0 tests must pass before merge. P1 tests document known behavior and may be addressed in follow-up.
