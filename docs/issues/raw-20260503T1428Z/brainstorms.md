# Brainstorm: run-acp-prompt.py Disconnects Before Bridge Finishes

## Source

- Issue: #187 (raw-20260503T1428Z)
- Root cause: confirmed — run-acp-prompt.py closes bridge socket immediately after receiving `stopReason=end_turn`, before the bridge finishes sending all follow-up `session/update` notifications.

## Architecture Context

```
run-acp-prompt.py ←→ [Unix socket] ←→ acp-bridge.py ←→ claude-agent-acp
```

- **run-acp-prompt.py**: ACP JSON-RPC client. Sends `session/prompt`, receives streaming `session/update` notifications (text chunks) via `_recv_loop` daemon thread, then receives the final response with `stopReason`.
- **acp-bridge.py**: Persistent relay. Keeps `claude-agent-acp` alive across AI cycles. Forwards client requests to server, broadcasts server notifications to all connected clients, sends server responses back to the requesting client.
- **freely** daemon: Monitors AI process (`monitor-ai-cli.sh` → `run-acp-prompt.py`). On non-zero exit, increments restart storm counter. If `RESTART_STORM_COUNT` (currently 4) is exceeded within `RESTART_STORM_WINDOW_SECS` (30s), triggers restart storm escalation.

## Root Cause — Detailed Trace

1. run-acp-prompt.py calls `client.request("session/prompt", ...)` — this sends a JSON-RPC request and blocks waiting for the matching response.
2. `acp-bridge.py` forwards the request to `claude-agent-acp` via `_send_request()`.
3. `claude-agent-acp` processes the prompt and writes to stdout:
   - Multiple `session/update` notifications (text chunks, tool calls)
   - The final response `{id: N, result: {stopReason: "end_turn", ...}}`
   - Potentially MORE `session/update` notifications after the response (session summary, usage info, etc.)
4. `acp-bridge.py` `_read_stdout()` thread reads each line and dispatches:
   - Notifications → `_broadcast_notification()` → sent to all connected clients
   - Response → sets pending event → `_send_request()` returns
5. Bridge sends the response to run-acp-prompt.py via `conn.send()`.
6. run-acp-prompt.py receives the response in `_recv_loop` → `_handle_message()` → matches pending request → `request()` returns.
7. `send_prompt()` extracts `stopReason=end_turn`, prints it, returns.
8. The `finally` block runs `client.close()` → `SocketTransport.close()` → `sock.shutdown(socket.SHUT_RDWR)` + `sock.close()`.
9. **The socket is now closed, but the bridge's `_read_stdout()` thread may still be reading post-response notifications from the server's stdout.**
10. Bridge calls `_broadcast_notification()` for these notifications → `sock.send(data)` → **BrokenPipeError** (client already disconnected).
11. Bridge logs `send response error: [Errno 32] Broken pipe` and removes the dead client socket.
12. The Broken pipe error — and the general disruption of the bridge's client management — contributes to the AI cycle being marked with rc=1 upstream, triggering a restart storm.

### Why rc=1

The precise mechanism from Broken pipe to rc=1:

- **Path A**: The bridge's `_read_stdout()` thread encounters an error cascading from the broken client connection, causing the bridge to become unstable or restart its server process. This disrupts the `session/update` notification delivery, causing run-acp-prompt.py to exit with an exception → rc=1.
- **Path B**: The bridge fails to cleanly forward the final response to the client due to the race condition, causing run-acp-prompt.py to timeout or get a partial response → rc=1.

Both paths lead to the daemon seeing `ai process exited rc=1` and incrementing the restart storm counter.

### Timing Evidence (from issue)

```
21:20:03  bridge: session/prompt id=5 sent
21:22:31  bridge: send response error: [Errno 32] Broken pipe
21:22:41  daemon: ai process exited rc=1 → restart storm triggered
```

## Fix Option 1: Grace Period Before Disconnect (run-acp-prompt.py)

**Approach**: After receiving `end_turn`, wait 2 seconds before closing the socket. This gives the bridge time to finish sending any outstanding `session/update` notifications.

**Implementation**: Modify `main()` in `run-acp-prompt.py` to add a `time.sleep(2)` before `client.close()`, but only in non-loop mode when `stop_reason == "end_turn"`.

