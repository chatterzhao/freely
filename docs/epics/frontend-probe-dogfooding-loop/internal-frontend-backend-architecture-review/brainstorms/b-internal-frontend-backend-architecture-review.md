# Brainstorm: internal-frontend-backend-architecture-review

## Focus

把 Freely 当前形态下的“内部前后端”重新定义清楚，避免后续实现直接绑死在某一种 transport 或部署假设上。

## Key Questions

1. 在 Tauri 桌面工具内，frontend 与 backend 的职责边界分别是什么？
2. 哪些状态属于 frontend view state，哪些必须由 backend 作为事实源持有？
3. day-1 协议面是否应先定义抽象 command / event / snapshot，而不是直接定义 WS/HTTP 细节？
4. transport adapter 如何设计，才能让 `tauri_adapter` 与未来 `ws_adapter` 共存？
5. terminal、session、governance、skill routing 这几类能力，哪些是 backend service contract，哪些只是 frontend 的展示或交互？
6. 人类如何在“不阻塞主循环”的前提下，仍然通过高优先级输入及时纠偏？
7. 多个输入源如何仲裁优先级，才能既保持自治又保留人类纠偏权？
8. UI 如何把多个 AI agent 呈现成“一个团队”的可观察界面，而不是单线程日志窗？

## Initial Direction

- 先冻结边界和协议分层，再决定第一阶段 transport 实现。
- 第一阶段优先 `tauri_adapter`，但不得把业务协议写死在 Tauri API 细节上。
- `ws_adapter` 作为未来兼容目标，从 day-1 就保留语义兼容面。
- day-1 主入口应是应用内终端和控制台，而不是外部 shell。
- 人类默认不阻塞主循环，但 `chat input` 必须具备比普通自治事件更高的纠偏优先级。
- UI 不能只显示“当前 CLI 输出”，还要显示 agent 级状态、阶段、进展、阻塞、最近动作和输入来源。
