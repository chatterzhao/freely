---
local_id: raw-20260621T133847Z47Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3220'
    url: https://github.com/chatterzhao/freely/issues/3220
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T13:38:47Z'
updated_at: '2026-06-21T13:38:47Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

# Fix: Inline Python -c quoting breaks manager_exit_contract_kind

## Root Cause
`"rows"` inside bash `-c "..."` inline Python strings silently breaks quoting. The inner `"` terminates the bash string → Python NameError → `|| echo "0"` → always 0. Affects 7 sites.

## Fix
Change `"rows"` → `'rows'` and `"exit_kind"` → `'exit_kind'` in all inline Python -c strings.

Absorbed into I-20260621T130954Z-A (PR #3219 follow-up).
