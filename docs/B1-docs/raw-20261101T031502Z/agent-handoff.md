---
analysis_id: HANDOFF-20261101T031502Z
phase_state: in_progress
created_at: 2026-11-01
---

# Manager/Worker/Reviewer 交接：是协议缺陷还是实现缺陷

## 0. 结论

**两者都有，但首先是“协议层选错了抽象”。**

- Freely 的 Manager/Worker/Reviewer 是**同一项目内的领导—员工—独立评审**关系，不是 A2A 的“跨组织、黑盒远程 Agent”关系。
- 最接近的参考不是 AHP/ACP，而是 Super-agent 的 **Router → Worker + Report/Attention/ownership/handback**。AHP/ACP 是 host/client 与 agent 的通信层；A2A 是 agent-to-agent 的任务层，但 Freely 只实现了它的一层皮。
- Freely 当前所谓 A2A 实际是一个 **SQLite task 表 + 自定义 REST + SSE**：只有 task state 是 A2A 名字，没有 contextId/messageId/artifact 历史，也没有 task immutability。
- 在这个薄协议上，交接只能靠一个 `message`/`summary` 字段；Manager、Worker、Reviewer 反复覆盖同一行，后续消息没有 owner。这是结构性的。
- 另外有一个**确定的实现缺陷**：`acp_session_connect()` 在 `session/new` / `session/fork` 路径**不发送传入的 message**；只有已存活 session 的 `session/prompt` 和 `session/resume` 会发。首次 Reviewer 交接、Worker 死亡后的 fail 反馈，消息可能直接丢。
- 还有一个**契约矛盾**：`reviewer-agent.md` 禁止 Reviewer 调 `a2a-exit`，但 watchdog 的 review task message 明确让 Reviewer “调 a2a-exit 声明 verdict”。

所以：不是“A2A 协议不好”，而是 Freely 用了 A2A 的外壳，却没有 A2A 的 message/context/artifact 语义；同时内部角色关系更像 DSH 的 Router/Worker 领导 delegation。

## 1. Freely 当前交接的实际数据模型

`freely.db` 的 `a2a_tasks` 列：

```
id, task_id, name, description, state, agent_id, skill, session_id,
message, raw_key, prompt_file, worktree, branch, exit_kind, reason,
progress, next_action, completion_summary, evidence_paths, worker_prompts_csv
```

没有：

- `context_id`
- `message_id`
- `artifacts` / `artifact_id`
- 消息历史表
- `parent_task_id` / `handoff_id`
- `owner` / `followup_owner`
- 读/未读状态

这意味着：

1. 一个 Task 只有一条 `message`，后续 `summary/reason/next_action` 更新会覆盖它。
2. Manager 派工、Worker 阶段汇报、Reviewer verdict 都写同一行；谁拥有后续消息没有记录。
3. 没有 artifact 版本，Reviewer 的 required_fixes 和 Worker 的 evidence 只能覆盖 `evidence_paths`。
4. 没有 contextId，无法把“同一 issue 的多轮审查”组织成可追溯上下文。
5. `state` 是唯一的状态真相；但 task 行可以被任意 `update`，没有 terminal 不可变约束。

## 2. “A2A”实现的协议偏差

`a2a_server.py` 的真实行为：

- 提供自定义 REST：`POST /tasks`、`PATCH /tasks/{id}`、`GET /tasks`、`/tasks/{id}/messages`，不是官方 A2A 的 `SendMessage`/`GetTask`/`SubscribeToTask` JSON-RPC。
- 收到官方 SDK 的 A2A 请求时，`FreelyAgentExecutor.execute()`：
  - 生成一个**外部** A2A `task_id`；
  - 在本地 SQLite 里创建另一个**内部** task id；
  - 通过 artifact 告诉调用方 `internal_task_id=...`；
  - 对外立刻发 `COMPLETED`（“task creation is complete”），而内部 task 实际是 `submitted`。
- 因此外部观察者看到“任务已完成”，内部还在跑；task id 也有两套。这是审计/交接的根因之一。
- `a2a_types.py` 定义了 `Message.messageId/contextId/Artifact`，但 `a2a_tasks` 表没有持久化它们；类型层和存储层脱节。

