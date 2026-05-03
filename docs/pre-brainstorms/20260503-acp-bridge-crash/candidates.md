# C-20260503-0000-A: ACP bridge crash resilience and self-healing

- candidate_id: `C-20260503-0000-A`
- title: `ACP bridge crash resilience and self-healing`
- status: `promoted`
- priority: `P0`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_to: `I-20260503-0000-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/acp-bridge-crash-resilience/issues/I-20260503-0000-A.md`
- source_intake: `raw-20260503-0000`

## Problem

ACP bridge (`acp-bridge.py`) has five linked failure modes that cause restart storms:
1. `msg.get('result','')[:100]` KeyError on dict results crashes stdout reader thread
2. Crashed reader thread doesn't stop bridge → zombie bridge holds socket
3. `_ensure_acp_bridge_running` reuses zombie bridge (no health check)
4. `session/resume` doesn't call `session/set_mode` → permissions revert to `default` → Write tools hang
5. `_send_request` holds `server_lock` during wait → blocks permission response forwarding → deadlock

## Fix

See `I-20260503-0000-A` for full implementation details.
