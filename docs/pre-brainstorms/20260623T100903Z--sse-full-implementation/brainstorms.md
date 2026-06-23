# Brainstorm: 彻底实现 SSE — 从轮询到推送的完整迁移

## Discovery

### Source
- raw issue: `raw-20260623T100903Z` (GitHub #3388)
- 上游分析: #3381 — 14 条评论完成完整根因分析，结论是 SSE 缺失是所有问题的中枢

### 时效性判断
- **最高优先级**。#3381 分析的 6 个问题中有 5 个直接或间接因为 SSE 未彻底实现：
  - 问题 1（语义空循环）：Manager 不知道 Worker 状态变化 → decision loop 不运行 → task 腐烂
  - 问题 2（79 stale pending）：delivery_status 列只为替代 SSE 轮询而存在
  - 问题 3（cache 0%）：会话污染导致每轮 new session，SSE 可让 session 更稳定
  - 问题 4（scan 不刷新）：Worker 完成不能即时触发 scan 刷新
  - 问题 5（A2A 通道不健康）：filesystem_fallback 因为 SSE 不可靠才需要
- SSE 做完后重新评估剩余的独立问题

### 问题边界

**彻底实现 SSE 的范围**：
1. SSE 客户端（a2a_task.py）——当前零实现
2. freely 脚本接 SSE 替代轮询——当前全靠 list-pending-delivery
3. 废弃 delivery_status——SSE 后不需要
4. _restore_tasks() 修复——当前 no-op
5. filesystem_fallback deprecated——SSE 稳定后可以删
6. manager-agent.md 更新——从手工 curl 到自动化

**不在此范围**：
- 内存优先架构（acp-a2a-refactor Phase A，10 个 pending task）——独立重构
- L0-L3 兜底检测——独立安全网
- CSV 清理——SSE 稳定后的后续工作
- scan_state 完善——独立优化

## Research

### A2A 协议标准：SSE 应该如何工作

```
Worker task state 变更（submitted→working→completed/failed）
  → A2A Server PATCH handler 调用 _notify_sse()
    → SSE 推送 TaskStatusUpdateEvent 到所有订阅者
      → 订阅者（Manager）收到事件 → 更新本地状态 → 触发 decision loop

stream close = 终态信号（completed/failed/canceled/rejected）
  客户端收到 stream close → 知道任务结束 → 不再重连
  非终态断开 → tasks/resubscribe 重连
```

### 当前实现状态

| 组件 | A2A 标准 | 当前 | 差距 |
|------|---------|------|------|
| SSE 服务端 | `_task_stream_endpoint` | ✅ 完整（a2a_server.py:383-432） | 无 |
| `_notify_sse()` | PATCH 时推送 | ✅ 完整（a2a_server.py:428-432） | 无 |
| `_sse_subscribers` | 订阅者注册表 | ✅ 完整（a2a_server.py:386） | 无 |
| `stream_task()` | 客户端连接 | ❌ 不存在 | 需新建 |
| `resubscribe` | 断线重连 | ❌ 不存在 | 需新建 |
| Manager 消费 SSE | 实时接收事件 | ❌ 只用 list-pending-delivery 轮询 | 需替换 |
| `_restore_tasks()` | 恢复订阅 | ❌ no-op（调 get() 后丢弃） | 需修复 |
| delivery_status | 不需要（A2A 标准用 state 终态） | ❌ 手搓轮询替代品 | 需删除 |

### 代码路径详细分析

#### 1. SSE 客户端（a2a_task.py）

需要新增的方法：
- `stream_task(task_id)` — 连接 `/tasks/{task_id}/stream`，解析 SSE `text/event-stream`
- 事件类型处理：
  - `TaskStatusUpdateEvent` → 提取 state、timestamp、message → 写入本地事件队列
  - `TaskArtifactUpdateEvent` → 提取 artifact 变更
  - stream close → 标记 task 终态
- `resubscribe(task_id, last_event_id)` — 断线重连，从 last_event_id 之后恢复

连接管理：
- Manager 维护 SSE 连接池（最多 10 个并发，与 Worker 槽位一致）
- 每个活跃 Worker 一个连接
- 心跳检测 + 自动重连（指数退避，max 30s）
- 非终态断开 → resubscribe；终态断开 → 关闭连接

#### 2. freely 脚本替换轮询

**当前轮询路径**（需替换）：
- `append_manager_task_context_if_needed`（第 19234 行）→ 调 `list-pending-delivery` → 注入 Worker 汇报到 prompt
- after_run（第 21699-21720 行）→ 标记 delivery_status=delivered

**替换为 SSE 事件驱动**：
- Manager 启动时 → 对每个 scan_state=working 的 item → 查 A2A task → 建 SSE 连接
- SSE 事件到达 → 写入 Manager 的事件队列（`.freely/run/sse-events.jsonl`）
- prompt 构建时 → 读事件队列 → 注入 Worker 状态变更到 prompt
- 不再需要 delivery_status 字段

#### 3. Manager decision loop

SSE 事件驱动后的 Manager patrol 流程：
```
SSE: Worker state=completed
  → Manager 收到 → 委派 review subagent 评审产出
    → 达标 → Manager a2a-exit state=completed（自我收口）
            → 释放 Worker 槽位 → 看 scan 有无新任务
    → 不达标 → wt-create 建新工位 → 重新委派 Worker

SSE: Worker state=failed / stream 断开
  → Manager 收到 → 查 PID 确认死亡
    → 发 prompt 唤醒 / wt-close 清理
    → 标记对应 scan_state → 决定是否重建工位重新委派
```

#### 4. delivery_status 废弃

**需删除的代码**：
- `freely_db_manager.py`：`delivery_status` 列 + CHECK 约束 + `h_a2a_task_list_pending_delivery` + `h_a2a_task_update_delivery_status`
- `a2a_task.py`：`mark_delivered()`（第 273 行）、`pending_delivery()`（第 258 行）
- `a2a_server.py`：`/tasks/{id}/delivery` PATCH 端点（第 474-478 行）
- `freely` 脚本：after_run delivery 标记（第 21699-21720 行）、prompt 中 `PENDING_DELIVERY_COUNT`

**一次性迁移**：79 条 `delivery_status=pending` 旧记录 → 标记为 delivered（Worker 早已完成，Manager 早已处理）

#### 5. _restore_tasks() 修复

当前（`a2a_server.py` 第 340-360 行）：调 `get_all_dicts()` → 过滤非终态 → 调 `get()` 丢弃返回值 → 打印 restored 计数。完全 no-op。

修正后：
1. 读所有非终态 task
2. 对于 `working`/`input-required` task：检查对应进程是否存活（PID 文件 + kill -0）
3. 存活 → 恢复 SSE 订阅
4. 已死 → 标记 `failed`（进程在停机期间死亡）
5. 对于 `submitted` task（Manager task）：检查是否有对应 Worker task → 无且超 30s → 标记 completed

### 风险评估

**高风险**：
- DB schema 变更（删 delivery_status 列）：需 migration 脚本 + 回滚方案 + 验证
- SSE 连接池管理：连接泄漏、重连风暴、心跳超时需要仔细设计
- 轮询→推送切换：过渡期可能双写（同时保留轮询和 SSE），确认 SSE 稳定后再删轮询

**中风险**：
- Manager decision loop 行为变更：从被动轮询到事件驱动
- filesystem_fallback deprecated：保留代码但加 warn，不立即删除

**低风险**：
- manager-agent.md 文档更新：纯文本
- delivery_status 代码删除：纯清理，无行为变更

### 依赖关系

**上游依赖**：无

**下游影响**：
- 此 issue 完成后，以下问题自然消失或大幅缓解：
  - 问题 2（79 stale pending）→ 消失
  - 问题 5（A2A 通道不健康）→ filesystem_fallback 可 deprecated
  - 问题 1（空循环）→ Manager decision loop 正常运行
- 以下 issue 需重新评估：
  - parse 兜底修复 → 优先级降低
  - L0-L3 兜底 → 优先级可能调整
  - CSV 清理 → 前置条件满足（SSE 稳定）

### 不可变性检查
- CONSTITUTION.md 未禁止通信协议升级
- 不涉及分支/worktree/合并操作
- 不涉及 .githooks/ 修改
- DB schema 变更需要 migration 脚本

## Decision

### 方案：5 阶段递进实施

SSE 实现按依赖关系分 5 阶段，每阶段可独立验证：

**阶段 1：SSE 客户端基础（无行为变更）**
- a2a_task.py：`stream_task()` + `resubscribe()` + SSE 事件解析
- 独立测试：连接 SSE 端点，接收事件，验证 stream close
- 此时 Manager 仍用轮询，SSE 客户端只是"可用了"

**阶段 2：freely 脚本双写过渡**
- Manager 同时走 SSE 和轮询两条路径
- 优先消费 SSE 事件，轮询作为 fallback
- 写 runtime event 对比两条路径的结果
- SSE 事件到达率 > 99% 且持续稳定 → 进入阶段 3

**阶段 3：废弃轮询 + delivery_status**
- 移除 list-pending-delivery 调用
- 删除 delivery_status 列和相关代码
- 执行 79 条旧记录迁移
- after_run delivery 标记代码移除

**阶段 4：服务端修复**
- `_restore_tasks()` 改为恢复 SSE 订阅 + 进程 liveness 检查
- filesystem_fallback 标记 deprecated（加 warn 日志，保留代码）

**阶段 5：文档 + 验证**
- manager-agent.md 更新
- 端到端验证：daemon start → Manager 通过 SSE 监督 Worker → Worker 完成 → Manager decision loop

### 拒绝的替代方案

**方案 B：一次性全切换（无过渡期）**
- 拒绝理由：风险过高。SSE 客户端是全新代码，直接替换轮询在出问题时无法回退。双写过渡期提供安全网。

**方案 C：只实现 SSE 客户端，保留 delivery_status**
- 拒绝理由：delivery_status 是 A2A 非标准字段，SSE 实现后它没有存在理由。保留它只会增加维护负担和混淆。

### 做完 SSE 后重新评估清单

- [ ] Manager task 腐烂是否不再复现
- [ ] 79 条 stale pending 是否不再出现
- [ ] filesystem_fallback 是否可以安全删除（后续 issue）
- [ ] parse_a2a_task_json_reply 的兜底修复是否仍需要
- [ ] L0-L3 兜底的优先级是否需要调整
- [ ] CSV 清理（#3387）是否可以安全执行

### 下一跳
- 进入 B2_IBM → 产出 PRD + pre-tests + tasks + code-review → milestone
