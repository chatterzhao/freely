---
local_id: raw-20260703T162506Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260703T162506Z-A
platform_ids:
  github:
    issue_id: '3714'
    url: https://github.com/chatterzhao/freely/issues/3714
    synced_at: ''
  gitee:
    issue_id: IJYPOO
    url: https://gitee.com/zhaoquan/freely/issues/IJYPOO
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-03T16:25:28Z'
updated_at: '2026-07-03T16:25:28Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Bug
_update_agent_table_slot searches for 'agent_id =' (e.g. 'worker_01 =') 
but agent-table.toml has 'worker_id = "worker_01"' — the pattern never matches.
Log message 'updated worker_01 slot → ...' is printed unconditionally — a lie.

## Fix
Search for '_id = "{agent_id}"' pattern instead.
