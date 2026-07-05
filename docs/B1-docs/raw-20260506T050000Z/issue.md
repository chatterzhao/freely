---
local_id: raw-20260506T050000Z00Z
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
kind: raw
source_family: chat_inbox
created: 2026-05-06 05:00:00+00:00
platform_ids:
  github:
    issue_id: '275'
    url: https://github.com/chatterzhao/freely/issues/275
    synced_at: '2026-05-10T09:29:11Z'
updated_at: '2026-06-21T20:15:02Z'
primary_platform: github
created_at: '2026-05-10T09:29:11Z'
platform_state: closed
---

# raw-20260506T050000Z: scan 增加远端分支治理面

## 现象

scan 的 `scan_worktree_governance` 只用 `git branch` 查本地分支，远端（GitHub/Gitee）上的未合并 feature 分支完全不可见。当前 Gitee 有 4 个未合并分支，scan 扫不到。

## 缺口

| 检查面 | 本地 | 远端 |
|---|---|---|
| 分支命名规范 | ✅ | ❌ |
| issue 已完成但分支未删 | ✅ | ❌ |
| 分支已合并到 develop | ✅ | ❌ |
| PR 状态 | ❌ | ❌ |

## 设计

### 新增 `scan_remote_branch_governance`

对每个配置的 remote（github, gitee）：
1. `git ls-remote --heads <remote>` 列出所有远端分支
2. 排除 main/develop
3. 检查是否 merged to develop（`git merge-base --is-ancestor`）
4. 已合并 → 报告 `ready_to_delete`（分支已合但未删除）
5. 未合并 → 按 issue key 分类：
   - 有 key 且 issue 未完成 → 跳过（chain_trace 覆盖）
   - 有 key 且 issue 已完成 → 报告 `stale_branch`（issue 已完但分支未合）
   - 无 key → 报告 `命名不规范`

### scan 输出增强

`next_action` 指引：
- `ready_to_delete` → "删除远端分支：git push <remote> --delete <branch>"
- `stale_branch` → "评估是否需合入 develop，或丢弃"
- 未合并 + 有 PR → "优先处理 PR，合并后再继续后续开发"

### 本地分支检查保留

现有 `scan_worktree_governance` 不变，继续检查本地 worktree 和分支状态。
