---
local_id: raw-20260624T152500Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T152500Z-A
platform_ids:
  github:
    issue_id: '3442'
    url: https://github.com/chatterzhao/freely/issues/3442
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T15:32:22Z'
updated_at: '2026-06-24T15:32:22Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`pr-create-guarded` 当前只检查 IBM 文档（B1/B2 产物），不检查 pretests 执行证据。pretests-retirement-gate 只在 `wt-close` 阶段运行——太晚了，此时代码已合并。

## 应在 pr-create-guarded 中加入 pretests 检查

在 Step 2b（IBM governance gate）之前或之后，调用 `pretests-retirement-gate` 验证：
- workcell-state.env 存在
- pre-tests.md acceptance items 全部 pass
- 测试证据完整

这样可以在 PR 创建之前就拦截未测试代码，而不是等到 wt-close。

## 改动位置

`docs/system/workspace/scripts/worktree/pr-create-guarded`

## 注意

手工执行场景（没有 Worker 写 workcell-state.env）会被拦截——这是预期行为。手工执行应补充 workcell-state.env 再提交。
