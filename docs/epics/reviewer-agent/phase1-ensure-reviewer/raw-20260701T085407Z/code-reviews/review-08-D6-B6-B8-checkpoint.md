# Code Review 08: D6+B6+B8 Checkpoint

- issue_id: I-20260701T085407Z-A

**Reviewer**: Claude Code
**Date**: 2026-07-01
**Branch**: fix/raw-20260701T085407Z-reviewer-a2a-integration
**Focus**: `_notify_sse` is_global flag, `_restore_tasks` SSE broadcast, agent_working migration files

---

## Verdict: NEEDS_FIX

2 HIGH, 2 MEDIUM, 4 LOW findings. The raw_key format inconsistency is systemic and will cause lookup failures across multiple callers.

---

## Finding H1 [HIGH]: raw_key format inconsistency between agent_working writes and reads

**File**: Multiple files
**Files affected**: `pr-review-guarded`, `task-lifecycle-scan.py`, `wt-close`, `watchdog_sse.py`, `freely-cycle`, `freely_db_manager.py`
**Type**: Data format inconsistency

### Description

There are two conflicting conventions for raw_key format across the codebase:

**Convention A (no prefix, just timestamp)**: Used by A2A task metadata and agent_working INSERT paths:
- `freely-cycle` (line 94): `agent_list_by_raw_key("{project}", "{rk}")` where `rk` comes from `a2a_tasks.raw_key` — just timestamp
- `freely-cycle` (line 100): `agent_assign("{project}", "{rk}", "reviewer", rid)` — stores just timestamp
- `watchdog_sse.py` `_handle_needs_reviewer` (line 95/109): `raw_key = metadata.get("raw_key", "")` then `agent_assign(project, raw_key, ...)` — stores just timestamp
- `a2a_server.py` `_tasks_endpoint` POST (line 689): `"raw_key": body.get("raw_key", ...)` — stores whatever the caller sends
- `freely-review` (line 176): `--raw-key "$raw_key"` where `$raw_key` is timestamp-only (from branch name extraction `grep -oE '[0-9]{8}T[0-9]{6}Z'`)

**Convention B (with "raw-" prefix)**: Used by agent_working READ paths:
- `pr-review-guarded` (lines 39, 226): `agent_list_by_raw_key('$ROOT_DIR', 'raw-'+rk)` — **adds prefix**
- `task-lifecycle-scan.py` (line 516): `agent_list_by_raw_key(str(project), f"raw-{raw_key}")` — **adds prefix**
- `wt-close` (line 1089): `agent_list_by_raw_key('$_dev_wt', 'raw-${_tp_raw_key}')` — **adds prefix**

**Impact**: The agent_working table stores raw_key without the "raw-" prefix (Convention A), but three out of five query sites add the "raw-" prefix (Convention B). These three sites will never find matching rows in the agent_working table. The agent_working migration is partially non-functional.

### Root cause

The canonical format in the codebase for file paths is `raw-{key}` (e.g., `docs/issues/raw-20260629T.../issue.md`). But the A2A metadata flow uses just `{key}` (extracted from branch names with `grep -oE '[0-9]{8}T[0-9]{6}Z'`). The agent_working table inherits the A2A metadata format, but the query sites add the document path prefix.

### Fix

Standardize on one format. The `raw-{key}` format (with prefix) is more explicit and matches document paths. Two options:

**Option A** (recommended): Add "raw-" prefix at INSERT time in `watchdog_sse.py` and `freely-cycle`, and keep "raw-" in reads.

In `watchdog_sse.py` `_handle_needs_reviewer` (line 91, 95, 109):
```python
raw_key = metadata.get("raw_key", "")
```
→ Change to:
```python
raw_key_raw = metadata.get("raw_key", "")
raw_key = f"raw-{raw_key_raw}" if raw_key_raw and not raw_key_raw.startswith("raw-") else raw_key_raw
```

