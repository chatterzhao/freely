# Brainstorm — Chat Inbox SQLite 架构

## 问题

`freely chat --new-issue` / `--issue <id>` 直接写入 `docs/issues/`，污染 protected branch。
之前 `.freely/intake/` 用文件系统，扫描慢、格式不一致。

## 设计决策

### ID：纯 UTC 时间戳

- 数据库 `id` = UTC 时间戳（如 `20260429204530`），永远唯一，无时区问题
- 前缀（`raw-` / `chat-`）是 scan 时根据 `chat_type` 组装的展示层逻辑，不存数据库

### 状态：布尔 consumed

- `consumed INTEGER DEFAULT 0` — 0=未消费，1=已消费
- 写入默认 0，被消费后改 1
- `WHERE consumed=0` 是简单整数索引扫描，比字符串快

### 角色边界：全部脚本化

- `freely chat` 写入 SQLite（脚本）
- `task-source-scan.py` 读取 SQLite + 消费 + 标记（脚本）
- AI agent 只消费 scan JSON 结果，不直接接触 SQLite

## SQLite Schema

```sql
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY,              -- UTC timestamp YYYYMMDDHHMMSS
    chat_type TEXT NOT NULL,             -- 'new-issue' | 'issue-id:raw-xxx' | 'issue-id:I-xxx'
    author TEXT NOT NULL DEFAULT 'human',
    channel TEXT NOT NULL DEFAULT 'chat',
    message TEXT NOT NULL,
    consumed INTEGER NOT NULL DEFAULT 0, -- 0=pending, 1=done
    session_refs TEXT DEFAULT '[]',
    created_at TEXT NOT NULL,
    intake_id TEXT,
    materialized_as TEXT                 -- 消费后记录产物引用
);

CREATE INDEX IF NOT EXISTS idx_consumed ON chats(consumed);
```

## 写入流程

```
freely chat --new-issue "消息"
  → INSERT INTO chats (id={ts}, chat_type='new-issue', message='...')
  → develop 零文件变更 ✓

freely chat --issue raw-20260401-1200 "评论"
  → INSERT INTO chats (id={ts}, chat_type='issue-id:raw-20260401-1200', ...)
```

## 消费流程（task-source-scan.py）

```
SELECT * FROM chats WHERE consumed=0 ORDER BY id ASC LIMIT 50

对每条 pending chat：

  chat_type='new-issue'
    → 组装 chat_id = "raw-{id}"
    → 放入 scan JSON sources[]
    → source_type='chat_intake', restart_point='pre_brainstorm'
    → next_action='Create worktree, materialize as docs/issues/raw-{id}/issue.md'
    → UPDATE consumed=1, materialized_as='raw-{id}'

  chat_type='issue-id:raw-xxx'
    → 查找 docs/issues/raw-xxx/issue.md
       ├─ 找到且未关闭 → 组装 chat_id = "chat-{id}"
       │    → source_type='chat_comment', restart_point='continuation'
       │    → next_action='Append comment to raw-xxx'
       │    → UPDATE consumed=1
       │
       ├─ 找到且 status=absorbed → 读取 absorbed_into (I-*)
       │    → 重定向：追加到 I-* issue 的 Comments
       │    → UPDATE consumed=1, materialized_as='{I-*}'
       │
       └─ 未找到或已关闭
            → source_type='chat_orphan'
            → next_action='Target issue closed/missing, AI decides: reopen or drop'
            → UPDATE consumed=1（避免重复扫描）

  chat_type='issue-id:I-xxx'
    → 同上逻辑，查找 docs/issues/I-xxx/issue.md
```

## AI agent 视角

AI 只消费 scan JSON，看到的 source 已经过脚本预处理：

```json
{
  "source_type": "chat_intake",
  "source_ref": "intake://raw-20260429204530",
  "restart_point": "pre_brainstorm",
  "next_action": "Create worktree, materialize as docs/issues/raw-20260429204530/issue.md, then B1_IBM."
}
```

AI 不需要知道 SQLite、chat-inbox 的存在。它拿到的是一个标准的 `discovery` source，按现有流程处理。

## 旧 intake 不迁移

`.freely/intake/` 231 条记录全部为 absorbed/dropped，无 pending。保留不动，新 chat 全部走 SQLite。

## 与现有流程对比

| | 现在 | 改后 |
|---|---|---|
| chat 写入位置 | `docs/issues/` | `.freely/chat-inbox.db` |
| develop 污染 | 是 | 否 |
| 扫描方式 | `iterdir()` + `read_text()` | `SELECT WHERE consumed=0` |
| 扫描复杂度 | O(n) 磁盘 IO | O(log n) 索引 |
| AI 是否感知 | 直接读 issue.md | 只读 scan JSON |
| 消费标记 | canonical_issue_path 非空 | consumed=1 |
