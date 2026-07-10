---
local_id: raw-20260626T000126Z26Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3524'
    url: https://github.com/chatterzhao/freely/issues/3524
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T00:01:46Z'
updated_at: '2026-06-26T00:01:46Z'
intake_id: ''
author: platform
channel: github
session_refs: []
pre_tests_path: docs/B2-docs/wt-close-consistency/verification/pre-tests.md
absorbed_into: I-20260625T235348Z-A
source_candidate: docs/B1-docs/raw-20260625T235348Z48Z/candidates.md#C-20260625T235348Z-A
promoted_issue_path: docs/issues/I-20260626T000126Z-A/issue.md
platform_state: closed
---

## 问题

#3522 加了 consistency check 里的 CWD 安全，但 Phase 5 (worktree removal) 和 Phase 6 (local branch delete) 之间没有再次 cd，导致 consistency check 之后 CWD 仍在 worktree 内，git branch -d 同样 fatal。

## 修复
Phase 5 和 Phase 6 之前各加 `cd "$PROJECT_ROOT"`。

## 改动
- docs/system/workspace/scripts/worktree/wt-close: 2 lines