In `freely-cycle` (line 94, 100):
```python
row = agent_list_by_raw_key("{project}", "{rk}")
...
agent_assign("{project}", "{rk}", "reviewer", rid)
```
→ Prefix `rk` with "raw-" before using in agent_working calls.

**Option B**: Remove "raw-" prefix from all query sites. This is simpler but less explicit.

---

## Finding H2 [HIGH]: asyncio.Queue cross-event-loop access in _restore_tasks D6 SSE broadcast

**File**: `docs/system/workspace/scripts/runtime/a2a/a2a_server.py`
**Lines**: 542-554
**Type**: Thread-safety / Runtime error

### Description

`_restore_tasks()` is a synchronous method launched via `threading.Thread(target=self._restore_tasks, ...)` at line 807. The D6 section (lines 542-554) calls:

```python
_asyncio.run(self._notify_sse("__system__", "restore_complete", event_data, is_global=True))
```

`_asyncio.run()` creates a NEW event loop in the background thread. Inside `_notify_sse`, `await q.put(...)` is called on `asyncio.Queue` objects stored in `self._sse_subscribers`. These queues were created in the MAIN event loop (by the Starlette SSE endpoint handlers `_global_task_stream_endpoint` and `_task_stream_endpoint`).

In Python 3.12+, `asyncio.Queue` stores a reference to its creating event loop and raises `RuntimeError` when a coroutine from a different loop tries to `await put()`. In Python 3.10-3.11, this works by accident but is undefined behavior.

The `except Exception: pass` at line 553 swallows the error silently. The restore-complete SSE broadcast NEVER reaches global subscribers.

### Impact

Watchdog never receives the `restore_complete` event after an A2A server restart. This breaks the recovery notification chain.

### Fix

Use `asyncio.run_coroutine_threadsafe()` to schedule the coroutine on the main event loop:

```python
# D6: push restore-complete SSE event
if restored > 0 or failed > 0:
    try:
        import asyncio as _asyncio6, json as _json6
        event_data = {
            "state": "restore_complete",
            "restored": restored, "failed": failed,
            "notifications_count": len(notifications)
        }
        # Get the main event loop
        try:
            main_loop = _asyncio6.get_event_loop()
        except RuntimeError:
            main_loop = _asyncio6.new_event_loop()
            _asyncio6.set_event_loop(main_loop)
        if main_loop.is_running():
            _asyncio6.run_coroutine_threadsafe(
                self._notify_sse("__system__", "restore_complete", event_data, is_global=True),
                main_loop
            )
        else:
            _asyncio6.run(self._notify_sse(
                "__system__", "restore_complete", event_data, is_global=True))
    except Exception:
        pass
```

Note: This requires `main_loop` to be stored or accessible. A simpler approach is to store the main event loop reference at startup:

```python
# In __init__ or start():
self._main_loop = asyncio.get_event_loop()
```

Then in D6:
```python
future = asyncio.run_coroutine_threadsafe(
    self._notify_sse("__system__", "restore_complete", event_data, is_global=True),
    self._main_loop
)
future.result(timeout=5)  # wait for completion
```

---

## Finding M1 [MEDIUM]: pr-review-guarded REVIEWER_SLOT agent_working query runs before review_branch is parsed

**File**: `bin/pr-review-guarded`
**Lines**: 34-69 (first agent_working block) vs 72 (review_branch initialization)
**Type**: Dead code / Logic error

### Description

Lines 34-69 execute the REVIEWER_SLOT resolution logic, including an agent_working query. However, `review_branch` is declared and initialized at line 72 (`review_branch=""`), AFTER this block runs. The regex on line 39:

```bash
rk = '$(echo "$review_branch" | grep -oE "[0-9]{8}T[0-9]{6}Z" | head -1 || echo "")'
```

extracts from an empty string, so `rk` is always empty. The agent_working query on line 41 (`if rk:`) is never entered. The subsequent agent-id.env fallback (lines 56-68) also fails because `$(pwd)` matching doesn't help without knowing the raw_key.

