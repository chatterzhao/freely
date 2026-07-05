# Brainstorm — Chat Inbox SQLite 架构

## 问题

`freely chat` 直接写 `docs/B1-docs/raw-` 污染 develop（protected branch）。

## 核心约束

**每个工位必须对应一个 issue。** 没有 issue 就不能创建工位。

## 消费闭环

```
chat 写入 DB（consumed=0）
  │
  ├─ 工位存在？──YES──→ 直接同步到 worktree/docs/B1-docs/ → consumed=1
  │
  └─ 无工位 ──→ 留在 DB（consumed=0）
                   │
                   ├─ wt-create 触发 ──→ materialize → consumed=1
                   │
                   └─ scan 扫出 ──→ AI 判断
                        ├─ 有价值 → 创建工位（wt-create 自动 materialize）
                        ├─ 是评论 → AI 追加到对应 issue
                        └─ 噪声（"你好"）→ consumed=-1 丢弃
```

## SQLite Schema

```sql
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY,              -- UTC YYYYMMDDHHMMSS
    chat_type TEXT NOT NULL,             -- 'new-issue' | 'comment'
    issue_id TEXT NOT NULL,              -- 'raw-{id}' | 'raw-xxx' | 'I-xxx-X'
    author TEXT NOT NULL DEFAULT 'human',
    channel TEXT NOT NULL DEFAULT 'chat',
    message TEXT NOT NULL,
    consumed INTEGER NOT NULL DEFAULT 0, -- -1=丢弃, 0=待消费, 1=已消费
    session_refs TEXT DEFAULT '[]',
    intake_id TEXT,
    materialized_as TEXT
);
CREATE INDEX IF NOT EXISTS idx_consumed ON chats(consumed);
CREATE INDEX IF NOT EXISTS idx_issue_id ON chats(issue_id);
```

| consumed | 含义 | 谁标记 |
|----------|------|--------|
| `0` | 待消费 | 写入默认 |
| `1` | 已消费 | 同步到 worktree 后 / materialize 后 |
| `-1` | 丢弃 | AI 判断为噪声后 |

## 触发点 1：chat 写入时

```
freely chat --new-issue "msg"
  → INSERT (consumed=0)
  → find worktrees-root/*raw-{ts}* → 无（新 issue）
  → 留在 DB

freely chat --issue raw-xxx "评论"
  → INSERT (consumed=0)
  → find worktrees-root/*raw-xxx*
     ├─ 找到 → cat >> worktree/docs/B1-docs/raw-xxx/issue.md → consumed=1
     └─ 未找到 → 留在 DB
```

## 触发点 2：wt-create 时

```
wt-create feature/raw-{ts}-{slug} --base develop
  → _extract_issue_key → raw-{ts}
  → _require_issue_exists:
       raw-*: 查 DB(consumed=0) → 查 DB(consumed=1+恢复) → 查 docs/B1-docs/
       I-*:   查 docs/B1-docs/
       都无 → 拒绝
  → git worktree add
  → _materialize_chat_if_needed:
       查 DB WHERE id={ts} AND consumed=0
       ├─ 找到 → worktree/docs/B1-docs/raw-{ts}/issue.md → consumed=1
       │         → 同时搬入该 issue 的待处理评论
       │         → 失败回滚 worktree
       └─ 未找到 → 已有 issue，跳过
```

## 触发点 3：scan 扫出 + AI 判断

```
scan_chat_inbox:
  SELECT * WHERE consumed=0
  → 全部放入 scan JSON sources[]
  → source_type='chat_intake'
  → AI 逐条判断：

      new-issue + 有价值
        → AI 创建工位 feature/raw-{ts}-{slug}
        → wt-create 自动 materialize → consumed=1

      comment + 目标 issue 有工位
        → AI 在 worktree 内追加评论 → chat-inbox consume

      噪声（"你好"、空内容等）
        → chat-inbox discard → consumed=-1
```

## 场景推演

| # | 场景 | 路径 |
|---|------|------|
| 1 | `--new-issue` 正常 | 触发点1(留DB) → 触发点3(AI建工位) → 触发点2(materialize) |
| 2 | `--issue` 评论，工位存在 | 触发点1(直接同步) ✓ |
| 3 | `--issue` 评论，无工位 | 触发点1(留DB) → 触发点3(AI追加) |
| 4 | "你好" 噪声 | 触发点1(留DB) → 触发点3(AI标-1) |
| 5 | wt-create I-* 重新开工 | 触发点2(docs/B1-docs/raw-找到) |
| 6 | 同秒两个 chat | INSERT OR IGNORE + +1s 重试 |
| 7 | materialize 失败 | 触发点2 回滚 worktree |
| 8 | consumed=1 但 issue 缺失 | 触发点2 异常恢复 reset→0 |

## 重构范围

### 新增
`chat-inbox.py` — init / add / query / consume / discard / reset / materialize

### 修改
| 位置 | 改动 |
|------|------|
| `freely init` | 调 `chat-inbox init` |
| `_write_chat_to_issue` | INSERT + find worktree 尝试直接同步 |
| `wt-create` | `_require_issue_exists` + `_materialize_chat_if_needed` |
| `task-source-scan.py` | `scan_chat_inbox()` — 扫 consumed=0，全量放入 sources |

### 不变
`freely chat` CLI、`scan_raw_issues`、`governance-merge-gate`、`issue-sync`、B1→B2

## 不变式

- **develop 零写入**
- **consumed 三态**：0=待消费，1=已消费，-1=丢弃
- **工位 = issue**：wt-create 强制验证
- **原子 materialize**：失败回滚
- **AI 全权判断**：scan 只负责扫出来，不替 AI 做路由决定
