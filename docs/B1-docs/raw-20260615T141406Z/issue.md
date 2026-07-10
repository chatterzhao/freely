---
local_id: raw-20260615T141406Z06Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2777'
    url: https://github.com/chatterzhao/freely/issues/2777
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-15T14:14:23Z'
updated_at: '2026-06-21T20:13:27Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed---

## Revision from #2776

Original proposed git alias approach rejected: `command git` cannot bypass git config aliases.
Correct approach: shell function + auto-sourcing.

## Plan

1. Restructure bin/git-worktree-guard so it can work as both sourced function and PATH wrapper
2. Install guard to .freely/bin/ via sync_project_tooling
3. Add FREELY_WT_BYPASS_GUARD=1 env check to guard itself (defense in depth)
4. Fix wt-close line 393: bare `git worktree remove --force` → `FREELY_WT_BYPASS_GUARD=1 command git worktree remove --force`
5. Add guard auto-source to freely init/runtime (shell profile or PATH priority)

## Why shell function over git alias
- `command git` bypasses shell functions but NOT git config aliases
- Git has no --no-aliases flag
- Shell function is the standard Unix pattern (same as how nvm, rbenv, pyenv work)
