# PRD: session-lifecycle-rotation-and-handoff-governance

## Goal

让 Freely 的 auto-run runtime 在长期运行中能正确决定：

- 什么时候继续 `resume`
- 什么时候切到 `fresh_with_handoff`
- fresh 时如何保留最小可追溯上下文

## Requirements

1. `resume` 仍然是默认优先路径。
2. 最近 cycle 出现 `context compacted` 时，下一轮必须允许转为 `fresh_with_handoff`。
3. Runtime 需要记录最小 session state。
4. Fresh handoff 至少包含 rotation reason、上一轮 session / cycle log 信息和最近输出摘录。
5. Codex 默认模型与默认 reasoning effort 必须项目级显式化。
