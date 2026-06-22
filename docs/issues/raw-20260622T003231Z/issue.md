---
local_id: raw-20260622T003231Z
kind: raw
phase_state: absorbed
absorbed_into: fix/raw-20260622T003231Z-hook-fix
platform_ids:
  github:
    issue_id: '3307'
    url: https://github.com/chatterzhao/freely/issues/3307
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T00:32:48Z'
updated_at: '2026-06-22T00:32:48Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

The pre-push hook uses 'local' keyword outside a function at line 13, which fails on macOS bash 3.x. This blocks git push --delete operations. Fix: replace 'local' with compatible pattern.
