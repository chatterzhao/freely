# PRD

## Goal

让 Freely 对 manager continuation handoff 的 runtime 生命周期可观测、可追溯，并在 session rotation / auth failure 边界保持稳定。

## Requirements

1. 当 delegated continuation handoff 针对当前工位生成时，runtime 能记录 pending intake ids。
2. 当下一轮 prompt 实际注入 delegated continuation handoff 时，runtime 能记录 consumed intake ids。
3. `live-status` 默认显示 pending 与 last consumed handoff 状态。
4. `fresh_with_handoff` handoff 文件写入必须 shell-safe。

## Non-Goals

- 不要求本 issue 直接产出新的项目级治理结论文本
- 不要求本 issue 改写 interruption triage 逻辑
- 不要求把 tool TUI 变成主路径
