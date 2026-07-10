---
local_id: raw-20260615T084023Z23Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2746'
    url: https://github.com/chatterzhao/freely/issues/2746
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-15T08:40:39Z'
updated_at: '2026-06-17T00:22:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
absorbed_into: raw-20260710T005219Z---

## Problem

Two governance gaps allow bypassing wt-close lifecycle:

1. git worktree remove --force has no hook to block it.
   The reference-transaction hook only intercepts ref changes,
   not worktree metadata operations. This allows removing worktrees
   without wt-close's frontmatter updates, issue sync, or governance checks.

2. wt-close requires the main repo to be on a non-protected branch
   (checks git -C ROOT_DIR rev-parse --abbrev-ref HEAD).
   But the main repo is always on develop for Freely self-hosting.
   This means wt-close is unusable from develop, forcing manual workarounds.

## Needed

1. Gate for git worktree remove on managed branches (fix/feature/hotfix/test-pre-merge)
2. Gate for git push --delete on managed branches  
3. Fix wt-close to work when called from develop worktree
   (close OTHER branches, not develop itself)
