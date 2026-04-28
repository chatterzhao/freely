# Resume start/restart enforcement based on JSONL evidence - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `AI_RESUME_ON_RESTART forces resume (JSONL must exist, hard error if missing). AI_RESUME_ON_START checks JSONL: if exists → resume; if not → allow one fresh.`
- why_this: `Restart means a previous launch created JSONL files. If they're missing, state is corrupted and fresh would waste tokens. Start may be first-ever launch, so allow fresh only when JSONL directory is empty.`
- alternatives_considered: `1) Always allow fresh fallback: rejected, token waste. 2) Only check state file: rejected, state file can be lost while JSONL exists. 3) JSONL-based enforcement: chosen.`
- boundary_non_goals: `No change to per-tool session dir abstraction (already in _tool_session_dir).`
- residual_risk: `None — this is a guardrail, not a functional change.`

## Verification
- bash -n: `pass`
- start with JSONL: `pass` (forces resume)
- start without JSONL: `pass` (allows one fresh)
- restart without JSONL: `pass` (hard error)

### Amendment 20260428-3: session state consistency audit
- Fixed _persist_session_anchor_early from destructive cat > to merge mode
- Added SESSION_PARENT_ID to write_session_state (was lost every cycle)
- Added SESSION_PARENT_ID to write_live_session_state_if_possible
- Fork launch kind added to tool-launchers.sh (claude --fork-session)
- Session lifecycle protocol documented in docs/system/workspace/
