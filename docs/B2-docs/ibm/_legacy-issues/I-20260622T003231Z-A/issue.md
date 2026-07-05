---
local_id: I-20260622T003231Z-A
kind: linked
phase_state: completed
milestone_state: committed
milestone: M-20260622T003231Z-A
platform_ids:
  github:
    issue_id: '3307'
    url: https://github.com/chatterzhao/freely/issues/3307
primary_platform: github
canonical_issue_path: docs/epics/hook-bash-local-fix
source_candidate: docs/B1-docs/raw-20260622T003231Z/candidates.md#C-20260622T003231Z-A
verification_artifact_dir: docs/epics/hook-bash-local-fix/code-reviews
created_at: '2026-06-22T00:32:48Z'
updated_at: '2026-06-22T00:32:48Z'
author: platform
channel: github
platform_state: open
---

# I-20260622T003231Z-A: Fix pre-push.sh local keyword for macOS bash compat

## Problem
`docs/system/workspace/hooks/pre-push.sh` uses `local` keyword outside a bash function. On macOS bash 3.x, `local` is only valid inside functions, causing immediate hook failure under `set -euo pipefail`. This blocks ALL gitee push operations.

## Solution
Replace `local _pid _ppid _cmd _is_wt_close=0` and `local _full_cmd` with plain variable assignments.

## Files Changed
- `docs/system/workspace/hooks/pre-push.sh`: 2 occurrences of `local` removed

## Verification
- git push to gitee should no longer fail with hook error
- wt-close remote branch deletion should work on gitee