结论：**这不是 A2A 协议实现，而是“A2A 命名的本地任务总线”**。如果只做本地角色交接，这层自定义并不必然错；但它缺少内部 delegation 需要的 ownership/message/artifact，而 A2A 的远程语义又没有真正实现。

## 3. 跨 harness 交接的确定缺陷

`agent_working.acp_session_connect()` 的分支：

| 分支 | 是否发送 `message` | 结果 |
| --- | --- | --- |
| 已有 session alive → `session/prompt` | 是 | 正常 |
| `session/resume` + prompt | 是 | 正常 |
| `session/fork` | **否** | Reviewer/Worker 新 fork 的 session 收不到 task_msg |
| `session/new`（含跨 tool） | **否** | 新 session 收不到 task_msg |
| `force_new` | **否** | gate Reviewer 收不到 task_msg |

`watchdog_sse._handle_needs_reviewer()` 传入 `message=task_msg`，但首次 Reviewer 通常是 `session/new` 或 `session/fork`，于是 task_msg 被丢弃。`_handle_needs_worker()` 的 fail 反馈同理：如果 Worker session 已死、需要 new，verdict 消息也会丢。

另外，`acp-bridge.session_new()` 只传 `cwd/mcpServers`，`session/fork` 只传 `sessionId/role/agentId`；**新 session 不会自动加载 Reviewer/Worker 角色定义**。因此“新建 session + 丢 task_msg”可能让 Reviewer 既没有角色 prompt，也没有审查任务。

## 4. Reviewer 契约矛盾

- `reviewer-agent.md`：`不用 a2a_task.py / a2a-exit（Manager 专属）`。
- `watchdog_sse._build_review_task_message()`：`请根据 Skill 指令进行审查，完成后调 a2a-exit 声明 verdict。`
- `freely-tdd-review` 输出格式是 JSON verdict（pass/fail + required_fixes），没有说用 `a2a-exit`。

三条说法不一致。Reviewer 到底用 JSON block、`a2a-exit`、还是 SSE metadata？没有单一契约。这会让 Reviewer 的 verdict 落在不同地方，Manager/Worker 读到的东西不一致。

## 5. 对照 Super-agent 的 Router/Worker

Super-agent 的 delegation 不是“远程 A2A”，而是**同一个 runtime 内的领导 delegation**：

- Router 拥有 Ticket、Decision、Policy、对外回复；Worker 拥有执行。
- Worker 通过 **Report**（progress/waiting/ready/blocked/failed/dropped）汇报，不是改一行 `state`。
- 需要人决策时用 **Attention**：单问题、目标会话、`human_action`、`question_for_trigger_id`。
- 后续消息有 **followupOwners**；Worker 可 **handback**；未读 Input 在 Assignment 结束时重投。
- Assignment 有 pending/running/ended，Ticket 状态独立于 Executor 状态。
- “A person's message that reaches a Ticket stays with that Ticket; every other Trigger enters Eval” 是明确的 ownership 规则。

这正是 Freely 缺的：**Task 状态 ≠ 消息归属 ≠ 执行者状态**。Freely 把三者压进一行 `a2a_tasks`，所以 Review/Worker/Manager 互相覆盖。

## 6. 对照 A2A / AHP / ACP

| 协议 | 解决什么 | 是不是领导 delegation | 对 Freely 的用法 |
| --- | --- | --- | --- |
| ACP | 单 client ↔ 单 agent：session/prompt、工具、权限 | 否，通信层 | harness 传输；不能承载 Manager/Worker 语义 |
| AHP | N client ↔ host：共享 session 状态、actions、重连 | 否，host/UI 协调层 | 可用于 DSH panel/多端查看，不用于角色交接 |
| A2A | agent ↔ agent：Task/Message/Artifact/contextId，面向不透明远程 Agent | 部分，跨组织任务协议 | 可做外部互操作；内部 delegation 不应只靠它 |
| DSH Router/Worker | 单 runtime 内领导 delegation：Ticket/Assignment/Report/Attention/ownership | **是** | 最值得参考 |

结论：**Freely 的 Manager/Worker/Reviewer 更接近 DSH 的 Router/Worker，不是 AHP/ACP；A2A 是跨 Agent 的任务协议，不是团队内部交接的完整模型。** 可以继续用 A2A 作为外部线格式，但内部应有一层 delegation contract。

