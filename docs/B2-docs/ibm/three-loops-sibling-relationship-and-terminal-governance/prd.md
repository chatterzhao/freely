# PRD: three-loops-sibling-relationship-and-terminal-governance

## Problem

Freely 当前高层真源已经广泛依赖 `auto-loop`、`doc-loop`、`dev-loop`，但中文口径和部分结构图仍把它们渲染成“`三层`”。这会把：

- `doc-loop` / `dev-loop` 的 sibling 关系误导成层级包含
- verification / cleanup / recovery 误导成额外 loop
- issue completion、worktree retirement、outer governance closure 混成一个“完成”

## Users

- manager-agent
- worker-agent
- auto-loop-orchestrator
- 在 Freely 中开发 Freely 的 human/operator
- 未来用 Freely 开发其他应用的 agent/runtime

## Goals

1. 统一 active truth 与 runtime-facing prompt/script contract 中“**三个 loop**”的高层语义。
2. 固定 `auto-loop` outer orchestration、`doc-loop` / `dev-loop` sibling execution 的关系。
3. 固定 verification / cleanup / recovery 的非-loop 定位。
4. 固定 loop exit 与 terminal closure 的关系。
5. 覆盖脚本、agent、skill、提示词入口等系统真源，避免只改高层文档留下旧 contract 漏网。

## Non-goals

1. 不在本 issue 中全仓替换历史 evidence。
2. 不在本 issue 中实现新的 runtime/state machine 或 watchdog 算法。
3. 不在本 issue 中做 observability UI/API 产品化。

## Acceptance Shape

- active truth 与 runtime-facing prompt/script contract 读起来不再暗示包含关系
- outer routing、sibling execution、terminal cleanup 三者语义一致
- 脚本、agent、skill、提示词入口不再残留“第二层 auto-loop”“第四个 loop”或局部 loop 自行宣布 terminal completion 的旧语义
- 后续 issue / candidate 可直接引用这套真源，而不再需要人工解释“为什么不是三层”
