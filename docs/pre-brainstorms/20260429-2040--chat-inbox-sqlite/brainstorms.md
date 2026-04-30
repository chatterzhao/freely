# Brainstorm — Chat Inbox SQLite 架构

## 为什么需要 chat-inbox

`freely chat --new-issue` / `--issue <id>` 是人机插话入口。
插话发生时还没有对应的 feature worktree。

如果 chat 直接写入 `docs/issues/`，文件就落在 daemon 所在分支上。
daemon 运行在 develop（protected branch），每次插话都在污染受保护分支。

所以需要一个**暂存区**：chat 先落地到 git-ignored 的 SQLite，
scan 消费后搬迁到 worktree 的 `docs/issues/` 进入 Git 跟踪。

## chat-inbox.db 的定位

**故意设计为不健壮**。原因：
- 它只存未消费的 chat（`consumed=0`）。消费后内容原样进入 `docs/issues/`
- `docs/issues/` 是 Git 跟踪的 canonical 真相源，换电脑不会丢
- 每次 scan 只看 `consumed=0`，数据量极小
- 没有跨阶段溯源需求——chat ID 不需要被其他组件引用
- 换电脑丢失 pending chat 是可接受的（插话本身是实时交互，用户会重发）

## ID 设计

纯 UTC 时间戳 `YYYYMMDDHHMMSS`，如 `20260429204530`。
- 不翻译、不组合、不做时区转换
- DB 内无前缀。`raw-` / `chat-` 前缀仅 scan 消费时根据 `chat_type` 组装

## SQLite Schema

```sql
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY,              -- UTC YYYYMMDDHHMMSS
    chat_type TEXT NOT NULL,             -- 'new-issue' | 'issue-id:xxx'
    author TEXT NOT NULL DEFAULT 'human',
    channel TEXT NOT NULL DEFAULT 'chat',
    message TEXT NOT NULL,
    consumed INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    session_refs TEXT DEFAULT '[]',
    intake_id TEXT,
    materialized_as TEXT
);
CREATE INDEX IF NOT EXISTS idx_consumed ON chats(consumed);
```

## 重构范围

### 新增

| 文件 | 职责 |
|------|------|
| `docs/system/workspace/scripts/runtime/chat-inbox.py` | SQLite 操作模块：init_db(), insert_chat(), get_pending(), mark_consumed() |
| （在 `freely init` 中调用） | 初始化 chat-inbox.db 表结构 |

### 修改

| 文件 | 改动 |
|------|------|
| `freely` runtime `_write_chat_to_issue` | `docs/issues/` 文件写入 → `chat_inbox.insert_chat()` |
| `freely` runtime `freely init` | 调用 `chat_inbox.init_db()` |
| `task-source-scan.py` | 新增 `scan_chat_inbox()`，调用 `get_pending()` |

### 不变

| 组件 | 原因 |
|------|------|
| `scan_raw_issues` / `scan_linked_issues` | 继续扫 `docs/issues/`，chat 消费后已在那里 |
| `governance-merge-gate` GATE 6.2/6.3 | 验证 `docs/issues/` 下的 C/M/I 链 |
| AI agent (lead-agent, context-source-skill) | 只读 scan JSON + `docs/issues/` |
| `issue-sync` | 从 `docs/issues/` 同步到平台 |
| B1_IBM → B2_IBM 全流程 | unchanged |

## 完整链路

```
freely init
  → chat_inbox.init_db()                    # 建表

freely chat --new-issue "msg"
  → chat_inbox.insert_chat(type='new-issue') # SQLite INSERT
  → develop 零变更 ✓

task-source-scan.py scan_chat_inbox()
  → chat_inbox.get_pending()                 # SELECT WHERE consumed=0
  → 按 chat_type 组装 source
  → chat_inbox.mark_consumed(id)             # UPDATE consumed=1

AI agent 读 scan JSON
  → 看到 chat_intake source
  → 创建 worktree
  → 在 worktree 中写 docs/issues/raw-{id}/issue.md

后续 B1_IBM → B2_IBM → merge to develop → issue-sync → platform
  （完全不变）
```

## 消费分支逻辑（task-source-scan.py 内）

```
chat_type='new-issue'
  → source_ref = "intake://raw-{id}"
  → restart_point='pre_brainstorm'
  → mark_consumed(id)

chat_type='issue-id:xxx'
  → 查 docs/issues/xxx/issue.md
     ├─ 找到且未关闭 → source_type='chat_comment' → mark_consumed
     ├─ absorbed → 重定向到 I-* → 追加评论 → mark_consumed
     └─ 未找到/已关闭 → source_type='chat_orphan' → mark_consumed
```

## 旧 intake 不迁移

`.freely/intake/` 231 条全部 absorbed/dropped。保留不动。
