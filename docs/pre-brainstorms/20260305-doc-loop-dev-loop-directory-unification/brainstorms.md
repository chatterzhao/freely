# 研究：Doc-Loop / Dev-Loop 文档目录结构统一（Freely 吃狗粮）

## Context

- 日期：2026-03-05
- 触发：当前 `docs/` 仍处于 research-first 过渡态，目标结构与最终 doc-loop/dev-loop 产物结构尚未对齐。
- 原则：先以 pre-brainstorms 形式收敛，再进入 issue 落地。

## 当前结构（实况）

当前活跃目录：
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/PROJECT_INTENT.md`
- `docs/pre-brainstorms/`
- `docs/research/`

当前缺失（相对目标产物）：
- `docs/epics/`
- `docs/progress/`
- `docs/milestones.md`

## 目标结构（按产出物反推）

```text
docs/
  CONSTITUTION.md
  LAWS.md
  PROJECT_INTENT.md
  pre-brainstorms/
    INDEX.md
    CONVERGENCE.md
    <id>/
      brainstorms.md
      candidates.md
  milestones.md
  epics/
    <epic>/
      <story>/
        issues/<issue>.md
        prd.md
        pre-tests.md
        tasks.md
  progress/
    <epic>/
      p-<issue>.md
  research/
    deferred/
```

## 不符合项与判断

1. 目标目录（`epics/progress/milestones`）尚未启用，仅在宪法/法律中定义。
2. 现有脚本对旧路径仍有遗留依赖（需后续统一到新结构）。
3. 历史执行态资产已归档并从工作区移除（见 `docs/research/ARCHIVE.md`），后续按 issue 节奏选择性重建。

## 收敛策略

1. 先在 doc-loop 产出“目录迁移契约”（何时创建、何时切流、何时删旧）。
2. 再在 dev-loop 落地脚本/门禁对齐（doctor、bmad-check、hooks）。
3. 分阶段启用：
- Phase A: 研究与候选（当前）
- Phase B: 创建目标目录与最小模板
- Phase C: 门禁切换到新目录
- Phase D: 清退过渡依赖

## 结论

当前应继续遵守“先 brainstorm + candidate”的输入规则；目录统一本身已达到进入 issue 队列条件。
