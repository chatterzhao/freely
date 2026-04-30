# Brainstorm — Chat Inbox SQLite 架构

## 问题

`freely chat` 直接写 `docs/issues/` 污染 develop（protected branch）。

## 设计审查（全局推演）

### 审查 1：consumed 标记时机 — BUG

原设计：scan 对 `new-issue` 直接 `mark consumed=1` 再放入 sources。
问题：AI 拿到 source 后可能 crash、context loss、被更高优先级任务抢占。chat 已标记 consumed 但从未 materialize，永久丢失。

**修复**：`new-issue` 不在 scan 时标记 consumed。scan 只读 consumed=0，放入 sources，**不改状态**。
AI 成功创建 worktree + 写入 `docs/issues/raw-{id}/issue.md` 后，调 `chat-inbox consume <id>` 完成标记。
scan 每次都会看到同一个 pending chat，直到 AI 处理掉。AI 需去重（同 source_ref 出现多次则跳过）。

### 审查 2：评论直接写 develop — BUG

原设计：`issue-id:xxx` 未找到 worktree 时，查 develop 上的 issue 并 `cat >>` 追加评论。
问题：develop 是 protected branch。`cat >>` 同样是污染。

**修复**：消费脚本**永远不写 develop**。对 develop 上的 issue：
- 已 merge 且 phase_state 完成 → `chat_orphan`（issue 已关闭，让 AI 决定是否需要 reopen）
- 已 merge 且 phase_state 未完成 → `chat_orphan`（异常状态，让 AI 判断）

### 审查 3：消费脚本写 worktree 的竞态 — RISK

原设计：`cat >> worktree/docs/issues/xxx/issue.md`。
问题：worktree 可能正被 AI 修改同一文件，`cat >>` 在外部追加可能造成冲突或 dirty state。

**修复**：评论也走 scan sources，不直接写文件。
- `issue-id:xxx` + 找到活跃 worktree → `source_type='chat_comment'`，放入 sources，AI 在 worktree 上下文中追加
- 这样评论在 AI 的正常工作流中处理，无外部写入竞态

### 审查 4：同秒碰撞 — BUG

两个 chat 在同一秒到达 → 第二个 INSERT 因 PRIMARY KEY(UTC秒) 冲突失败。

**修复**：`INSERT OR IGNORE`，冲突时 +1 秒重试，最多 3 次。

### 审查 5：created_at 冗余

`id` 已是 UTC 时间戳。`created_at` 完全冗余。

**修复**：删除 `created_at` 字段。

### 审查 6：信号文件清理

chat 被消费完后，`intake.pending` 文件不删除，dispatcher 下次还会触发空扫。

**修复**：`scan_chat_inbox()` 结尾检查 `SELECT COUNT(*) WHERE consumed=0`，为 0 则 `rm intake.pending`。

## 最终设计

### SQLite Schema

```sql
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY,              -- UTC YYYYMMDDHHMMSS
    chat_type TEXT NOT NULL,             -- 'new-issue' | 'issue-id:xxx'
    author TEXT NOT NULL DEFAULT 'human',
    channel TEXT NOT NULL DEFAULT 'chat',
    message TEXT NOT NULL,
    consumed INTEGER NOT NULL DEFAULT 0, -- 0=pending, 1=done (AI 标记)
    session_refs TEXT DEFAULT '[]',
    intake_id TEXT,
    materialized_as TEXT                 -- AI 填写：产物 issue ID 或 worktree 路径
);
CREATE INDEX IF NOT EXISTS idx_consumed ON chats(consumed);
```

### 写入（freely chat）

```
freely chat --new-issue / --issue <id>
  → chat-inbox add（INSERT OR IGNORE, +1s retry）
  → touch intake.pending
  → develop 零变更
```

### 消费路由（scan_chat_inbox，由 interruption_dispatcher 触发）

```
SELECT * FROM chats WHERE consumed=0

对每条：

  chat_type='new-issue'
    → source_type='chat_intake'
    → restart_point='pre_brainstorm'
    → next_action='Create worktree named with raw-{id}, materialize issue'
    → 不标记 consumed（AI 处理后才标记）

  chat_type='issue-id:xxx'
    → find worktrees-root/*xxx*/docs/issues/xxx/issue.md
       ├─ 找到且 phase_state 未关闭
       │    → source_type='chat_comment'
       │    → next_action='Append comment to xxx in worktree {path}'
       │    → 不标记 consumed（AI 处理后才标记）
       │
       ├─ raw-xxx 被 absorb → 读 absorbed_into 得到 I-*
       │    → 同上，递归查 I-* 的 worktree
       │
       └─ 未找到 worktree 或已关闭
            → source_type='chat_orphan'
            → 标记 consumed=1（无法处理，交给 AI 判断去向）

结尾：SELECT COUNT(*) WHERE consumed=0，为 0 则 rm intake.pending
```

### AI 处理后的收尾

AI 在 worktree 中完成处理后：
```
# new-issue 被 materialize 后
chat-inbox consume <id> --materialized-as raw-{id}

# 评论被追加后
chat-inbox consume <id> --materialized-as {issue-id}
```

### 完整链路

```
freely chat --new-issue "msg"
  → chat-inbox add + touch intake.pending
  → dispatcher 触发 scan_chat_inbox
    → source_type='chat_intake' 放入 scan sources（consumed 仍为 0）
  → AI 读 scan → 建 worktree 20260429-raw-{id}-feature-{slug}
  → AI 写 worktree/docs/issues/raw-{id}/issue.md
  → AI 调 chat-inbox consume <id>（consumed=1）

freely chat --issue raw-xxx "评论"
  → chat-inbox add + touch intake.pending
  → dispatcher 触发 scan_chat_inbox
    → find worktrees-root/*raw-xxx*
       ├─ 找到活跃工位 → source_type='chat_comment'（consumed 仍为 0）
       │    → AI 读 scan → 在 worktree 中追加评论
       │    → AI 调 chat-inbox consume <id>
       │
       └─ 未找到/已关闭 → source_type='chat_orphan'（consumed=1）
            → AI 读 scan → 决定 reopen 或 drop
```

### 核心原则

| 原则 | 说明 |
|------|------|
| scan 不直接写文件 | 避免 develop 污染、worktree 竞态 |
| scan 不标记 consumed | AI 确认处理后才标记，防止丢失 |
| 写 develop 是唯一红线 | scan 永远不 touch develop |
| consumed 由 AI 标记 | AI 完成 materialize/comment 后调 CLI |
| 信号文件及时清理 | 无 pending 就 rm，避免空扫 |

## 重构范围

### 新增
`chat-inbox.py` — init / add / list / consume / show

### 修改
| 位置 | 改动 |
|------|------|
| `freely init` | 调 `chat-inbox init` |
| `_write_chat_to_issue` | 两个分支 → `chat-inbox add` + touch signal |
| `ensure_interruption_dispatch_once` | 新增 `scan_chat_inbox()` |
| `task-source-scan.py` | 新增 `scan_chat_inbox()`，只读不写 |

### 不变
`freely chat` CLI、`scan_raw_issues`、`governance-merge-gate`、`issue-sync`、B1→B2
