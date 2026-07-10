---
candidate_id: C-20260710T142858Z-A
status: absorbed
source_raw: raw-20260710T142858Z
absorbed_into: I-20260710T142858Z-A
created_at: 2026-07-10
milestone: M-20260710T142858Z-A
---

## C-20260710T142858Z-A: Runtime Worker Launch 接入 A2A

- candidate_format_version: v2
- title: Runtime Worker Launch 接入 A2A 协议
- status: absorbed
- decision_reason: A2A 集成完成 Phase 1 (Server) + Phase 2 (Manager 侧) 后，Phase 3 (Runtime 侧 Worker launch) 未完成。Manager 委派的 Worker 任务停留在 A2A submitted 状态，从未被启动。需要将 Runtime 的 Worker launch 从旧的 CSV/continuity 管道切换到 A2A tasks 查询。
- next_action: B2 设计实现
- revisit_trigger: 如果 Option A 接入后 Worker 仍不启动 → 检查 ACP session/fork 链路
- acceptance_criteria:
  - `manager_runtime_launch_workers_from_latest_task()` 查询 a2a_tasks (submitted, role=worker)
  - A2A Task.message → 临时 prompt file → Worker ACP session 启动
  - Worker 启动后 task state 更新为 working
  - 旧 continuity 系统保留作为 fallback
  - Manager 委派后 30s 内 Worker bridge 收到 session/prompt
- promotion_gate: B1 预研完成，设计路径明确
- open_questions:
  - Worker ACP session/fork 链路是否完整
  - Worker 完成后 SSE 通知是否到达 Manager
  - Reviewer watchdog 触发链路是否需要同步验证
- acceptance_reviews: []
- promoted_issue_id: I-20260710T142858Z-A
- promoted_issue_path: docs/B2-docs/a2a/task-lifecycle/raw-20260710T142858Z/issues/I-20260710T142858Z-A.md
- milestone: M-20260710T142858Z-A
- session_refs: []

## 改动计划

### 1. freely: manager_runtime_launch_workers_from_latest_task() 
- 新增 a2a_tasks 查询: `python3 a2a_task.py list --state submitted --role worker`
- 对每个 task: 从 message 生成临时 prompt file
- 调用现有 `launch_worker_from_manager_prompt_if_needed()` 启动 Worker
- 更新 task state: submitted → working (via `a2a_task.py update`)
- 保留旧 continuity 路径在 `[[ -z "$a2a_tasks" ]]` 时作为 fallback

### 2. 验证 ACP session/fork 链路
- 检查 `launch_worker_from_manager_prompt_if_needed()` 是否正确使用 session/fork
- 检查 Worker 启动后的 session_id 是否正确写回 a2a_tasks

### 3. 验证 SSE 通知链路
- Worker 完成后 a2a-exit completed → A2A Server TaskStatusUpdateEvent → Manager SSE

### 不在此次范围
- 旧 CSV/continuity 系统移除（后续 PR）
- Reviewer watchdog 触发链路修复（独立 issue）
