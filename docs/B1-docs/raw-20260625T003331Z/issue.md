---
local_id: raw-20260625T003331Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3455'
    url: https://github.com/chatterzhao/freely/issues/3455
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T00:33:31Z'
updated_at: '2026-06-25T02:21:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T003331Z-A
source_candidate: docs/pre-brainstorms/20260625T003331Z--feedback-platform-only/candidates.md#C-20260625T003331Z-A
---

## 问题

#3435 合并的 cmd_feedback 重写引入了回归：在 develop 上创建本地 docs/issues/ 文件 + 调用 issue-sync create。两者都被 develop 保护机制阻止，导致 freely feedback 在 develop 上不可用。

## 根因

#3435 的设计评审遗漏了关键约束：feedback 是 INPUT 操作，不应写本地文件。正确设计是：

- feedback: 纯平台操作（只创建 GitHub/Gitee issue），不写本地文件，允许在 develop 执行
- issue-sync create: 写本地文件 + 平台同步，应在 worktree 中执行
- raw-issue-pull: 从平台拉取到本地，应在 worktree 中执行

## 修复

重写 cmd_feedback 为平台-only 模式：
1. 去掉 --repo 参数（保留 #3435 的自动检测）
2. 去掉 _resolve_gh_repo()（保留 #3435 的删除）
3. 去掉本地文件创建 + issue-sync 调用
4. 直接用 gh + gitee-issue.py 创建平台 issue
5. 不创建 docs/issues/ 目录，不调用 issue-sync

## 改动

仅 docs/system/workspace/scripts/runtime/freely 中 cmd_feedback 函数。
