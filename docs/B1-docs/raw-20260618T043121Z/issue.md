---
local_id: raw-20260618T043121Z21Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T043121Z-A
platform_ids:
  github:
    issue_id: '2968'
    url: https://github.com/chatterzhao/freely/issues/2968
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T04:31:38Z'
updated_at: '2026-06-18T04:31:38Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Bug

PR #2958 added Step 0a cleanliness check to pr-create-guarded, but it's not detecting dirty worktree state.

### Suspected root cause

The check uses `git diff --quiet` after `cd "$ROOT_DIR"` where ROOT_DIR comes from `git rev-parse --show-toplevel`. While this returns the worktree path when run inside a worktree, the `2>/dev/null` may be swallowing git errors that should be surfaced.

### Investigation needed

1. Reproduce: create a dirty file in a fix/feature worktree, run pr-create-guarded
2. Check if git diff --quiet in the worktree correctly detects untracked files
3. Note: `git diff --quiet` only detects tracked file modifications, NOT untracked files
4. For untracked files, need `git status --porcelain` or `git ls-files --others --exclude-standard`
5. The `2>/dev/null` may hide git errors (e.g. if .git index is corrupt)
