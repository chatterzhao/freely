---
b1_id: B1-20260703T080443Z
phase_state: completed
source_raw: raw-20260703T080443Z
produced_candidate: C-20260703T080443Z-A
---

# B1: manager agent_working record at daemon startup

## Problem
1. __manager__ record only written lazily by _handle_needs_manager → fork unavailable during window gap
2. start-lead-agent.sh uses meta_env_value (subprocess can't access runtime function)

## Decision
1. Write __manager__ UPSERT at daemon startup (supervisor loop entry)
2. Inline _meta_env_value in start-lead-agent.sh (same pattern as _tool_registry_tools)
