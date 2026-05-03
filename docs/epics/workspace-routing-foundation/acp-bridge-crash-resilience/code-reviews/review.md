# Code Review: ACP bridge crash resilience

- reviewer: human
- date: 2026-05-03
- status: approved
- owner_issue: I-20260503-0000-A
- owner_issue_path: docs/epics/workspace-routing-foundation/acp-bridge-crash-resilience/issues/I-20260503-0000-A.md
- artifacts_reviewed:
  - docs/system/workspace/scripts/runtime/acp-bridge.py
  - docs/system/workspace/scripts/runtime/freely
  - docs/system/workspace/scripts/runtime/run-acp-prompt.py

## Decision

Approve the five-layer fix for ACP bridge crash resilience. All root causes
addressed with self-healing chain that prevents restart storms.

## why_this

Without these fixes, the ACP bridge enters a zombie state (alive process, dead
reader thread) that causes all AI cycles to timeout after 900s. The restart
storm renders freely daemon non-functional. Each layer catches failures from
the layer below, forming a complete self-healing chain.

## alternatives_considered

- **Increase timeout only**: Would mask the permission deadlock and lock contention
  issues; does not fix root cause.
- **Manual cleanup**: Requires operator intervention, violates self-healing goal.
- **Remove bridge entirely**: Loses session persistence (cache hits), increases cost.

## boundary_non_goals

- Does not refactor session-state.env to SQLite (separate follow-on)
- Does not change the ACP protocol or Claude agent SDK behavior
- Does not modify tool alias configuration (`cc-ds-flash-auto` settings)
- Does not add new monitoring/metrics (existing runtime events cover this)

## residual_risk

- Activity-based timeout depends on AI producing streaming output. If the model
  is completely silent for ACP_IDLE_TIMEOUT (300s), the idle timeout still fires.
  This is by design — total silence indicates a real problem.
- `session/set_mode` is called after resume; if it fails silently, the session
  could still have `default` permissions. Defense-in-depth: called in both
  `handle_client` and `run-acp-prompt.py`.

## Test evidence

- Cycle time: 5.2s (was 904s before fix)
- session/set_mode confirmed in bridge log after session/resume
- Activity-based timeout works correctly
- Lock split (stdin_write_lock) verified — permission forwarding no longer blocked
