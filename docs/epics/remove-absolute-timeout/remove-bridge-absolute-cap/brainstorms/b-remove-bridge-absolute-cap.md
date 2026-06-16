# Brainstorm: Remove BRIDGE_TIMEOUT Absolute Cap

## Problem Space

The `_send_request()` method in `acp-bridge.py` uses a `deadline = time.time() + timeout` pattern with `BRIDGE_TIMEOUT=1800s`. This imposes an unconditional 30-minute wall-clock limit on AI session/prompt operations. Even when the AI is actively producing output (streaming tokens, making tool calls), if the wall clock reaches 30 minutes, the session is killed with an absolute timeout error.

The idle timeout (ACP_IDLE_TIMEOUT) already watches `last_activity_ts` and raises TimeoutError when no activity is detected for the configured period. This is sufficient to detect hung or stuck sessions.

## Alternatives Considered

1. **Remove absolute timeout entirely (chosen)**: Simplest change, aligns with industry standard. The idle timeout remains as the sole safeguard.

2. **Increase absolute timeout threshold**: Would postpone the problem but not solve it. Any wall-clock cap will eventually kill a legitimately long-running session.

3. **Make absolute timeout configurable**: Adding complexity without solving the fundamental issue. Users would need to know to increase the timeout for long-running tasks.

4. **Per-request timeout instead of wall-clock**: Not feasible without significant refactoring of the session/prompt polling loop.

## Decision

Remove the absolute timeout entirely. Change `while time.time() < deadline:` to `while True:`, remove the deadline variable and post-loop absolute timeout check. The idle timeout alone is the correct safeguard.
