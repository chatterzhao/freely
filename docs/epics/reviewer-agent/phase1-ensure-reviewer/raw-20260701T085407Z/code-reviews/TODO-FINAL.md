# Freely Phase 1 Reviewer Agent — Final Converged TODO
- date: 2026-07-01
- based on: 7 review docs + B1 design + subagent convergence (3 iterations)

## Status Summary

| Track | Tasks | Done | Remaining |
|-------|-------|------|-----------|
| A: Foundation | 6 | 6 | 0 |
| B: agent-id.env → agent_working | 8 | 8 | 0 |
| C: ACP + SSE Integration | 14 | 13 | 1 |
| D: Lifecycle | 13 | 7 | 6 |
| **Total** | **41** | **34** | **7** |

## Track A: Foundation (DONE ✅)

- [x] A1. _restore_tasks 3 bugs fixed (L403/442/663)
- [x] A2. agent_working table + 9 RPC handlers in freely_db_manager
- [x] A3. agent-roles.toml + agent card ?role= endpoint
- [x] A4. InputRequiredReason enum (12 values)
- [x] A5. agent-table.toml v2 flat format
- [x] A6. 18 unit tests GREEN

## Track B: agent-id.env → agent_working (NEW)

- [x] B1 ✅ → agent_working query
- [x] B2 ✅ → agent_working.agent_next_free()
- [x] B3 ✅ → agent_working.assign()
- [x] B4 ✅ → agent_working.cleanup_stale()
- [x] B5 ✅ → agent_working.release_all()
- [x] B6 ✅: agent-id.env → agent_working
- [x] B7 ✅ removed, --next-free delegates to agent_working
- [x] B8 ✅: agent-id.env file read → agent_working query

## Track C: ACP + SSE (NEW)

- [x] C1 ✅ (not just log)
- [x] C2 ✅project, role, agent_id, slot, raw_key)
- [x] C3 ✅project, role, raw_key) — for restart recovery
- [x] C4 ✅project, role, raw_key) — for wt-close
- [x] C5 ✅ global SSE endpoint
- [x] C6 ✅ (statusUpdate + metadata)
- [x] C7 ✅
- [x] C8 ✅ → actual ACP session/new
- [x] C9 ✅ → actual session/resume
- [x] C10 ✅ → actual session/resume
- [x] C11 ✅ with exponential backoff
- [x] C12 ✅ (process liveness check)
- [x] C13 ✅
- [ ] C14. SSE + ACP integration tests

## Track D: Lifecycle (NEW)

- [x] D1 ✅ enforcement
- [x] D2 ✅ → actual execution (not just log)
- [x] D3 ✅ + delete worktree
- [x] D4 ✅ agents
- [x] D5 ✅ for working agents
- [x] D6 ✅ after daemon restart
- [x] D7 ✅ (periodic)
- [ ] D8. Freely restart integration test
- [ ] D9. Agent crash restart integration test
- [ ] D10. Active session communication test (A2A SSE direct)
- [ ] D11. Dead session communication test (ACP new → A2A SSE)
- [ ] D12. Three-loop integration test (L1→L2→L3 with reviewer gates)
- [ ] D13. Full end-to-end: Manager→Worker→Reviewer→Manager closed loop

## Dependency Order

```
A (done) → B+Track C4 (parallel) → C1-C3 (ACP) + C5-C6 (SSE) (parallel)
  → C7-C13 (Watchdog integration) → Track D (lifecycle)
```

## Contradictions Resolved

| Contradiction | Resolution |
|---------------|------------|
| agent-id.env ref count (30 vs 44) | Replace by file, not by count. Track B covers all. |
| SSE stream endpoint missing | C5: add GET /tasks/stream |
| SSE event format mismatch | C6: align to statusUpdate+metadata |
| ACP session just logs | C1-C4: real ACP bridge calls |
| Reviewer allocation dual path | B7: agent-table-query delegates to agent_working |
| input-required schema unenforced | D1: JSON schema validation |
| freely-cycle dispatch only logs | D2: connect to actual Reviewer creation |
| Restart recovery incomplete | D5-D6: ACP resume + SSE re-subscribe |
