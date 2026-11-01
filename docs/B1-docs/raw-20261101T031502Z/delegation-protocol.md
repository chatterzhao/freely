---
protocol_id: DELEGATION-20261101T031502Z
phase_state: draft
created_at: 2026-11-01
---

# Delegation Protocol v0（Manager/Worker/Reviewer 交接）

> 这是 C-B/C 的协议草案，不是实现。目标是把“Task 状态、执行者状态、消息归属”拆开，替换当前 `a2a_tasks` 单行覆盖模型。

## 1. 三个分离

| 概念 | 回答 | 存储 |
| --- | --- | --- |
| Task | 这件工作是什么、到哪个阶段 | `delegation_tasks` |
| Handoff | 谁在什么时候把什么交给谁 | `handoffs`（append-only） |
| Message | 具体一轮说了什么、谁读过 | `handoff_messages`（append-only） |

当前 Freely 把三者压进 `a2a_tasks` 一行；新协议必须拆开。

## 2. Handoff Envelope

```json
{
  "handoff_id": "H-20261101T031502Z-A-001",
  "task_id": "T-20261101T031502Z-A",
  "parent_handoff_id": null,
  "from": {"role": "manager", "agent_id": "manager_01", "session_id": "..."},
  "to":   {"role": "worker",  "agent_id": "worker_03", "session_id": "..."},
  "intent": "实现 pre-tests 中的 AT-001..AT-005",
  "constraints": ["只改 docs/system/...", "不碰 develop"],
  "acceptance": ["pre-tests 全绿", "reviewer pass"],
  "artifacts": [
    {"id": "A-1", "kind": "prd", "path": "docs/B2-docs/.../prd.md", "sha256": "..."},
    {"id": "A-2", "kind": "pre-tests", "path": ".../pre-tests.md", "sha256": "..."}
  ],
  "context_refs": [
    {"kind": "issue", "id": "I-...", "revision": "..."},
    {"kind": "prior_verdict", "handoff_id": "H-...-000"}
  ],
  "expected_output": {"kind": "implementation", "schema": "freely.worker.exit.v1"},
  "ownership": {"owner": "worker_03", "thread_key": "github:owner/repo#4110", "lease_until": "..."},
  "status": "pending",
  "created_at": "..."
}
```

必填：`handoff_id`、`task_id`、`from`、`to`、`intent`、`acceptance`、`expected_output`、`ownership`、`status`、`created_at`。

## 3. 消息模型

```json
{
  "message_id": "M-...",
  "handoff_id": "H-...",
  "role": "worker",
  "parts": [
    {"type": "text", "text": "..."},
    {"type": "data", "data": {"report_state": "ready", "verdict": "pass"}}
  ],
  "created_at": "...",
  "read_by": ["manager_01"]
}
```

规则：

- append-only；不允许 update 覆盖。
- `message_id` 幂等：同一 id 重复投递只记一次。
- `read_by` 记录谁读过；未读消息在 Assignment 结束时重投。
- 结构化字段放 `data`，不要塞进自由文本 summary。

## 4. Task 状态机

```
pending → delivering → accepted → working
                                   ├─ waiting（等人/等输入）
                                   ├─ ready（可验收）
                                   ├─ blocked
                                   ├─ failed
                                   └─ handback（越界/换人）
ready → reviewing → completed
                 └─ changes_requested → working
任何非终态 → canceled（人 stop / 明确取消）
```

- **terminal 不可变**：`completed/failed/canceled` 后只能新建 Task，不能复活；后续消息走新 Task 或明确的 reopen。
- Task 状态与 Assignment/执行者状态分离；Worker 死亡不等于 Task 失败。
- `waiting` 不是终态；需要 owner 与超时释放。

## 5. Ownership 规则（五类后续消息）

| 场景 | owner | 规则 |
| --- | --- | --- |
| 新建请求 | Manager | 进入 Eval/B1；未分配前 Manager 拥有 |
| 活跃工单的 Thread 后续 | 当前 Worker | 同一 `thread_key` 直达 Worker；Manager 不再中转 |
| 已完成工单的 Thread 后续 | 原 Worker（lease） | 在 lease 内归原 Worker；超时/越界 handback 回 Manager |
| 跨工单消息 | 当前 Worker | 只能 handback 一次，带目标 task/理由；不直接改别的 Task |
| 人的 stop | Manager/人 | stop 优先于 Worker ownership；Worker 不能自行恢复 |
| Reviewer 反馈 | Reviewer → Worker | Reviewer 拥有 verdict；Worker 拥有 fix；3 轮失败回 Manager |

