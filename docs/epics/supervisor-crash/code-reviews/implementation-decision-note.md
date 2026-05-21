# Implementation Decision Note: I-20260521T032154Z-A

## Decision

Implement **方案 A**: Reorder `_on_supervisor_err` to capture `BASH_COMMAND` before any conditional check that could trigger a recursive ERR trap.

## Why This

方案 A is a 2-line reorder within the existing function. It:
- Requires no structural changes to the ERR trap mechanism
- Preserves all existing error handling paths
- Is trivially verifiable by code inspection
- Has zero side effects on non-recursive ERR trap scenarios

## Alternatives Considered

### 方案 B: Disable ERR trap inside handler
- `trap '' ERR` at function entry, restore at exit
- More robust against other recursive trap scenarios
- **Rejected per acceptance review**: Over-engineered for the specific bug; introduces trap save/restore complexity

## Boundary / Non-Goals

- The bash rc=0 false positive (C-20260517T083030Z-A) is a separate issue with a different root cause and independent fix
- No changes to crash report format, supervisor logic, or runtime behavior

## Residual Risk

- Low: If other code paths in `_on_supervisor_err` also trigger ERR trap, 方案 A alone may not prevent recursion. Mitigation: functional testing covers the known paths.
