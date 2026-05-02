# Remaining tasks completion - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add DEPRECATED markers to intake_dir_for_project and scan_intake. These functions remain for backward compat but should not be extended.`
- why_this: `Completes REMOVE 8.1/8.2 from TASKS.md. Markers guide future developers away from deprecated paths.`
- alternatives_considered: `1) Remove functions entirely: rejected, breaks backward compat during transition. 2) No markers: rejected, unclear what's deprecated. 3) DEPRECATED comments: chosen, clear and safe.`
- boundary_non_goals: `No code removal. No behavior change.`
- residual_risk: `None. Pure documentation.`
