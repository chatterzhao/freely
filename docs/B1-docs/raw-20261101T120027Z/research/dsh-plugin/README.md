# DSH 插件研究：相邻课题，不是 Manager/Worker 对比的主线

## 为什么单独放

Super-agent 本身是 **DSH 的一个插件**（`dsh-superagent` bundle），不是 DSH core。它证明的是：

- DSH 的插件可以启动 Runtime、注入 `agents/sessionController/tools/skills`、拥有自己的 Router/Ticket/Store；
- 插件的边界、生命周期、配置真源需要单独设计；
- “Freely 作为 DSH 插件”与“Freely 主应用 + 可插拔 harness”是两个部署问题，不是同一个架构问题。

所以这部分**不是** Super-agent 与 Freely 的 Manager/Worker 对比结论，也不改变 C-F/C-B 的优先级。它只是：

1. 评估 Freely 是否值得进入 DSH 生态；
2. 如果进入，应该是 `@freely/dsh-freely` Freely-host 插件，还是 DSH-host 治理插件；
3. 从 Super-agent 的插件形态借鉴“一个 loop 一个 owner”的边界。

## 结论

- **不做 DSH-as-harness adapter**：那会把 DSH 的 Router/Thread/Mandate 阉割成执行器。
- **如果做插件，做 Freely-host 插件**：Freely 保留 Manager/Worker/Reviewer、A2A、scan、gates、worktree、PR；DSH 只做 Session/Agent/模型/tools。
- **不加载 `dsh-superagent`**：避免 DSH Router/Ticket 与 Freely Manager/A2A 双 loop。
- **先 spike，不先产品化**：P0/P1 验证服务注入、首次 session 消息、handoff、gate。

## 文档

- [dsh-freely-plugin-design.md](dsh-freely-plugin-design.md)：插件架构、RPC、角色 session、迁移/验收。
- [../harness/harness-strategy.md](../harness/harness-strategy.md)：HarnessPort、两种部署形态、DSH A/B1/B2/C 判定。
- [../harness/harness-selection.md](../harness/harness-selection.md)：角色级 harness/model 选择与配置落点。

## 与主线的关系

- 主线：C-F 讨论入口 → C-B/C 交接 → C-D HarnessPort。
- 本课题：C-E 插件，依赖 C-B/C-D-C-F；在主线未闭环前不进入实现。
