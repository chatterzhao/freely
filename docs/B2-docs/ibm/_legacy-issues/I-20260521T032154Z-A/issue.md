---
local_id: I-20260521T032154Z-A
kind: linked
status: done_b2_ibm
phase_state: done_b2_ibm
promoted_from: raw-20260521T032154Z
source_candidate: docs/B1-docs/raw-20260521T032154Z/candidates.md
canonical_issue_path: ""
platform_ids:
  github:
    issue_id: '1523'
    url: https://github.com/chatterzhao/freely/issues/1523
    synced_at: '2026-05-21T03:02:00Z'
primary_platform: github
last_synced_comment_at: {}
hash: ""
created_at: 2026-05-21T03:02:00Z
updated_at: 2026-05-21T03:57:00Z
intake_id: ""
author: zhaoquan
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/B2-docs/supervisor-crash/verification/pre-tests.md
verification_artifact_dir: docs/epics/supervisor-crash/code-reviews
milestone: M-20260521T032154Z-A
---

# I-20260521T032154Z-A: Fix _on_supervisor_err recursive ERR trap false positive

- source_candidate: `docs/B1-docs/raw-20260521T032154Z/candidates.md#C-20260521T032154Z-A`
- pre_tests_path: `docs/B2-docs/supervisor-crash/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/supervisor-crash/code-reviews`
- milestone: M-20260521T032154Z-A

## Problem

In the `_on_supervisor_err` function (freely runtime ~line 18951), the ERR trap handler captures the failing command and exit code. However, the handler itself can trigger a recursive ERR trap:

```bash
_on_supervisor_err() {
    local _err_rc=$?                        # 18952
    if [[ "$_err_rc" -eq 0 ]]; then         # 18953 ← [[ returns rc=1 when false → recursive ERR trap
        LAST_WORKCELL_EXIT_REASON="..."
        return
    fi
    local _err_cmd
    _err_cmd="${BASH_COMMAND%% *}"           # 18958 ← after recursion, BASH_COMMAND is "[[", not the original command
    if [[ "$_err_rc" -eq 1 ]] && [[ "$_err_cmd" == "[[" || "$_err_cmd" == "[" ]]; then  # 18960
        LAST_WORKCELL_EXIT_REASON="..."
        return
    fi
    # ... false positive crash report generated
```

The `[[` at line 18953 exits with rc=1 when the comparison is false, which triggers the `ERR` trap. The trap calls `_on_supervisor_err` recursively. Inside the recursive call:
- `BASH_COMMAND` now contains `[[` instead of the original command
- The benign check at line 18960 fails because `_err_cmd` is wrong
- A false positive crash report is generated

## Solution

**方案 A** (selected via acceptance review): Reorder lines so `BASH_COMMAND` is captured before any command that could trigger the ERR trap:

```bash
_on_supervisor_err() {
    local _err_rc=$?
    local _err_cmd="${BASH_COMMAND%% *}"     # ← capture early, before any [[ check
    if [[ "$_err_rc" -eq 0 ]]; then
        LAST_WORKCELL_EXIT_REASON="..."
        return
    fi
    # _err_cmd is already correct here
    if [[ "$_err_rc" -eq 1 ]] && [[ "$_err_cmd" == "[[" || "$_err_cmd" == "[" ]]; then
        LAST_WORKCELL_EXIT_REASON="..."
        return
    fi
    # ... proper crash report generation
```

## Verification

- [ ] Unit test: Set ERR trap, trigger [[ comparison that returns false, verify no false crash report
- [ ] Integration: Run normal supervisor workflow, verify crash detection still works for real errors
- [ ] Regression: Verify C-20260517T083030Z-A (bash rc=0) is not affected

## See Also

- C-20260517T083030Z-A: Separate crash mode (bash exit code 0 false positive)
