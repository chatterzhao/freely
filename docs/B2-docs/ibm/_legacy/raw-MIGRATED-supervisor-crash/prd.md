# PRD: Fix _on_supervisor_err recursive ERR trap false positive

## Goal

Eliminate false positive crash reports caused by recursive ERR trap in `_on_supervisor_err` handler, without affecting legitimate crash detection.

## Background

The `_on_supervisor_err` function is called by `trap '_on_supervisor_err $LINENO' ERR`. When a `[[` condition evaluates to false (rc=1), the ERR trap fires. Inside the handler, the guard condition `[[ "$_err_rc" -eq 1 ]] && [[ "$_err_cmd" == "[[" ]]` is meant to detect this benign case, but due to a race where `BASH_COMMAND` changes during recursive trap invocation, the guard fails.

## Scope

**In scope:**
- Fix `_on_supervisor_err` in the freely runtime script
- Add minimal test coverage for the fix
- Update related documentation

**Out of scope:**
- Other crash modes (bash rc=0, handled by C-20260517T083030Z-A)
- General ERR trap robustness improvements (方案 B deferred)
- Runtime behavior changes beyond the crash handler

## Requirements

1. `[[` / `[` commands returning rc=1 must not trigger false positive crash reports
2. Real supervisor crashes (non-zero exit from non-`[[` commands) must still be detected
3. Existing ERR trap behavior for all other commands must be unchanged
4. Fix must be minimal (2-line reorder, not structural rewrite)

## Dev-Loop Handoff

- Issue: I-20260521T032154Z-A
- Worktree: fix/raw-20260521T032154Z-supervisor-crash-b2
- Epic: docs/B2-docs/supervisor-crash/
- Implementation boundary: single function `_on_supervisor_err`, ~4 lines affected
- Verification: pre-tests.md → test the fix; code-reviews/ → decision note
