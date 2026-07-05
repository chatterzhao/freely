---
local_id: raw-20260527T081215Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2334'
    url: https://github.com/chatterzhao/freely/issues/2334
    synced_at: '2026-05-30T05:39:10Z'
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: 2026-05-27 08:12:15+00:00
updated_at: '2026-06-17T00:20:42Z'
intake_id: ''
author: zhaoquan
channel: local
session_refs: []
platform_state: closed
---

## Problem

pr-create-guarded has a bug:  unbound variable when no --title/--body passed.
This forces use of FREELY_SKIP_CREATE_GATE=1 to bypass the gate entirely,
which defeats the purpose of the enforcement.

The pre-push hook correctly blocks pushes without pr-create-gate-passed marker,
but we've been skipping it for all recent PRs because the gate itself is broken.

## Fix

Fix gh_pr_args unbound variable error when no title/body params:
- Guard array expansion with conditional
- Or always provide a default title/body

Then restore proper flow: pr-create-guarded (no skip) for all future PRs.

## Files
- docs/system/workspace/scripts/worktree/pr-create-guarded