补充：

- `ownership.thread_key` 是平台线程键（`github:owner/repo#issue`、`feishu:chat:thread`）。
- `lease_until` 到期后 owner 释放；未读消息回 Manager。
- handback 必须写 `parent_handoff_id`，目标明确，不能“广播”。

## 6. 幂等与去重

- `handoff_id` = `task_id + stage + attempt` 的稳定 hash；重试复用。
- relay key = `handoff_id + message_kind`；重复发送只投递一次。
- 平台事件 id（GitHub comment id / Feishu message id）作为外部幂等键；没有就拒绝自动 intake。
- 任务创建以 `handoff_id` 幂等；重复 accept 不产生第二个 Task。

## 7. 超时与恢复

| 事件 | 动作 |
| --- | --- |
| delivery 失败 | 退避重试；超过阈值 → `blocked` + Attention |
| Worker session 死亡 | Assignment failed；Task 保持 working/waiting；新 Assignment 带 recovery note |
| ownership lease 到期 | 释放 owner；未读消息回 Manager；不自动开新单 |
| Reviewer 3 轮 fail | handback Manager；Task `blocked`，不无限循环 |
| 进程重启 | 从 DB 恢复 handoff/message/read 状态；未读重投 |

## 8. 与 A2A / DSH 的映射

### A2A（外部互操作）

- 一个 Freely Task 可以映射为一个 A2A Task；`contextId` = Freely task/thread key 的稳定 id。
- 后续消息作为新 A2A Message，带 `referenceTaskIds`；终态 Task 不复活，新建 Task。
- Artifact 用 `artifactId` 持久化；Reviewer verdict 是 artifact，不是覆盖 summary。
- 不要求内部实现完整 A2A；只在需要外部 Agent 时做 adapter。

### DSH（内部 delegation 参考）

| Freely | DSH |
| --- | --- |
| Handoff | Report/Assignment 变化 |
| `waiting` | Report waiting / Attention |
| `ready` | Report ready |
| `blocked/failed` | Report blocked/failed |
| ownership | followupOwners |
| handback | handback |
| 未读消息 | Input read/unread |
| recovery note | Assignment recovery note |

Freely 保留自己的 Task/Handoff 存储；DSH 只提供语义参考，不直接复用其 Ticket。

## 9. 迁移策略

1. 新增表 `delegation_tasks`、`handoffs`、`handoff_messages`；保留 `a2a_tasks` 只读兼容。
2. 双写开关：Manager/Worker/Reviewer 写新表，同时更新旧行供旧查询读取。
3. 读路径逐步切到新表；SSE 事件带 `handoff_id`/`message_id`。
4. 旧 `a2a_tasks` 停止写入；保留历史查询。
5. 迁移完成后删除覆盖式 update 路径。

## 10. 验收场景

1. 首次 Manager→Worker：new session 收到 envelope + role prompt。
2. 首次 Worker→Reviewer：new/fork session 收到 review envelope；verdict 追加为 artifact。
3. Worker 死亡：fail 反馈重投到新 session；消息不丢。
4. 同一 PR 两条后续评论：同一 owner，不重复开单。
5. 跨工单评论：handback 一次，目标正确，不广播。
6. 人 stop：Worker 不能继续；Task canceled。
7. 重复 relay：同一 message_id 只投递一次。
8. 跨 harness：context pack 包含 PRD/pre-tests/artifact/verdict，Reviewer 能独立审查。

## 11. 未解

- `thread_key` 的平台映射由谁维护（issue-sync 还是 scan）？
- 旧 `a2a_tasks` 双写期间，谁拥有 state 真相？
- `lease_until` 默认多长？按角色/工单类型是否不同？
- 跨项目/跨仓 thread 是否允许？
- A2A 外部 Task 与内部 Task 的 ID 映射是否要暴露给用户？
