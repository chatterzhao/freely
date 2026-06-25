---
local_id: raw-20260625T020333Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260625T020333Z-A
platform_ids: {}
primary_platform: ''
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T02:03:33Z'
updated_at: '2026-06-25T02:03:33Z'
intake_id: ''
author: ai-manager
channel: internal
session_refs: []
---

## 问题
`wt-close --force` currently allows bypassing gate/pretests errors with misleading examples, making it easy for developers to mistakenly use `--force` to skip legitimate checks instead of fixing the underlying issue. The `--force` flag should be strictly for abandon-only scenarios where the raw issue is being discarded.

## 修复
- `--help` now states `--force` = 确定丢弃此 raw issue
- Add explicit list of scenarios that should NOT use `--force`
- pretests gate error now shows 保留→fix vs 放弃→force paths
- Removed misleading examples that implied `--force` for non-abandon scenarios
