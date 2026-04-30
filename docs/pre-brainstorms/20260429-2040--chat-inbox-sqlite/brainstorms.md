# Brainstorm — Chat Inbox SQLite 架构

## 为什么需要 chat-inbox

`freely chat --new-issue` / `--issue <id>` 是人机插话入口。插话时还没有 worktree。

如果 chat 直接写 `docs/issues/`，文件落在 daemon 所在分支（develop，protected），
每次插话都在污染受保护分支。

解决方案：chat 先写入 git-ignored 的 `.freely/chat-inbox.db`（SQLite 暂存），
scan 消费后进入 worktree 的 `docs/issues/`（Git 跟踪）。

## chat-inbox.db 的定位

**故意不健壮**：
- 只存 `consumed=0` 的 chat。消费后原样进入 `docs/issues/`
- 换电脑丢失 pending chat 可接受（插话实时交互，重发即可）
- chat ID 不被溯源——内容消费后已在 issue 里

## 用户接口：不变

```
freely chat --new-issue "消息"       # 不变
freely chat --issue <id> "评论"      # 不变
freely intake chat ...               # 不变
```

内部唯一变化：`_write_chat_to_issue` 不再写 `docs/issues/`，
改为调用内部命令写入 SQLite。

## 内部命令（非用户面）

```
chat-inbox init                       # freely init 调用，建表
chat-inbox add --type ... --msg ...   # _write_chat_to_issue 调用
chat-inbox list [--limit 50]          # task-source-scan 调用
chat-inbox consume <id>               # task-source-scan 消费后标记
chat-inbox show <id>                  # debug 用
```

这些命令不暴露给用户。`freely chat` 参数和行为完全不变。

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
| `chat-inbox.py` | `init_db()` `add_chat()` `list_pending()` `mark_consumed()` `show_chat()` |

### 修改
| 调用方 | 改动 |
|--------|------|
| `freely init` | 调用 `chat-inbox init` |
| `_write_chat_to_issue` — new-issue 分支 | `mkdir docs/issues/`+`cat > issue.md` → `chat-inbox add --type new-issue` |
| `_write_chat_to_issue` — 评论分支 | `cat >> issue.md` → `chat-inbox add --type issue-id:xxx` |
| `task-source-scan.py` | 新增 `scan_chat_inbox()`，调 `list` + `consume` |

### 不变
| 组件 | 原因 |
|------|------|
| `freely chat` CLI 参数 | 用户接口不变 |
| `scan_raw_issues` / `scan_linked_issues` | 继续扫 `docs/issues/` |
| `governance-merge-gate` | 验证 `docs/issues/` |
| AI agent | 只读 scan JSON + `docs/issues/` |
| `issue-sync` | 从 `docs/issues/` 同步平台 |
| B1→B2 全流程 | unchanged |

## 完整链路

```
freely chat --new-issue "msg"               # 用户接口不变
  → _write_chat_to_issue
    → chat-inbox add --type new-issue ...   # 内部：写入 SQLite
  → develop 零变更 ✓

freely chat --issue raw-xxx "评论"          # 用户接口不变
  → _write_chat_to_issue
    → chat-inbox add --type issue-id:xxx .. # 内部：写入 SQLite
  → develop 零变更 ✓

task-source-scan.py scan_chat_inbox()
  → chat-inbox list                        # SELECT WHERE consumed=0
  → 按 chat_type 组装 source JSON
  → chat-inbox consume <id>                # UPDATE consumed=1

AI agent 读 scan JSON
  → chat_intake source → 创建 worktree
  → worktree/docs/issues/raw-{id}/issue.md

后续 B1_IBM → B2_IBM → merge → issue-sync → platform（完全不变）
```
