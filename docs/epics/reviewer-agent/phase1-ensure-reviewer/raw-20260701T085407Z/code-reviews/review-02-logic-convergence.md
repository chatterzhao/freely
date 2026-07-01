# Review 02: Logic + Design Convergence
- date: 2026-07-01
- reviewer: subagent (Plan)
- verdict: 7 contradictions between design and implementation

## Contradictions
1. agent-id.env: design says "completely deprecated", 7+ sites still active
2. SSE stream endpoint: GET /tasks/stream does not exist (only /tasks/{id}/stream)
3. SSE event format: watchdog parser format ≠ a2a_server output format
4. ACP session creation: design specifies session/new|fork|resume per route, implementation only logs
5. FREELY_SKILLS: design says agent-roles.toml only, implementation keeps hardcoded fallback
6. Reviewer allocation: two independent paths (agent-table-query vs agent_working)
7. input-required metadata: schema not enforced, fields not normalized

## Root Cause
watchdog_sse.py is an orphan module — its SSE subscription targets a nonexistent endpoint,
its event parser uses the wrong format, and its handlers only log, never act.
The input-required → route → ACP session chain is broken.
