---
local_id: raw-20260508T124041Z41Z
kind: raw
- phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17 04:47:25+00:00
platform_ids:
  github:
    issue_id: '258'
    url: https://github.com/chatterzhao/freely/issues/258
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-08T12:40:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

`wt-create` 在 `_require_issue_exists`（第 410-417 行）中调用 `_pull_raw_issue`，但此时工位还未创建（工位创建在第 542/548 行）。`_pull_raw_issue` 调用 `raw-issue-pull`，后者要求当前分支名包含 raw-key（拒绝 develop/main）。

结果：`--source platform` 的 wt-create 永远失败，因为 pull 在 develop 上执行。

## 设计意图

所有 pull 必须在 fix/feature 工位创建之后、从工位内部执行。工位分支名包含 raw-key，`raw-issue-pull` 的工位检查才能通过。

## 修复

1. `_require_issue_exists`：移除 pull 调用（保留 scan 验证）
2. 在 fix/feature 工位创建后：cd 入工位，执行 pull + fill_platform_ids

## 相关

- #256 已修复 reference-transaction hook delete 拦截（已合并）
- #257 platform-adapter.py 标题 key 标准化 bug

- pre_tests_path: docs/B2-docs/wt-create-pull-after-worktree/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/wt-create-pull-after-worktree/code-reviews
