---
local_id: raw-20260625T131154Z54Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3503'
    url: https://github.com/chatterzhao/freely/issues/3503
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T13:12:14Z'
updated_at: '2026-06-25T13:12:14Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T131154Z-A
source_candidate: docs/B1-docs/raw-20260625T131154Z54Z/candidates.md#C-20260625T131154Z-A
promoted_issue_path: docs/issues/I-20260625T131154Z-A/issue.md
pre_tests_path: docs/B2-docs/pr-create-rebase/verification/pre-tests.md
---

## 问题

当多工位并行开发时，第一个 PR 合并到 develop 后，第二个工位分支落后于 develop。pr-create-guarded Step 3 使用 `git merge develop` 拉取最新代码，导致 develop 上所有新文件（来自其他已合并 issue）在一个 merge commit 中进入当前分支。

checkpoint-guard 检测到这个 merge commit 跨多个 scope（epics、pre-brainstorms、issues、scripts、skills 等），触发 MAX_SCOPE_COUNT 拦截，阻止提交。

## 修复

pr-create-guarded Step 3 改为 `git rebase develop` 替代 `git merge develop`：
- rebase 将每个 commit 逐个重放到 develop 最新位置，每个 commit scope 保持原样
- 如有冲突在 rebase 过程中逐个解决，不会产生跨 scope 的大 merge commit
- rebase 后需要 `--force-with-lease` push

## 改动

- docs/system/workspace/scripts/worktree/pr-create-guarded
