# Implementation Decision Note

## decision

做薄插件：不复制 Freely loop，只注入 Session/工具/subprocess；三角色 preset 放 bundle patch；工具白名单用 `agent.ctx.tools.restrict`；bridge 用 argv 显式 subprocess。

## why_this

- 避免双 Router/Ticket。
- 与 B1 spike 证据一致：web profile + rc.5 可用，headless 不假设。
- handoff 状态仍归 Freely DB，插件不造第二份。

## alternatives_considered

- 把 Freely scan/gates 搬进插件：双状态，拒绝。
- DSH Router 接管：与 Freely 主意图冲突。
- 只做 CLI 包装：没有 Session/工具面。

## boundary_non_goals

- Panel、DSH Source、多项目、headless/desktop、A2A RPC。

## residual_risk

- DSH private API 跨版本变化；pin rc.5 + feature detect。
- preset 工具插件名依赖 DSH bundle；headless 缺服务。
- issue→PR E2E 未跑前不能宣称完成。
