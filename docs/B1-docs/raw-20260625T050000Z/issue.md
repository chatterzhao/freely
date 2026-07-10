---
local_id: raw-20260625T050000Z00Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260625T050000Z-A
platform_ids:
  github:
    issue_id: '3456'
    url: https://github.com/chatterzhao/freely/issues/3456
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T00:36:54Z'
updated_at: '2026-06-25T00:36:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 改动

pr-create-guarded 当前 Step 1 是 git pull origin develop，在 gate 之前。每次 gate 失败重试都重复拉取。

改为：pull 移到 Step 3（push 之前），gate 全过才拉。

任何 gate 失败直接 exit 1，pull 永远不执行。

## 改动位置

docs/system/workspace/scripts/worktree/pr-create-guarded

- 删除当前 Step 1 的 git pull 逻辑
- 在 Step 2c（pretests gate）之后、Step 3（push）之前插入 pull
