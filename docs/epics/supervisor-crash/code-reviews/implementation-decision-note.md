## Implementation Decision Note
- issue_id: I-20260521T032154Z-A
- issue_path: docs/issues/I-20260521T032154Z-A/issue.md
- decision: Plan A - Reorder _on_supervisor_err to capture BASH_COMMAND before any conditional check that could trigger a recursive ERR trap.
- why_this: Plan A is a 2-line reorder within the existing function. It requires no structural changes to the ERR trap mechanism, preserves all existing error handling paths, is trivially verifiable by code inspection, and has zero side effects on non-recursive ERR trap scenarios.
- alternatives_considered: Plan B (Disable ERR trap inside handler via trap '' ERR at function entry, restore at exit) is more robust against other recursive trap scenarios but was rejected per acceptance review as over-engineered for the specific bug; introduces trap save/restore complexity without proportional benefit.
- boundary_non_goals: The bash rc=0 false positive (C-20260517T083030Z-A) is a separate issue with a different root cause and independent fix. No changes to crash report format, supervisor logic, or runtime behavior.
- residual_risk: Low. If other code paths in _on_supervisor_err also trigger ERR trap, Plan A alone may not prevent recursion. Mitigation: functional testing covers the known paths.
