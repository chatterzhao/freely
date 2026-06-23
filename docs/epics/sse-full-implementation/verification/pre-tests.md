# Pre-Tests: SSE 彻底实现

## Unit

### U1 — stream_task 连接
- requirement: `stream_task(task_id)` 成功连接 SSE 端点，接收 text/event-stream
- evidence_level: script regression
- environment: local (mock A2A server)
- evidence: pytest 测试通过，验证 HTTP 200 + Content-Type: text/event-stream
- failure signal: 连接超时 / 非 200 响应 / Content-Type 不匹配
- failure handling: 检查 A2A server SSE 端点注册

### U2 — SSE 事件解析
- requirement: 正确解析 TaskStatusUpdateEvent（state, timestamp）、TaskArtifactUpdateEvent
- evidence_level: script regression
- environment: local
- evidence: pytest 参数化测试覆盖 valid/malformed/missing-field 事件
- failure signal: 解析异常 / 字段缺失
- failure handling: 增强解析器容错

### U3 — stream close 检测
- requirement: stream close → 识别为终态信号（completed/failed/canceled）
- evidence_level: script regression
- environment: local
- evidence: mock server 在发送完成事件后关闭 stream，客户端正确检测
- failure signal: stream close 未被识别 / 误判为非终态

### U4 — resubscribe 重连
- requirement: 非终态断开 → 指数退避重连（1s→2s→4s→8s→max 30s）
- evidence_level: script regression
- environment: local
- evidence: mock server 主动断开，验证客户端重连时序
- failure signal: 不重连 / 退避时间不符合预期 / 终态后仍重连

### U5 — 连接池管理
- requirement: 最多 10 并发，add/remove/active_count 正确
- evidence_level: script regression
- environment: local
- evidence: 并发测试：同时添加 15 个连接，验证 10 个上限
- failure signal: 超过上限 / 计数不准确 / remove 后连接未关闭

## Integration

### I1 — SSE 事件队列写入
- requirement: SSE 事件到达 → 写入 `.freely/run/sse-events.jsonl`
- evidence_level: integration
- environment: test-pre-merge worktree
- evidence: daemon start → Worker 完成 → 检查 jsonl 文件存在且内容正确
- failure signal: 事件丢失 / 格式错误 / 重复写入

### I2 — 双写一致性
- requirement: SSE 事件队列和 list-pending-delivery 返回的 Worker 完成列表一致
- evidence_level: integration
- environment: test-pre-merge worktree
- evidence: runtime event `sse_vs_poll_consistency` 显示 match/mismatch 计数
- failure signal: mismatch > 1%
- failure handling: 回退到优先消费 list-pending-delivery

### I3 — delivery_status migration
- requirement: 79 条 pending → delivered，delivery_status 列删除
- evidence_level: integration
- environment: test-pre-merge worktree
- evidence: migration 脚本执行前后 DB dump 对比
- failure signal: 迁移失败 / 数据丢失 / 列删除后 CHECK 约束残留
- failure handling: 回滚脚本恢复列和约束

### I4 — _restore_tasks 进程 liveness
- requirement: 重启后恢复 SSE 订阅（存活进程）/ 标记 failed（死进程）
- evidence_level: integration
- environment: test-pre-merge worktree
- evidence: 模拟 working task + 已死 PID → restart → 验证 state=failed
- failure signal: 死进程未标记 / 活进程订阅未恢复

## End-to-End

### E1 — Manager 通过 SSE 实时收到 Worker 完成
- requirement: daemon start → Manager SSE 监督 → Worker 完成 → Manager prompt 实时反映
- evidence_level: end-to-end scenario
- environment: test-pre-merge worktree
- evidence: cycle log 显示 Worker 完成时间与 Manager prompt 注入时间的间隔 < 3s
- failure signal: 延迟 > 10s / 完全未收到
- failure handling: 检查 SSE 连接池状态 / 事件队列

### E2 — delivery_status 依赖为零
- requirement: grep 确认 delivery_status 不在任何活跃代码路径中
- evidence_level: end-to-end scenario
- environment: test-pre-merge worktree
- evidence: `grep -r "delivery_status" docs/system/workspace/scripts/runtime/` 只在已废弃代码中出现
- failure signal: 活跃代码路径引用 delivery_status

### E3 — 79 stale pending 不再出现
- requirement: daemon 运行 10+ 周期后，无新的 stale pending 产生
- evidence_level: end-to-end scenario
- environment: test-pre-merge worktree
- evidence: PENDING_DELIVERY_COUNT 不再出现在 prompt 中（已移除）
- failure signal: 新 pending 产生

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本次实现为通信协议升级（轮询→SSE），不需要真实环境测试。端到端验证在 test-pre-merge worktree 中完成，已覆盖所有集成面。

## Acceptance Items

| id | requirement | evidence_level | status | artifact_ref |
|----|------------|---------------|--------|-------------|
| A1 | stream_task 连接 SSE 端点 | script regression | pending | pytest test_stream_connect.py |
| A2 | SSE 事件解析（含容错） | script regression | pending | pytest test_sse_parse.py |
| A3 | stream close 终态检测 | script regression | pending | pytest test_stream_close.py |
| A4 | resubscribe 指数退避 | script regression | pending | pytest test_resubscribe.py |
| A5 | 连接池 10 并发上限 | script regression | pending | pytest test_pool_concurrency.py |
| A6 | SSE 事件 → jsonl 写入 | integration | pending | .freely/run/sse-events.jsonl |
| A7 | 双写一致性 > 99% | integration | pending | runtime event sse_vs_poll_consistency |
| A8 | delivery_status migration | integration | pending | migration script |
| A9 | _restore_tasks liveness | integration | pending | restart cycle log |
| A10 | Manager 实时收到 Worker 完成 (< 3s) | end-to-end scenario | pending | cycle log timing |
| A11 | delivery_status 无活跃引用 | end-to-end scenario | pending | grep audit |
| A12 | premerge-integration gate | premerge-integration | pending | test-pre-merge worktree verification |

- surface_kind: protocol-upgrade
- target_lane: premerge-integration
- promotion_gate: develop_merge
