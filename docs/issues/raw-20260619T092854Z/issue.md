---
local_id: raw-20260619T092854Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T092854Z-A
platform_ids:
  github:
    issue_id: '3051'
    url: https://github.com/chatterzhao/freely/issues/3051
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T09:29:11Z'
updated_at: '2026-06-21T20:13:55Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Root Cause

freely_db_manager.py line 991-1016, a2a_task.insert handler:

- Column names: 20 (task_id..error)
- ? placeholders: 21  
- VALUES tuple params: 19

SQLite returns '21 values for 20 columns', insert fails silently.
A2A Server does not check save() return value, returns ok:true with
a generated UUID that was never persisted.

## Impact

- Every a2a-exit call returns ok:true, task_id, but task never stored
- list --role worker --status submitted always returns []
- worker_prompts_csv always none
- Manager cannot delegate any Worker — entire A2A delegation chain broken
- 46 stale manager tasks accumulated in DB, 0 worker tasks created since June 15

## Fix

1. Add missing params.get('prompt_file', '') between position 10 and 11
2. Remove extra ? from VALUES (21→20)
3. Verify column-to-value alignment for positions 11-20
