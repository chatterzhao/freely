# Code Review: ACP bridge crash resilience

- reviewer: human
- date: 2026-05-03
- status: approved
- artifacts_reviewed:
  - docs/system/workspace/scripts/runtime/acp-bridge.py
  - docs/system/workspace/scripts/runtime/freely
  - docs/system/workspace/scripts/runtime/run-acp-prompt.py

## Decision

All five root causes addressed. Self-healing chain verified end-to-end:
daemon start → bridge health check → session/resume → set_mode → AI cycle completes.
Write tool calls no longer hang. No restart storms observed.

## Test evidence

- Cycle time: 5.2s (was 904s before fix)
- session/set_mode confirmed in bridge log after session/resume
- Activity-based timeout works correctly
- Lock split (stdin_write_lock) verified — permission forwarding no longer blocked
