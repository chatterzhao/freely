---
local_id: raw-20260619T124418Z18Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T124418Z-A
platform_ids:
  github:
    issue_id: '3071'
    url: https://github.com/chatterzhao/freely/issues/3071
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T12:44:37Z'
updated_at: '2026-06-21T20:14:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

freely line 21483: manager_runtime_launch_workers_after_ai_cycle_if_needed called with >/dev/null. This suppresses all stdout from the function, making it impossible to debug why worker launches are failing. The function's log_info/log_warn go to stderr (daemon log), but the early-return printf messages and any unexpected errors are lost. Fix: remove >/dev/null.
