# Resume circuit breaker + JSONL fallback + state protection - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Three-layer defense: (1) protect CLAUDE_SESSION_ID_CURRENT from empty overwrite, (2) JSONL directory fallback when state file lost session ID, (3) circuit breaker tracking fresh launches in time window. Always prefer resume over fresh — no freshness threshold.`
- why_this: `Fresh launches send 60KB+ system prompt without cache. Resume reuses cache (5min TTL for Anthropic, possibly 24h for DeepSeek). The daemon was stuck in a fresh-launch loop because session state was corrupted and resume never triggered.`
- alternatives_considered: `1) Fix only state persistence: insufficient, state file can still be lost. 2) ACP mode: not supported for Claude Code, over-engineered. 3) Three layers: chosen, defense in depth.`
- boundary_non_goals: `No change to worker dispatch mechanism. No freshness threshold (always prefer resume).`
- residual_risk: `Circuit breaker may false-trigger if legitimately rapid fresh launches needed. Mitigated by configurable FRESH_LAUNCH_MAX_COUNT and FRESH_LAUNCH_COOLDOWN_SECS.`

## Verification
- bash -n: `pass` (both freely and monitor-ai-cli.sh)
- Layer 1: CLAUDE_SESSION_ID_CURRENT not overwritten by empty ✓
- Layer 2: JSONL fallback extracts session ID from ~/.claude/projects/<slug>/ ✓
- Layer 3: 3 fresh launches in 300s → circuit breaker trips → daemon stops ✓
- Manager/worker session isolation: different worktrees → different state files ✓

### Amendment 20260428-2: resume enforcement + tool dir abstraction + new-session
- AI_RESUME_ON_RESTART=true → zero tolerance for fresh launches (max_count=1 in circuit breaker)
- ensure_runtime_tool_session_anchor errors immediately if no valid session found
- _tool_session_dir() abstracts tool→session directory mapping
- cmd_new_session() clears all session state for forced fresh starts
