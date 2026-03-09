# Pre-Tests: internal-frontend-backend-architecture-review

1. 文档必须明确“前后端边界”不等于“必须先做远端服务”。
2. 协议层必须明确 transport adapter 可替换，不能把业务语义写死在 Tauri 或 WS 之一上。
3. `ClientCommand`、`ServerEvent`、`Snapshot` 三类对象必须都有清晰职责。
4. terminal、session、run、governance、skill routing 的状态归属必须能落到 frontend 或 backend。
5. 技术栈约束必须保持 Rust + Tauri + Bun + React + TypeScript，且不引入 Node.js 产品运行时。
6. 文档必须定义一个明确的 `MVP autonomy milestone`，而不是只写“以后可自治”。
7. 该 milestone 必须至少覆盖 Frontend Probe、backend boundary、governance as features、single-issue dev loop、human correction loop。
8. 文档必须明确 day-1 主入口是应用内终端 / 控制台，而不是外部 shell。
9. 文档必须明确 human chat input 高于普通自治事件的纠偏优先级。
10. 文档必须明确一个最小 AI team visibility UI，而不是只描述日志流。
