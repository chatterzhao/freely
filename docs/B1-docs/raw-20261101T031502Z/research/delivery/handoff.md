---
analysis_id: HANDOFF-20261101T031502Z
phase_state: in_progress
created_at: 2026-11-01
---

# Manager/Worker/Reviewer 交接：缺陷、协议与吸收

## 0. 结论

**既有协议层选错，也有实现 bug。**

- Manager/Worker/Reviewer 是同一项目内的“领导—员工—独立评审”，最接近 DSH Router/Worker + Report/Attention/ownership，不是 AHP/ACP，也不是完整 A2A。
- Freely 当前所谓 A2A 实际是 SQLite task 表 + 自定义 REST + SSE：只有 state 名字是 A2A，没有 contextId/messageId/artifact 历史，也没有 terminal 不可变。
- 确定的实现 bug：`acp_session_connect()` 在 `session/new|fork` 不发送传入 message；首次 Reviewer 交接、Worker 死亡后的 fail 反馈可能丢。
- Reviewer 契约矛盾：agent 文档禁止 `a2a-exit`，watchdog 要求 `a2a-exit`，skill 要 JSON verdict。

## 1. 当前数据模型的硬缺陷

`freely.db` 的 `a2a_tasks` 列：

```
id, task_id, name, description, state, agent_id, skill, session_id,
message, raw_key, prompt_file, worktree, branch, exit_kind, reason,
progress, next_action, completion_summary, evidence_paths, worker_prompts_csv
```

没有：`context_id`、`message_id`、artifact 历史、`parent_task_id`、`handoff_id`、`owner`、读/未读。

后果：

1. 一个 Task 只有一条 `message`，后续 summary/reason/next_action 覆盖。
2. Manager 派工、Worker 汇报、Reviewer verdict 都写同一行。
3. 没有 artifact 版本；Reviewer required_fixes 和 Worker evidence 只能覆盖 `evidence_paths`。
4. 没有 contextId，多轮审查无法组织。
5. state 可被任意 update，没有 terminal 不可变约束。

## 2. “A2A”实现的协议偏差

`a2a_server.py`：

- 自定义 REST `/tasks`、`PATCH /tasks/{id}`、`/tasks/{id}/messages`，不是官方 A2A `SendMessage`/`GetTask`/`SubscribeToTask` JSON-RPC。
- `FreelyAgentExecutor.execute()` 生成一个外部 A2A task_id，在本地 SQLite 创建另一个内部 task_id，再用 artifact 告诉调用方 `internal_task_id=...`；对外立刻发 `COMPLETED`，内部实际是 `submitted`。
- `a2a_types.py` 定义了 Message.messageId/contextId/Artifact，但表里没有持久化；类型层与存储层脱节。

结论：不是 A2A 协议实现，而是“A2A 命名的本地任务总线”。

## 2.1 五类后续消息：现状 vs 目标

| 场景 | 当前实际行为 | 目标 owner | 缺口 |
| --- | --- | --- | --- |
| 新建请求 | scan 拉 open issue/body → Manager → B1 | Manager 直到分配 | 无 per-event 准入；同一 issue 可能重复开单 |
| 活跃工单的 Thread 后续 | issue comment 不进 scan；chat 进 Manager prompt；PR review 无入口 | 当前 Worker（thread_key 直达） | **主要漏接点**；Manager 靠轮询/人转述 |
| 已完成工单的 Thread 后续 | issue 已 close；`freely` 对 closed issue 新评论有 gate 拦截；无 owner | 原 Worker lease → 超时/越界 handback Manager | 没有 lease/复活规则；容易新开单或完全忽略 |
| 跨工单消息 | 无检测；靠人/Manager 发现 | 当前 Worker 只能 handback 一次，带目标/理由 | 没有目标校验；可能广播/重复 |
| 人的 stop | `freely stop`/`wt-close` 停 runtime/工位；chat 停止请求进 Manager prompt | Manager/人优先；Worker 不能自行恢复 | 没有事件级 stop；Worker 可能继续跑 |
| Worker 死亡 | supervisor/A2A failed；新 session 可能收不到 fail message | Task 保持 working；新 Assignment 带 recovery note | `session/new|fork` 丢 message（已确认 bug） |
| Reviewer 反馈 | watchdog 要求 `a2a-exit`；agent 文档禁止；skill 要 JSON verdict | Reviewer 拥有 verdict；Worker 拥有 fix；3 轮回 Manager | 契约矛盾，verdict 落点不唯一 |

