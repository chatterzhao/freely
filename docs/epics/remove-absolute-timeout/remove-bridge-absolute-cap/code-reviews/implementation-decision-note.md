# Implementation Decision Note

## Decision

Remove the absolute timeout (BRIDGE_TIMEOUT) check from `_send_request()` for `session/prompt` handling in `acp-bridge.py`.

## Why This

1. **Industry standard**: 6 ACP projects checked use only idle timeouts, no absolute caps.
2. **Problem elimination**: The absolute 30-minute timeout kills legitimate long-running AI sessions even when actively producing output. No configuration toggle could fix this — the code itself imposes the limit.
3. **Minimal surface**: The change is 3 lines removed, 1 line changed. The idle timeout (ACP_IDLE_TIMEOUT) remains untouched and continues to protect against hung sessions.
4. **No new dependencies or configuration**: No new environment variables, no new imports, no new classes or methods.

## Alternatives Considered

1. **Remove absolute timeout entirely (chosen)**: Simplest, most maintainable, aligned with industry standard.
2. **Increase threshold**: Would just postpone the same problem. Any cap will eventually hit a legitimately long session.
3. **Configurable timeout**: Adds complexity. The idle timeout already handles the "session stuck" case correctly.
4. **Per-request timeout**: Would require significant refactoring of the polling loop, not worth the complexity.

## Boundary Non-Goals

- No change to non-session/prompt methods (completion, status, etc. still use their own timeout)
- No change to ACP_IDLE_TIMEOUT value
- No change to timeout handling for other request methods
- No change to the ACP protocol or bridge configuration

## Residual Risk

- **Extremely low**: The idle timeout remains intact and actively protects against hung sessions. The only change is removing a redundant absolute timeout that had no semantic value beyond what the idle timeout already provides.
- If a session hangs without updating `last_activity_ts`, the idle timeout will still catch it.
- If a session produces output continuously for hours, it will not be interrupted — which is the desired behavior.
