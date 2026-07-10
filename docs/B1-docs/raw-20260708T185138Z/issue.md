---
local_id: raw-20260708T185138Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260708T185138Z-A
platform_ids:
  github:
    issue_id: '3826'
    url: https://github.com/chatterzhao/freely/issues/3826
    synced_at: ''
  gitee:
    issue_id: IJZRZN
    url: https://gitee.com/zhaoquan/freely/issues/IJZRZN
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T18:51:59Z'
updated_at: '2026-07-08T18:51:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n## 问题

### Bug 1: _sync_issues_changed_in_merge git diff 路径过滤器用绝对路径
pr-merge-guarded 第 487 行: git diff --name-only ... -- "$issues_dir"。$issues_dir 是 worktree 绝对路径（/Users/.../freely-worktrees/.../docs/B1-docs），而 git diff -- 需要 repo-relative 路径（docs/B1-docs）。绝对路径不匹配 → git diff 返回空 → changed_issues 为空 → return 0 跳过 → issue-sync 静默不执行。

修复: git diff -- "docs/B1-docs"（repo-relative），读文件仍用 $issues_dir（worktree absolute）。

### Bug 2: 上次 PR 残留的手动修复未正规化
- raw-20260708T174039Z issue.md 缺少 platform_state: closed（已手动补上但 stash 在 develop）
- milestones.md 中 M-20260708T174039Z-A 有重复空 section（已手动删除但 stash 在 develop）
这两个修改在 git stash 中，需要走正规流程提交到 develop。

## 修复

1. pr-merge-guarded: git diff path filter 改为 repo-relative
2. 将 stash 中的 platform_state 和 milestone fix pop 到新工位，按流程提交
