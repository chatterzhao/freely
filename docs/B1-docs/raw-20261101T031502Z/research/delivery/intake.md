---
analysis_id: INTAKE-20261101T031502Z
phase_state: research_closed
created_at: 2026-11-01
---

# 讨论入口与事件准入（C-F）

## 0. 结论

主意图要求 scan 监控 **issue、issue 讨论、freely chat**。当前只做到 issue body + chat；issue comment/PR review/CI 没有进入 runtime。

推荐：

1. **保留 scan 的生命周期判断**（stage/next_action）。
2. 新增 **append-only `events` 表** 存增量事件，scan/Manager 消费。
3. 事件先过**权威 gate**（来源/actor/bot/explicit），价值判断仍归 B1。
4. 平台 adapter 补 actor/comment/review/CI 字段；没有 event_id 就不自动 intake。
5. 不用 webhook 起步；先用轮询 + event_id 去重，后续可换 Source。

## 1. 六类来源

| source | 事件 | 当前可得 | 缺口 |
| --- | --- | --- | --- |
| `issue` | 新建/更新 issue body | `list_open_issue_records`：number/title/body/state；`fetch_issue`：title/body/dates/labels/state/comments[body] | 无 author/association、无 issue event id |
| `issue_comment` | issue 讨论评论 | `fetch_issue.comments[body]` | 无 comment id、author、created_at、association；scan 不消费 |
| `pr_review_comment` | 行内 review 评论 | 无 adapter 方法 | 无 id/author/path/line/thread |
| `pr_review` | approve/request changes/comment | 无 adapter 方法 | 无 review id/state/author/commit |
| `ci` | check run / status | 无 adapter 方法 | 无 check id/name/conclusion/head_sha |
| `chat` | `freely chat` 插话 | `chats`：id/chat_type/issue_id/author/message/created_at | chat 已有；需统一 event_id/thread_key |

## 2. Event schema

```json
{
  "event_id": "github:issue_comment:123456789",
  "source": "issue_comment",
  "source_event_id": "123456789",
  "thread_key": "github:owner/repo#4110",
  "subject": {"kind": "issue", "id": "4110", "raw_key": "20261101T031502Z"},
  "actor": {"id": "123", "login": "alice", "association": "MEMBER", "is_bot": false},
  "kind": "comment.created",
  "body_ref": "events/2026/.../123456789.md",
  "body_preview": "…",
  "created_at": "2026-11-01T...",
  "addressed": true,
  "strength": "explicit",
  "dedupe_hash": "sha256(...)"
}
```

规则：

- `event_id` 全局稳定，重复拉取只写一次。
- `thread_key` 是所有权键：issue/PR 用 `platform:repo#number`；chat 用 `chat:conversation_id`。
- `actor` 必须有平台账号/id；没有就 `unknown`，不能自动 intake。
- `addressed`：明确 @agent、assignee、label、回复 bot；否则 `false`。
- `strength`：explicit（明确请求）/ inferred（规则推断）；inferred 只能 observe 或 B1 判断。
- `body_ref` 存全文，preview 进 prompt；不要把长评论全塞 Manager。

## 3. 准入

放在 **intake 边界**，只做权威判断：

| 判断 | 规则 | 失败 |
| --- | --- | --- |
| source enabled | 项目配置允许该 source | 记录 `source_disabled` |
| actor allowed | allowlist / team member / owner | 记录 `actor_not_allowed` |
| bot policy | bot 只能 inferred 或拒绝 | 记录 `bot_filtered` |
| addressed | 明确 @/assignee/label | inferred/observe |
| dedupe | event_id 已存在 | 丢弃 |
| rate/loop | 同一 actor/线程短时间重复 | 合并/冷却 |

不在这里判断“值不值得做”；B1 仍负责价值/边界。

数据前提：当前 adapter 没有 author/comment id/PR review/CI 字段。必须先补，否则只能做来源级粗判，不能做 actor 级准入。

## 4. scan / 事件流选型

