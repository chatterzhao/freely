---
local_id: raw-20260620T083454Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T083454Z-A
platform_ids:
  github:
    issue_id: '3153'
    url: https://github.com/chatterzhao/freely/issues/3153
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T08:35:12Z'
updated_at: '2026-06-21T18:29:02Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Bug
task-source-scan reports 74 items as incomplete (dev_worktree_missing, b1_brainstorm_missing, etc.) but all have phase_state=absorbed/dropped/completed in their frontmatter.

## Root Cause
Scan checks file/directory existence (e.g., does docs/pre-brainstorms/{key}--{slug}/brainstorms.md exist?) instead of reading phase_state from issue frontmatter.

## Fix
In the lifecycle scan logic, before reporting an item as incomplete with dev_worktree_missing or b1_brainstorm_missing, check:
1. Does the issue.md frontmatter exist?
2. If yes, read phase_state field
3. If phase_state is absorbed/dropped/completed, skip the item

## Impact
47 items shown as ready_for_work, 27 as blocked. None are actually actionable. This blocks Manager patrol from finding real work.

## Files
- docs/system/workspace/scripts/runtime/freely (lifecycle scan logic)
