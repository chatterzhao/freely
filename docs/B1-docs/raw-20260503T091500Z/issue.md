---
local_id: raw-20260503T091500Z00Z
kind: raw
priority: high
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
phase_state: dropped
source: platform
platform_ids:
  github:
    issue_id: "180"
    owner: chatterzhao
    repo: freely
created_at: "2026-05-03T09:15:00Z"
title: "feat: enforce test-pre-merge before develop merge"
platform_state: closed
---
## 问题
hotfix→develop 跳过 test-pre-merge，pretests-gate 不触发。
所有非紧急合并走 feature→test-pre-merge→develop 完整链路。

## 要求
- 所有合并到 develop 必须先通过 test-pre-merge
- hotfix 分支也需要走 test-pre-merge
- 仅在紧急时可绕过（须有理由记录）
