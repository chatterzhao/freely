# Wiring Guide: agent-id.env → agent_working

## Freely Script (docs/system/workspace/scripts/runtime/freely)

| Line | Current | Replace With |
|------|---------|-------------|
| ~278 | `_agent_env="$project/.freely/agent-id.env"` | `agent_list_by_raw_key(project, raw_key)` |
| ~2010 | Reconcile zombie entries | `agent_cleanup_stale(project)` |
| ~4190 | Resolve agent identity from agent-id.env | `agent_get_session(project, raw_key, role)` |
| ~4701 | Resolve current agent identity | same |
| ~5880 | Write agent-id.env (echo >>) | `agent_assign(project, raw_key, role, agent_id, worktree, branch)` |
| ~12783 | `manager_reconcile_agent_id_env` | `agent_cleanup_stale(project)` |
| ~13619 | `grep agent-id.env` for a2a_task | `agent_list_by_raw_key(project, raw_key)` |
| ~23515 | Write discuss to agent-id.env | `agent_assign(...)` |

## Bin Scripts

| File | Current | Replace With |
|------|---------|-------------|
| pr-review-guarded L32-46 | `grep agent-id.env` | `agent_get_session()` or direct agent-table query |
| pr-review-guarded L197 | same | same |
| freely-review L23 | `AGENT_ENV=...` | remove (dead code) or query agent_working |
| agent-table-query L250 | `--next-free` reads agent-id.env | query `agent_working.agent_next_free()` |
| agent-table-query L287 | `--reconcile` reads agent-id.env | query `agent_working.agent_cleanup_stale()` |

## Python Modules

| File | Current | Replace With |
|------|---------|-------------|
| a2a_types.py L373 | `FREELY_SKILLS` hardcoded | Add `_load_role_skills()` or import from a2a_server |
| task-lifecycle-scan.py L512 | Reads agent-id.env file | Query `agent_working` table |

## Documentation

| File | Update |
|------|--------|
| reviewer-agent.md L18,29,121,135,142 | Update naming to reviewer_01, reference agent_working |
| manager-agent.md L104,111 | Update reviewer_manager_01 → reviewer_01 |
