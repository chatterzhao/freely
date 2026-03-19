# 研究：三层循环能力映射与生命周期治理

## Context

- 日期：2026-03-19 11:05 America/Los_Angeles
- 触发：Freely 当前已经形成大量自治能力，但它们散落在 `runtime/scripts`、`agents`、`skills`、`milestones/issues/progress/recovery` 之间；缺少一个自包含、唯一真源的“三层循环能力地图”，导致能力归属、调用边界和生命周期不够稳定。
- 约束：遵循宪法第 11 章与法律第 2A/2B/2C/11 章；不新增第四层循环，不把脚本保活职责和 AI 判断职责混写。

## 现状问题

1. `CONSTITUTION.md`、`PROJECT_INTENT.md`、多个 skills 与若干 pre-brainstorm 都在描述 `auto-loop / doc-loop / dev-loop`，但表达粒度不同，长期容易失同步。
2. 很多能力已经存在，但没有明确写出它们在三层循环中的“归宿”：
   - 切号 / availability
   - continuity / `fresh_with_handoff`
   - watchdog / supervision
   - milestone intake
   - IBM
   - review / verification / cleanup
3. 当前文档更像“组件说明”，不够像“生命周期状态机 + 能力挂载图”，导致后续新能力容易漂移到错误位置。
4. `Freely 产品方法论` 与 `Freely 当前用此方法论开发自己` 两层语义容易混淆。

## 收敛判断

Freely 需要一份唯一真源文档，明确三件事：

1. 三层循环本身的职责边界：
   - `auto-loop` 负责编排、监督、恢复、委派与多工位治理
   - `doc-loop` 负责发现收敛、candidate、milestone intake、IBM 与文档 continuity
   - `dev-loop` 负责实现、测试、review、verification、promotion/cleanup readiness
2. 每个能力挂在哪一层、由哪种 owner 承担：
   - `runtime/scripts`
   - `manager-agent` / `worker-agent`
   - `skills`
   - `milestones/issues/progress/recovery`
3. 从发现到完成再到 cleanup 的生命周期和回写落点。

## 最小变更原则

1. 保持 `CONSTITUTION` 只定义边界，`PROJECT_INTENT` 只定义方向；不要把大量明细继续散在这些高层文档里。
2. 新增一个系统级、自包含的三层循环能力与生命周期真源文档，其他文档只保留摘要并引用它。
3. 不把所有能力都塞进某个单一 skill；能力地图属于系统治理事实源，不等于执行步骤本身。
4. 旧 pre-brainstorm 中关于 `doc-loop(IBM+G)` 的结论应被吸收到新真源，而不是继续让历史研究文档承担现行事实源角色。

## 初步结论

该问题具备 issue-ready 条件，但先在当前研究线完成唯一真源文档和引用收敛，再决定是否需要单独 materialize 为 milestone-owned issue。

## 本轮新增收敛

1. 已新增 `docs/system/workspace/three-loop-capability-lifecycle.md` 作为三层循环能力映射与生命周期的唯一细节真源。
2. 已把高层文档、agent 文档、scripts/skills 索引和关键 loop skills 收紧为“摘要 + 引用真源”，减少平行定义。
3. 已把当前系统能力按 `auto-loop / doc-loop / dev-loop` 做显式 inventory，并补充跨层能力规则：
   - `continuity`
   - `checkpoint/hygiene`
   - `milestone`
   - `verification/cleanup`
4. 已列出当前仍需持续盯住的边界：
   - `ai-cli-availability-manager` 与更广义 watchdog 的关系
   - `workspace-skill-governance` 的主 loop 归属
   - toolchain/bootstrap 类能力是否会外溢到 runtime
   - completion verification 的细节真源仍待后续继续收紧
