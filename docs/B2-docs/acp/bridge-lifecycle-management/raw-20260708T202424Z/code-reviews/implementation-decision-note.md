---
issue_id: I-20260708T202424Z-A
issue_path: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260708T202424Z/issues/I-20260708T202424Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260708T202424Z-A
- issue_path: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260708T202424Z/issues/I-20260708T202424Z-A.md

## Implementation Decision Note

- decision: 在 acp-bridge.py 新增 idle monitor daemon thread 实现空闲超时优雅退出 + 在 freely daemon startup 只启动 Manager bridge + 在 _sync_project_tooling 委派前检查并自动唤醒 bridge + 用 agent_next_free() 替换简单轮询
- why_this: 最小改动方案（4 文件 ~60 行），覆盖全部 4 个问题。复用现有的 `_ensure_acp_bridge_running`、`acp_session_connect`、`agent_next_free` 等已有基础设施。不引入新的进程模型或状态文件。
- alternatives_considered:
  1. 全懒启动（含 Manager bridge）— Manager 首次 cycle 延迟 +5s，无实质性收益
  2. Bridge Sleep 模式（保留 Python 进程）— 内存占用 ~50MB + 子进程管理复杂度
  3. 渐进式迭代（3 次 PR）— 周期太长，4 个问题关联紧密，一次 PR 更高效
- boundary_non_goals:
  - 不改变 Reviewer bridge 的委派流程（Reviewer 跟随 Worker 工作流）
  - 不新增 agent-table-query --bridge-status 子命令
  - 不改变 agent_next_free 的返回结构
  - 不改变 `_send_request` 已有的 per-prompt idle timeout 逻辑
- residual_risk:
  - Bridge 启动竞态：_ensure_acp_bridge_running 已有 pid file + socket 检测，低风险
  - agent_next_free RPC 超时：有 fallback 到原 grep 逻辑，不影响可用性
  - Idle monitor 误判：activity_lock 保护 + grace period 30s，充分容忍短暂空闲
