- issue_id: I-20260521T115809Z-A
- issue_path: docs/issues/I-20260521T115809Z-A/issue.md

## Implementation Decision Note

- decision: Remove "forbidden" parameter from render_merge_message call, leaving only merge_path and source_branch
- why_this: render_merge_message only accepts 2 parameters (merge_path, source_branch). The extra "forbidden" parameter was incorrectly occupying the source_branch slot
- alternatives_considered: |
    1. Change render_merge_message to accept 6 params — unnecessary, function signature is correct
    2. Add validation to reject non-branch-looking names — addresses symptom not root cause
- boundary_non_goals: Not changing render_merge_message signature. Not changing write_guarded_state bypass_mode handling.
- residual_risk: None. The fix is a one-parameter removal that aligns the call with the function signature.
