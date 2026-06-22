- issue_id: I-20260622T003231Z-A
- issue_path: docs/issues/I-20260622T003231Z-A/issue.md
- phase_state: in_dev

# code-review: pre-push.sh local keyword fix

## Implementation Decision Note

- decision: Remove `local` keyword from variable declarations in pre-push.sh hook to support macOS bash 3.x
- why_this: `local` is only valid inside bash functions; `set -euo pipefail` causes immediate failure when `local` is used outside a function
- alternatives_considered: Rewrite hook as function-call based — rejected, too invasive; upgrade bash on macOS — rejected, not under project control; skip gitee entirely — rejected, gitee is required
- boundary_non_goals: No other hook behavior changes
- residual_risk: None — the fix is syntactically correct for all bash versions (3.x to 5.x)

## Changes reviewed
- `docs/system/workspace/hooks/pre-push.sh`: 2 `local` keyword removals (lines 13, 19)

## Decision: Approve
