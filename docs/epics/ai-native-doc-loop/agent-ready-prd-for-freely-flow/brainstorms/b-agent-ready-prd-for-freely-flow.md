# B: agent-ready-prd-for-freely-flow

## Question

在 Freely 的 IBM 流程里，AI 时代的 `prd.md` 应该包含什么，才能既服务人类判断，也服务后续 AI 的 doc/dev/review/recovery 循环？

## Key Decisions

### 1. `B` 不是 PRD 的替身

`B` 的职责是 issue-bound brainstorm：

- 收敛分歧
- 记录证据
- 比较候选结构
- 判断是否 reroute

`PRD` 的职责才是把稳定结论整理成执行控制面。

### 2. PRD 的中心从“描述产品”转为“约束 AI 行动”

对 Freely 来说，PRD 的主要用途不是给人存档，而是给 AI 后续循环继续工作。因此它必须优先回答：

- 目标是什么
- 什么不能做
- 需要哪些上下文
- 应如何拆解
- 先做什么 prototype
- 用什么 eval 判断成败
- 哪些 slice 可以独立推进
- 何时必须因为模型/工具变化而重判

### 3. PRD 不应只是一篇 prose 文档

研究显示，AI 时代的高价值产物是：

- prototype
- eval
- task graph
- revisit hook

所以 `prd.md` 也应围绕这些执行对象组织，而不是只写长篇背景说明。

## Alternatives Considered

### 方案 A：保留当前短 PRD，仅补更多描述文字

不采用。

原因：

- 仍然偏向人类阅读
- 无法自然派生 `pre-tests.md`
- 无法稳定驱动 AI 切 slice

### 方案 B：把 PRD 直接替换为 tasks

不采用。

原因：

- 会丢失“为什么做、什么不能做、哪些事实为真”的上层约束
- dev-loop 可能在 task 正确但方向错误的前提下高速偏航

### 方案 C：PRD 作为执行控制面，tasks 作为其派生产物

采用。

原因：

- 能保留方向判断
- 能自然派生 prototype/eval/tasks
- 更适合 AI 在后续循环中反复读取和回流

## Result

本 issue 采用的 PRD 结构为：

1. Goal
2. Why now
3. Product surface
4. Non-goals
5. Non-negotiables
6. Context pack
7. Decomposition tree
8. Prototype path
9. Eval plan
10. Execution slices
11. Revisit triggers
12. Dev-loop handoff

## Ready for `done_ibm`

当前：

- issue scope 稳定
- `B` 与 `PRD` 的边界已明确
- `prd.md`、`pre-tests.md`、`tasks.md` 已能直接驱动下一跳治理改造

因此本 issue 可以停在 `done_ibm`，等待后续 dev-loop 或治理吸收。
