# Chat comment append + active detection - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add --issue and --urgent to cmd_intake_chat. _write_chat_to_issue appends ### comments to existing issues. Active issue detection triggers signal for B2+dev+verification phases.`
- why_this: `Chat messages about active issues must be seen immediately by the AI worker (corrections, supplements). Comments are supplements to the issue body.`
- alternatives_considered: `1) AI-based routing only: deferred because requires chat-routing skill. 2) Always create new issue: rejected, loses context. 3) --issue flag + active detection: chosen, simple and correct.`
- boundary_non_goals: `No AI-based issue routing. No comment sync to platform (phase 2).`
- residual_risk: `Comment consumption by AI workers requires them to read ## Comments section during work. This is the next step.`
