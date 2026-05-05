---
local_id: I-20260429-2040-A
issue_title: SQLite chat-inbox staging for protected-branch chat intake
kind: linked
phase_state: completed
promoted_from: raw-20260429-2040
platform_ids:
  github:
    issue_id: '220'
    url: https://github.com/chatterzhao/freely/issues/220
    synced_at: '2026-05-05T14:20:24Z'
  gitee:
    issue_id: ''
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/chat-inbox-sqlite/issues/I-20260429-2040-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-04-29T20:40:00Z'
updated_at: '2026-05-05T14:20:31Z'
session_refs:
- tool: ccds
  session_id: 20260429-chat-inbox-sqlite
  role: author
platform_state: closed
---

## Pre-Brainstorm Summary

SQLite-backed chat-inbox staging area. Chats write to DB instead of docs/issues/.
Three consumption triggers: chat-write (direct sync), wt-create (materialize), scan (AI judge).
