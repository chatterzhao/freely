# Brainstorm: freely-layered-architecture-and-tooling-topology

- brainstorm_id: `20260326-1810--freely-layered-architecture-and-tooling-topology`
- created_at: `2026-03-26`
- status: `active`
- related_signals:
  - 当前 `three-loop-capability-lifecycle` 能解释 loop / route / lifecycle，但不等于整套 Freely 产品/系统分层图。
  - 当前 `docs/system/workspace/tools.md` 已经定义 `codex`、`cc`、`cc-use-codex-cli`、`iflow` 等 AI tool/runtime 使用方式，但这些工具层还没有被放进一张更上位的体系拓扑图里。
  - 用户明确指出上一版方块图有两个错误：`chat` 不应和 `CLI/TUI/GUI` 并列；AI tool usage layer 不能缺席，尤其 Freely 如何使用 `codex cli`、`claude code` 等是系统本体的一部分。

## Problem

Freely 现在缺一份更总览的 architecture/topology 真源，导致几个层面容易混在一起：

- loop/lifecycle 真源
- 产品交互入口
- 终端/界面载体
- 外部 AI tool orchestration layer
- runtime/agent orchestration layer
- eval/harness/supporting substrate

结果是：

- `three-loop-capability-lifecycle` 容易被误当成整栋系统地图
- `chat` 这种交互入口会和 `CLI/TUI/GUI` 这种载体/表面形态并列
- `codex cli`、`Claude Code`、`codex MCP` 这种“Freely 如何借力外部 AI 工具”没有稳定层级归属

## Desired Outcome

收敛一份更准确的 Freely 分层图，至少回答：

1. 哪些层是 Freely 产品本体
2. 哪些层是 Freely 借力外部 AI 的工具编排层
3. 哪些层是 eval / harness / evidence / replay 支撑层
4. `chat`、`start`、`tui`、`cli`、`gui` 到底分别属于“入口”、“交互模式”还是“表面载体”
5. `three-loop-capability-lifecycle` 应是这张图的一部分，还是只被它引用

## Tensions

- 不能为了画大图，把现有 `three-loop`、`tools.md`、agent/runtime/contracts 的边界打散。
- 不能把“交互入口”与“前端/终端载体”混成一层。
- 不能把外部 AI tool 当成 Freely 的外部杂项；按当前 dogfooding 方式，它们是 Freely architecture 中被明确编排的一层。
- 不能过早决定一定改 `three-loop`；更可能是新增一份更上位的 topology 文档，再让 `three-loop` 和 `tools.md` 各守其位。

## Likely Landing Zones

- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/tools.md`
- 新增一个更上位的 architecture/topology 真源，可能位于：
  - `docs/system/workspace/layered-architecture.md`
  - 或 `docs/system/architecture/freely-layered-topology.md`

## Working Hypothesis

目前更合理的方向不是“把所有内容都塞回 three-loop”，而是：

- 新增一份更上位的 layered architecture / topology 真源
- `three-loop-capability-lifecycle` 继续只负责 loop/lifecycle map
- `tools.md` 继续只负责外部 AI tool inventory / routing contract
- 新的 topology 文档负责把它们放进同一张楼层图里

其中至少要把这几类层分开：

1. operational substrate
2. harness / eval support
3. autonomy evals / acceptance plane
4. external AI tooling / execution provider layer
5. Freely runtime / agent orchestration
6. interaction entry layer
7. product surface / host form factor

## Open Questions

1. `chat`、`start`、`init` 更适合作为 front-door entry layer，还是 command surface 的一部分？
2. `CLI / TUI / GUI` 是单独的 “host form factor layer”，还是都属于 product surface 的不同切面？
3. `codex cli`、`Claude Code`、`iflow`、`kiro-cli` 是“tooling layer”，还是“execution provider layer”更贴切？
4. `autonomy evals` 与 `harness` 应否分成两层，而不是合成一层？
