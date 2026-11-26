---
issue_id: I-20260807T121205Z-A
issue_path: docs/B2-docs/a2a/reviewer-agent/raw-20260807T121205Z/issues/I-20260807T121205Z-A.md
phase_state: completed
---

- issue_id: I-20260807T121205Z-A
- issue_path: docs/B2-docs/a2a/reviewer-agent/raw-20260807T121205Z/issues/I-20260807T121205Z-A.md

# Implementation Decision Note

- decision: 在 a2a_task.py 的 a2a-exit 更新分支构造 PATCH 字段时，为 needs-review 的 input-required 转换补上 raw_key（--raw-key 优先，--task-id 回读任务记录兜底）；无法解析则 fail-closed 返回 ok:false 且不发 PATCH。
- why_this: 根因即更新调用漏字段；生产端修复让 SSE state_update 自然携带 raw_key，下游 watchdog 的 FAIL-CLOSED 断言无需降级。
- alternatives_considered: watchdog 按 task_id 回查（引入第二套真源）与 server 按 task store 补字段（a2a SDK 依赖使 AT 无法裸环境导入，且与调用方必填契约重复）均不采用。
- boundary_non_goals: 不改 watchdog_sse.py 的 FAIL-CLOSED 逻辑；不改 a2a_server.py 的 SSE 构造；不新增服务端回查；不触碰其他 raw key。
- residual_risk: 只有走 a2a-exit CLI 的 needs-review 转换被修复；直接 PATCH 的其他调用方仍需自行声明 raw_key，但 watchdog 的 FAIL-CLOSED 仍会阻止误路由。
