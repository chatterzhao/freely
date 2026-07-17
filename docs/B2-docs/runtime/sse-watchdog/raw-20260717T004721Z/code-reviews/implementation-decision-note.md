---
issue_id: I-20260717T004721Z-A
issue_path: docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/issues/I-20260717T004721Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260717T004721Z-A
- issue_path: docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/issues/I-20260717T004721Z-A.md

## Implementation Decision Note

- decision: valid_sse_watchdog_pid_for_project 声明行参数顺序修复为 (project, pid)
- why_this: 全部调用方按家族约定传 (project, pid)（B1 已枚举），单点改函数侧改动面最小
- alternatives_considered: 改全部调用方适配反转签名（改动面大、违反家族约定，否）
- boundary_non_goals: 不改 sse-watchdog 生命周期、discover、launch、其他 valid_* 函数
- residual_risk: 修复后 reconcile 将首次真正"看见"活 sse-watchdog——若历史上依赖误杀行为清理重复实例，可能短期出现多实例并存；cmd_ensure_sse_watchdog_watch 自身有 pid 文件去重，风险低
