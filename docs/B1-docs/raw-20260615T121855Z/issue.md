---
local_id: raw-20260615T121855Z55Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2774'
    url: https://github.com/chatterzhao/freely/issues/2774
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-15T12:19:12Z'
updated_at: '2026-06-21T20:12:21Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed---

## Problem

freely-db-cli callers silently suppress all errors with `>/dev/null 2>&1 || true`.
When the DB daemon stops between cycles, session IDs and tool_switch records
are lost with zero visibility. The runtime has no way to know why session
persistence failed.

Key call sites:
- _tool_switch_writeback_session_id (monitor-ai-acp.sh)
- _tool_switch_atomic_write (freely)
- session.get-active, session.tool-switch-read (freely)

## Fix

1. Replace `>/dev/null 2>&1 || true` with structured error logging to a known path
2. Runtime reads error log and surfaces to continuity/handoff
3. Add timeout+retry for DB operations (socket may be temporarily unavailable during daemon restart)

This makes DB failures visible instead of silent, enabling the runtime to
self-heal (e.g., restart DB daemon, retry, or gracefully degrade).
