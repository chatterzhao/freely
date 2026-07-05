# 预研头脑风暴：runtime-adapter-axis-and-per-tool-adapter-selection

## 背景

ACP optional adapter boundary 已经完成 issue-bound IBM 收口，但当前 runtime 仍然没有 first-class `adapter axis`：

- config 里只有 `AI_TOOL`
- launcher 主要仍是 `tool -> launcher case`
- continuity / evidence / resume / policy writeback 直接和 tool-specific launch glue 纠缠在一起

这意味着后续无论要不要接 ACP，都还缺一个更基础的实现切口：

- 先把 `tool contract`
- 和 `adapter contract`

从 runtime 中拆开。

## 当前最小问题

如果继续在现有结构上直接接某个工具的 ACP bridge，会同时引入三类混层风险：

1. 把 `adapter selection` 误写成 `tool selection`
2. 把 ACP communication plane 误接到 continuity / recovery truth 上
3. 把当前所有 direct path 的稳定行为一起拖进一次重构

因此下一环应收窄成：

- 只抽出 `adapter axis`
- 保持当前工具默认仍走 `direct`
- 为未来 `acp` path 预留 canonical config / launch dispatch / status surface

## 预期边界

本轮不实现 ACP bridge，本轮要实现的是：

1. `AI_TOOL_ADAPTER` 进入 runtime config truth
2. 每工具可声明默认 adapter，当前 canonical tools 默认仍为 `direct`
3. runtime launch path 先决定 adapter，再进入 tool-specific direct implementation
4. `freely status` / session state / lifecycle writeback 继续使用同一套 continuity truth
5. 若选择未实现的 adapter，例如 `acp`，runtime 必须 fail fast，而不是静默回退或伪装支持

## 与 ACP owner 的关系

- `I-20260401T154500Z-A` 冻结边界
- 本轮 owner 承接第一个 implementation slice
- 只有本轮 owner 完成后，后续才适合再开 first-tool ACP prototype
