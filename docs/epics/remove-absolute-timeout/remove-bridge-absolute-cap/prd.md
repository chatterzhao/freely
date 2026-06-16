# PRD: Remove BRIDGE_TIMEOUT Absolute Cap

## Goal

Remove the absolute 30-minute wall-clock timeout for `session/prompt` in `acp-bridge.py`, keeping only the idle timeout as the safeguard against hung sessions.

## Why

BRIDGE_TIMEOUT=1800s kills legitimate long-running AI sessions even when the AI is actively producing output. Industry standard (6 ACP projects checked) uses only idle timeouts.

## Dev-Loop Handoff

### Scope
- File: `docs/system/workspace/scripts/runtime/acp-bridge.py`
- Method: `_send_request()` — `session/prompt` handling (lines 415-435 pre-change)
- Remove: deadline tracking, absolute timeout check, post-loop `if not event.is_set()` block
- Change: `while time.time() < deadline:` → `while True:`

### Non-goals
- No change to non-session/prompt methods (they have their own timeout path)
- No change to ACP_IDLE_TIMEOUT value or behavior
- No change to configuration or environment variables
- No change to the ACP protocol itself

### Acceptance
1. Absolute timeout check removed from session/prompt handling
2. Idle timeout still functioning: raises TimeoutError when no activity for ACP_IDLE_TIMEOUT seconds
3. No regression in other method types (completion/status/etc.)
4. No syntax or runtime errors introduced
