---
issue_id: I-20260717T084757Z-A
issue_path: docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/issues/I-20260717T084757Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260717T084757Z-A
- issue_path: docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/issues/I-20260717T084757Z-A.md

## Implementation Decision Note

- decision: _get_agent_slot 搬至 main 前 + 日志时间戳 + AST 静态断言
- why_this: 位置性缺陷搬移即愈；断言与时间戳补可观测防复发
- alternatives_considered: 三处内联（重复，否）
- boundary_non_goals: 不改路由逻辑/Reason 语义/ACP 调用
- residual_risk: 07-04 起经此环丢失的路由不可追溯；A2A submitted 兜底扫描已兜住 worker 启动，reviewer 自动调度受损面留运行观察
