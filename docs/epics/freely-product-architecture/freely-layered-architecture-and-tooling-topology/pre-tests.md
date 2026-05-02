# Pre-Tests: freely-layered-architecture-and-tooling-topology

## Pre-merge acceptance

1. `PROJECT_INTENT` 必须明确 Freely product / core / CLI / TUI app / GUI app 的关系，且 `chat` / `status` family 不再与 shell 并列。
2. `PROJECT_INTENT` 必须明确 external AI tooling 属于 external AI tooling layer，不是 Freely 自身 product shell。
3. `CONSTITUTION` 必须把 canonical CLI shell、optional TUI shell / GUI app、semantic surface 与 external AI tooling layer 的边界写成硬约束。
4. `LAWS` 必须要求新讨论先分类为 continuation、Freely 自身产品架构、开发治理或可复用能力，再决定文档落点。
5. `AGENTS.md` 必须复用同一分类顺序，且保持“开发入口指引”身份，不复制架构正文。
6. milestone、candidate 与 issue 路径必须完成 promote/writeback，不再把这条线挂在 `workspace-routing-foundation`。

## Post-merge acceptance

1. 后续 Freely 自举中再次出现产品形态讨论时，默认先回到 `PROJECT_INTENT / CONSTITUTION / LAWS / AGENTS.md`，而不是直接往 `docs/system/**` 写。
2. 若后续讨论转成“通用产品形态方法”，应能自然分流为新的 pre-brainstorm，而不是继续扩写本 issue。
