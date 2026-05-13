# Candidate: Bridge Disconnect Fix (GitHub #187)

## Evaluation Summary

| Option | Approach | Score (1-5) | Verdict |
|---|---|---|---|
| 1 | Grace period in run-acp-prompt.py | 5 | **PRIMARY** — fix the root cause |
| 2 | Don't treat Broken pipe as failure | 3 | **DEFENSE-IN-DEPTH** — secondary guard |
| 3 | Increase RESTART_STORM_COUNT to 10 | 1 | **REJECT** — band-aid, reduces storm sensitivity |

## Option-by-Option Analysis

### Option 1: Grace Period (PRIMARY)

**Score**: 5/5

**Why**: Directly addresses the root cause. The race window is real and well-understood: run-acp-prompt.py shuts down the socket before the bridge finishes forwarding server notifications. A 2-second grace period closes this window with negligible latency cost.

**Implementation plan**:

In `run-acp-prompt.py`, modify the `finally` block (lines 478-484) to add a grace delay when the stop reason is `end_turn`:

```python
finally:
    if stop_reason == "end_turn" and not args.loop:
        time.sleep(2)  # grace period for bridge to finish sending notifications
    if args.loop:
        try:
            client.request("session/close", {"sessionId": session_id}, timeout=10)
        except Exception:
            pass
    client.close()
```

The `stop_reason` variable is already available in scope (set at line 451).

**Why 2 seconds?**:
- Post-response notifications (usage info, session summary) are typically delivered within <500ms.
- 2s provides a comfortable margin without being noticeable to the user (AI cycles are typically 30s-5m).
- Short enough that a genuinely crashed client would still be detected quickly by the daemon's wait loop (1s poll interval).

**Future-proofing**: Consider making the grace period configurable via environment variable (e.g., `ACP_DISCONNECT_GRACE_SECS`) for flexibility.

---

### Option 2: Broken Pipe Tolerance (DEFENSE-IN-DEPTH)

**Score**: 3/5

**Why**: Good as a secondary safety net, but insufficient alone. The daemon already has precedent for rc normalization (line 19048-19052 normalizes rc=1→0 when `SessionEnd:.*completed with status 0` is found in debug log). Extending this pattern for Broken pipe is natural, but the heuristics risk false negatives or masking real failures.

**Implementation plan**:

In `freely` (around line 19048-19052), extend the rc normalization:

```python
# Existing normalization:
if [[ "${rc:-0}" != "0" && -f "$cycle_debug_log" ]]; then
    if grep -q 'SessionEnd:.*completed with status 0' "$cycle_debug_log" 2>/dev/null; then
        rc=0
        log_info "normalized rc=1→0: clean SessionEnd detected in debug log"
    fi
fi

# New normalization: Broken pipe after valid output
if [[ "${rc:-0}" != "0" && -f "$cycle_log" ]]; then
    # Check the cycle log for evidence that the AI produced valid output
    # before the Broken pipe occurred (stop_reason=end_turn present)
    if grep -q 'stop_reason=end_turn' "$cycle_log" 2>/dev/null; then
        rc=0
        log_info "normalized rc=1→0: end_turn received before disconnect"
    fi
fi
```

**Why validate via `stop_reason=end_turn`**:
- `stop_reason=end_turn` is printed by run-acp-prompt.py at line 431 (`print(f"stop_reason={stop_reason}", flush=True)`) as the last action before the finally block.
- If this line exists in the cycle log, the AI completed its response successfully.
- The subsequent Broken pipe is purely a notification delivery issue, not a processing failure.

**Risk**: If run-acp-prompt.py crashes *after* printing `stop_reason=end_turn` but *before* completing the finally block, rc=1 would be incorrectly normalized. However:
- The script's output is already written and flushed at that point.
- The AI session completed successfully (end_turn was received).
- The only thing lost is post-response notifications.

---

### Option 3: Increase RESTART_STORM_COUNT (REJECT)

**Score**: 1/5

**Why**: Merely raises the threshold without addressing the underlying issue. The current value is already 4 (not 3 as stated in the issue description). Increasing to 10 would:
- Allow 10 rapid restarts before detection (vs. current 4).
- During a genuine failure, waste more cycles and time.
- Mask the problem without fixing it.
- The restart storm detection was designed to catch pathological restart loops; raising the threshold undermines that purpose.

**Verdict**: Do not implement. If the primary fix (Option 1) and secondary guard (Option 2) are both in place, this is unnecessary.

---

## Recommended Combination: Option 1 + Option 2

Apply both Option 1 (primary fix) and Option 2 (defense-in-depth) together.

**Rationale**:
| Layer | What it does | Failure mode covered |
|---|---|---|
| Option 1 | Prevents the race condition entirely | Normal operation |
| Option 2 | Falls back if grace period is insufficient | Server takes >2s or other edge cases |

**Not implementing**: Option 3 — reduces detection sensitivity with no benefit once Options 1+2 are in place.

---

## Files to Change

### 1. `run-acp-prompt.py` (Option 1)

**Path**: `docs/system/workspace/scripts/runtime/run-acp-prompt.py`

**Change**: Add `time.sleep(2)` in the `finally` block before `client.close()`, conditioned on `stop_reason == "end_turn"` and non-loop mode.

**Lines affected**: 478-484 (the `finally` block).

**Details**:
- `stop_reason` is already in scope after line 451.
- The sleep is only for non-loop mode because loop mode already keeps the connection alive between iterations.
- The sleep goes BEFORE `client.close()` to give the bridge time to drain its notification queue.

### 2. `freely` daemon (Option 2)

**Path**: `docs/system/workspace/scripts/runtime/freely`

**Change**: Add rc=1→0 normalization when the cycle log contains `stop_reason=end_turn`.

**Lines affected**: Around line 19048-19052, after the existing `SessionEnd` normalization.

**Details**:
- Insert new normalization block after the existing one (but before line 19054 `LAST_WORKCELL_EXIT_REASON=...`).
- Same pattern: check `rc != 0`, check cycle log for `stop_reason=end_turn`, set `rc=0` if found.
- Uses the same `$cycle_log` variable already available in scope.

---

## Test Plan

### Pre-implementation verification
1. Confirm the race condition exists by checking recent bridge logs for `send response error: [Errno 32] Broken pipe`.
2. Note the current RESTART_STORM_COUNT value (4) for baseline.

### Post-implementation verification
1. **Unit test**: Run `run-acp-prompt.py` with `--bridge-socket` and verify that `client.close()` is delayed by ~2s after `end_turn`.
2. **Integration test**: Simulate the race condition by sending a prompt, receiving `end_turn`, and checking that bridge does not log BrokenPipeError.
3. **Integration test**: Force rc=1 with `stop_reason=end_turn` in cycle log and verify daemon normalizes to rc=0.
4. **Edge case**: Loop mode — verify no delay is added (connection stays alive naturally).
5. **Edge case**: Error path (non-end_turn stop reason) — verify no delay is added.

### Rollback plan
- If Option 1 causes unexpected latency: reduce grace period to 500ms or make configurable.
- If Option 2 causes false normalization: tighten heuristics (e.g., also check that output text exists).

---

## Acceptance Criteria

1. Bridge logs no longer show `send response error: [Errno 32] Broken pipe` during normal AI cycles.
2. `run-acp-prompt.py` stays connected for at least 2 seconds after receiving `end_turn`.
3. Daemon normalizes rc=1→0 when `stop_reason=end_turn` is present in the cycle log.
4. Restart storm no longer triggers due to premature disconnect.
5. All existing tests pass (no regression in exit code handling).
