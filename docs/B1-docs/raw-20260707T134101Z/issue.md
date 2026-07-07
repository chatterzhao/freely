---
local_id: raw-20260707T134101Z
kind: raw
phase_state: absorbed
absorbed_into: 'I-20260707T134101Z-A'
platform_ids:
  github:
    issue_id: '3805'
    url: https://github.com/chatterzhao/freely/issues/3805
    synced_at: ''
  gitee:
    issue_id: IJZHCZ
    url: https://gitee.com/zhaoquan/freely/issues/IJZHCZ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T13:41:24Z'
updated_at: '2026-07-07T13:41:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 审计结果

以下命令中存在绕过 platform-adapter 的硬编码平台调用：

### pr-merge-guarded（最严重）
- L433: `for platform in gitee` — 只迭代 Gitee，漏了 GitHub
- L436: 直接调 `gitee` CLI 而不是 adapter
- L272-285: `gh api` 原始 GitHub API 调用
- L527: `git push origin` — 只推一个平台
- L575: `gh pr list` — 直接调 gh
- L611-612: 错误消息建议 `git push github` / `git push origin`（引导用户用原子命令！）
- L653: issue-sync commit 后没有自动同步 test worktree → 导致 dev↔test 不一致循环

### pr-review-guarded
- L141: `gh pr list --repo chatterzhao/freely` — 硬编码 repo 名
- L547-552: 自己的平台检测逻辑（应该用 adapter）

### pr-create-guarded
- L374: `git pull --no-rebase origin` — 硬编码 origin
- L424-447: 自己的平台检测逻辑（应该用 adapter）
- L482: `git push --force-with-lease` — 没走 adapter

### wt-close
- L670: `gh issue list --repo chatterzhao/freely` — 硬编码 repo
- L673: `gitee issue list --repo zhaoquan/freely` — 硬编码 repo
- L678: `platform-adapter.py close github` — 只关 GitHub
- L808-810: `gitee-issue.py delete-branch` — 直接调 gitee CLI

## 修复方案

1. **所有平台操作走 platform-adapter**：create/close/comment/push 统一封装
2. **issue-sync 后自动同步 test worktree**：commit → cd test && git merge → cd dev && push
3. **消除硬编码 repo 名**：从 remote URL 自动检测
4. **消除直接 gh/gitee CLI 调用**：改为 adapter 方法

## 原则

platform-adapter 设计意图：新平台只需维护 adapter，配置读取，自动执行。硬编码破坏了这个设计。
