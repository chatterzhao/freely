# Brainstorm: frontend-probe-v0

## Focus

基于已冻结的 boundary contract，把 Freely 的 day-1 Probe 收敛成一个极薄但可运行的产品面。

## Key Questions

1. Probe 首屏最少要展示哪些状态，才能让人知道谁在做什么？
2. 哪些交互必须 day-1 就支持，哪些可以后置？
3. 应用内终端 / 控制台如何与 `control bar`、`chat intervention panel`、`agent roster` 组合？
4. 哪些 UI 能力严格依赖 boundary contract，哪些只是 view-local state？

## Working direction

- day-1 只做 Probe，不做完整工作台。
- UI 必须优先支撑观察、打断、恢复与回放。
- UI 只消费 backend 已发布事实，不从日志反推主状态。
