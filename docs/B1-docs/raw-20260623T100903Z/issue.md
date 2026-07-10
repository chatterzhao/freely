---
local_id: raw-20260623T100903Z03Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260623T100903Z-A
platform_ids:
  github:
    issue_id: '3388'
    url: https://github.com/chatterzhao/freely/issues/3388
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-23T10:09:21Z'
updated_at: '2026-06-23T10:09:21Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 为什么这是唯一需要先做的

#3381 的 14 条评论分析得出：当前系统中 6 个问题有 5 个直接或间接因为 SSE 没有彻底实现。SSE 一旦实现完毕：

- **delivery_status 列** → 删除（A2A 标准用 task state 终态 + stream close 作为投递信号）
- **79 条 stale pending** → 随列删除消失
- **list-pending-delivery 轮询** → 被 SSE 事件替代
- **mark_delivered() routing bug** → 函数删除
- **filesystem_fallback** → deprecated（#3387 CSV 清理的前置条件解除）
- **Manager task 腐烂** → 大幅减少（Manager 实时知道 Worker 状态变化，decision loop 能正常运行）
- **_restore_tasks() no-op** → 改为恢复 SSE 订阅
- **scan 刷新时机** → Worker 完成通过 SSE 即时触发

SSE 做完后再评估：parse 兜底是否仍需、L0-L3 兜底优先级是否调整、CSV 清理是否可安全推进。

## 当前状态

### 服务端（已完成 ✅）
`a2a_server.py`：SSE 端点、`_notify_sse()` 推送、`_sse_subscribers` 注册表全部完整。状态变更确实会触发推送——但无人接收。

### 客户端（零实现 ❌）
- `a2a_task.py`：无 `stream_task()`、无 SSE 事件解析、无 `resubscribe`
- `freely` 脚本：无 SSE 消费者，全靠 `list-pending-delivery` REST 轮询
- `manager-agent.md`：写了一句 "curl -N ... 后台运行" 作为 AI 的手工操作 ← AI 从不执行

## SSE 实现清单

### 阶段 1：SSE 客户端（a2a_task.py）

1. **`stream_task(task_id)` 方法**
   - 连接 `GET /tasks/{task_id}/stream`
   - 解析 `TaskStatusUpdateEvent`（state 变更）和 `TaskArtifactUpdateEvent`（产出变更）
   - 处理 stream close：终态信号（state 到达 completed/failed/canceled → stream 关闭）
   - 连接断开时 `tasks/resubscribe`（A2A 官方协议 v1.0 重连机制）

2. **SSE 连接池**
   - Manager 维护最多 10 个并发 SSE 连接
   - 按需订阅活跃 Worker
   - 连接健康检查 + 心跳

### 阶段 2：freely 脚本接 SSE

3. **替代 `list-pending-delivery` 轮询**
   - `append_manager_task_context_if_needed`：用 SSE 事件队列替代 `list-pending-delivery` REST 调用
   - Manager 通过 SSE 实时收到 Worker 完成通知——不再等下一轮 patrol

4. **Manager 收到 Worker 状态变更后执行 decision loop**
   - Worker state=completed → Manager 知道 "Worker X 完成了"
   - Manager 委派 review subagent 评审产出 → 达标/不达标
   - 达标 → Manager 自我 a2a-exit state=completed，释放槽位，看 scan 有无新任务
   - 不达标 → wt-create 建新工位 → 重新委派 Worker
   - Worker state=failed/input-required → Manager 决定：prompt 唤醒 / wt-close 清理

5. **Worker 死掉检测**
   - SSE stream 断开且无重连 → Manager 知道 Worker 可能死了
   - 检查 PID → 确认死亡 → 标记 failed 或 prompt 唤醒

### 阶段 3：废弃 delivery_status

6. **数据库迁移**
   - 一次性脚本：79 条 `delivery_status=pending` 旧记录标记为 delivered（对应 Worker 早已完成）
   - 移除 `freely_db_manager.py` 中 `a2a_tasks` 表的 `delivery_status` 列和 CHECK 约束

7. **代码清理**
   - 移除 `a2a_task.py`：`mark_delivered()`、`pending_delivery()`
   - 移除 `a2a_server.py`：`/tasks/{id}/delivery` PATCH 端点
   - 移除 `freely`：after_run delivery 标记代码（第 21699-21720 行）
   - 移除 `freely`：prompt 中 `PENDING_DELIVERY_COUNT` 显示

### 阶段 4：服务端修复

8. **`_restore_tasks()` 修正**
   - 当前是 no-op（`a2a_server.py` 第 340-360 行，调 get() 后丢弃返回值）
   - 改为：恢复非终态 task 的 SSE 订阅
   - 如果无法恢复（进程已死）→ 标记对应 state 为需要 Manager 关注

9. **filesystem_fallback deprecated**
   - `manager_exit_contract_kind` Step 4 文件系统扫描（第 14737-14771 行）：保留代码，加 `[DEPRECATED]` 注释 + warn 日志
   - SSE 稳定运行后由后续 issue 移除

### 阶段 5：文档

10. **manager-agent.md 更新**
    - 移除 "curl -N ... 后台运行" 的手工操作说明
    - 替换为 "SSE 自动推送 Worker 状态变更，Manager 无需手动轮询"
    - 补充 Manager decision loop：收到 completed → review → pass/fail → complete/redelegate

## 成功标准

- `a2a_task.py stream_task()` 功能性完整：连接、解析事件、重连
- Manager 通过 SSE 实时收到 Worker 完成通知（不再等下一轮 patrol）
- `delivery_status` 列和所有相关代码完全移除
- 79 条旧记录一次性迁移完成
- `_restore_tasks()` 不再是无操作的 no-op
- filesystem_fallback 标记 deprecated
- manager-agent.md 文档更新

## 注意

- 涉及 DB schema 变更（删列）——需要 migration 脚本 + 回滚方案
- SSE 连接池需要合理的心跳和超时策略
- 阶段 2 的 Manager decision loop 需要与现有 patrol 流程（a2a-exit、scan、continuity）整合
- 本 issue 只做 SSE 实现和 delivery_status 废弃。不做 CSV 清理、L0-L3 兜底、scan_state 等其他独立工作

## 做完 SSE 后重新评估

SSE 稳定运行后，重新打开 #3381 的最终梳理，逐一确认：
- [ ] Manager task 腐烂是否不再复现
- [ ] 79 条 stale pending 是否不再出现
- [ ] filesystem_fallback 是否可以安全删除
- [ ] parse_a2a_task_json_reply 的兜底修复是否仍需要（如果需要，优先级降低）
- [ ] L0-L3 兜底的优先级是否需要调整

## 参考

- 原始分析：https://github.com/chatterzhao/freely/issues/3381
- A2A 官方协议 SSE 规范：https://a2a-protocol.org
- SSE 服务端（已完成）：`a2a_server.py` 第 383-432 行
- 当前轮询路径：`freely` 第 21699-21720 行
- `_restore_tasks` no-op：`a2a_server.py` 第 340-360 行
- A2A 标准状态所有权模型：见 #3381 最终讨论
