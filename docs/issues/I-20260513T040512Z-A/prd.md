# PRD: task-lifecycle-scan 批量化

> I-20260513T040512Z-A | C-20260513T040512Z-A | M-20260513T040512Z-A

## 概述

`task-lifecycle-scan.py` 当前对每个 lifecycle item 调用 `_is_github_closed()` → `gh issue view N`，导致 O(n) API 调用。本 PRD 定义 1+3 阶段批量化改造方案。

## Phase 0 — Batch 全量抓取

**输入**: 无（首次调用 `gh issue list`）

**操作**: 
- 调用 `gh issue list --state all --limit 1000 --json number,title,state,body`
- 解析返回 JSON，构建 `platform_all: dict[number → state]`
- 失败时 fallback 到逐项查询（兼容网络/权限异常）

**输出**: `platform_all` 字典

**关键决策**:
- `--limit 1000` 覆盖当前仓库（远未达到），未来可配置
- fallback 行为默认回退到旧 O(n) 行为

## Phase 1 — 本地 vs 平台分类

**输入**: `platform_all` + `docs/issues/` 目录扫描

**操作**:
遍历 `docs/issues/` 下每个 issue 的 frontmatter：
- `pid ∈ platform_all` 且 `state == platform_state` → **一致**
- `pid ∈ platform_all` 但 `state != platform_state` → **状态不一致**
- `pid ∉ platform_all` → **仅本地**

**输出**: 分类清单（local_only / platform_closed / state_mismatch）

## Phase 2 — 反向发现

**输入**: `platform_all`

**操作**:
遍历 `platform_all` 中的 key：
- `raw-{key}` 格式的 issue → 本地是否存在？
- 不存在 → 标记为 `platform_only`，建议 materialize

**输出**: `platform_only` 列表

## Phase 3 — Lifecycle chain trace

**输入**: Phase 0 的 `platform_all` + Phase 1/2 的分类结果

**操作**:
- 仅用本地缓存结果（`platform_all` dict）判断 lifecycle chain 状态
- 零 API 调用
- 保持与现有 chain trace 输出格式兼容

**输出**: lifecycle chain trace 报告

## 移除 SKIP_PLATFORM_CHECK

- 删除 `SKIP_PLATFORM_CHECK` 环境变量/配置检查
- Phase 1 的平台分类解决了其原始目的（判断平台可见性）
- 确保向下兼容：移除后不影响已有行为

## 非功能性要求

- 扫描总耗时 < 5s（之前 > 2min）
- 与现有 chain trace 输出格式兼容
