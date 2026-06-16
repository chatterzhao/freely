---
local_id: I-20260616T044825Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260616T044825Z
source_candidate: docs/pre-brainstorms/20260616T044825Z--remove-absolute-timeout/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-16T04:48:25Z
updated_at: 2026-06-16T04:48:25Z
intake_id: ""
author: claude
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/epics/remove-absolute-timeout/remove-bridge-absolute-cap/pre-tests.md
verification_artifact_dir: docs/epics/remove-absolute-timeout/remove-bridge-absolute-cap/code-reviews
---

# I-20260616T044825Z-A: Remove BRIDGE_TIMEOUT absolute cap for session/prompt in acp-bridge.py

- source_candidate: `docs/pre-brainstorms/20260616T044825Z--remove-absolute-timeout/candidates.md`
- pre_tests_path: `docs/epics/remove-absolute-timeout/remove-bridge-absolute-cap/pre-tests.md`
- verification_artifact_dir: `docs/epics/remove-absolute-timeout/remove-bridge-absolute-cap/code-reviews`

## Summary

Remove the absolute timeout (BRIDGE_TIMEOUT=1800s) in `acp-bridge.py`'s `_send_request()` method for `session/prompt` handling. The absolute 30-minute wall-clock limit kills legitimate long-running AI sessions even when the AI is actively producing output. Only the idle timeout (ACP_IDLE_TIMEOUT) should remain.

## Changes

File: `docs/system/workspace/scripts/runtime/acp-bridge.py`

### Before (lines 415-435):
```python
if method == "session/prompt":
    poll_interval = min(ACP_IDLE_TIMEOUT // 2, 30)
    deadline = time.time() + timeout
    while time.time() < deadline:
        if event.wait(timeout=poll_interval):
            break
        with self.activity_lock:
            idle_secs = time.time() - self.last_activity_ts
        if idle_secs > ACP_IDLE_TIMEOUT:
            with self.server_lock:
                self.pending.pop(req_id, None)
            raise TimeoutError(
                f"idle timeout: no AI activity for {idle_secs:.0f}s "
                f"(limit={ACP_IDLE_TIMEOUT}s) waiting for {method}"
            )
    if not event.is_set():
        with self.server_lock:
            self.pending.pop(req_id, None)
        raise TimeoutError(
            f"absolute timeout ({timeout}s) waiting for {method}"
        )
```

### After:
```python
if method == "session/prompt":
    poll_interval = min(ACP_IDLE_TIMEOUT // 2, 30)
    while True:
        if event.wait(timeout=poll_interval):
            break
        with self.activity_lock:
            idle_secs = time.time() - self.last_activity_ts
        if idle_secs > ACP_IDLE_TIMEOUT:
            with self.server_lock:
                self.pending.pop(req_id, None)
            raise TimeoutError(
                f"idle timeout: no AI activity for {idle_secs:.0f}s "
                f"(limit={ACP_IDLE_TIMEOUT}s) waiting for {method}"
            )
```

## Rationale

- Industry standard (6 ACP projects checked): none use absolute caps, only idle timeouts.
- Absolute timeouts kill sessions that are actively producing output but happen to run past 30 minutes.
- The idle timeout (ACP_IDLE_TIMEOUT) already provides sufficient protection against hung sessions.
