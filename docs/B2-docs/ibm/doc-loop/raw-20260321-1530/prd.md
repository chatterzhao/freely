# PRD: agent-ready-prd-for-freely-flow

## Goal

把 Freely 的 `prd.md` 从“人类可读摘要”升级为“AI 可编译的执行控制面”，使后续 agent 能稳定完成 prototype、eval、task slicing、dev-loop handoff 和 model-upgrade revisit。

## Why Now

- 用户已明确提出：在 IBM 流程里，AI 来产 PRD 时应该是什么样
- 外部研究已经收口到同一方向：AI 时代的高价值产物不是更长的文档，而是更强的执行控制面
- Freely 作为自主循环运行器，如果不先给自己定义 agent-ready PRD，后续 doc-loop 仍会停留在旧的文档范式

## Product Surface

- `docs/B2-docs/**/prd.md`
- `docs/B2-docs/**/pre-tests.md`
- `docs/B2-docs/**/tasks.md`
- `doc-ibm-execution` 对 `prd.md` 的完成判断

## Non-Goals

- 本 PRD 不要求一次性改写仓库中全部历史 PRD
- 不要求本轮实现自动生成器或模板脚本
- 不把组织岗位职责变化写成 Freely 的硬治理

## Non-Negotiables

1. PRD 必须能被 AI 继续消费，而不是只给人类回忆上下文
2. PRD 必须显式写出 non-goals 和 non-negotiables，防止 AI 为了“做出来”擅自扩 scope
3. PRD 必须能自然派生 prototype path、eval 和 task slicing
4. PRD 必须允许在模型、工具、用户行为发生变化时重新评估，而不是把旧 workaround 固化为永久结构

## Context Pack

### External evidence

1. 微信公众号文章《面向Agent的PRD架构：从“人类可读 PRD”到“Agent 可编译 PRD”》
2. 微信公众号文章《Anthropic 产品经理：PRD 已死，原型万岁》
3. Anthropic 官方文章《Product management on the AI exponential》，2026-03-19

### Current Freely gap

- 现有 `prd.md` 多数只写目标和产品面
- 缺少：
  - prototype path
  - eval plan
  - decomposition tree
  - revisit triggers

## Decomposition Tree

### D1. PRD 的角色重定义

把 PRD 从“说明文”定义为“执行控制面”。

输出：

- 面向 AI 的最小字段清单
- 与 `B`、`pre-tests`、`tasks` 的边界关系

### D2. 执行结构冻结

把 PRD 拆成后续 AI 可直接消费的几个稳定区块。

输出：

- context pack
- decomposition tree
- prototype path
- eval plan
- execution slices
- revisit triggers

### D3. Dev-loop 接口定义

确保 PRD 能直接生成：

- `pre-tests.md`
- `tasks.md`
- 后续实现切片

## Prototype Path

在大规模改治理前，先用本 story 作为最小原型，验证：

1. 一套完整 IBM 产物是否能说明 `B` 与 `PRD` 的关系
2. 新结构的 `prd.md` 是否能自然派生 `pre-tests.md` 和 `tasks.md`
3. 人类阅读成本是否仍然可控

## Eval Plan

### Success

- 读完当前 PRD 后，AI 能回答：
  - 目标是什么
  - 什么不能做
  - 先做哪个 prototype
  - 用什么判断成功
  - 下一步能切出哪些任务
- `pre-tests.md` 与 `tasks.md` 均能直接从本 PRD 派生

### Failure

- PRD 仍然只是背景说明，无法约束 AI 决策
- `pre-tests.md` 或 `tasks.md` 需要依赖大量额外口头解释才能写出
- PRD 无法表达何时因模型升级而重判

### Regression risk

- 文档过厚，重新退化成面向人类的“大说明书”
- 字段过多但没有稳定消费方，形成新的形式主义

## Execution Slices

1. 冻结最小 AI-ready PRD 结构
2. 给出 issue-bound IBM 示例
3. 后续再决定是否推广到 `doc-ibm-execution` 与模板真源

## Revisit Triggers

- frontier model 的任务能力显著上升
- Freely 引入新的 AI 工具或上下文能力
- 用户开始稳定通过 prototype/eval 而不是 prose 来驱动故事推进
- 现有 PRD 字段在多个 story 中持续被证明过厚或过薄

## Dev-Loop Handoff

若后续要把本 PRD 模式正式推广到 Freely：

- 先开独立治理 issue
- 再修改 `doc-ibm-execution` reference 或模板真源
- 最后选择 1-2 个真实 story 做迁移验证，而不是全量替换
