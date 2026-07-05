---
b1_id: B1-20260624T141559Z
phase_state: completed
source_raw: raw-20260624T141559Z
source_url: https://github.com/chatterzhao/freely/issues/3435
produced_candidate: C-20260624T141559Z-A
created_at: 2026-06-24
---

# B1_IBM: cmd_feedback 对齐 issue-sync 多平台架构

## Input

- **raw issue**: `raw-20260624T141559Z` — `cmd_feedback` 绕过 `issue-sync` 直接用 `gh`，不支持多平台且 `--repo` 应自动获取
- **来源**: 用户在使用 `freely feedback` 时发现必须手工传 `--repo` 参数，且只能创建到 GitHub

## Problem

`cmd_feedback` 是 `freely` 命令集中唯一绕过多平台抽象层 `issue-sync` 的命令：

| 命令 | 平台方式 |
|------|---------|
| `wt-close` | → `issue-sync close`（多平台） |
| `pr-create-guarded` | → `develop-push`（多平台） |
| **`feedback`** | **`gh issue create` 硬编码（仅 GitHub）** |

三个具体问题：
1. 硬编码 `gh issue create`，不支持 Gitee
2. `--repo` 参数需要用户手工传，而 `issue-sync` 已有 `_gh_repo()`/`_gitee_repo()` 自动检测
3. 不写本地 `docs/B1-docs/` 文件，与 `issue-sync` 的 local-first 设计脱节

## Brainstorm

### Option A: 在 `cmd_feedback` 里加多平台分支（不推荐）

在 `cmd_feedback` 内部像 `issue-sync` 一样写 `if github ... elif gitee ...` 分支。

**评估**：
- ❌ 重复实现平台逻辑，违反 DRY
- ❌ 加平台需要改两处（feedback + issue-sync）
- ❌ 不写本地文件，后续 `wt-close` 无法通过 `issue-sync close` 找到平台 ID

### Option B: `cmd_feedback` 改为 `issue-sync create` 的薄封装（推荐 ✅）

```
cmd_feedback:
  1. 生成 raw_key → 写 docs/B1-docs/raw-{key}/issue.md
  2. 调用 issue-sync create raw-{key}
  3. issue-sync 处理多平台创建 + 回写 platform_ids
```

**评估**：
- ✅ issue-sync 已有 `_gh_repo()`/`_gitee_repo()` 自动检测，无需 `--repo`
- ✅ 加新平台（GitLab/…）只需在 issue-sync 加 adapter，feedback 零改动
- ✅ 本地 issue.md 成为 single source of truth
- ✅ 后续 `wt-close`/`issue-sync close` 能正确找到所有平台的 issue ID

### Option C: 移除 `cmd_feedback`，只用 `gh issue create` 外部命令（不推荐）

**评估**：
- ❌ 无法多平台
- ❌ 不写本地文件
- ❌ 用户体验差

## Decision: Option B

Option B 是唯一正确的架构选择。`issue-sync` 已经提供了完整的多平台抽象，`cmd_feedback` 不应该重复实现。

改动范围（仅 `docs/system/workspace/scripts/runtime/freely` 一个文件）：
1. `cmd_feedback` 去掉 `--repo` 参数
2. 生成 `raw_key` → 写 `docs/B1-docs/raw-{key}/issue.md`
3. 调用 `bin/issue-sync create` 替代 `gh issue create`
4. 删除 `_resolve_gh_repo()` helper
5. 修复 crash reporter 中的 `feedback --repo` 调用
6. 更新 `--help` 文本

## Candidate

- candidate_id: C-20260624T141559Z-A
- status: promoted
- milestone: M-20260624T141559Z-A
- decision_reason: Option B — feedback 作为 issue-sync 薄封装，架构对齐且未来加平台零改动
