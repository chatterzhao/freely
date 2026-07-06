# PRD

## Goal

让 Freely runtime 在主管已运行的情况下，仍能稳定消费最新一轮 manager continuity 与 worker prompt set，并把 generated/consumed truth 暴露出来。

## Requirements

1. runtime 必须能识别 latest continuity 与 latest prompt set。
2. 主管 watchdog 每轮都要尝试消费最新 continuity，而不是只在恢复分支执行。
3. launch-state 必须区分 generated 与 consumed。
4. `live-status` / `baseline-status` 必须可见这层 truth。

## Non-Goals

- 不重写 manager patrol / disposition 文本逻辑
- 不增加新的 loop
- 不把 tool TUI 变成主执行路径
