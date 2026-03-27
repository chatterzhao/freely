# PRD: freely-layered-architecture-and-tooling-topology

## Goal

把 Freely 自身产品/系统架构收敛成统一高层表达，并同步修正开发入口的判断顺序，避免再把 shell、command、semantic surface、能力目录与开发文档混层。

## Problem

当前局部真源已分别写对部分边界，但缺统一总图，导致：

- `chat` / `status` family 被错误拿去和 `CLI/TUI/GUI` 并列
- `tools.md` 的外部 AI tooling layer 没被放回产品架构
- `AGENTS.md` 开发入口仍缺“先判断这是 Freely 自身产品架构还是可复用能力”的前置分流

## Requirements

1. `PROJECT_INTENT` 必须表达 Freely product / core / shell / semantic surface / external execution provider 的总关系。
2. `CONSTITUTION` 必须冻结以下硬边界：
   - CLI 是 canonical shell
   - TUI / GUI 是 optional shells
   - shell 不等于 command / semantic surface
   - external AI tools 不是 Freely 自身 product shell
3. `LAWS` 必须明确当 Freely 自举中出现新讨论时，先做分类，再决定落点。
4. `AGENTS.md` 必须把上述分类顺序写成开发入口指引，但不复制高层架构正文。

## Product rules

1. Freely 的产品形态表达首先属于开发 Freely 的高层真源，而不是能力目录。
2. `Freely core` 是被 CLI / TUI / GUI 复用的能力本体。
3. `chat`、`init`、`start`、`status family` 是 semantic surfaces，不是 shell。
4. `codex`、`Claude Code`、MCP 组合路径属于 external execution provider layer。
5. 若未来要泛化出“通用产品形态方法”，必须另开独立 lifecycle。

## Eval Plan

### Pre-merge acceptance

1. 单独阅读 `PROJECT_INTENT`，应能准确说出：
   - Freely product、Freely core、CLI、TUI app、GUI app 的关系
   - `chat` / `status` family 为什么不是 shell peer
   - external AI tooling 在总图中的位置
2. 单独阅读 `CONSTITUTION`，应能看出哪些是硬边界，而不是仅仅叙事。
3. 单独阅读 `LAWS`，应能恢复“新讨论出现时的分类顺序与落点顺序”。
4. 单独阅读 `AGENTS.md`，应能恢复“开发 Freely 时怎么先判断 product architecture / development governance / reusable capability / continuation”，且不会把 `AGENTS.md` 误读成架构真源。

### Post-merge acceptance

1. 后续任何涉及 Freely 产品形态的新讨论，都应先引用 `PROJECT_INTENT / CONSTITUTION / LAWS / AGENTS.md`，而不是直接跳到 `docs/system/workspace/**`。
2. 当后续讨论落到“通用产品形态方法”时，应自然分流成新的 pre-brainstorm，而不是继续扩写本 issue。

## Exit criteria for `done_ibm`

1. issue、brainstorm、`prd.md`、`pre-tests.md`、`tasks.md` 完整。
2. 四份高层开发文档的职责分工清楚。
3. 可以直接驱动文档改写与 verification，不再依赖口头解释。
