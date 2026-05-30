---
local_id: raw-20260527T080702Z
kind: raw
phase_state: absorbed
platform_ids: {}
primary_platform: ''
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: 2026-05-27 08:07:02+00:00
updated_at: '2026-05-30T05:22:10Z'
intake_id: ''
author: zhaoquan
channel: local
session_refs: []
platform_state: closed
---

## Problem

codex-acp takes ~8 seconds to cold-start (fork + handshake), but
_ensure_acp_bridge_running only waits 5 seconds for the socket.
Bridge actually starts successfully, but supervisor sees "socket
did not appear" and exits before bridge is ready.

Race condition: bridge init at 00:47:56, socket at 00:48:04 (8s),
timeout check at 00:48:02 (6s).

## Fix

Increase bridge socket wait timeout from 5s to 15s in
_ensure_acp_bridge_running. Also increase per-cycle health check
timeout for the same reason.

## Files
- docs/system/workspace/scripts/runtime/freely:
  _ensure_acp_bridge_running socket wait loop
