# Brainstorm — Chat Inbox SQLite 架构

## 为什么需要 chat-inbox

`freely chat --new-issue` / `--issue <id>` 是人机插话入口。
插话发生时，还没有对应的 feature worktree——工位是 daemon 后续根据 scan 结果才创建的。

如果 chat 直接写入 `docs/issues/`，文件就落在当前分支上。
daemon 运行在 develop（protected branch），每次插话都在污染受保护分支。

所以需要一个**暂存区**：chat 先落地到 git-ignored 的 SQLite，
等 scan 消费后，再搬迁到 worktree 的 `docs/issues/` 下进入 Git 跟踪。

```
chat → .freely/chat-inbox.db (git-ignored, 暂存)
     → task-source-scan 消费
     → worktree/docs/issues/ (git 跟踪, canonical)
     → issue-sync → GitHub/Gitee 平台 issue
```

`docs/issues/` 是 canonical 真相源的原因：
- Git 跟踪，门禁可审计
- AI agent 直接读文件，命中 prompt cache，无需 API/CLI 调用
- 平台 issue 是从这里 sync 出去的副本

## ID 设计

纯 UTC 时间戳 `YYYYMMDDHHMMSS`，如 `20260429204530`。

- 直接用 UTC，不翻译、不组合、不做时区转换
- 永不重复（同一秒内两次插话概率极低，INSERT OR IGNORE +1s 重试即可）
- DB 内无前缀。`raw-` / `chat-` 前缀是 scan 消费时根据 `chat_type` 组装的展示层逻辑

## SQLite Schema

```sql
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY,              -- UTC YYYYMMDDHHMMSS
    chat_type TEXT NOT NULL,             -- 'new-issue' | 'issue-id:raw-xxx' | 'issue-id:I-xxx'
    author TEXT NOT NULL DEFAULT 'human',
    channel TEXT NOT NULL DEFAULT 'chat',
    message TEXT NOT NULL,
    consumed INTEGER NOT NULL DEFAULT 0, -- 0=未消费, 1=已消费
    created_at TEXT NOT NULL,
    session_refs TEXT DEFAULT '[]',
    intake_id TEXT,
    materialized_as TEXT                 -- 消费后产物引用（issue ID 或 worktree 路径）
);

CREATE INDEX IF NOT EXISTS idx_consumed ON chats(consumed);
```

- `id` 纯 UTC 时间戳，无时区歧义
- `consumed` 整数 0/1，`WHERE consumed=0` 索引扫描
- `materialized_as` 记录消费产物，用于审计追踪

## 写入（freely chat）

```
freely chat --new-issue "消息"
  → INSERT INTO chats (id={UTC_TS}, chat_type='new-issue', message='...')
  → develop 零文件变更 ✓

freely chat --issue raw-20260401-1200 "评论"
  → INSERT INTO chats (id={UTC_TS}, chat_type='issue-id:raw-20260401-1200', ...)
  → develop 零文件变更 ✓
```

## 消费（task-source-scan.py）

```
SELECT * FROM chats WHERE consumed=0 ORDER BY id ASC LIMIT 50

对每条 pending：

  chat_type='new-issue'
    → 组装 source_ref = "intake://raw-{id}"
    → source_type='chat_intake', restart_point='pre_brainstorm'
    → next_action='Create worktree, materialize as docs/issues/raw-{id}/issue.md'
    → UPDATE consumed=1

  chat_type='issue-id:raw-xxx'
    → 查找 docs/issues/raw-xxx/issue.md
       ├─ 找到且未关闭
       │    → source_type='chat_comment'
       │    → next_action='Append comment to raw-xxx'
       │    → UPDATE consumed=1
       │
       ├─ status=absorbed → 读 absorbed_into → 重定向到 I-*
       │    → 追加 comment 到 I-* issue
       │    → UPDATE consumed=1, materialized_as='{I-*}'
       │
       └─ 未找到或已关闭
            → source_type='chat_orphan'
            → UPDATE consumed=1（避免死循环扫描）

  chat_type='issue-id:I-xxx'
    → 同上逻辑
```

## 消费后的完整链路

```
chat-inbox.db (consumed=1)
     ↓ AI agent 读 scan JSON，创建 worktree
worktree/docs/issues/raw-{id}/issue.md  (git 跟踪)
     ↓ AI agent B1_IBM → B2_IBM → merge to develop
develop/docs/issues/I-{id}-A/issue.md   (canonical)
     ↓ issue-sync
GitHub/Gitee platform issue              (外部同步)
```

## 角色边界

| 组件 | 职责 | 接触什么 |
|------|------|---------|
| `freely chat` | 写入 chat 记录 | SQLite |
| `task-source-scan` | 消费 + 标记 + 组装 source | SQLite + docs/issues/ |
| AI agent | 读 scan JSON，创建 worktree，B1_IBM | scan JSON + docs/issues/ |
| `issue-sync` | 本地→平台同步 | docs/issues/ |

AI 完全不接触 SQLite。它只读 `docs/issues/` 下的文件——直接文件读取，命中 prompt cache，不经过 API 或 CLI。

## 旧 intake 不迁移

`.freely/intake/` 231 条全部 absorbed/dropped。保留不动。
