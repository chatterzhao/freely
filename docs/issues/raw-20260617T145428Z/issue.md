---
local_id: raw-20260617T145428Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2932'
    url: https://github.com/chatterzhao/freely/issues/2932
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T14:54:45Z'
updated_at: '2026-06-17T14:54:45Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Bug 1: freely-db-cli IndentationError

`docs/system/workspace/scripts/runtime/freely-db-cli` line 282: `for k in (` prefix missing before tuple, causing all CLI operations (db.ping etc.) to fail with IndentationError. Prevents daemon from detecting running freely-db.

## Bug 2: AGENTS.md workflow missing feedback entry

AGENTS.md §核心开发流程 starts with '问题发现（scan/chat/平台issue）' — `feedback` is buried as a sub-option in step 2 instead of being the explicit first entry. The correct branching: feedback → raw-issue OR scan → existing raw-issue/worktree.
