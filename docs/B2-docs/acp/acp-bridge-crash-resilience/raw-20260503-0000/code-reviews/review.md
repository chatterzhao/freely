# Code Review: ACP bridge crash resilience

- issue_id: `I-20260503-0000-A`
- issue_path: `docs/B2-docs/acp/acp-bridge-crash-resilience/raw-20260503-0000issues/I-20260503-0000-A.md`
- review_date: `2026-05-03`
- reviewer: `human`
- status: `approved`
- decision: `approve`
- artifacts_reviewed:
  - docs/system/workspace/scripts/runtime/acp-bridge.py
  - docs/system/workspace/scripts/runtime/freely
  - docs/system/workspace/scripts/runtime/run-acp-prompt.py

## Implementation Decision Note

- decision: Approve the five-layer fix for ACP bridge crash resilience. All root
  causes addressed with self-healing chain that prevents restart storms.
- why_this: Without these fixes, the ACP bridge enters a zombie state (alive process,
  dead reader thread) that causes all AI cycles to timeout after 900s. The restart
  storm renders freely daemon non-functional.
- alternatives_considered: Increase timeout only (masks root cause, doesn't fix
  permission deadlock); manual cleanup (violates self-healing); remove bridge entirely
  (loses session persistence and cache hits).
- boundary_non_goals: Does not refactor session-state.env to SQLite; does not change
  ACP protocol or Claude agent SDK behavior; does not modify tool alias configuration.
- residual_risk: Activity-based timeout depends on streaming output — total silence
  for ACP_IDLE_TIMEOUT (300s) still fires timeout by design. session/set_mode after
  resume could fail silently; mitigated by defense-in-depth (called in both
  handle_client and run-acp-prompt.py).

## Test evidence

- Cycle time: 5.2s (was 904s before fix)
- session/set_mode confirmed in bridge log after session/resume
- Activity-based timeout works correctly
- Lock split (stdin_write_lock) verified — permission forwarding no longer blocked
