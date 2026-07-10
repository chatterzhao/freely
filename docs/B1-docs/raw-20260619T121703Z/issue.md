---
local_id: raw-20260619T121703Z03Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T121703Z-A
platform_ids:
  github:
    issue_id: '3061'
    url: https://github.com/chatterzhao/freely/issues/3061
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T12:17:19Z'
updated_at: '2026-06-19T12:17:19Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Root cause

freely script line 12834-12835: consume_delegate_workers prints worker tasks as
tab-separated lines: task_id<TAB>message<TAB>worktree<TAB>branch<TAB>raw_key<TAB>skill

But message contains 11+ newlines (multi-paragraph worker prompt). Each newline
breaks the line-based while-read loop. Only the first fragment is read — subsequent
lines have no tabs, causing the loop to skip all tasks via the 'tid and msg' guard.

## Impact

All 18 worker tasks silently skipped. Manager creates them, Runtime finds them,
but every single one is discarded before launch. Active worker count always 0.

## Fix

Insert msg = msg.replace('\n', ' ').replace('\r', '') before the tab-separated
print at line 12835. Messages become single-line, while-read loop works correctly.