### Option A：扩展 scan 每轮拉评论

- 优点：改动少，复用现有 scan。
- 缺点：评论/CI 量大，scan 变慢；容易重复；没有增量游标。

### Option B：webhook 事件流

- 优点：实时、事件级。
- 缺点：需要公网/回调/签名/重放；Freely 本地 runtime 不适合起步。

### Option C（推荐）：scan 生命周期 + events 增量表

```
platform adapter poll (issue/comment/review/CI/chat)
  → normalize event → events table (event_id unique)
  → admission gate (source/actor/bot/addressed)
  → scan reads unread events + lifecycle docs
  → Manager sees event summary + stage/next_action
```

- 保留 scan 的 stage 判断。
- events 表提供增量、幂等、未读/已读。
- 轮询间隔可按 source 配置；CI 只在状态变化时写事件。
- 后续可把 poll 换成 Source/webhook，不改 events 消费端。

## 5. Adapter 要补的接口

```python
list_issue_comments(issue_number) -> [{id, author, association, body, created_at, updated_at}]
list_pr_reviews(pr_number) -> [{id, author, state, body, commit_id, submitted_at}]
list_pr_review_comments(pr_number) -> [{id, author, body, path, line, created_at, in_reply_to_id}]
list_ci_checks(pr_number) -> [{id, name, status, conclusion, head_sha, completed_at}]
```

- GitHub: `gh issue view --json comments`、`gh pr view --json reviews,comments`、`gh pr checks --json`。
- Gitee: 对应 API；没有的字段标 `unknown`，不伪造。
- 所有列表返回稳定 id；没有 id 的来源不能自动 intake。

## 6. Thread/owner 映射

| source | thread_key | owner 初始 |
| --- | --- | --- |
| issue | `github:repo#4110` | Manager → B1 |
| issue_comment | 同 issue | 当前 Worker（若有）否则 Manager |
| pr_review_comment | `github:repo#pr:4110` | PR Worker |
| pr_review | 同 PR | PR Worker |
| ci | 同 PR | PR Worker |
| chat | `chat:conversation_id` | Manager 路由 |

后续消息归属按 `handoff.md` 的 ownership 规则；C-F 只负责“事件进来”。

## 7. 回放结果（2026-11-01）

已跑只读 spike：`research/ops/replay/intake_replay.py`。

- 真实 issue comment：`chatterzhao/freely#4070` 的 2 条评论（`IC_kw...`，author/association/createdAt）。
- 真实 PR review：`cli/cli#14879` 的 `APPROVED` review（`PRR_kw...`，author/commit/submittedAt）。
- 真实 CI check：同 PR 的 `build (macos-latest)` `SUCCESS`（job id）。
- chat：fixture（格式与 `chats` 表一致）。
- 输入 10 行（5 事件 × 2 次），SQLite `event_id` 唯一后存 **5 行**，`dedupe_ok=true`。
- 线程分组：issue 4070 两条、PR 14879 两条、chat 一条。

结论：event schema/幂等可运行；PR review/CI 的真实字段形状可用。**adapter 方法仍未实现**，所以“进入 scan/queue”是 B2 实现验收，不是本文能关闭的。

## 8. 验收映射（C-F）

| acceptance | 关闭证据 |
| --- | --- |
| 六类来源入口/event_id/thread_key/actor/去重 | 本文 schema + adapter 接口 + 回放日志 |
| issue comment/PR review 进入 scan/queue | adapter 方法 + events 表 + scan 读取测试（B2） |
| CI 进入 | adapter `list_ci_checks` + 事件测试 |
| 重复拉取不重复任务 | event_id unique + 双写回放 |

## 9. 未解

- 轮询间隔/速率限制；CI 事件是否只取 fail→success 变化。
- Gitee 字段缺失时是否降级为 `unknown`/需要人工。
- events 表保留多久、如何归档。
- 事件 body 存文件还是 DB；隐私/凭据过滤。
- 是否把 chat 也统一成 event（建议是）。
