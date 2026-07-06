# Tasks: task-lifecycle-scan 批量化

> I-20260513T040512Z-A | M-20260513T040512Z-A

## Phase 0 — Batch 全量抓取

- [ ] T0.1: 实现 `gh issue list --state all --limit 1000` 调用并解析 JSON
- [ ] T0.2: 构建 `platform_all: dict[number → state]` 缓存结构
- [ ] T0.3: 实现 fallback：gh 不可用时回退到逐项 `gh issue view N`

## Phase 1 — 本地 vs 平台分类

- [ ] T1.1: 扫描 `docs/issues/` 下所有 issue 的 frontmatter 提取 `platform_ids` 和 `platform_state`
- [ ] T1.2: 实现分类逻辑：一致 / 状态不一致 / 仅本地
- [ ] T1.3: 输出分类清单（含统计摘要）

## Phase 2 — 反向发现

- [ ] T2.1: 遍历 `platform_all` 中 `raw-{key}` 格式的 issue 检查本地存在性
- [ ] T2.2: 标记 `platform_only` 并输出建议 materialize 列表

## Phase 3 — Lifecycle chain trace

- [ ] T3.1: 将 `_is_github_closed()` 改为查 `platform_all` dict，零 API
- [ ] T3.2: 验证与现有 chain trace 输出格式兼容

## SKIP_PLATFORM_CHECK 移除

- [ ] T4.1: 查找并删除 `SKIP_PLATFORM_CHECK` 引用
- [ ] T4.2: 确保移除后不影响 code path
