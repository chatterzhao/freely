---
local_id: raw-20260622T131109Z09Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260622T131109Z-A
platform_ids:
  github:
    issue_id: '3366'
    url: https://github.com/chatterzhao/freely/issues/3366
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T13:11:26Z'
updated_at: '2026-06-22T13:11:26Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

pr-merge-guarded 将 raw issue 的 phase_state 设为 absorbed（已被 I-* 吸收），这是正常完成状态。但 wt-close 只接受 completed，导致每次正常合并后关闭工位都需 --force + --reason。

## 修复

wt-close Phase 1 检查：`completed` 和 `absorbed` 都是有效完成状态。
`proposed`、`dropped` 等其他状态仍需 --force。

## 涉及

- `docs/system/workspace/scripts/worktree/wt-close` L294
