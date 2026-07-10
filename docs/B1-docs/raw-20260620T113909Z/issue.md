---
local_id: raw-20260620T113909Z09Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T113909Z-A
platform_ids:
  github:
    issue_id: '3162'
    url: https://github.com/chatterzhao/freely/issues/3162
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/issues/I-20260620T113909Z-A/issue.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T11:39:27Z'
updated_at: '2026-06-20T11:39:27Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Problem

pr-review-guarded commits the review document but only prints 'git push' as a next step instruction. It does NOT auto-push to the platform remotes like pr-create-guarded does.

pr-create-guarded auto-pushes to all platforms (github + gitee). pr-merge-guarded fetches review from github remote. When pr-review-guarded doesn't push, pr-merge-guarded fails with 'PR review missing.'

This breaks the workflow: after pr-review-guarded passes, the user has to manually git push, and if they forget or push to the wrong remote (e.g. origin/gitee instead of github), pr-merge-guarded can't find the review file.

## Fix

Add auto-push to all configured platforms in pr-review-guarded, using the same platform detection logic as pr-create-guarded.

## Expected Behavior

pr-review-guarded should:
1. Commit the review document (already does)
2. Auto-push to all configured platforms (same as pr-create-guarded)
3. NOT require manual git push step
