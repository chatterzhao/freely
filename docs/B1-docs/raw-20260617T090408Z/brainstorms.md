# Brainstorm: Fix worker_prompts_csv=none dead loop

## Discovery
Manager 每次 delegate_workers 周期 worker_prompts_csv 恒为 none，Worker ACP session 永不启动。
根因: FreelyAgentExecutor.execute() 在 tasks/send 时不持久化 worker_prompts_csv 等 Freely 特有字段。

## Decision
**Promote**. 单行修复: execute() 中补齐缺失字段。
