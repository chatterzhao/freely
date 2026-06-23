# Tasks: SSE 彻底实现

## Phase 1: SSE Client Foundation

### T1.1 — a2a_task.py stream_task()
- [ ] 实现 `stream_task(task_id)` 方法：HTTP GET `/tasks/{task_id}/stream`，Accept: text/event-stream
- [ ] 解析 SSE 事件格式（event:, data:, id: 字段）
- [ ] 处理 `TaskStatusUpdateEvent`（提取 state、timestamp）
- [ ] 处理 `TaskArtifactUpdateEvent`（提取 artifact 变更）
- [ ] stream close 检测 → 终态信号
- [ ] CLI 入口: `a2a_task.py stream --task-id <id> [--timeout <s>]`

### T1.2 — a2a_task.py resubscribe()
- [ ] 实现 `resubscribe(task_id, last_event_id)` 方法
- [ ] POST `tasks/resubscribe` 携带 last-event-id
- [ ] 指数退避重连: 1s→2s→4s→8s→max 30s

### T1.3 — SSE 连接池
- [ ] `SSEPool` 类: add/remove/active_count/close_all
- [ ] 最大 10 并发连接
- [ ] 心跳: 每 30s 检查连接存活
- [ ] 死连接自动 resubscribe

### T1.4 — 单元测试
- [ ] stream_task 连接测试（mock A2A server SSE 端点）
- [ ] 事件解析测试（valid/invalid/malformed events）
- [ ] 重连退避测试
- [ ] 连接池并发测试

## Phase 2: Dual-Write Transition

### T2.1 — SSE 事件队列
- [ ] `.freely/run/sse-events.jsonl` 写入逻辑
- [ ] 事件格式: `{"task_id":"...","state":"...","timestamp":"...","event_type":"..."}`
- [ ] 消费后标记 consumed（追加 `.consumed` 字段）

### T2.2 — freely 双写集成
- [ ] `append_manager_task_context_if_needed` 优先读 SSE 事件队列
- [ ] 保留 list-pending-delivery 作为 fallback
- [ ] 对比两条路径 → runtime event `sse_vs_poll_consistency`

### T2.3 — 过渡期监控
- [ ] SSE 事件到达率统计（event_count / expected_count）
- [ ] > 99% 持续 24h → 触发 Phase 3 就绪信号

## Phase 3: Remove Polling + delivery_status

### T3.1 — DB Migration
- [ ] 一次性 migration 脚本: 79 条 delivery_status=pending → delivered
- [ ] 验证: 对应 Worker 已完成且工位已关闭
- [ ] 删除 delivery_status 列 + CHECK 约束

### T3.2 — Code Removal
- [ ] a2a_task.py: 删除 mark_delivered()、pending_delivery()
- [ ] a2a_server.py: 删除 /tasks/{id}/delivery PATCH 端点
- [ ] freely: 删除 after_run delivery 标记代码 (L21699-21720)
- [ ] freely: 删除 prompt 中 PENDING_DELIVERY_COUNT

### T3.3 — SSE-Only Mode
- [ ] 移除 list-pending-delivery 调用
- [ ] SSE 事件为唯一 Worker 状态来源
- [ ] SSE 连接失败告警（不再 fallback 到已删除的轮询）

## Phase 4: Server-Side Fixes

### T4.1 — _restore_tasks() 修复
- [ ] 读非终态 task → 检查进程 liveness (PID + kill -0)
- [ ] 存活 → 恢复 SSE 订阅
- [ ] 已死 → 标记 state=failed, reason="process_died_during_downtime"

### T4.2 — filesystem_fallback deprecated
- [ ] manager_exit_contract_kind Step 4 (L14737-14771): 加 [DEPRECATED] + warn 日志
- [ ] after_run worker detection (L21655-21697): 同上
- [ ] 保留代码，不删除

## Phase 5: Documentation + Verification

### T5.1 — manager-agent.md 更新
- [ ] 移除 "curl -N ... 后台运行"
- [ ] 替换为 "SSE 自动推送 Worker 状态变更，Manager 无需手动轮询"
- [ ] 补充 Manager decision loop: SSE completed → review → pass/fail → complete/redelegate

### T5.2 — End-to-End Verification
- [ ] daemon start → Manager 通过 SSE 监督 Worker
- [ ] Worker a2a-exit completed → Manager 实时收到 TaskStatusUpdateEvent
- [ ] delivery_status 依赖为零（grep 确认）
- [ ] 79 条 stale pending 不再出现
- [ ] _restore_tasks 在重启后正确恢复 SSE 订阅

### T5.3 — SSE 后重新评估清单（来自 B1 brainstorms）
- [ ] Manager task 腐烂是否不再复现
- [ ] 79 条 stale pending 是否不再出现
- [ ] filesystem_fallback 是否可以安全删除（后续 issue）
- [ ] parse_a2a_task_json_reply 的兜底修复是否仍需要（如果需要，优先级降低）
- [ ] L0-L3 兜底的优先级是否需要调整
- [ ] CSV 清理（#3387）是否可以安全执行
