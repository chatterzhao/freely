# PRD: watchdog-restart-storm-and-process-churn-governance

## Problem

Freely 目前能检测 stall，但还不能检测“短窗口内反复退出并被拉起”的 restart storm / process churn。结果是 watchdog 可能持续 blind relaunch，而 manager 没有足够 signal 做 dead-loop / thrash judgement。

## Product Goal

让 watchdog 把 restart storm / process churn 暴露成 runtime signal，再由 manager 在 `auto-loop` 进行治理裁决，避免恢复机制掩盖死循环。

## Requirements

1. signal 真相面写入 `session-state.env`
2. `workcell-state.env` 不镜像该类计数
3. `live-status` / `fleet-status` 能消费并展示 signal
4. signal 命中后 watchdog 进入低频观察，不继续 blind relaunch
5. manager continuity 只带 signal ref 与 followthrough judgement
6. 默认阈值：
   - `RESTART_STORM_WINDOW_SECS=30`
   - `RESTART_STORM_COUNT=4`
   - `PROCESS_CHURN_PEAK=3`

## Non-Goals

1. 不在本 issue 扩 UI/TUI/API 产品面
2. 不重写整套 watchdog 架构
3. 不把业务阻塞误判成 restart storm

## Success Criteria

- runtime 能稳定写出 restart storm / process churn signal
- manager 能在 `auto-loop` 中基于 signal 继续裁决
- 真实状态面可观察，而不是只能靠人工翻日志猜