补充 AHP 的定位：AHP 是“N 个 client ↔ 一个 host 的 session 状态同步”，核心是 channels、immutable state tree、action 序列、write-ahead reconciliation、断线重连；它明确不管 agent 实现、模型路由、工具定义，也不管 agent-to-agent 通信（官方 “What AHP Does Not Do”）。因此 AHP 适合 Freely 的 **多端 panel/观察面**，不适合 Manager/Worker/Reviewer 的任务交接。

ACP 的定位：单 client ↔ 单 agent 的初始化、prompt、流式更新、工具调用、权限；它是 Freely 的 harness 传输层，不是 delegation 层。


## 7. 建议的最小修法（研究结论，不是实现）

### 7.1 先修确定的 bug

1. `acp_session_connect()` 在 `session/new` / `session/fork` / `force_new` 成功后，如果有 `message`，显式 `session/prompt`。
2. `session/new` 时注入角色定义（manager/worker/reviewer agent prompt）或由调用方在首条 prompt 带上。
3. 统一 Reviewer 契约：只允许一种 verdict 写回方式（建议结构化 JSON → runtime 写 A2A message/artifact，不让 Reviewer 直接改 task）。
4. A2A server 对外的 task 状态不要“创建即 COMPLETED”；internal/external task id 只保留一个映射，并在 API 返回。

### 7.2 再把交接升级成 delegation contract

新增 append-only `handoffs` / `handoff_messages` 表，字段至少：

```
handoff_id, task_id, parent_handoff_id,
from_role, to_role, from_agent, to_agent,
intent, constraints, acceptance, artifacts,
context_refs, session_id, expected_output,
ownership, status, created_at
```

规则：

- 每次 role 交接写一条新 handoff，不覆盖旧 message。
- 消息只追加，不 update；task state 只由明确 transition 改。
- Reviewer verdict 作为 artifact/message 追加，不直接改 Worker 的 summary。
- `owner` 决定后续消息归谁；handback 明确转移 ownership。
- 跨 harness 时，handoff 必须带 context pack（文档路径 + artifacts + 上一轮 verdict），不能只靠 session fork。

### 7.3 与 DSH 的对应

| Freely 概念 | DSH 参考 |
| --- | --- |
| Manager | Router/main Session |
| Worker | Executor Session/Assignment |
| Reviewer | 独立 Session + 结构化 verdict（DSH 无内建 Reviewer） |
| A2A task state | Ticket state + Assignment state 分离 |
| `message` | Report/Input/Message |
| `input-required` | Report waiting/blocked + Attention |
| Worker 完成 | ready/blocked/failed report |
| 后续消息 | followupOwners + handback |
| 死信/重试 | unread Input 重投 + recovery note |

## 8. 未解

- Freely 是否要保留 A2A 线格式，还是内部完全改成 handoff envelope？
- Reviewer 是否应该成为 DSH 的独立角色/preset，还是只是 Worker 的一个 review skill？
- 同一 harness 的 session/fork 能继承多少上下文？跨 harness 必须显式 context pack 的边界在哪？
- `a2a_tasks` 迁移到 append-only 后，现有 Manager/SSE/scan 查询怎么兼容？

## 9. 参考来源

- A2A Core Concepts: https://a2a-protocol.org/latest/topics/key-concepts/
- A2A Life of a Task: https://a2a-protocol.org/latest/topics/life-of-a-task/
- A2A Specification: https://a2a-protocol.org/latest/specification/
- AHP What is AHP: https://microsoft.github.io/agent-host-protocol/guide/what-is-ahp.html
- AHP and ACP: https://microsoft.github.io/agent-host-protocol/guide/ahp-and-acp.html
- ACP: https://agentclientprotocol.com/
- DSH prototype: https://github.com/deepseek-ai/dsh-superagent-prototype @ 6337fc823ce20251c8de8085948165c81aaa701e
- DSH handoff prompts: `prompts/handoff.md`、`prompts/handoff-orchestrator.md`、`prompts/handoff-worker.md`
- DSH execution/report states: `docs/003-execution.md`
