- issue_id: I-20260522T071901Z-A
- issue_path: docs/issues/I-20260522T071901Z-A/issue.md
## Implementation Decision Note
- decision: Use *-apikey-*/ *-account-* glob patterns for kind inference. Use $slot directly in switch.
- why_this: list_tool_slots now returns full names. Partial-name assumptions broke kind detection and created double prefix.
- alternatives_considered: Keep partial names and convert everywhere (more invasive), add tool prefix check in every caller (fragile)
- boundary_non_goals: Not changing codex-specific slot naming conventions (apikey-codex-xxx).
- residual_risk: Legacy codex slots with manifest.json are fine. Only the infer-from-name fallback needed fixing.
