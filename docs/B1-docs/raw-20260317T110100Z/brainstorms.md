# Brainstorm: frontend-runtime-baseline-for-probe

## Context

`I-20260317T100200Z` 在进入 `dev-loop-execution` 后，已经完成了 contract、shell、adapter、bootstrap、host 的最小骨架，但继续推进时暴露出新的边界外问题：

- 仓库中没有真实 frontend build/runtime baseline
- 没有可注入的 React renderer / host entry
- 没有可对接的 Tauri runtime 初始化路径

这不是 `Frontend Probe v0` 自身 UI 范围的问题，而是一个新的基础设施缺口。

## Why now

如果不先补齐 frontend build/runtime baseline，后续对 Probe v0 的继续实现只会停留在更多样板代码，无法进入可运行阶段。

## Candidate direction

- 形成一个专门的 frontend runtime baseline issue：
  - 明确最小 frontend build/layout 结构
  - 明确 React renderer 挂载入口
  - 明确 Tauri runtime 注入路径
  - 明确最小测试/运行方式
