# Pre-Tests: I-20260521T032154Z-A — supervisor crash recursive ERR trap fix

## Acceptance Items

### AI-1: Benign [[ check does not generate crash report
- **type:** regression
- **adequacy:** v2
- **verification method:** code inspection + simulation
- **pre-test:** Set ERR trap, execute `[[ "a" == "b" ]]`, verify `_on_supervisor_err` exits via benign check path without crash report generation.
- **pass condition:** No crash report file written, no issue created.

### AI-2: Real crash is still detected
- **type:** regression
- **adequacy:** v2
- **verification method:** code inspection + simulation
- **pre-test:** Set ERR trap, execute `false` (non-[[ command), verify `_on_supervisor_err` proceeds to crash report generation.
- **pass condition:** Crash report generated with correct `_err_cmd` and `_err_rc`.

### AI-3: _err_cmd is captured correctly before any [[ check
- **type:** correctness
- **adequacy:** v2
- **verification method:** code inspection
- **pre-test:** Inspect the reordered `_on_supervisor_err`: confirm `_err_cmd="${BASH_COMMAND%% *}"` appears before the `[[ "$_err_rc" -eq 0 ]]` check.
- **pass condition:** Line ordering confirmed: capture before any conditional.

### AI-4: No regression on bash rc=0 crash mode (C-20260517T083030Z-A)
- **type:** cross-boundary
- **adequacy:** v2
- **verification method:** code inspection
- **pre-test:** Confirm `bash` command with rc=0 is still handled by the separate C-20260517T083030Z-A fix path, not affected by this change.
- **pass condition:** The code path for bash rc=0 is independent and unchanged.

## Test Plan

1. Unit test: Source the fixed function, trigger ERR trap with various commands
2. Integration: Run `_on_supervisor_err` with simulated error conditions
3. Verify no false positives for [[, [, and other benign commands
