---
local_id: raw-20260625T000114Z14Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3452'
    url: https://github.com/chatterzhao/freely/issues/3452
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T00:01:14Z'
updated_at: '2026-06-25T02:21:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T000114Z-A
---

## 现状混乱

| 脚本 | 变量 | 实际指向 |
|------|------|------|
| `pr-create-guarded` | `ROOT_DIR` | worktree root |
| `pr-merge-guarded` | `PROJECT_ROOT` | 主 repo root |
| `wt-close` | `PROJECT_ROOT` | 主 repo root |
| `wt-close` | `PROJECT_WORKTREE_PATH` | worktree root |
| `wt-create` | `ROOT_DIR` | 主 repo root |
| `pretests-retirement-gate` | `--project` + `--worktree-path` | 各自推断 |

## 核心问题

- `ROOT_DIR` 和 `PROJECT_ROOT` 在不同文件含义不同
- 没有明确的 "repo root" vs "worktree root" 语义区分
- pr-create-guarded 的 `--project "$ROOT_DIR"` 实际是 worktree，wt-close 的 `--project "$PROJECT_ROOT"` 实际是 repo——gate 行为不可预测

## 设计目标

两个语义清晰的变量名，全项目统一：

| 变量 | 含义 | 来源 |
|------|------|------|
| `PROJECT_REPO_DIR` | 主仓库根目录（develop checkout） | `.freely/config.toml` PROJECT_ROOT 或 git worktree list --porcelain 主工位 |
| `PROJECT_WORKTREE_DIR` | 当前工位目录 | `git rev-parse --show-toplevel`（工位内）或 `PROJECT_WORKTREES_ROOT/<branch-dir>` |

## 涉及文件

`docs/system/workspace/scripts/worktree/` 下全部脚本：
- pr-create-guarded
- pr-merge-guarded
- wt-close
- wt-create
- pr-review-guarded
- pretests-retirement-gate / pretests-gate

还要同步更新调用方（bin/ 下 wrapper、freely runtime 中的引用）。

## 约束

- 向后兼容：旧 config.toml 中 PROJECT_ROOT 继续可用
- 优先级：环境变量 > config.toml > 自动检测
- worktree 脚本和 main repo 脚本应该用同一个公共 source 文件（类似 worktree-common.sh）统一定义
