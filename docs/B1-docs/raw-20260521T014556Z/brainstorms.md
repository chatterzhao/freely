# Brainstorms — worker-dispatch-feedback

## Discovery

### 来源
- GitHub issue #1520 (raw-20260521T014556Z)
- 类型: runtime anomaly — Manager 委派 Worker 后无即时反馈导致空等

### 问题描述

Manager 委派 Worker 的完整链路：

```
Manager 写 prompt → delegate_workers → Runtime launch worker → ?
```

Runtime 知道 launch 是否成功（launch_failed / stale_pid / launched），但 Manager **下一轮才能从 handoff DB 读到**——而且只在"消费汇报"环节被动检查。

导致的实际损失：
1. Worker 初始化超时 → Manager 不知道，继续等（等了 15 轮）
2. Worker 被派到已退休工位 → launch_failed → Manager 不知道原因
3. Worker 进程死亡 → stale_pid → Manager 继续等

### 当前为什么不能直接进入 B2/dev

- 设计方向已明确（inject dispatch results section），但需要先收敛边界条件、确认实现点、评估与已有 handoff 消费机制的兼容性
- 候选 acceptance 尚未 review，需要先过 acceptance boundary

### 当前问题边界

- 只解决 Manager prompt 中"上一轮委派结果"的信息缺失
- 不改变 Worker dispatch 的异步模型
- 不改变 handoff DB 的写入逻辑
- 不引入新的 Runtime/Manager 通信通道

---

## Research

### 方案 A（Issue 已有设计）：Manager prompt 注入"委派结果" section

在 `append_manager_handoff_context_if_needed` 的 "Worker 汇报" section 之前，增加 "委派结果" section。

格式示例：
```
### 委派结果（上一轮 delegate_workers 的反馈）

- 20260520T1207Z-worker-sync-from-worktree.txt → launch_failed: worktree does not exist (target=已退休工位)
- 20260520T1237Z-worker-b1-continuation.txt → launched (PID 12345, session abc)
- 20260520T1233Z-worker-closeout-premerge.txt → stale_pid: worker process no longer alive
```

**优点：**
- 实现简单，只改 prompt 组装逻辑
- 不改 Runtime/Manager 通信架构
- 不改 handoff DB schema
- Manager 下一轮即可看到结果并做出正确决策

**风险/边界：**
- 需确认 Runtime 能在写 handoff 时保留 dispatch 结果（launch_failed/stale_pid/launched）
- 需确认 `append_manager_handoff_context_if_needed` 的调用点是否在 Manager 看到 Worker 汇报之前
- 需处理大量 Worker 时的摘要/截断策略
- Manager 的 decision-making prompt 需要知道如何消费这个新 section

### 方案 B：同步 dispatch 验证

Manager 在 `delegate_workers` 后同步等待 Worker launch 确认再返回。

**评估：** 破坏异步模型，增加 Manager 单轮耗时，且 Worker 初始化超时场景下 Manager 同样会等。不采纳。

### 方案 C：改进 handoff DB 轮询

Manager 在每轮开始时主动扫描 handoff DB 中未消费的 dispatch 结果。

**评估：** 实际上 `append_manager_handoff_context_if_needed` 已经在做这件事。目前的 gap 是 dispatch 结果没有被格式化成 Manager 可读的 section。方案 A 本质上就是方案 C 的改进——把已存在的信息格式化后注入 prompt。不另开方案。

### 方案 D：Runtime 回调/通知机制

Runtime 在 launch 完成后通过回调通知 Manager。

**评估：** 架构侵入性大，引入新的通信通道，与现有异步消费模型冲突。过度设计。

---

## Decision

**采纳方案 A**：Manager prompt 注入"委派结果" section。

理由：
1. 改动范围最小，只改 prompt 组装逻辑
2. 直接消除信息 gap——Runtime 已知的信息格式化后给 Manager
3. 与现有 handoff 消费机制兼容
4. 不改异步架构

### 下一跳

B2_IBM materialization，产出 I-* issue，包含：
1. 确认 `append_manager_handoff_context_if_needed` 的精确实现位置
2. 确认 Runtime 在 handoff 中保留 dispatch result 的字段
3. 设计 dispatch result section 的格式化逻辑
4. 处理边界：无 dispatch 结果、大量 worker、错误信息截断
5. 更新 Manager prompt 的 decision-making section 以消费新信息
