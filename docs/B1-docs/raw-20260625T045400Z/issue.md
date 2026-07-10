---
local_id: raw-20260625T045412Z00Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3478'
    url: https://github.com/chatterzhao/freely/issues/3478
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T04:54:19Z'
updated_at: '2026-06-25T04:54:19Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T045400Z-A
source_candidate: docs/B1-docs/raw-20260625T045412Z00Z/candidates.md#C-20260625T045400Z-A

platform_state: closed---

## 改动

platform-adapter.py:
1. create-issue CLI 子命令：调用已有 create_issue()，接受 local_id/title/body
2. comment CLI 子命令：调用新 comment_issue()，接受 local_id/comment

已有子命令不变：search, fetch, close, pull, create-pr, merge-pr, close-pr

## 设计

所有平台操作通过 adapter 统一。适配器内部根据 FREELY_REPO_PLATFORMS 遍历平台执行。

## 依赖关系

#3464（FREELY_REPO_PLATFORMS 自动检测可用后，adapter 基于它决策）

## 不是本 issue

- 各命令迁移用 adapter → 独立 issue
