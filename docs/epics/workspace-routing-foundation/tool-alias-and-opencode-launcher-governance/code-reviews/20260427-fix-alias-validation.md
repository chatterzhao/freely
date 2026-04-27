# Fix alias tool validation - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Allow unknown tools to pass through start-lead-agent.sh validation. Alias resolution happens in tool-launchers.sh.`
- why_this: `cc-ds-auto was blocked as "unsupported tool" because validation ran before alias resolution.`
- alternatives_considered: `1) Add every alias to list: rejected, not scalable. 2) Remove validation: rejected, useful for catching typos. 3) Pass-through with warning: chosen.`
- boundary_non_goals: `No change to actual tool launching.`
- residual_risk: `Typo tools will pass validation but fail in launcher with a clear error.`
