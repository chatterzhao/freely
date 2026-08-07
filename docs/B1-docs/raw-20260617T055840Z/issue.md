---
local_id: raw-20260617T055840Z40Z
kind: raw
phase_state: dropped
platform_state: closed
completed_at: '2026-08-07T06:00:00Z'
closeout_note: legacy raw closeout (platform closed)
platform_ids:
  github:
    issue_id: '2893'
    url: https://github.com/chatterzhao/freely/issues/2893
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T05:58:56Z'
updated_at: '2026-06-17T06:27:15Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-06-17T06:27:15Z'
force_closed_reason: phase_state field fix only, code already merged to develop
---

## 问题
develop 分支可以被 GitHub UI "Merge pull request" 直接合入，绕过 pr-merge-guarded 的所有 governance gate。近期 ACP/A2A 的 3 个 PR (#2879, #2881, #2882) 均通过此路径合并，导致 rebase 丢失代码未被发现。

## 修复
1. 去掉 pr-merge-guarded 中的 `gh pr merge --admin`，改为 `gh pr merge`（服从 branch protection）
2. pr-merge-guarded 在 merge 前通过 GitHub API 将 `governance/pr-merge-guard` check run 设为 success
3. 配置 develop 分支 ruleset：require `governance/pr-merge-guard` check pass
4. GitHub UI merge 按钮自然灰掉，只有 pr-merge-guarded 能合入

## 影响文件
- `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- `.github/workflows/pr-merge-guard.yml`
- GitHub repo settings（develop branch protection ruleset）

## 验收
- [ ] GitHub UI "Merge pull request" 按钮灰掉（check 未通过）
- [ ] pr-merge-guarded 正常合并（check 被设为 success）
- [ ] 手动 `git merge` 到 develop 仍被 pre-merge-commit hook 拦截
