# Brainstorm — Chat Inbox SQLite 架构

## 问题

`freely chat --new-issue` / `--issue <id>` 直接写入 `docs/issues/`，污染 protected branch。
之前 `.freely/intake/` 用文件系统存储，231 条记录已占满，scan 会越来越慢。

## 调研：`docs/issues/` 读写依赖

### 写入方
| 入口 | 位置 | 操作 |
|------|------|------|
| `freely chat --new-issue` | `_write_chat_to_issue` L5494 | 创建 `raw-{ts}/issue.md` |
| `freely chat --issue <id>` | `_write_chat_to_issue` L5442 | 追加 comment |
| `issue-sync` | `bin/issue-sync` | 同步 platform_ids |
| AI agent (B1 promote) | lead-agent | 创建 `I-*` linked issue |

### 读取方
| 入口 | 位置 | 目的 |
|------|------|------|
| `task-source-scan` | `scan_raw_issues` | 扫描未处理 raw issue |
| `task-source-scan` | `scan_linked_issues` | 扫描未读评论 |
| `governance-merge-gate` | GATE 6.2/6.3 | 验证 C/M/I 链 |
| `_route_chat_to_issue` | L5559 | chat 路由匹配 |
| AI agent | lead-agent / context-source-skill | 任务路由 |

## SQLite 方案

### 为什么 SQLite

- 文件系统扫描 231+ 目录：每次 `iterdir()` + `read_text()` + YAML 解析，O(n) 磁盘 IO
- SQLite：`SELECT ... WHERE status='pending' LIMIT 50`，索引查找，O(log n)
- 单个 `.freely/chat-inbox.db` 文件，git-ignored
- Python 标准库自带 `sqlite3`，零依赖

### 表结构

```sql
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT UNIQUE NOT NULL,
    chat_type TEXT NOT NULL,          -- 'new-issue' | 'issue-id:raw-xxx' | 'issue-id:I-xxx'
    author TEXT NOT NULL DEFAULT 'human',
    channel TEXT NOT NULL DEFAULT 'chat',
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    session_refs TEXT DEFAULT '[]',
    created_at TEXT NOT NULL,
    intake_id TEXT,
    claimed_at TEXT,
    materialized_as TEXT,
    error_message TEXT
);

CREATE INDEX IF NOT EXISTS idx_status ON chats(status);
CREATE INDEX IF NOT EXISTS idx_type ON chats(chat_type);
CREATE INDEX IF NOT EXISTS idx_created ON chats(created_at);
```

### Chat 写入流程

```
freely chat --new-issue "消息"
  → INSERT INTO chats (chat_id='raw-{ts}', chat_type='new-issue', ...)
  → develop 无文件变更 ✓

freely chat --issue raw-20260401-1200 "评论"
  → INSERT INTO chats (chat_id='chat-{ts}', chat_type='issue-id:raw-20260401-1200', ...)
  → develop 无文件变更 ✓
```

### Chat 消费流程

```
task-source-scan.py::scan_chat_inbox()
  → SELECT * FROM chats WHERE status='pending' ORDER BY created_at DESC LIMIT 50
  → 返回给 AI agent

AI agent 根据 chat_type 处理：
```

#### 分支 1：`chat_type = 'new-issue'`

```
chat_id = raw-{ts}
  → AI 创建 worktree
  → AI 在 worktree 中创建 docs/issues/raw-{ts}/issue.md
  → UPDATE chats SET status='materialized', materialized_as='raw-{ts}'
  → 继续 B1_IBM 预研
```

#### 分支 2：`chat_type = 'issue-id:raw-{ts}'`

```
target = raw-{ts}
  → 查找 docs/issues/raw-{ts}/issue.md
     ├─ 找到且 status != absorbed/closed
     │    → 追加 comment 到该 issue
     │    → UPDATE chats SET status='delivered'
     │
     ├─ 找到且 status = absorbed（已被 promote 到 I-*）
     │    → 读取 absorbed_into 字段获取 I-* ID
     │    → 追加 comment 到 I-* issue
     │    → UPDATE chats SET status='delivered', materialized_as='{I-*}'
     │
     └─ 未找到，或 status = closed/completed
          → 选项 A: 自动转为 new-issue（创建新 raw issue）
          → 选项 B: 记录 error_message，标记 status='error'
```

#### 分支 3：`chat_type = 'issue-id:I-{ts}'`

```
target = I-{ts}
  → 查找 docs/issues/I-{ts}/issue.md
     ├─ 找到且 phase_state 未完成
     │    → 追加 comment
     │    → UPDATE chats SET status='delivered'
     │
     └─ 未找到或已完成
          → 同分支 2 的 closed 处理
```

### 旧数据迁移

`.freely/intake/` 中 231 条记录，状态全部为 `absorbed` 或 `dropped`。
方案：不迁移到 SQLite（已消费完毕，无 pending 项）。保留旧目录不动，新 chat 全部走 SQLite。

### 索引与性能

- `WHERE status='pending'` — idx_status 覆盖，常数时间
- `ORDER BY created_at DESC` — idx_created 覆盖
- `LIMIT 50` — 只取最近 50 条 pending
- 即使积累 10000 条记录，pending 通常只有个位数

## 待决策

1. **已关闭 issue 的评论处理**：自动转 new-issue 还是标记 error？
2. **materialized 记录清理**：保留多久？定期 VACUUM？
3. **chat-inbox.db 的 WAL 模式**：是否需要（并发读写）？
