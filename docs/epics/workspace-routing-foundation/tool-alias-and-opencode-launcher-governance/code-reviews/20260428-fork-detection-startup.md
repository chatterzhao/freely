# Fork detection + parent session injection - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `On startup, detect fork condition (SESSION_PARENT_ID set + no own session) and fork from parent. Manager injects parent session into worker's session-state.env before worker supervisor starts. Fork generates child UUID, preserves parent ID for resume target.`
- why_this: `Worker needs manager's context for correct task execution. Forking gives cache hit (same system prompt prefix) while keeping sessions isolated.`
- alternatives_considered: `1) Fresh launch per worker: rejected, no context inheritance. 2) Share session: rejected, concurrent write risk. 3) Fork: chosen, context + isolation.`
- boundary_non_goals: `No change to OpenCode/Codex fork (Claude-only for now).`
- residual_risk: `Fork copies full conversation; if parent session is very long, child's first launch is expensive. Mitigated by prompt cache.`

## Verification
- bash -n: `pass`
- Fork detection: SESSION_PARENT_ID + empty CLAUDE_SESSION_ID_CURRENT → fork ✓
- Worker resume after fork: own session ID → resume ✓
- Parent session preserved: SESSION_PARENT_ID immutable across cycles ✓
- Manager injection: writes to worker session-state.env before supervisor start ✓
