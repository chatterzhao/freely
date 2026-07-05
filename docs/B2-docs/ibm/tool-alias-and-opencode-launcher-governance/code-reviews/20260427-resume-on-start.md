# Resume on start config - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add AI_RESUME_ON_START (default true). When set and session state exists, daemon start skips fresh launch and falls through to resume.`
- why_this: `Previous session context is in deepseek cache. Re-reading 60KB docs on every restart wastes tokens and time.`
- alternatives_considered: `1) Always fresh: rejected, wastes cache. 2) Always resume: rejected, need fresh for debugging. 3) Config with default true: chosen.`
- boundary_non_goals: `No change when no session exists (still fresh).`
- residual_risk: `If session state is corrupted, resume may fail. Fallback to fresh on next cycle.`
