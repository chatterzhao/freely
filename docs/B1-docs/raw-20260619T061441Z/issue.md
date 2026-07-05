---
local_id: raw-20260619T061441Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T061441Z-A
platform_ids:
  github:
    issue_id: '3036'
    url: https://github.com/chatterzhao/freely/issues/3036
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T06:14:58Z'
updated_at: '2026-06-21T20:13:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

Root cause found: Manager prompt template uses --agent-id worker but a2a-exit handler reads --role instead. Result: tasks created with agent_id=manager (default), never found by list --role worker --status submitted. Manager continuity confirms 'Workers created via a2a-exit are never executed'. Fix: update prompt template line ~30-38 to use --role worker.
