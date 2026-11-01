# PRD：讨论入口 + 消息级 handoff（I-F / I-B）

## 1. Goal

让 Freely 的“讨论 → 工单 → 执行 → 交接”闭环成立：

1. issue comment / PR review / CI / chat 能进入 scan/Manager。
2. 事件先归一化、幂等、过权威准入。
3. Task / Handoff / Message 分离；后续消息有 owner；跨工单 handback 一次。
4. new/fork session 不再丢 task message；Reviewer verdict 契约统一。

## 2. 非目标

- 不做 webhook/Source 基础设施；轮询 + event_id 去重。
- 不做完整 A2A RPC/事件溯源。
- 不重写 `freely` 20K 行单体；新增模块 + 最小接线。
- 不做 UI；先让 runtime/CLI 可用。

## 3. 架构

```
platform-adapter (issue/comment/review/CI/chat)
  → discussion_events.normalize()
  → SQLite discussion_events (event_id PK)
  → admission (source/actor/bot/addressed/dedupe)
  → scan summary (unread events)
  → Manager prompt

A2A task / delegation
  → handoff_store (delegation_tasks/handoffs/handoff_messages)
  → acp_session_connect (new/fork + prompt)
  → Reviewer verdict
```

## 4. 事件模型

表 `discussion_events`：

| 列 | 类型 | 说明 |
| --- | --- | --- |
| event_id | TEXT PK | `{source}:{source_event_id}` |
| source | TEXT | issue/issue_comment/pr_review_comment/pr_review/ci/chat |
| source_event_id | TEXT | 平台 id |
| thread_key | TEXT | issue/PR/chat 线程键 |
| subject_kind/subject_id | TEXT | issue/pr/chat |
| raw_key | TEXT | 可选 |
| actor_login/actor_id/actor_association/actor_is_bot | TEXT/INT | 准入 |
| kind | TEXT | comment.created/review.approved/ci.failed/chat.message |
| body_ref | TEXT | 全文路径；可空 |
| body_preview | TEXT | ≤500 字 |
| created_at | TEXT | ISO |
| addressed | INT | 明确 @/assignee/label |
| strength | TEXT | explicit/inferred |
| disposition | TEXT | accept/observe/ignore/unavailable |
| disposition_reason | TEXT | 可追溯 |
| read_at | TEXT | NULL=unread |

索引：`(thread_key, created_at)`、`(read_at)`、`(source)`。

## 5. Adapter 接口

```python
list_issue_comments(issue_number) -> list[dict]
list_pr_reviews(pr_number) -> list[dict]
list_pr_review_comments(pr_number) -> list[dict]
list_ci_checks(pr_number) -> list[dict]
```

- GitHub 用 `gh issue view --json comments`、`gh pr view --json reviews,comments`、`gh pr checks --json`。
- Gitee 不支持的返回 `[]` + `unsupported` 标记，不伪造。
- 所有 id 稳定；缺 id 的来源不自动 intake。

## 6. 准入

- source enabled；actor allowlist/owner/member；bot 只能 inferred/ignore；addressed；dedupe；rate/loop。
- 结果写 `disposition/reason`；`observe` 也入库但不进 Manager 任务池。
- unknown actor → observe，不自动开工。

## 7. Handoff 模型

表：

- `delegation_tasks(task_id PK, thread_key, state, owner, lease_until, handback_done, created_at, updated_at)`
- `handoffs(handoff_id PK, task_id, parent_handoff_id, from_role, to_role, from_agent, to_agent, intent, artifacts_json, context_refs_json, expected_output, status, created_at)`
- `handoff_messages(message_id PK, handoff_id, role, parts_json, created_at, read_by_json)`

规则：

- terminal 不可变；后续消息新 Task 或显式 reopen。
- `ownership` lease；过期回 Manager。
- handback 一次；`parent_handoff_id` 必填。
- relay key = handoff_id + message_kind；重复只投一次。

## 8. new/fork 修复

`agent_working.acp_session_connect()`：

- `session/new` / `session/fork` 成功后，必须发 `session/prompt`，内容 = task message + 角色 prompt（最小）。
- 失败要回滚/报错，不能静默创建空 session。
- 保持 resume/prompt 现有路径不变。

Reviewer 契约：

- `reviewer-agent.md` 改为允许 `a2a-exit --state completed --summary <verdict-json>`。
- `watchdog_sse._build_review_task_message()` 改成同一指令。
- `freely-tdd-review` JSON 作为 summary 内容；Manager 解析失败时 fallback 原文 + needs_human。

## 9. scan 接线

- `task-lifecycle-scan.py` 调 `discussion_events.collect(project)`；输出 `events: {unread, by_source, latest}`。
- Manager prompt 增加“未读讨论事件”段（只 preview + thread_key）。
- 没有事件时输出空数组，不改变现有 scan JSON 结构。

## 10. 迁移

- 新表 additive；`a2a_tasks` 双写（新表权威，旧表镜像）。
- 旧查询继续可用；SSE 事件带 `handoff_id/message_id`（可选）。
- 回滚：停止写新表，旧表仍可用；新表保留审计。

## 11. 验收映射

- C-F：`test-discussion-events.py`（schema/dedupe/actor/thread）+ scan integration + real fixture。
- C-B：`test-handoff-store.py`（owner/handback/terminal/lease）+ new/fork prompt test + Reviewer contract test。
- 真实环境：scan 在测试项目读到真实 issue comment；new/fork 用 mock ACP 验证 prompt。

## 12. 风险

- 平台字段缺失 → unknown/observe。
- 双写不一致 → 新表写权威，旧表 best-effort + 日志。
- 角色 prompt 注入不完整 → 先随 message；后续 preset。
- Reviewer summary JSON 解析失败 → fallback + needs_human。
