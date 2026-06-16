---
kind: raw
issue_id: raw-20260616T044825Z
title: Remove BRIDGE_TIMEOUT absolute cap for session/prompt in acp-bridge.py
key: raw-20260616T044825Z
description: BRIDGE_TIMEOUT=1800s imposes an absolute 30-minute wall-clock limit that
  kills legitimate long-running AI sessions. Remove the absolute timeout, keep only
  idle timeout.
phase_state: absorbed
---

BRIDGE_TIMEOUT=1800s imposes an absolute 30-minute wall-clock limit on session/prompt in acp-bridge.py. This kills legitimate long-running AI sessions even when the AI is actively producing output. Industry standard (6 ACP projects checked): none use absolute caps, only idle timeouts.

## Changes needed
- Remove the absolute timeout check in `_send_request()` in `docs/system/workspace/scripts/runtime/acp-bridge.py`
- Change `while time.time() < deadline:` to `while True:`
- Keep only the idle timeout check
