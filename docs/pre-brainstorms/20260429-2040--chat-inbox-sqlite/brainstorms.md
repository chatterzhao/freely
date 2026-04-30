# Brainstorm — Chat Inbox SQLite 架构

## 问题

`freely chat` 直接写 `docs/issues/` 污染 develop（protected branch）。

## 核心设计：共享 Key

工位目录名、分支名、issue ID 共享同一个 key（`raw-{ts}` 或 `I-{ts}-X`）。

```
分支:   feature/raw-20260429204530-fix-bug-20260429
工位:   20260429-raw-20260429204530-feature-fix-bug
issue:  docs/issues/raw-20260429204530/issue.md
key:    raw-20260429204530
```

`wt-create` 在创建工位前提取 key，查找对应 issue。**找不到就拒绝创建**。

## SQLite Schema

```sql
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY,              -- UTC YYYYMMDDHHMMSS（即 key 的时间戳部分）
    chat_type TEXT NOT NULL,             -- 'new-issue' | 'issue-id:xxx'
    author TEXT NOT NULL DEFAULT 'human',
    channel TEXT NOT NULL DEFAULT 'chat',
    message TEXT NOT NULL,
    consumed INTEGER NOT NULL DEFAULT 0,
    session_refs TEXT DEFAULT '[]',
    intake_id TEXT,
    materialized_as TEXT
);
CREATE INDEX IF NOT EXISTS idx_consumed ON chats(consumed);
```

## 写入（freely chat）

```
freely chat --new-issue "msg"
  → chat-inbox add（INSERT OR IGNORE, +1s retry）
  → touch intake.pending
  → develop 零变更

freely chat --issue <id> "评论"
  → 同上
```

不做任何工位判断，全进 DB。

## 消费：wt-create 关卡（new-issue）

```
wt-create feature/raw-{ts}-{slug} --base develop
  → 提取 key = raw-{ts}

  1. 查 chat-inbox:  SELECT * WHERE id={ts} AND consumed=0
     ├─ 找到 → materialize:
     │    → 在 worktree 中创建 docs/issues/raw-{ts}/issue.md
     │    → UPDATE consumed=1, materialized_as='raw-{ts}'
     │    → 继续创建 worktree ✓
     │
     └─ 未找到 → 步骤 2

  2. 查 docs/issues/:  [ -d docs/issues/raw-{ts}/ ]
     ├─ 找到 → 已有 issue（重新开工场景）
     │    → 继续创建 worktree ✓
     │
     └─ 未找到 → BLOCK
          → "拒绝创建: 未找到 issue raw-{ts}"
          → 退出
```

## 消费：scan 处理评论（issue-id:xxx）

对于 `chat_type='issue-id:xxx'`，scan 在 dispatcher 触发时处理：

```
SELECT * FROM chats WHERE consumed=0 AND chat_type LIKE 'issue-id:%'

  提取 target = chat_type 中 'issue-id:' 后面的部分

  1. find worktrees-root/*{target}*
     ├─ 找到活跃工位 → source_type='chat_comment'
     │    → AI 在 worktree 内追加评论
     │    → AI 调 chat-inbox consume <id>
     │
     └─ 未找到 → 查 docs/issues/{target}/

  2. 查 docs/issues/{target}/issue.md
     ├─ 找到且 raw-* 被 absorb → 读 absorbed_into → 回到步骤 1
     ├─ 找到且 phase_state 未关闭 → source_type='chat_orphan'
     │    （issue 在 develop 上，不在工位中，AI 决定）
     └─ 未找到或已关闭 → source_type='chat_orphan'
          → mark consumed=1
```

## 不需要 AI 手动标记 consumed

- `new-issue`：wt-create 在 materialize 时自动标记
- `issue-id:xxx` 评论：AI 追加评论后调 `chat-inbox consume`
- `chat_orphan`：scan 直接标记 consumed=1

## wt-create 改动

```bash
# 新增：提取 issue key 并验证
_require_issue_exists() {
  local branch="$1"
  local key
  key="$(_extract_issue_key "$branch")"  # raw-{ts} 或 I-{ts}-X
  [[ -n "$key" ]] || return 0  # 无 key 则不强制

  # 1. chat-inbox（new-issue）
  local ts="${key#raw-}"
  if [[ "$key" == raw-* ]]; then
    if chat-inbox show "$ts" >/dev/null 2>&1; then
      _materialize_chat_to_worktree "$ts" "$target_path"
      return 0
    fi
  fi

  # 2. docs/issues/（已有 issue）
  if [[ -d "$ROOT_DIR/docs/issues/$key" ]]; then
    return 0
  fi

  echo "拒绝创建: 未找到 issue $key（chat-inbox 和 docs/issues/ 均无）" >&2
  return 1
}
```

## 完整链路

```
── new-issue ──
freely chat --new-issue "msg"
  → chat-inbox add（DB）
  → scan 看到 → 放入 sources（consumed 仍为 0）
  → AI 决策 → wt-create feature/raw-{ts}-fix-bug
    → wt-create 提取 key → 查 chat-inbox → 找到
    → materialize: worktree/docs/issues/raw-{ts}/issue.md
    → mark consumed=1
  → worktree 创建完成，AI 开始 B1_IBM

── 评论（有工位）──
freely chat --issue raw-xxx "评论"
  → chat-inbox add（DB）
  → scan 看到 → find worktree/*raw-xxx* → 找到
  → source_type='chat_comment'
  → AI 在 worktree 中追加评论
  → AI 调 chat-inbox consume

── 评论（无工位）──
freely chat --issue raw-xxx "评论"
  → chat-inbox add（DB）
  → scan 看到 → 查 worktree → 无 → 查 develop → 已关闭
  → source_type='chat_orphan', mark consumed=1
  → AI 决定是否 reopen

── 重新开工（已有 issue）──
AI 决策 → wt-create feature/I-xxx-A-continue
  → 提取 key=I-xxx-A → chat-inbox 无 → docs/issues/ 有
  → worktree 创建 ✓
```

## 重构范围

### 新增
`chat-inbox.py` — init / add / list / consume / show / materialize

### 修改
| 位置 | 改动 |
|------|------|
| `freely init` | 调 `chat-inbox init` |
| `_write_chat_to_issue` | `chat-inbox add` + touch signal |
| `wt-create` / `worktree-common.sh` | `_require_issue_exists` 关卡 |
| `ensure_interruption_dispatch_once` | 调 `scan_chat_inbox()` |
| `task-source-scan.py` | 新增 `scan_chat_inbox()`（只处理评论） |

### 不变
`freely chat` CLI、`scan_raw_issues`、`governance-merge-gate`、`issue-sync`、B1→B2
