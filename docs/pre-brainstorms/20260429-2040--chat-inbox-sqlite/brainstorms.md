# Brainstorm — Chat Inbox SQLite 架构

## 为什么需要 chat-inbox

`freely chat --new-issue` / `--issue <id>` 是人机插话入口。
插话发生时还没有对应的 feature worktree。

如果 chat 直接写入 `docs/issues/`，文件就落在 daemon 所在分支上。
daemon 运行在 develop（protected branch），每次插话都在污染受保护分支。

所以需要一个**暂存区**：chat 先落地到 git-ignored 的 SQLite，
scan 消费后进入 worktree 的 `docs/issues/`（Git 跟踪）。

## chat-inbox.db 的定位

**故意设计为不健壮**：
- 只存未消费的 chat（`consumed=0`）
- 消费后内容原样进入 `docs/issues/`（Git 跟踪的 canonical 真相源）
- 换电脑丢失 pending chat 可接受（插话是实时交互，用户重发即可）
- chat ID 不需要被溯源——消费后内容已在 issue 里

## ID 设计

纯 UTC 时间戳 `YYYYMMDDHHMMSS`，如 `20260429204530`。
- 不翻译、不组合、不做时区转换
- DB 内无前缀。`raw-` / `chat-` 前缀仅 scan 组装 source_ref 时附加

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

## CLI 设计（CLI-first）

```
freely chat-inbox init                        → 建表（freely init 调用）
freely chat-inbox add --type new-issue \      → 写入 chat（freely chat 调用）
  --message "..." --author human
freely chat-inbox add --type issue-id:xxx \   → 写入评论
  --message "..."
freely chat-inbox list [--limit 50]           → 列出未消费 chat（debug）
freely chat-inbox show <id>                   → 查看 chat 内容（debug）
freely chat-inbox consume <id> \              → 标记已消费（scan 调用）
  --materialized-as <ref>
```

### 各 CLI 命令的调用方

| 命令 | 调用方 | 说明 |
|------|--------|------|
| `chat-inbox init` | `freely init` | 项目初始化时建表 |
| `chat-inbox add --type new-issue` | `freely chat --new-issue` | 插话新建 issue |
| `chat-inbox add --type issue-id:xxx` | `freely chat --issue <id>` | 插话评论 |
| `chat-inbox list` | `task-source-scan.py` / 人工 debug | 获取 pending 列表 |
| `chat-inbox consume` | `task-source-scan.py` | 消费后标记 |

### 实现：CLI 命令 → Python 模块

```
bin/freely chat-inbox ...
  → docs/system/workspace/scripts/runtime/freely
    → cmd_chat_inbox() 分发
      → add/list/show/consume → chat_inbox.py 对应函数
```

`chat-inbox.py` 是纯函数模块，所有 SQLite 操作集中在此。
CLI 命令是薄封装，负责参数解析后调用模块函数。

## 重构范围

### 新增

| 文件 | 职责 |
|------|------|
| `docs/system/workspace/scripts/runtime/chat-inbox.py` | `init_db()` `add_chat()` `list_pending()` `show_chat()` `mark_consumed()` |
| `freely` runtime `cmd_chat_inbox` | CLI 命令分发（add/list/show/consume/init） |

### 修改

| 调用方 | 改动 |
|--------|------|
| `freely init` | 增加调用 `chat-inbox init` |
| `freely chat --new-issue` | `_write_chat_to_issue` → `chat-inbox add --type new-issue` |
| `freely chat --issue <id>` | `_write_chat_to_issue` → `chat-inbox add --type issue-id:xxx` |
| `task-source-scan.py::scan_chat_inbox()` | 调用 `chat-inbox list` + `chat-inbox consume` |

### 不变

| 组件 | 原因 |
|------|------|
| `scan_raw_issues` / `scan_linked_issues` | 继续扫 `docs/issues/` |
| `governance-merge-gate` | 验证 `docs/issues/` |
| AI agent | 只读 scan JSON + `docs/issues/` |
| `issue-sync` | 从 `docs/issues/` 同步 |
| B1_IBM → B2_IBM 全流程 | unchanged |

## 完整链路

```
freely init
  → chat-inbox init                          # CLI → init_db()

freely chat --new-issue "msg"
  → chat-inbox add --type new-issue ...       # CLI → add_chat()
  → develop 零变更 ✓

task-source-scan.py scan_chat_inbox()
  → chat-inbox list                          # CLI → list_pending()
  → 按 chat_type 组装 source
  → chat-inbox consume <id>                  # CLI → mark_consumed()

AI agent 读 scan JSON
  → chat_intake source → 创建 worktree
  → docs/issues/raw-{id}/issue.md（Git 跟踪）

后续 B1_IBM → B2_IBM → merge → issue-sync → platform
  （完全不变）
```

## 消费分支逻辑（task-source-scan.py 内）

```
chat_type='new-issue'
  → source_ref = "intake://raw-{id}"
  → restart_point='pre_brainstorm'
  → mark_consumed

chat_type='issue-id:xxx'
  → 查 docs/issues/xxx/issue.md
     ├─ 找到未关闭 → source_type='chat_comment' → mark_consumed
     ├─ absorbed → 重定向到 I-* → 追加评论 → mark_consumed
     └─ 未找到/已关闭 → source_type='chat_orphan' → mark_consumed
```