### 2.1.1 现状证据

- `task-lifecycle-scan.py` 没有 `comments`/`comment` 处理。
- `platform-adapter.fetch_issue` 返回 comments 但只有 body；`list_open_issue_records` 只有 number/title/body/state。
- `freely` 对 closed issue 新评论有 gate（#3302），但没有“谁来读这条评论”的 owner。
- `acp_session_connect` 在 new/fork 不发送 message；`acp-bridge.session_new` 不注入角色 prompt。
- `watchdog_sse._build_review_task_message` 与 `reviewer-agent.md`/`freely-tdd-review` 三处 verdict 契约不一致。

### 2.1.2 回放结果（2026-11-01）

已跑只读状态机 `research/ops/replay/handoff_replay.py`：

- new→worker 拥有；active follow-up 直达 worker。
- 跨工单 handback 一次，第二次拒绝。
- Worker 死亡：Task 保持 working，owner 回 Manager，带 recovery。
- Reviewer 2 轮 changes_requested；3 轮回 Manager/blocked。
- completed 工单 lease 内归原 Worker；过期回 Manager。
- 人 stop 优先，owner=human。

这是协议自洽验证，不是 runtime E2E；E2E 在 B2 验收。

### 2.1.3 E2E 场景（B2 验收）

1. issue #4070 两条真实评论 → 同一 thread，不新开 issue。
2. 关闭 issue 后的评论 → 不自动复活；按 lease/handback 处理。
3. 同一 PR 两条 review comment → 同一 owner，不重复。
4. 跨工单评论 → handback 一次，目标正确。
5. 人 stop → Worker 停止，Task canceled。
6. Worker 死亡 → fail 反馈进新 session，消息不丢。
7. Reviewer 3 轮 fail → handback Manager，不无限循环。

## 3. 跨 harness 交接的确定 bug

`agent_working.acp_session_connect()`：

| 分支 | 是否发送 message | 结果 |
| --- | --- | --- |
| 已有 session alive → `session/prompt` | 是 | 正常 |
| `session/resume` + prompt | 是 | 正常 |
| `session/fork` | **否** | 新 fork session 收不到 task_msg |
| `session/new`（含跨 tool） | **否** | 新 session 收不到 task_msg |
| `force_new` | **否** | gate Reviewer 收不到 task_msg |

`watchdog_sse._handle_needs_reviewer()` 传入 `message=task_msg`，但首次 Reviewer 通常是 new/fork，于是 task_msg 被丢弃。`_handle_needs_worker()` 的 fail 反馈同理。

另外 `acp-bridge.session_new()` 只传 `cwd/mcpServers`，`session/fork` 只传 `sessionId/role/agentId`；新 session 不会自动加载 Reviewer/Worker 角色定义。于是可能“没有角色 prompt + 没有任务消息”。

## 4. Reviewer 契约矛盾

- `reviewer-agent.md`：`不用 a2a_task.py / a2a-exit（Manager 专属）`。
- `watchdog_sse._build_review_task_message()`：`完成后调 a2a-exit 声明 verdict`。
- `freely-tdd-review`：输出 JSON verdict（pass/fail + required_fixes）。

三条不一致。Reviewer verdict 可能落在不同地方，Manager/Worker 读到的不一致。

## 5. 为什么 AHP/ACP 不是答案

| 协议 | 解决什么 | 是不是领导 delegation |
| --- | --- | --- |
| ACP | 单 client ↔ 单 agent：prompt、工具、权限 | 否，通信层 |
| AHP | N client ↔ host：session 状态同步、actions、重连 | 否；官方明确不管 agent-to-agent |
| A2A | agent ↔ agent：Task/Message/Artifact/contextId | 部分，跨组织任务协议 |
| DSH Router/Worker | 单 runtime 内领导 delegation：Ticket/Assignment/Report/Attention | **是** |

Freely 的 Manager/Worker/Reviewer 是内部团队，不是跨组织黑盒 Agent；最值得学的是 DSH 的：

- Report 六态：progress/waiting/ready/blocked/failed/dropped。
- Attention：单问题、目标会话、human_action、question_for_trigger_id。
- followupOwners + handback。
- Assignment 状态与 Ticket/消息归属分离。
- 未读 Input 重投 + recovery note。

## 6. Delegation Protocol v0

### 6.1 三个分离

