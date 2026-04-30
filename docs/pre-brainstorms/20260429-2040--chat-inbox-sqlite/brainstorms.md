# Brainstorm — Chat Inbox SQLite 架构

## 为什么需要 chat-inbox

`freely chat` 直接写 `docs/issues/` 会污染 develop（protected branch）。

## 核心决策：统一先写 DB，scan 时统一消费

**不在 `freely chat` 写入时判断工位**。原因：

- 写入时上下文不足——不知道是否有工位、工位是否活跃、issue 是否已 absorb、是否已 merge
- 存在竞态——写入时没工位，1 秒后 AI 建了工位；写入时有工位，1 秒后 merge 删了
- 已 merge 删除的工位和从未建工位，对写入时而言无法区分

**全部交给 scan**。scan 有全量上下文——所有 worktree、develop 状态、issue 的 absorbed_into。

```
freely chat（无论 --new-issue 还是 --issue）
  → chat-inbox add（只写 SQLite，不做任何判断）

task-source-scan（每 CHECK_INTERVAL 秒，默认 10s）
  → chat-inbox list（SELECT WHERE consumed=0）
  → 此时有全量上下文，做出准确路由
  → chat-inbox consume（UPDATE consumed=1）
```

## 消费时的准确路由（scan 内）

scan 消费每条 pending chat 时，上下文完备：

```
chat_type='new-issue'
  → 必然无工位（新 issue）
  → 放入 scan JSON sources[]
  → source_type='chat_intake', restart_point='pre_brainstorm'
  → AI 创建 worktree → docs/issues/raw-{id}/issue.md
  → mark consumed=1

chat_type='issue-id:xxx'
  → 按优先级查找目标 issue：
     1. develop/docs/issues/xxx/issue.md         ← 已 merge 到 develop 的
     2. worktrees/*/docs/issues/xxx/issue.md      ← 活跃工位中的
     3. develop/docs/issues/ 查 absorbed_into     ← raw→I 重定向
  →
  ├─ 找到且 phase_state 未关闭
  │    → 直接 cat >> 追加评论到该 issue.md
  │    → mark consumed=1
  │
  ├─ 找到但已关闭（completed/closed）
  │    → 放入 scan JSON sources[]
  │    → source_type='chat_orphan'
  │    → next_action='Target closed, AI decides: reopen or drop'
  │    → mark consumed=1
  │
  └─ 全都没找到
       → 放入 scan JSON sources[]
       → source_type='chat_orphan'
       → next_action='Target not found, AI decides: create new or drop'
       → mark consumed=1
```

## 为什么准确

| 写入时判断 | scan 时判断 |
|-----------|-----------|
| 只有当前瞬间快照 | 全量 worktree + develop 状态 |
| 竞态窗口大 | 无竞态（scan 原子执行）|
| 已 merge 删除 ≈ 从未建工位，无法区分 | 能找到 develop 上的 issue（已 merge） |
| absorb 重定向需要额外查询 | 已有 issue 全貌，直接查 |

## 为什么及时

- daemon 每 `CHECK_INTERVAL`（默认 10s）跑一次 scan
- AI startup patrol 也触发 scan
- urgent 标记可触发即时 scan
- 10 秒内消费，对插话场景完全可接受

## 触发链

```
daemon supervisor loop（每 10s）
  → task-source-scan.py
    → scan_chat_inbox()  ← 消费 chat-inbox
    → scan_raw_issues()  ← 扫已有 issue
    → scan_linked_issues()
    → ... 组装 scan JSON
  → AI agent 消费 scan JSON
```

chat-inbox 消费是 scan 的第一步，后续步骤看到的是已更新的状态。

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
| `_write_chat_to_issue` | new-issue 分支：`chat-inbox add --type new-issue` |
| `_write_chat_to_issue` | 评论分支：`chat-inbox add --type issue-id:xxx` |
| `task-source-scan.py` | 新增 `scan_chat_inbox()`，含完整路由逻辑 |

### 不变
`freely chat` CLI、`scan_raw_issues`、`governance-merge-gate`、AI agent、`issue-sync`、B1→B2 全流程

## 完整链路

```
freely chat --new-issue "msg"
  → chat-inbox add（SQLite，10ms）
  → develop 零变更 ✓

freely chat --issue raw-xxx "评论"
  → chat-inbox add（SQLite，10ms）
  → develop 零变更 ✓

--- 最多 10 秒后 ---

task-source-scan.py scan_chat_inbox()
  → SELECT WHERE consumed=0
  → 对每条：全量上下文查找目标 → 直接写评论 或 放入 sources[]
  → UPDATE consumed=1

AI agent 读 scan JSON
  → 看到 chat_intake / chat_orphan source
  → 建工位 / 决定去向

后续 B1_IBM → B2_IBM → merge → issue-sync（完全不变）
```
