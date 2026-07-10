---
local_id: raw-20260601T004034Z34Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2380'
    url: https://github.com/chatterzhao/freely/issues/2380
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-01T00:40:49Z'
updated_at: '2026-06-17T00:24:22Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed---

## Changes
1. Heartbeat-based supervisor liveness (replaces L220-L240 grace chain)
2. Parent-liveness check in heartbeat subprocess (no orphaned heartbeat)
3. select_launch_kind trusts _tool_switch_launch_kind session ID
4. Stall watchdog: bridge-dead only (no mtime false-positive)
5. Tool registry aliases field (comma-separated)
6. _resolve_tool_alias + dedup in fallback loop
7. AI_FALLBACK_TOOLS canonical names only
8. printf || true pipe guards
