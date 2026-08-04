---
local_id: raw-20260720T055358Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260720T055358Z-A
platform_ids:
  github:
    issue_id: '4056'
    url: https://github.com/chatterzhao/freely/issues/4056
    synced_at: ''
  gitee:
    issue_id: IK29JY
    url: https://gitee.com/zhaoquan/freely/issues/IK29JY
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T05:54:24Z'
updated_at: '2026-07-20T05:54:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---



# fix: wt-create silent exit when issue.md lacks phase_state

## Root cause

Line 311 of docs/system/workspace/scripts/worktree/wt-create:
  _phase=$(grep 'phase_state:' ... | head -1 | sed | tr)

When issue.md has no phase_state field (e.g. chain_trace merged_develop items), grep returns exit code 1. With set -euo pipefail, this propagates through the pipeline and causes the entire script to exit silently — no error message, no worktree creation.

## Fix applied (2026-07-20 patrol)

Added || true after the pipeline on line 311:
  _phase=$(... | tr -d "'\"" || true)

## Work needed

Worker: commit the fix → pr-create-guarded → pr-merge-guarded → wt-close. Affects file: docs/system/workspace/scripts/worktree/wt-create
