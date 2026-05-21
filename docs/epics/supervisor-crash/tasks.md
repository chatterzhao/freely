# Tasks: I-20260521T032154Z-A — supervisor crash recursive ERR trap fix

## Task Breakdown

### T1: Reorder _on_supervisor_err to capture BASH_COMMAND early
- **owner:** dev-loop worker
- **effort:** 1 line change (move `_err_cmd` assignment before `[[ "$_err_rc" -eq 0 ]]`)
- **file:** `docs/system/workspace/scripts/runtime/freely` (~line 18951)
- **acceptance:** AI-1, AI-3 pass

### T2: Verify benign check still works for [
- **owner:** dev-loop worker
- **effort:** 1 line check (confirm `[[ "$_err_cmd" == "[" ]]` is also in the guard)
- **file:** same function
- **acceptance:** AI-1 pass (both `[[` and `[` covered)

### T3: Verify real crash detection preserved
- **owner:** dev-loop worker
- **effort:** Trace the function after fix for non-[[ error paths
- **acceptance:** AI-2 pass

### T4: Regression check against C-20260517T083030Z-A
- **owner:** dev-loop worker
- **effort:** Confirm the bash rc=0 fix path is independent
- **acceptance:** AI-4 pass

### T5: Run pre-tests and verification
- **owner:** dev-loop worker
- **effort:** Execute pre-tests.md acceptance items
- **acceptance:** All 4 AI items pass
