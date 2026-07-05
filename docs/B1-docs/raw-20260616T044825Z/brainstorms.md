# Brainstorms: Remove BRIDGE_TIMEOUT Absolute Cap

## Discovery

**Source**: Local raw issue (raw-20260616T044825Z) — direct implementation task from human instruction.

**Original problem**: BRIDGE_TIMEOUT=1800s imposes an absolute 30-minute wall-clock limit on session/prompt in `acp-bridge.py`. This kills legitimate long-running AI sessions even when the AI is actively producing output. The timeout is unconditional — it does not distinguish between an idle session and a session that is actively producing output but happens to run past 30 minutes.

**Root cause**: `_send_request()` in `acp-bridge.py` uses a `deadline = time.time() + timeout` pattern and checks `while time.time() < deadline:`. After the loop exits (or times out), it checks `if not event.is_set():` and raises `TimeoutError` with the absolute timeout message. This means even if the AI is actively streaming output, once the 30-minute wall clock runs out, the session is killed.

**Why this can't be fixed without code change**: The deadline check is in the code — there is no configuration toggle or environment variable to disable it. The only fix is to remove the absolute timeout check and rely solely on the idle timeout.

## Research

We checked 6 ACP (AI Communication Protocol) projects — none use absolute wall-clock caps. All use only idle timeouts. This confirms the industry standard: absolute timeouts are an anti-pattern for long-running AI sessions because:

1. AI sessions for complex tasks can legitimately run >30 minutes while actively producing output.
2. Absolute timeouts introduce non-deterministic failures that are hard to reproduce.
3. Idle timeouts are sufficient to detect hung sessions — if the AI is not producing output for ACP_IDLE_TIMEOUT seconds, the session is clearly stuck and should be killed.

The existing idle timeout (ACP_IDLE_TIMEOUT) is already in place and works correctly. It tracks `last_activity_ts` and raises `TimeoutError` when no activity is detected for the configured period.

## Decision

Remove the absolute timeout check entirely. Change the while loop from `while time.time() < deadline:` to `while True:`, and remove the post-loop `if not event.is_set()` absolute timeout check block. The session/prompt handling will then only use the idle timeout.

This is a minimal, safe change:
- The idle timeout remains as the sole safeguard against hung sessions.
- Sessions that are actively producing output will not be killed.
- The change aligns with industry standard practice.
- No configuration changes needed — existing ACP_IDLE_TIMEOUT continues to work as before.

No alternatives considered because:
- Adding a configurable absolute timeout would still have the same fundamental problem (just with a different threshold).
- Removing only the deadline but keeping the post-loop check would leave dead code.
- The idle timeout alone is sufficient and is the industry standard.

**Next action**: Already implemented and committed. Proceed to candidate promotion and B2_IBM materialization for governance gate compliance.
