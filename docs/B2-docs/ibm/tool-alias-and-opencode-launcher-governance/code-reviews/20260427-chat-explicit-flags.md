# Chat explicit flags - verification

- issue_id: `I-20260426-0000-A`

## Implementation Decision Note
- decision: `Require --issue or --new-issue for every chat. No default behavior. Prevents accidental raw issue creation.`
- why_this: `Without explicit flags, forgotten parameters silently create new issues. Explicit intent prevents accidents.`
- alternatives_considered: `1) Auto-routing fallback: rejected, may route incorrectly. 2) Only --issue: rejected, need way to create new issues. 3) --issue + --new-issue: chosen, explicit and safe.`
- boundary_non_goals: `No auto-routing fallback. No AI-based smart routing in this slice.`
- residual_risk: `None. Intent is always explicit.`