**Effectiveness**: **High**. Directly addresses the root cause. The 2s grace period covers the typical window for post-response notifications. If the server takes longer, the bridge still gets Broken pipe, but the window is greatly reduced.

**Risk**: 
- Minimal: 2s delay per AI cycle is negligible (cycles are typically minutes long).
- If the server takes >2s to send post-response notifications, the issue could still occur. But this is unlikely in practice.
- No behavior change for loop mode (already stays connected).

**Complexity**: Low. One file, ~3 lines of code.

**Files**:
- `docs/system/workspace/scripts/runtime/run-acp-prompt.py` — add `time.sleep(2)` before `client.close()` in non-loop mode.

## Fix Option 2: Don't Treat Broken Pipe as Failure (Daemon/Bridge)

**Approach**: Modify the daemon or bridge to treat Broken pipe as non-fatal when valid output exists (i.e., when `stop_reason=end_turn` was received and text was produced).

**Sub-options**:

**2a. Bridge side**: In `handle_client()`, when `conn.send()` fails with BrokenPipeError, don't propagate to the caller as an error. The bridge already catches this, but the broader disruption (server restart, etc.) needs to be prevented.

**2b. Daemon side**: In `freely`, normalize rc=1 to rc=0 when:
   - The AI process exited with rc=1
   - The cycle log contains `stop_reason=end_turn`
   - There is non-trivial output text
   
   The daemon already has an rc normalization pattern (line 19048-19052: normalizing rc=1→0 when `SessionEnd:.*completed with status 0` is found in the debug log). This extends that pattern.

**Effectiveness**: Medium. Mitigates the symptom (restart storm from Broken pipe) but doesn't fix the root cause. Bridges that lose client notifications may still have issues with session state tracking.

**Risk**:
- Medium: Could mask real errors. A genuine Broken pipe (e.g., client crash) would also be suppressed.
- Need careful heuristics to distinguish "harmless Broken pipe after valid output" from "genuine failure".
- The rc normalization already exists for a similar pattern (Claude Code -p mode exit 1 after clean session end), so this follows an established pattern.

**Complexity**: Medium. Requires adding Broken pipe detection + output validation logic.

**Files**:
- `docs/system/workspace/scripts/runtime/freely` — add rc=1→0 normalization for Broken pipe + valid output case.
- `docs/system/workspace/scripts/runtime/acp-bridge.py` — optionally, add more graceful handling.

## Fix Option 3: Increase RESTART_STORM_COUNT Threshold

**Approach**: Change `RESTART_STORM_COUNT` from 4 (currently coded) to 10.

**Effectiveness**: **Low**. Does not fix the root cause. Only increases the number of rapid restarts required to trigger the storm escalation. The bridge and server processes still churn unnecessarily.

**Risk**: During a real restart storm (genuine failure), it would take longer to detect and escalate. The system would burn more cycles before entering the observe-delay state. This reduces the sensitivity of the restart storm detection mechanism.

**Complexity**: Trivial. One constant change.

**Files**:
- `docs/system/workspace/scripts/runtime/freely` — line 3669: change `RESTART_STORM_COUNT=4` to `RESTART_STORM_COUNT=10`.

## Decision Framework

| Criteria | Option 1 (Grace) | Option 2 (Mask) | Option 3 (Threshold) |
|---|---|---|---|
| Fixes root cause | Yes | No | No |
| Prevents restart storm | Yes | Partially | Partially |
| Risk of masking real bugs | None | Medium | Low |
| Implementation complexity | Low | Medium | Trivial |
| Lines changed | ~3 in 1 file | ~15 in 1-2 files | 1 in 1 file |
| Testing effort | Low (timing-based) | Medium (output validation) | Low |

## Interaction Effects

- **Option 1 + Option 2**: The strongest defense. Fix the root cause (grace period) AND add a safety net (Broken pipe tolerance). Recommended combination.
- **Option 1 + Option 3**: Fix + higher safety margin. Option 3 becomes mostly unnecessary if Option 1 is effective.
- **Option 2 + Option 3**: Band-aid stack. Neither fixes the root cause.
