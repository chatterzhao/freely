---
local_id: raw-20260629T021625Z25Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260628T005815Z-A
platform_ids:
  github:
    issue_id: '3614'
    url: https://github.com/chatterzhao/freely/issues/3614
    synced_at: ''
  gitee:
    issue_id: IJXG5J
    url: https://gitee.com/zhaoquan/freely/issues/IJXG5J
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T02:16:49Z'
updated_at: '2026-06-29T02:16:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problems
1. wt-close line 917: local used outside function, breaks unmerged branch deletion
2. pr-merge-guarded: no next-step message after success, users forget wt-close

## Fix
1. wt-close: change local to regular var
2. pr-merge-guarded: print wt-close command and full flow after merge success
