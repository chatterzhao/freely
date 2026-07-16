---
issue_id: I-20260716T040152Z-A
issue_path: docs/B2-docs/agent-orchestration/agent-dispatch-fix/raw-20260716T040152Z/issues/I-20260716T040152Z-A.md
phase_state: in_b2_ibm
---

- issue_id: I-20260716T040152Z-A
- issue_path: docs/B2-docs/agent-orchestration/agent-dispatch-fix/raw-20260716T040152Z/issues/I-20260716T040152Z-A.md

## Implementation Decision Note

- decision: 分三个阶段修复 agent 编排链路的 6 个 bug。Phase 1 添加 `--reason` 参数到 a2a-exit 并写测试；Phase 2 移除 freely-cycle 的 reviewer 分配、添加 update_only 错误日志；Phase 3 创建 wrapper、统一参数、更新文档。

- why_this: Bug 1 是紧急阻断——Reviewer 调度完全断裂。`update` 子命令已有 `--reason`，A2A Server 已有 reason 处理，唯一断裂点在 `a2a-exit` CLI。修复是补全已有的设计意图，不是引入新机制。

- alternatives_considered:
  - **方案 A: 仅修 Bug 1**: 最快但竞态和静默失败留待后续
  - **方案 B: 一次性全修**: 范围太大，测试负担重
  - **方案 C (选择): 分阶段**: Phase 1 恢复链路 + 测试，Phase 2-3 消债，每阶段独立可验证

- boundary_non_goals:
  - 不改 A2A Server (a2a_server.py 已支持 reason)
  - 不改 watchdog_sse.py 路由逻辑 (已正确)
  - 不改 Manager/Worker agent 角色定义
  - 不改 ACP bridge
  - 不引入新的 agent 角色或通信协议

- residual_risk:
  - `a2a-exit` wrapper 需要确保 PATH 解析正确，避免与系统命令冲突
  - freely-cycle reviewer 分配移除后，必须确保 watchdog_sse.py 的 SSE 连接稳定
  - 端到端测试依赖 A2A Server 和 freely-db daemon 运行——测试环境需 mock 或提供 fixture