The second agent_working block (lines 220-231) runs after argument parsing (line 72-98) and works correctly.

### Impact

The REVIEWER_SLOT resolution through agent_working (first block) is always dead code. REVIEWER_SLOT falls through to the AI_TOOL default at line 295. Minor functional impact since the AI_TOOL default works, but the agent_working migration is partially defeated for this path.

Note: The second agent_working query at lines 220-231 has a similar structural issue — `review_branch` IS available by that point, so it works for `_my_worker_id` resolution. But the REVIEWER_SLOT-specific block is dead.

### Fix

Move the REVIEWER_SLOT resolution to after argument parsing, or restructure to use the parsed `review_branch`:

Option A: Move lines 34-69 to after line 98 (after the parsing loop).

Option B: Inline the agent_working query into the second block at line 220 and combine the REVIEWER_SLOT resolution there:

```bash
# After argument parsing (approx line 100):
if [[ -z "$REVIEWER_SLOT" ]]; then
  _my_worker_id=""
  if [[ -f "$_aw_py" ]]; then
    _raw_key_ts=$(echo "$review_branch" | grep -oE '[0-9]{8}T[0-9]{6}Z' | head -1 || true)
    ...
  fi
  ...
fi
```

---

## Finding M2 [MEDIUM]: D5 section in _restore_tasks calls agent_working.py without project argument

**File**: `docs/system/workspace/scripts/runtime/a2a/a2a_server.py`
**Lines**: 534-541
**Type**: Silent no-op

### Description

The D5 recovery block calls:
```python
_sp.run([_sys.executable, aw_py, 'stats'], timeout=10)
```