| 概念 | 回答 | 存储 |
| --- | --- | --- |
| Task | 这件工作是什么、到哪个阶段 | `delegation_tasks` |
| Handoff | 谁在什么时候把什么交给谁 | `handoffs`（append-only） |
| Message | 具体一轮说了什么、谁读过 | `handoff_messages`（append-only） |

### 6.2 Handoff Envelope

```json
{
  "handoff_id": "H-...-001",
  "task_id": "T-...",
  "parent_handoff_id": null,
  "from": {"role": "manager", "agent_id": "manager_01", "session_id": "..."},
  "to": {"role": "worker", "agent_id": "worker_03", "session_id": "..."},
  "intent": "实现 pre-tests 中的 AT-001..AT-005",
  "constraints": ["只改 docs/system/...", "不碰 develop"],
  "acceptance": ["pre-tests 全绿", "reviewer pass"],
  "artifacts": [{"id": "A-1", "kind": "prd", "path": "...", "sha256": "..."}],
  "context_refs": [{"kind": "issue", "id": "I-...", "revision": "..."}],
  "expected_output": {"kind": "implementation", "schema": "freely.worker.exit.v1"},
  "ownership": {"owner": "worker_03", "thread_key": "github:owner/repo#4110", "lease_until": "..."},
  "status": "pending",
  "created_at": "..."
}
```

### 6.3 消息

```json
{
  "message_id": "M-...",
  "handoff_id": "H-...",
  "role": "worker",
  "parts": [{"type": "text", "text": "..."}, {"type": "data", "data": {"report_state": "ready"}}],
  "created_at": "...",
  "read_by": ["manager_01"]
}
```

append-only；同一 message_id 只投递一次；结构化字段放 `data`，不塞 summary。

### 6.4 Task 状态

```
pending → delivering → accepted → working
  ├─ waiting / ready / blocked / failed / handback
ready → reviewing → completed
                   └─ changes_requested → working
任何非终态 → canceled（人 stop）
```

terminal 不可变；后续消息新 Task 或明确 reopen。

### 6.5 Ownership 五类消息

| 场景 | owner | 规则 |
| --- | --- | --- |
| 新建请求 | Manager | 未分配前 Manager 拥有 |
| 活跃工单 Thread 后续 | 当前 Worker | 同一 thread_key 直达 Worker |
| 已完成工单 Thread 后续 | 原 Worker（lease） | lease 内归原 Worker；超时/越界 handback |
| 跨工单消息 | 当前 Worker | 只能 handback 一次，带目标/理由 |
| 人的 stop | Manager/人 | stop 优先；Worker 不能自行恢复 |
| Reviewer 反馈 | Reviewer → Worker | Reviewer 拥有 verdict；Worker 拥有 fix；3 轮失败回 Manager |

`thread_key` 用平台线程键；`lease_until` 到期释放；未读回 Manager；handback 必须写 parent。

### 6.6 幂等/超时/恢复

- `handoff_id` = task_id + stage + attempt 的稳定 hash。
- relay key = handoff_id + message_kind；重复只投一次。
- 平台事件 id 作为外部幂等键；没有就拒绝自动 intake。
- delivery 失败退避；Worker 死亡→Assignment failed，Task 不失败，新 Assignment 带 recovery note。
- ownership lease 到期→释放 owner，未读回 Manager，不自动开新单。
- Reviewer 3 轮 fail→handback Manager，Task blocked。

## 7. 迁移与验收

迁移：

1. 新增 `delegation_tasks`、`handoffs`、`handoff_messages`；`a2a_tasks` 只读兼容。
2. 双写；读路径逐步切换；SSE 带 handoff_id/message_id。
3. 停止覆盖式 update；保留历史查询。

验收：

1. 首次 Manager→Worker：new session 收到 envelope + role prompt。
2. 首次 Worker→Reviewer：new/fork 收到 review envelope；verdict 追加为 artifact。
3. Worker 死亡：fail 反馈重投到新 session。
4. 同一 PR 两条评论：同一 owner，不重复开单。
5. 跨工单评论：handback 一次，目标正确。
6. 人 stop：Task canceled。
7. 重复 relay：只投一次。
8. 跨 harness：context pack 包含 PRD/pre-tests/artifact/verdict。

## 8. 未解

- `thread_key` 由 issue-sync 还是 scan 维护？
- 双写期间谁是 state 真相？
- lease 默认多长、按角色是否不同？
- A2A 外部 Task 与内部 Task 的 ID 映射是否暴露给用户？
