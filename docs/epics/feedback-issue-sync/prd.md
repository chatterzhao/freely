# PRD: cmd_feedback 对齐 issue-sync 多平台架构

- issue_id: raw-20260624T141559Z
- candidate: C-20260624T141559Z-A
- milestone: M-20260624T141559Z-A

## Goal

`cmd_feedback` 当前是唯一绕过多平台抽象层 `issue-sync` 的命令（硬编码 `gh issue create`，仅支持 GitHub）。将其改为 `issue-sync create` 的薄封装，实现：
1. repo 从 git remote 自动检测，去掉 `--repo` 参数
2. 创建本地 `docs/issues/raw-{key}/issue.md` 作为 single source of truth
3. 多平台创建委托给 `issue-sync`，加新平台只需在 adapter 层新增

## Dev-Loop Handoff

改动范围：仅 `docs/system/workspace/scripts/runtime/freely` 一个文件。

| 变更 | 说明 |
|------|------|
| `cmd_feedback` 重写 | 去 `--repo`，写本地 issue.md，调 `issue-sync create` |
| `_resolve_gh_repo()` | 删除（不再需要） |
| crash reporter L21465 | 去 `--repo "$FREELY_REPO_URL"` |
| `--help` | 更新 usage 文本 |

`issue-sync` 本身无需改动（已支持多平台 + git remote 自动检测）。

## Alternatives Considered

- **Option A**: 在 `cmd_feedback` 内加 if/else 分支 — 被拒绝（重复实现，违反 DRY）
- **Option B**: 改为 `issue-sync` 薄封装 — 采用
- **Option C**: 移除 `cmd_feedback`，只用 `gh` — 被拒绝（无法多平台）

## Boundary / Non-Goals

- 不改 `issue-sync` 的 API
- 不添加新平台 adapter（那是独立的 adapter 层工作）
- 不改 `wt-create`/`wt-close`/`pr-create` 等其他命令

## Residual Risk

- 低风险：`cmd_feedback` 调用链变为 `issue-sync create`，如果 `issue-sync` 不可用，feedback 会失败并保留本地 issue.md
