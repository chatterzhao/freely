# Persist session early - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Write CLAUDE_SESSION_ID_CURRENT to session-state.env immediately after generation, before AI launch. Add cc/claude case to session ID extraction.`
- why_this: `SIGTERM-killed sessions lost session_id because state was only written on cycle completion. Early persistence enables resume on next launch.`
- alternatives_considered: `1) Only log extraction: rejected, fragile. 2) JSONL scanning: rejected, slow. 3) Early persistence + log extraction: chosen.`
- boundary_non_goals: `No change to non-Claude tools session handling.`
- residual_risk: `Race condition if AI launch fails before state write completes. State file is best-effort.`
