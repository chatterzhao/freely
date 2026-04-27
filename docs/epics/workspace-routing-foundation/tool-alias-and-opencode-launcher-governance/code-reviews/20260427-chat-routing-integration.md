# Chat routing integration - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add _route_chat_to_issue() that extracts issue references from chat messages. Matches raw-xxx/I-xxx IDs or ISSUES.md local_id entries. Falls back to new raw issue.`
- why_this: `Without routing, every chat creates a new issue even when it's clearly about an existing issue (e.g., mentioning its ID). Script-based routing handles the common case.`
- alternatives_considered: `1) AI routing on every chat: rejected, adds token cost. 2) Only --issue flag: rejected, users forget. 3) Script match + AI deferred: chosen, handles 80% case.`
- boundary_non_goals: `No AI-based semantic routing. No urgency auto-detection.`
- residual_risk: `Messages without explicit issue references still create new raw issues. AI routing (chat-routing skill integration) needed for semantic matching.`