The `agent_working.py` CLI expects: `agent_working.py <action> <project> [args...]` (line 101-102). With only `['stats']`, `sys.argv` has length 2 (`['agent_working.py', 'stats']`), which is less than 3, so the CLI prints usage and exits with code 1. The `except Exception: pass` catches nothing (exit codes don't raise exceptions in `subprocess.run` without `check=True`), so this is a silent no-op rather than an error.

### Impact

Minor. The D5 section was intended as a diagnostic/health check after task restoration, but it does nothing. Not critical since the D6 broadcast has the same intent.

### Fix

Add the project path argument:
```python
_sp.run([_sys.executable, aw_py, 'stats', self.project], timeout=10)
```

---

## Finding L1 [LOW]: Duplicate 'canceled' key in state mapping

**File**: `docs/system/workspace/scripts/runtime/a2a/a2a_server.py`
**Line**: 160
**Type**: Cosmetic

### Description

```python
'canceled': TaskState.TASK_STATE_CANCELED,
'canceled': TaskState.TASK_STATE_CANCELED}
```

The second entry silently overwrites the first. Harmless but indicates sloppy code generation.

### Fix

Remove the duplicate line.

---

## Finding L2 [LOW]: SQL column name interpolation via f-strings in agent_working handlers

**File**: `docs/system/workspace/scripts/runtime/freely_db_manager.py`
**Lines**: 1310, 1314, 1337, 1356, 1369
**Type**: Code quality / SQL injection surface (low risk)

### Description

The `col` value (`{role}_id`) is interpolated into SQL query strings using f-strings and `.format()`:
```python
c.execute(f"UPDATE agent_working SET {col}=?, ...")
c.execute("INSERT INTO agent_working ... {col} ...".format(col=col))
c.execute(f"SELECT {col} FROM agent_working WHERE {col} IS NOT NULL")
```

While `role` is currently controlled by code (values: "worker", "manager", "reviewer"), the SQL interpolation pattern bypasses parameterized queries. If any caller passes an unexpected `role` value, it could inject SQL.

### Fix

Validate `role` against an allowlist:
```python
VALID_ROLES = {"worker", "manager", "reviewer"}
if role not in VALID_ROLES:
    raise ValueError(f"Invalid role: {role}")
col = f"{role}_id"
```

---

## Finding L3 [LOW]: B3 sync_project_tooling writes placeholder 'develop' as raw_key

**File**: `docs/system/workspace/scripts/runtime/freely` (sync_project_tooling_from_source)
**Context**: B3 commit (eb111b80b)
**Type**: Data quality

### Description

```python
agent_assign('${PROJECT_ROOT}', 'develop', 'worker', '$_next_worker', worktree='${target_project}')
```

This stores `raw_key='develop'` in the agent_working table. The value 'develop' is not a valid raw issue key — it's a branch name. This appears to be a placeholder/test value from the initial migration that was never updated to pass the actual raw_key.

### Impact

Entries with `raw_key='develop'` will not match any lookup by actual raw key. The agent_working table will contain junk entries that don't participate in lookups. If multiple workers are assigned (e.g., `worker_01` and `worker_02`), both will have `raw_key='develop'`, causing the second INSERT to fail with UNIQUE constraint violation (since `raw_key` is the PRIMARY KEY), unless the first row already exists and only the column is updated.

### Fix

The `sync_project_tooling_from_source` function needs access to the actual raw_key for the project. This is a design gap — the function doesn't know which raw_key it's associated with because it operates at the project/tooling level, not the raw issue level.

---

## Finding L4 [LOW]: f-string injection risk in inline Python snippets

**File**: `bin/pr-review-guarded`, `docs/system/workspace/scripts/worktree/wt-close`, `bin/freely-cycle`
**Type**: Security (low risk)

### Description

Several bash scripts construct inline Python code with bash-interpolated values:
```python
sys.path.insert(0, '$ROOT_DIR/docs/system/workspace/scripts/runtime')
row = agent_list_by_raw_key('$ROOT_DIR', 'raw-'+rk)
```

If `$ROOT_DIR` (from `git rev-parse --show-toplevel`) or branch names contain single quotes, they would break the Python string syntax. In practice, git paths and branch names don't contain quotes, but this is a latent vulnerability.

### Impact

Low. Exploitation requires a path or branch name containing single quotes, which is highly unusual in git repositories.

### Fix

Use heredoc-style input or base64-encode the arguments for safety. For example:
```bash
_py_code=$(cat << 'PYEOF'
import sys; sys.path.insert(0, sys.argv[1])
from agent_working import agent_list_by_raw_key
row = agent_list_by_raw_key(sys.argv[1], "raw-" + sys.argv[2])
if row:
    ...
PYEOF
)
python3 -c "$_py_code" "$ROOT_DIR" "$raw_key_ts"
```

---

## Summary Table

| ID | Severity | File | Line(s) | Description |
|---|---|---|---|---|
| H1 | HIGH | Multiple | Multiple | raw_key format mismatch: read sites add "raw-" prefix, write sites don't |
| H2 | HIGH | a2a_server.py | 542-554 | asyncio.Queue cross-event-loop in D6 SSE broadcast |
| M1 | MEDIUM | pr-review-guarded | 34-69 | REVIEWER_SLOT agent_working query runs before review_branch parsed |
| M2 | MEDIUM | a2a_server.py | 534-541 | D5 agent_working.py stats called without project argument |
| L1 | LOW | a2a_server.py | 160 | Duplicate 'canceled' dict key |
| L2 | LOW | freely_db_manager.py | 1310-1369 | Unvalidated SQL column name interpolation |
| L3 | LOW | freely (B3) | sync_project_tooling | Placeholder 'develop' written as agent_working raw_key |
| L4 | LOW | Multiple | Multiple | Inline f-string injection risk in bash->Python snippets |

## Root Cause Analysis

The raw_key format inconsistency (H1) is the most impactful finding. The fix requires a coordinated change across 6 files to standardize the format. The asyncio cross-event-loop issue (H2) breaks the SSE recovery notification chain that D6 was specifically designed to implement — the restore broadcast never reaches subscribers.

Both H1 and H2 should be fixed before the branch is merged to develop.
