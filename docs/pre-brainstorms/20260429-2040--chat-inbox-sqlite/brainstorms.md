# Brainstorm — Chat Inbox SQLite 架构

## 问题

`freely chat` 直接写 `docs/issues/` 污染 develop（protected branch）。

## 核心约束

**每个工位必须对应一个 issue。** 没有 issue 就不能创建工位。
`wt-create` 提取 key，查 chat-inbox + docs/issues/，找不到就拒绝。

## SQLite Schema

两个参数（`--new-issue` / `--issue xx`）都指向一个 issue，统一存为 `issue_id`：

```sql
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY,              -- UTC YYYYMMDDHHMMSS
    chat_type TEXT NOT NULL,             -- 'new-issue' | 'comment'
    issue_id TEXT NOT NULL,              -- 'raw-{id}' | 'raw-xxx' | 'I-xxx-X'
    author TEXT NOT NULL DEFAULT 'human',
    channel TEXT NOT NULL DEFAULT 'chat',
    message TEXT NOT NULL,
    consumed INTEGER NOT NULL DEFAULT 0,
    session_refs TEXT DEFAULT '[]',
    intake_id TEXT,
    materialized_as TEXT
);
CREATE INDEX IF NOT EXISTS idx_consumed ON chats(consumed);
CREATE INDEX IF NOT EXISTS idx_issue_id ON chats(issue_id);
```

### 字段说明

| 字段 | `--new-issue` | `--issue raw-xxx` | `--issue I-xxx` |
|------|--------------|-------------------|-----------------|
| `id` | `20260429204530` | `20260429204531` | `20260429204532` |
| `chat_type` | `new-issue` | `comment` | `comment` |
| `issue_id` | `raw-20260429204530` | `raw-xxx` | `I-xxx` |

- `id` 永远是本条 chat 的 UTC 时间戳
- `issue_id` 是目标 issue，`--new-issue` 时 = `raw-{id}`（即将创建的），`--issue` 时 = 参数值
- `idx_issue_id` 让 wt-create 和 scan 能快速按 issue 查所有相关 chat

## 写入

```
freely chat --new-issue "msg"
  → INSERT (id={ts}, chat_type='new-issue', issue_id='raw-{ts}', ...)
  → touch intake.pending

freely chat --issue raw-xxx "评论"
  → INSERT (id={ts}, chat_type='comment', issue_id='raw-xxx', ...)
  → touch intake.pending
```

## wt-create 关卡（new-issue 消费）

```
wt-create feature/raw-{ts}-{slug} --base develop
  → 提取 key = raw-{ts}

  → 查 chat-inbox:
      SELECT * WHERE id={ts} AND chat_type='new-issue' AND consumed=0
      ├─ 找到 → materialize
      │    → worktree/docs/issues/raw-{ts}/issue.md
      │    → UPDATE consumed=1, materialized_as='raw-{ts}'
      │    → 继续创建 ✓
      │
      └─ 未找到 → 查 docs/issues/raw-{ts}/
           ├─ 找到 → 已有 issue，继续创建 ✓
           └─ 未找到 → BLOCK

  → 顺便处理该 issue 的评论:
      SELECT * WHERE issue_id='raw-{ts}' AND chat_type='comment' AND consumed=0
      → 追加到 worktree/docs/issues/raw-{ts}/issue.md 的 Comments
      → UPDATE consumed=1
```

## scan 消费评论（无工位时）

scan 处理 `chat_type='comment'` 且 `consumed=0` 的条目：

```
SELECT * WHERE chat_type='comment' AND consumed=0

  → find worktrees-root/*{issue_id}*
     ├─ 找到工位 → AI 在 worktree 内追加
     │            → AI 调 chat-inbox consume
     │
     └─ 未找到 → 查 docs/issues/{issue_id}/
          ├─ raw-* 被 absorb → 递归查 I-* 的工位
          └─ 未找到/已关闭 → chat_orphan, mark consumed=1
```

## 完整链路

```
freely chat --new-issue "msg"
  → DB: (id={ts}, chat_type='new-issue', issue_id='raw-{ts}')
  → scan 放入 sources（consumed=0，AI 去重）
  → AI: wt-create feature/raw-{ts}-fix
       → wt-create 查 DB → 找到 → materialize → mark consumed=1
       → worktree/docs/issues/raw-{ts}/issue.md

freely chat --issue raw-xxx "评论"
  → DB: (id={ts2}, chat_type='comment', issue_id='raw-xxx')
  → scan: find worktree/*raw-xxx*
     ├─ 找到 → AI 在 worktree 内追加 → mark consumed=1
     └─ 未找到 → orphan, mark consumed=1
```

## 重构范围

### 新增
`chat-inbox.py` — init / add / query_by_issue / consume

### 修改
| 位置 | 改动 |
|------|------|
| `freely init` | 调 `chat-inbox init` |
| `_write_chat_to_issue` | `chat-inbox add`（chat_type + issue_id）|
| `wt-create` / `worktree-common.sh` | 提取 key，查 DB + docs/issues/ 关卡 |
| `task-source-scan.py` | 新增 `scan_chat_inbox()`（评论路由）|

### 不变
`freely chat` CLI、`scan_raw_issues`、`governance-merge-gate`、`issue-sync`、B1→B2
