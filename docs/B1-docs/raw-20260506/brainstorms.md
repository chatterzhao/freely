# Brainstorms: pr-merge-guarded fix/* whitelist

## Discovery

### 来源
- GitHub issue #273 — zhaoquan
- created_at: 2026-05-06 14:00 UTC
- platform_state: open
- raw issue local_id: raw-20260506T1400Z

### 问题陈述
pr-merge-guarded 只接受 `feature/*` 和 `hotfix/*` → `test-pre-merge-*` 方向，`fix/*` 不在白名单。但 `fix-execution` skill 产出 `fix/*` 分支，需要合法的 merge 路径进入 `test-pre-merge-*`。

### 当前为什么不能直接进入 IBM / dev
问题边界足够清晰，可以直接进入实现。但 pre-brainstorm 阶段缺少正式记录，需要先补齐 brainstorms.md 和完整 candidates.md。

### 价值与时效性判断
- 该 issue 由 `fix-execution` skill 的生产路径直接触发：`fix/*` 分支需要 merge 到 `test-pre-merge-*` 做验证
- 如果缺失此白名单，`fix/*` 分支无法通过 `pr-merge-guarded` 的门禁，整个 fix-execution 工作流将被阻断
- 当前项目阶段仍然高度活跃，fix-execution 是日常开发流程的一部分
- **结论**: 价值确认，继续 B1_IBM 流程

## Research

### 边界分析
- pr-merge-guarded 中控制方向的逻辑在 `validate_merge_direction` 函数
- 需要修改三处：
  1. `validate_merge_direction` 的 case pattern — 增加 `fix/*` 匹配
  2. help text — 增加 `fix/*` 到 allowed directions 说明
  3. pre-flight gate — 在条件判断中增加 `fix/*` 支持
- 不涉及其他 merge 方向（`main`、`develop`、`release/*` 等方向不受影响）

### 依赖检查
- 已有 `docs/epics/pr-merge-guarded-fix-whitelist/` 体系
- `pre-tests.md` 已定义三个测试层（unit / integration / end-to-end）
- `tasks.md` 已拆分三个任务并标记 completed
- `code-reviews/review.md` 已记录 implementation decision

### 边界文档对齐
- CONSTITUTION.md 第 2 章分支表：feature/* / hotfix/* 已有明确规则，fix/* 不在表中，但 issue 目标是在 pr-merge-guarded gate 层面增加支持，不修改宪法分支表
- LAWS.md 第 2 章 2D: pr-merge-guarded 是 protected-branch merge receipt 的唯一 canonical 入口；增加 fix/* 白名单不违反该规则
- 此变更不影响合并纪律或 protected-branch 保护策略

## Decision

### 收敛结论
- **方案**: 在 pr-merge-guarded 的 `validate_merge_direction` + help text + pre-flight gate 三处增加 `fix/*` 支持
- **原因**: `fix-execution` skill 产出 `fix/*` 分支，必须通过 pr-merge-guarded 进入 `test-pre-merge-*` 做验证
- **状态**: 直接进入实现，不需要进一步研究

### 理由
1. 问题边界清晰：只需在已有 case pattern 中增加一个分支前缀
2. 影响范围可控：仅修改 pr-merge-guarded 的 direction/display/gate 三处
3. 无副作用：不修改合并纪律、不修改 protected-branch 策略
4. 有现成测试定义和验收条件

### 下一跳
继续 B1_IBM 留痕 → 已 materialize 为 `I-20260506T1400Z-A`

### 会话引用

session_refs:
- tool: claude-code
- session_id: unavailable://wt-create
- jsonl_path: unavailable://wt-create
- role: worker

## 完成自检

- [x] brainstorms.md 包含 discovery、research、decision
- [x] candidates.md 每个 candidate 有 status/milestone/decision
- [x] milestones.md candidate_issues 条目已更新
- [x] 下一跳明确：继续 B1_IBM 还是进入 `freely-doc-B2_IBM-execution`
