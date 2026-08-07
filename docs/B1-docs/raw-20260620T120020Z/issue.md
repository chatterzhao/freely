---
local_id: raw-20260620T120020Z20Z
kind: raw
- phase_state: dropped
absorbed_into: I-20260620T120020Z-A
platform_ids:
  github:
    issue_id: '3166'
    url: https://github.com/chatterzhao/freely/issues/3166
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/issues/I-20260620T120020Z-A/issue.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T12:00:38Z'
updated_at: '2026-06-21T20:12:20Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Problem

PR #3165 introduced `local` variable declarations inside wt-close at script top-level (not inside a function). Bash only allows `local` inside functions. This breaks wt-close entirely with: `local: can only be used in a function`.

## Fix

Replace `local` with prefixed variable names (`_wt_i_*`) to avoid polluting the global namespace while still working at script top-level.
