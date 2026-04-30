# Brainstorm — Chat Inbox SQLite 架构

## 问题

`freely chat` 直接写 `docs/issues/` 污染 develop（protected branch）。

## 核心约束

**每个工位必须对应一个 issue。** 没有 issue 就不能创建工位。

## 消费闭环：两个触发点 + scan 兜底

```
chat 写入 DB
  │
  ├─ 工位存在？──YES──→ 立即同步到 worktree/docs/issues/ → consumed=1
  │
  └─ 无工位 ──→ 留在 DB（consumed=0）
                   │
                   ├─ wt-create 触发 ──→ materialize → consumed=1
                   │
                   └─ scan 兜底 ──→ chat_orphan → AI 决定
```

chat 写完就尝试消费（有工位直接同步）。没有工位不负责，留给后面两个触发点。

## SQLite Schema

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

| 字段 | `--new-issue` | `--issue raw-xxx` |
|------|--------------|-------------------|
| `id` | `20260429204530` | `20260429204531` |
| `chat_type` | `new-issue` | `comment` |
| `issue_id` | `raw-20260429204530` | `raw-xxx` |

## 触发点 1：chat 写入时（有工位直接同步）

```
freely chat --new-issue "msg"
  → INSERT INTO chats
  → find worktrees-root/*raw-{ts}*
     └─ 必然无工位（新 issue）→ 留在 DB，consumed=0

freely chat --issue raw-xxx "评论"
  → INSERT INTO chats
  → find worktrees-root/*raw-xxx*
     ├─ 找到工位
     │    → cat >> worktree/docs/issues/raw-xxx/issue.md
     │    → UPDATE consumed=1
     │    → done ✓
     │
     └─ 未找到 → 留在 DB，consumed=0
          （不写 develop。无工位插话不负责。）
```

## 触发点 2：wt-create 时（pending chat 立即 materialize）

```
wt-create feature/raw-{ts}-{slug} --base develop
  → _extract_issue_key → raw-{ts}

  → _require_issue_exists:
       raw-*: 查 DB (consumed=0) → 查 DB (consumed=1+恢复) → 查 docs/issues/
       I-*:   查 docs/issues/
       都无 → 拒绝创建

  → git worktree add（成功）

  → _materialize_chat_if_needed:
       查 DB: SELECT * WHERE id={ts} AND consumed=0
       ├─ 找到 → 创建 worktree/docs/issues/raw-{ts}/issue.md
       │         → 同时搬入该 issue 的待处理评论
       │         → UPDATE consumed=1
       │         → 失败则回滚 worktree + branch
       │
       └─ 未找到 → 已有 issue，无需 materialize
```

## 触发点 3：scan 兜底（孤儿评论）

```
scan_chat_inbox:
  SELECT * WHERE consumed=0 AND chat_type='comment'

  → find worktrees-root/*{issue_id}*
     ├─ 找到 → source_type='chat_comment'（AI 追加）
     └─ 未找到 → 查 docs/issues/{issue_id}/
          ├─ raw-* 被 absorb → 递归查 I-*
          └─ 未找到/已关闭 → chat_orphan, consumed=1
```

## 场景推演

| # | 场景 | 路径 |
|---|------|------|
| 1 | `--new-issue` → 无工位 → wt-create | 触发点 1(留DB) → 触发点 2(materialize) |
| 2 | `--issue raw-xxx` 评论，工位存在 | 触发点 1(直接同步) ✓ |
| 3 | `--issue raw-xxx` 评论，无工位 | 触发点 1(留DB) → 触发点 3(scan 兜底) |
| 4 | raw 被 absorb → I-* 工位存在 | 触发点 3(递归查 I-*) |
| 5 | wt-create I-* 重新开工 | 触发点 2(docs/issues/ 找到) |
| 6 | 同秒两个 chat | INSERT OR IGNORE + +1s 重试 |
| 7 | materialize 失败 | 回滚 worktree + branch |
| 8 | consumed=1 但 issue 缺失 | 触发点 2(异常恢复 reset) |
| 9 | 分支名无 issue key | 放行，兼容旧命名 |

## 重构范围

### 新增
`chat-inbox.py` — init / add / query / consume / reset / materialize

### 修改
| 位置 | 改动 |
|------|------|
| `freely init` | 调 `chat-inbox init` |
| `_write_chat_to_issue` | INSERT + find worktree 尝试直接同步 |
| `wt-create` | `_require_issue_exists` 关卡 + `_materialize_chat_if_needed` |
| `task-source-scan.py` | `scan_chat_inbox()` 兜底 |

### 不变
`freely chat` CLI、`scan_raw_issues`、`governance-merge-gate`、`issue-sync`、B1→B2

## 不变式

- **develop 零写入**
- **chat 写完就尝试消费**（有工位直接同步）
- **wt-create 强制验证**（没 issue 不能建工位）
- **原子 materialize**（失败回滚）
- **scan 只兜底**（处理前两个触发点都没覆盖的孤儿）
