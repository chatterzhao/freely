---
local_id: raw-20260627T121248Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3593'
    url: https://github.com/chatterzhao/freely/issues/3593
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
absorbed_into: I-20260627T121248Z-A
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-27T12:13:07Z'
updated_at: '2026-06-27T12:13:07Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Bug
- --worker-pid infrastructure exists (a2a_task.py set_worker_pid) but manager never calls it on insert
- delivery_status stays pending even after worker completion

## Fix
- freely insert: add --worker-pid flag
- worker a2a-exit: update delivery_status to delivered
