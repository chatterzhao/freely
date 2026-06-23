# PRD: SSE 彻底实现

## Goal

从轮询迁移到 SSE 推送，对齐 A2A 官方协议，消除 delivery_status 手搓字段。

## Current State → Target State

```
当前（轮询）:
  Worker 完成 → a2a-exit state=completed
  → delivery_status=pending (SQLite)
  → Manager 下一轮 patrol 调 list-pending-delivery (REST)
  → 注入 prompt → after_run 标记 delivered
  问题: 延迟一个 patrol 周期 / 79 条 stale pending

目标（SSE）:
  Worker 完成 → a2a-exit state=completed
  → A2A Server 推送 TaskStatusUpdateEvent
  → Manager SSE 客户端实时接收
  → 注入 prompt → 触发 Manager decision loop
  优势: 实时 / 无 delivery_status 依赖 / A2A 标准对齐
```

## Phase 1: SSE Client Foundation

### a2a_task.py: stream_task()

- 连接 `GET /tasks/{task_id}/stream`
- 解析 `text/event-stream` 格式
- 事件类型: `TaskStatusUpdateEvent`（state 变更）、`TaskArtifactUpdateEvent`（产出变更）
- stream close = 终态（completed/failed/canceled/rejected）
- CLI: `a2a_task.py stream --task-id <id> [--timeout <s>]`

### a2a_task.py: resubscribe()

- 非终态断开 → `tasks/resubscribe` 重连
- 指数退避: 1s → 2s → 4s → 8s → max 30s
- 携带 `last-event-id` header

### a2a_task.py: SSE 连接池

- Manager 侧维护连接池，最多 10 并发
- `stream_pool.add(task_id)` / `stream_pool.remove(task_id)` / `stream_pool.active_count()`
- 心跳: 每 30s 检查连接存活，死连接自动重连

## Phase 2: Dual-Write Transition

### freely 脚本: 双写模式

- `append_manager_task_context_if_needed`:
  - 优先消费 SSE 事件队列（`.freely/run/sse-events.jsonl`）
  - 同时保留 list-pending-delivery 轮询（fallback）
  - 对比两条路径结果 → runtime event `sse_vs_poll_consistency`
- 过渡期: SSE 事件到达率 > 99% 持续 24h → 进入 Phase 3

### SSE 事件队列

- 格式: JSONL（每行一个事件）
- 字段: `task_id, state, timestamp, event_type, payload`
- Manager prompt 构建时消费队列，处理后标记 consumed

## Phase 3: Remove Polling + delivery_status

### DB Migration

- 一次性脚本: 标记 79 条 delivery_status=pending → delivered
- 验证: 所有对应 Worker 已完成且工位已关闭
- 删除 delivery_status 列 + CHECK 约束

### Code Removal

- a2a_task.py: `mark_delivered()` (L273), `pending_delivery()` (L258)
- a2a_server.py: `/tasks/{id}/delivery` PATCH (L474-478)
- freely: after_run delivery 标记 (L21699-21720)
- freely: prompt 中 PENDING_DELIVERY_COUNT

### SSE-Only Mode

- 移除 list-pending-delivery 调用
- SSE 事件为唯一 Worker 状态来源
- 保留 SSE 连接失败时的告警（不 fallback 到轮询——轮询代码已删）

## Phase 4: Server-Side Fixes

### _restore_tasks() 修复

- 当前 no-op → 改为恢复非终态 task 的 SSE 订阅
- 新增进程 liveness 检查: PID 文件 + kill -0
- 存活 → 恢复订阅 / 已死 → 标记 failed

### filesystem_fallback deprecated

- manager_exit_contract_kind Step 4 (L14737-14771): 保留代码，加 `[DEPRECATED]` + warn 日志
- after_run worker detection (L21655-21697): 同上
- 后续 issue 在 SSE 稳定后安全删除

## Phase 5: Documentation + Verification

### manager-agent.md

- 移除 "curl -N ... 后台运行"
- 替换为 "SSE 自动推送 Worker 状态变更"
- 补充 Manager decision loop 说明

### End-to-End Validation

- daemon start → Manager SSE 监督 Worker → Worker 完成 → Manager decision loop
- 验证: 无 delivery_status 依赖 / 无 79 stale pending / Manager task 不腐烂

## Dev-Loop Handoff

- 实现顺序: Phase 1 → 2 → 3 → 4 → 5
- 每个 Phase 独立可测，有明确的 entry/exit criteria
- Phase 2 过渡期至少 24h，确认 SSE 稳定后再进入 Phase 3
- DB migration (Phase 3) 需要单独的回滚方案
