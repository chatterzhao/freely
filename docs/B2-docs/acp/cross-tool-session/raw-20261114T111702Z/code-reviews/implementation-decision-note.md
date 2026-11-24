---
issue_id: I-20261114T111702Z-A
issue_path: docs/B2-docs/acp/cross-tool-session/raw-20261114T111702Z/issues/I-20261114T111702Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20261114T111702Z-A
- issue_path: docs/B2-docs/acp/cross-tool-session/raw-20261114T111702Z/issues/I-20261114T111702Z-A.md

## Implementation Decision Note

- decision: 在 `cmd_comment()` 的 ACP 通知段，把两处 `python3 -c` 中的 `${PROJECT_ROOT}` 同行替换为 `${SELF_ROOT}`（2 行、4 处插值），不新增行。
- why_this: `SELF_ROOT` 是 `:32` 全局定义的唯一根路径真源；`PROJECT_ROOT` 只在 supervisor identity heredoc 中出现且被显式 unset，在 `cmd_comment()` 的 `set -u` 作用域下必然 unbound。同行替换同时满足语义与行数预算（27166/27166）。
- alternatives_considered: 新增 `local PROJECT_ROOT="$SELF_ROOT"`（新增行撞 check-runtime-size）；上调 `.size-budget`（split-plan.md:97 禁止）；删除 ACP 通知段（删除既有能力，违背 raw 边界）。
- boundary_non_goals: 不改平台写逻辑与 adapter；不改 agent_working 接口；不放宽任何门禁；不修其它文件的 PROJECT_ROOT 用法；不引入第二套根路径变量。
- residual_risk: 若将来 `SELF_ROOT` 语义变更，需同步复核本段；AT 为源码契约断言，真实平台写由合并后吃狗粮复验。
