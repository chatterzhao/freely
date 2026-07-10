---
local_id: raw-20260620T115242Z42Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T115242Z-A
platform_ids:
  github:
    issue_id: '3164'
    url: https://github.com/chatterzhao/freely/issues/3164
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/issues/I-20260620T115242Z-A/issue.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T11:52:59Z'
updated_at: '2026-06-20T11:52:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Problem

### Bug 1: wt-close only closes raw issue, not absorbed I-* issue

wt-close calls `issue-sync close <raw_id>` to close the raw issue on GitHub. But when the raw issue has `absorbed_into: I-XXXXX-A`, the I-* issue (which has its own GitHub issue via platform_ids) is never closed.

This leaves I-* issues on GitHub as OPEN even after their implementing PR is merged, worktree cleaned up, and raw issue closed.

### Bug 2: issue-sync close fallback uses deprecated field

issue-sync's cmd_close() fallback for I-* issues (kind=linked) only checks `promoted_from` to find the parent raw issue. Since ~2026-06-20, new I-* issues use `parent_raw` instead of `promoted_from`. The field rename breaks the fallback.

## Fix

1. **wt-close**: after closing the raw issue, check if it has `absorbed_into` field pointing to an I-* issue. If that I-* issue has `phase_state=completed` and `platform_ids`, call `issue-sync close` on it as well.

2. **issue-sync close**: add `parent_raw` as an additional fallback field (in addition to `promoted_from`):
   ```bash
   local parent_id="$(_fm_get "$file" "parent_raw")"
   [[ -z "$parent_id" ]] && parent_id="$(_fm_get "$file" "promoted_from")"
   ```

## Impact

~30 I-* issues currently open on GitHub with phase_state=completed will be closeable once this fix is deployed and wt-close is re-run on them.
