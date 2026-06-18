---
local_id: raw-20260618T015503Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2956'
    url: https://github.com/chatterzhao/freely/issues/2956
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T01:55:21Z'
updated_at: '2026-06-18T01:59:58Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260618T015503Z-A
---

## 问题概述

Freely 的多个命令在操作 `docs/issues/`、milestones、epics 等治理文档时，使用的是**主仓库（develop）的路径**，而非当前 worktree 的路径。这导致：

1. develop 反复被弄脏（raw issue frontmatter 被直接修改）
2. 需要 `_absorb_close_frontmatter` + `git commit --amend` 这种不可靠的补救机制
3. wt-close 检查的是 develop 上的 phase_state，而非 worktree 的
4. 多 worktree 并发时互相覆盖 raw issue

## 根因：ROOT_DIR 解析方式不一致

| 命令 | ROOT_DIR 解析 | 实际指向 |
|---|---|---|
| wt-create | `git rev-parse --show-toplevel` + `cd $ROOT_DIR` | develop（因为从 develop 目录执行） |
| pr-create-guarded | `git rev-parse --show-toplevel` | worktree（在 worktree 内执行）✓ |
| pr-merge-guarded | 相对路径 `docs/issues/` | develop（在 develop 执行） |
| **wt-close** | `$(dirname $0)/../../../../..` | **硬编码 develop** ✗ |
| worktree-common.sh | `$(dirname $0)/../../../../..` | **硬编码 develop** ✗ |

## 受影响的全量路径

### docs/issues/raw-{key}/issue.md

| 命令 | 行号 | 当前路径 | 应该用 |
|---|---|---|---|
| wt-create `_pull_raw_issue` | 307 | `$ROOT_DIR/docs/issues/raw-${key}` | worktree 路径 |
| wt-create `_pull_raw_issue` | 330 | `$ROOT_DIR/docs/issues/raw-${key}/issue.md` | worktree 路径 |
| wt-create `_mark_raw_issue_absorbed` | 357 | `$ROOT_DIR/docs/issues/raw-${key}/issue.md` | worktree 路径 |
| wt-create `_ensure_scan_index` | 439,455,467,505,513,522 | `$ROOT_DIR/docs/issues/$key` | worktree 路径 |
| wt-create `_materialize_chat_if_needed` | 561 | `$target_path/docs/issues/$key` | ✅ 这个是 worktree 路径！ |
| pr-merge-guarded `_absorb_close_frontmatter` | 274 | `docs/issues/${raw_key}/issue.md` | **不需要了（见下文）** |
| pr-merge-guarded `_update_issue_phase` | 413 | `$PWD/docs/issues` | develop（合理，merge 后在 develop 执行） |
| wt-close Phase 1 check | 7,195,199 | `$ROOT_DIR/docs/issues/$issue_id/issue.md` | worktree 路径 |
| wt-close Phase 3 force-close | 300,302,308,310-312 | `$ISSUES_DIR/$issue_id/issue.md` | worktree 路径 |
| freely runtime `cmd_intake` | 6153 | `$worktree_found/docs/issues/$issue_id` | ✅ 这个已经是 |
| freely runtime `cmd_intake_chat` | 6180 | `$project/docs/issues/$target_issue/issue.md` | 取决于 $project 值 |

### 配置路径 config.toml

| 字段 | 当前值 | 问题 |
|---|---|---|
| PROJECT_ROOT | 硬编码绝对路径 | 用户安装后需手动修改。应支持相对路径或自动推导 |
| FREELY_HOME | 硬编码绝对路径 | 同上 |

### 硬约束

Freely 强制 worktrees 目录与项目主目录的相对位置：
```
{project-root}/                  ← 主仓库（develop）
{project-root}-worktrees/        ← 所有 worktree 的父目录
  ├─ fix-raw-{key}-{slug}/
  └─ feature-raw-{key}-{slug}/
```

这个约束意味着：从 worktree 内可以通过 `git worktree list` 或相对路径推导出主仓库位置，反之亦然。

## 正确架构

```
wt-create（在 develop 执行）
  ├─ 从平台/chat-inbox 拉取 raw issue
  └─ 物化到 worktree 的 docs/issues/raw-{key}/  ← 不是 develop！

fix worktree（可写工位）
  ├─ docs/issues/raw-{key}/issue.md  ← phase_state 在这里
  ├─ docs/epics/{name}/              ← code-review 等在这里
  ├─ docs/pre-brainstorms/{key}/     ← brainstorms/candidates 在这里
  ├─ 代码修改
  └─ git commit（phase_state 变更作为普通 commit 提交）

pr-create-guarded（在 worktree 内执行）
  ├─ ROOT_DIR = git rev-parse --show-toplevel → worktree ✓
  ├─ 检查 worktree 内的 phase_state
  ├─ 不达标 → 阻塞并告知需要达到什么标准
  └─ 达标 → push → create PR

pr-merge-guarded（在 develop 执行）
  └─ merge → worktree 的全部内容（含 raw issue + phase_state）自然进入 develop
      → 删除 _absorb_close_frontmatter！

wt-close（在 develop 执行）
  └─ 检查 develop 的 docs/issues/（此时已由 merge 带入）→ 只做 worktree 删除
      → 不再需要 Phase 3 force-close trace 写 develop！
```

## 需要注意的边界

1. **wt-create 的 ROOT_DIR 歧义**：当前用 `git rev-parse --show-toplevel`，它返回的是 CWD 所在 git 仓库的根。wt-create 从 develop 目录运行时返回 develop，但如果有人在 worktree 内运行，会返回 worktree。应显式区分"主仓库根"和"目标 worktree 根"。

2. **worktree 内的相对路径**：pr-create-guarded 在 worktree 内运行，`git rev-parse --show-toplevel` 返回 worktree 路径。但 worktree 可能没有自己的 `.freely/` 运行时目录——测试 pre-merge 会通过 `pre-init-runtime` 复制，但普通 fix/feature worktree 不会。

3. **多平台部署**：用户用 Freely 开发自己的项目时，PROJECT_ROOT 和 FREELY_HOME 不应硬编码。应通过 `git rev-parse --show-toplevel` 自动推导，或从 config.toml 读取相对路径。

4. **向后兼容**：develop 的 `docs/issues/` 中已有大量历史 raw issue。新架构需要处理"worktree 中无 issue 但 develop 中有"的过渡情况。
