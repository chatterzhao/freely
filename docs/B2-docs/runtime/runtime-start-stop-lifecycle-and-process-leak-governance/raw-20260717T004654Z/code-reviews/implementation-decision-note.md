---
issue_id: I-20260717T004654Z-A
issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T004654Z/issues/I-20260717T004654Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260717T004654Z-A
- issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T004654Z/issues/I-20260717T004654Z-A.md

## Implementation Decision Note

- decision: _ensure_acp_bridge_running 重生前回收存活旧 pid + 健康检查失败的 20s 暖机宽限 + 主循环 per-cycle ensure 的 lazy-start 守卫
- why_this: 三缺陷同属 bridge 生命周期域（回收/判活/启动策略），一体修消除泄漏闭环并回归 lazy-start 设计真源（raw-20260708T202424Z）
- alternatives_considered: 只修孤儿（churn 与违约仍在，否）；重构独立 bridge 守护模块（Option C 改动面大，留 watchdog-control-plane 线）
- boundary_non_goals: 不改 acp-bridge.py 内部 idle-sleep、ACP 协议、auto-wake 委派路径
- residual_risk: 暖机宽限 20s 内真死的 bridge 会晚一轮才被替换（≤1 个 cycle 延迟，可接受）；lazy 守卫依赖 pid 文件存在性判断"曾启动"，bridge 自身 idle 关闭后 pid 文件由其清理——若清理失败会多一次无害的 ensure
