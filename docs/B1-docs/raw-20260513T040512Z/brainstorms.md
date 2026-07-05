# Brainstorm: task-lifecycle-scan batch optimization

## Discovery

### 来源
- GitHub issue #327 (`raw-20260513T040512Z`) from platform
- 相关已完成的 issue: `I-20260503-0200-A` (scan lifecycle migration v2)

### 时效性评估
当前 `task-lifecycle-scan.py` 已从 v1（废弃的 `task-source-scan.py`）切换到 v2 chain trace，但性能瓶颈仍然存在：对每个 lifecycle item 调用 `_is_github_closed()` → `gh issue view N`，O(n) API 导致扫描耗时数分钟甚至超时。该问题是当前扫描链路最明显的性能短板，值得投入。

### 是否已被覆盖
原始 `I-20260503-0200-A`（scan lifecycle migration）完成了链跟踪、信号扫描、分支治理、socket 修复，但未解决 per-item API 调用性能问题。本 issue 是其性能优化的自然延续，不属于重复。

### 当前为什么不能直接进入 B2_IBM
- 属于新功能/大型改动（`freely-feat-execution`），必须走 B1_IBM → B2_IBM → dev(fix|hotfix|feature) → test-pre-merge-* 验证 → dry-run门禁 → dev合并develop 完整链路
- 需要一个独立 candidate 以便在 milestone 中排队和追踪

## Research

### 现状：O(n) 问题
- `task-lifecycle-scan.py` 内部 `_is_github_closed()` 对每个 item 执行 `gh issue view N`
- 30+ lifecycle items → 30+ API 调用 → 2min+ 扫描耗时
- `SKIP_PLATFORM_CHECK` 作为 workaround 存在，掩盖了根因

### 方案：1+3 阶段批量化

```
Phase 0 — Batch 全量抓
  gh issue list --state all --limit 1000 --json number,title,state,body
  → platform_all: dict[number → state]

Phase 1 — 本地 vs 平台分类
  对 docs/B1-docs/ 每个 issue:
    pid ∈ platform_all? → 一致 / 不一致 / 仅本地

Phase 2 — 反向发现
  platform 上有 raw-{key} 但本地没有 → 需 materialize

Phase 3 — Lifecycle chain trace
  只用前两阶段结果做本地检查，零 API
```

### 关键变更点
1. `_is_github_closed()` 改为查预加载的 `platform_all` dict，不再调 `gh issue view`
2. `scan_platform_issues()` 增加 `--state all` 抓全量
3. 新增分类输出：`local_only` / `platform_closed` / `state_mismatch` / `platform_only`
4. `SKIP_PLATFORM_CHECK` 不再需要

### 风险与注意事项
- `gh issue list --state all --limit 1000` 有 1000 条上限：当前 repo 远未达到，可接受
- Phase 0 若失败应有 fallback：检测到 gh 不可用时回退到逐项查询
- 与现有 chain trace 输出格式的兼容性：需保持 `--json` 输出字段不变

### 验证标准
- 扫描总耗时 < 5s（之前 > 2min）
- 分类结果：`local_only`、`platform_closed`、`state_mismatch`、`platform_only` 四类都能正确识别

## Decision

收敛为 1 个 candidate：
- `C-20260513T040512Z-A`: task-lifecycle-scan batch optimization

方案明确（1+3 阶段批量化），边界清晰（仅改 `task-lifecycle-scan.py`），风险可控（有 fallback 路径）。推荐进入 B2_IBM materialize。

下一跳：`freely-doc-B2_IBM-execution`
