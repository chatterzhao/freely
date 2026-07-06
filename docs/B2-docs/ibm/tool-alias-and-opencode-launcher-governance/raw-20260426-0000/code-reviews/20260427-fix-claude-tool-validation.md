# Fix claude tool validation - verification
- issue_id: `I-20260426-0000-A`

## Implementation Decision Note
- decision: `Add claude to tool validation lists in start-lead-agent.sh and tool-launchers.sh. cc-ds-auto alias resolves to claude binary which must be recognized.`
- why_this: `cc-ds-auto → claude, but validation rejected claude as unsupported tool.`
- alternatives_considered: `1) Name alias to start with cc-: rejected, inflexible. 2) AI_TOOL_FAMILY override: works but adds config. 3) Add claude to lists: chosen, simple.`
- boundary_non_goals: `No other tool families. No behavior change.`
- residual_risk: `None. Claude was already handled in alias resolver and cc case.`
