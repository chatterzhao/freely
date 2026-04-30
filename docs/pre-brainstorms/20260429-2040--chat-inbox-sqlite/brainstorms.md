# Brainstorm — Chat Inbox SQLite 架构

## 问题

`freely chat` 直接写 `docs/issues/` 污染 develop（protected branch）。

## 核心设计

### 1. 统一先写 DB

```
freely chat（--new-issue / --issue，不做任何工位判断）
  → chat-inbox add（SQLite INSERT，10ms）
  → touch intake.pending 信号文件
  → develop 零变更
```

### 2. 事件触发消费

已有基础设施：`intake.pending` 信号文件 + `interruption_dispatcher` watch 循环。

```
freely chat → SQLite INSERT → touch intake.pending
  → interruption_dispatcher 检测到信号文件
    → ensure_interruption_dispatch_once()
      → scan_chat_inbox()  ← 消费
```

不是每 10s 轮询，是有信号才动作。

### 3. 工位名含 issue ID

当前工位名：`20260429-feature-chat-inbox-sqlite`（日期+分支名）
改进后：`20260429-raw-20260429204530-feature-fix-bug`（日期+issueID+分支名）

```
AI 创建工位时：
  wt-create feature/raw-{ts}-{slug} --base develop
  → worktree: {date}-raw-{ts}-feature-{slug}

scan 查找工位时：
  find worktrees-root -maxdepth 1 -name "*raw-{ts}*"
  → O(1) 定位
```

AI agent 在 B1_IBM 阶段创建工位时，自然知道 issue ID，
工位名包含 issue ID 是举手之劳。

## 消费路由（scan_chat_inbox 内）

```
SELECT * FROM chats WHERE consumed=0

对每条 pending chat：

  chat_type='new-issue'
    → source_type='chat_intake', restart_point='pre_brainstorm'
    → next_action='AI creates worktree named with raw-{id}'
    → mark consumed=1

  chat_type='issue-id:xxx'
    → find worktrees-root/*xxx*/docs/issues/xxx/issue.md
       ├─ 找到 worktree 且 phase_state 未关闭
       │    → cat >> 追加评论到该 worktree 的 issue.md
       │    → mark consumed=1
       │
       ├─ 找到 worktree 但已关闭
       │    → source_type='chat_orphan'
       │    → mark consumed=1
       │
       ├─ 未找到 worktree → 查 develop/docs/issues/xxx/
       │    ├─ 找到（已 merge）且未关闭
       │    │    → cat >> 追加评论
       │    │    → mark consumed=1
       │    │
       │    ├─ raw-xxx 被 absorb → 读 absorbed_into → 重定向到 I-*
       │    │    → 递归查找 I-* 的 worktree
       │    │    → 追加评论
       │    │    → mark consumed=1
       │    │
       │    └─ 全没找到或已关闭
       │         → source_type='chat_orphan'
       │         → mark consumed=1
       │
       └─ 注意：不区分"已 merge 删除"和"从未建工位"
           因为对评论投递而言结果一样——找不到可写的目标 issue
           统一标 orphan，让 AI 决定去向
```

## 为什么这样设计

| 问题 | 方案 |
|------|------|
| 写入时不知道工位状态 | 不判断，全写 DB |
| 写入时竞态 | scan 消费时有全量上下文 |
| 工位已 merge 删除 vs 从未建 | 对评论投递结果一样，统一处理 |
| 如何找工位 | 工位名含 issue ID，find 一行 |
| 消费触发 | 信号文件，事件驱动 |
| 消费不及时 | 信号触发 dispatcher，秒级响应 |

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
| `chat-inbox.py` | init / add / list / consume / show |

### 修改
| 位置 | 改动 |
|------|------|
| `freely init` | 调 `chat-inbox init` |
| `_write_chat_to_issue` | 两个分支都改为 `chat-inbox add` + touch signal |
| `ensure_interruption_dispatch_once` | 新增 `scan_chat_inbox()` 调用 |
| `task-source-scan.py` | 新增 `scan_chat_inbox()`，含完整路由 |

### 不变
`freely chat` CLI、`scan_raw_issues`、`governance-merge-gate`、AI agent、`issue-sync`、B1→B2

## 完整链路

```
freely chat --new-issue "msg"
  → chat-inbox add + touch intake.pending
  → interruption_dispatcher 检测信号
    → scan_chat_inbox()
      → new-issue → 放入 scan sources[]
      → AI 读 scan → 建工位 20260429-raw-{id}-feature-{slug}
      → worktree/docs/issues/raw-{id}/issue.md

freely chat --issue raw-xxx "评论"
  → chat-inbox add + touch intake.pending
  → interruption_dispatcher 检测信号
    → scan_chat_inbox()
      → find worktrees-root/*raw-xxx*
         ├─ 找到 → cat >> 直接写评论
         └─ 未找到 → 查 develop → 写评论或标 orphan
```
