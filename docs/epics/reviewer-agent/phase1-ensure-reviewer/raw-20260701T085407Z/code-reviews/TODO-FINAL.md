# Freely Phase 1 Reviewer Agent — Final Converged TODO
- date: 2026-07-01
- based on: 7 review docs + B1 design + subagent convergence (3 iterations)

## Status Summary

| Track | Tasks | Done | Remaining |
|-------|-------|------|-----------|
| A: Foundation | 6 | 6 | 0 |
| B: agent-id.env → agent_working | 8 | 0 | 8 |
| C: ACP + SSE Integration | 14 | 0 | 14 |
| D: Lifecycle | 13 | 0 | 13 |
| **Total** | **41** | **6** | **35** |

## Track A: Foundation (DONE ✅)

- [x] A1. _restore_tasks 3 bugs fixed (L403/442/663)
- [x] A2. agent_working table + 9 RPC handlers in freely_db_manager
- [x] A3. agent-roles.toml + agent card ?role= endpoint
- [x] A4. InputRequiredReason enum (12 values)
- [x] A5. agent-table.toml v2 flat format
- [x] A6. 18 unit tests GREEN

## Track B: agent-id.env → agent_working (NEW)

- [ ] B1. freely script: _resolve_current_agent_id → agent_working query
- [ ] B2. freely script: _ensure_reviewer_agent → agent_working.agent_next_free()
- [ ] B3. freely script: sync_project_tooling → agent_working.assign()
- [ ] B4. freely script: manager_reconcile_agent_id_env → agent_working.cleanup_stale()
- [ ] B5. wt-close: sed agent-id.env → agent_working.release_all()
- [ ] B6. freely-review + pr-review-guarded: agent-id.env → agent_working
- [ ] B7. agent-table-query: --get-reviewer removed, --next-free delegates to agent_working
- [ ] B8. task-lifecycle-scan.py: agent-id.env file read → agent_working query

## Track C: ACP + SSE (NEW)

- [ ] C1. _ensure_reviewer_agent: real ACP session/new (not just log)
- [ ] C2. _acp_session_new(project, role, agent_id, slot, raw_key)
- [ ] C3. _acp_session_resume(project, role, raw_key) — for restart recovery
- [ ] C4. _acp_session_close(project, role, raw_key) — for wt-close
- [ ] C5. A2A GET /tasks/stream global SSE endpoint
- [ ] C6. SSE event format alignment (statusUpdate + metadata)
- [ ] C7. watchdog_sse.py integration into daemon startup
- [ ] C8. watchdog_sse.py: _handle_needs_reviewer → actual ACP session/new
- [ ] C9. watchdog_sse.py: _handle_needs_manager → actual session/resume
- [ ] C10. watchdog_sse.py: _handle_needs_worker → actual session/resume
- [ ] C11. watchdog_sse.py: SSE reconnect with exponential backoff
- [ ] C12. Agent crash detection (process liveness check)
- [ ] C13. Session staleness timeout detection
- [ ] C14. SSE + ACP integration tests

## Track D: Lifecycle (NEW)

- [ ] D1. input-required metadata schema enforcement
- [ ] D2. freely-cycle: dispatch_reviewer → actual execution (not just log)
- [ ] D3. wt-close: session/close + agent_release_all + delete worktree
- [ ] D4. wt-close: cleanup test-pre-merge reviewer agents
- [ ] D5. _restore_tasks: ACP session/resume for working agents
- [ ] D6. _restore_tasks: SSE re-subscribe after daemon restart
- [ ] D7. Stale worktree detection + orphan cleanup (periodic)
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
