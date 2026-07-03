---
local_id: raw-20260703T003829Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260703T003829Z-A
platform_ids:
  github:
    issue_id: '3699'
    url: https://github.com/chatterzhao/freely/issues/3699
    synced_at: ''
  gitee:
    issue_id: IJYGUQ
    url: https://gitee.com/zhaoquan/freely/issues/IJYGUQ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-03T00:38:50Z'
updated_at: '2026-07-03T00:38:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Bug

write_workcell_state() sources old workcell-state.env to read LAST_ENTRYPOINT_MODE (line 8426). Unquoted multi-word values like `LAST_WORKER_CLOSEOUT_GATE_COMMAND=freely pr-create-guarded` get executed as commands (VAR=val cmd syntax). pr-create-guarded runs during daemon startup and fails on develop.

## Root Cause

`source "$state_file"` in write_workcell_state() — unsafe for env files with space-containing values.

## Fix

Replace source with meta_env_value to safely read LAST_ENTRYPOINT_MODE.
