# Brainstorm — Chat Inbox SQLite 架构

## 问题

`freely chat` 直接写 `docs/issues/` 污染 develop（protected branch）。

## 核心约束

**每个工位必须对应一个 issue。** 没有 issue 就不能创建工位。
`wt-create` 提取 key，查 chat-inbox + docs/issues/，找不到就拒绝。

## SQLite Schema

两个参数（`--new-issue` / `--issue xx`）都指向一个 issue，统一存为 `issue_id`：

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

### 字段说明

| 字段 | `--new-issue` | `--issue raw-xxx` | `--issue I-xxx` |
|------|--------------|-------------------|-----------------|
| `id` | `20260429204530` | `20260429204531` | `20260429204532` |
| `chat_type` | `new-issue` | `comment` | `comment` |
| `issue_id` | `raw-20260429204530` | `raw-xxx` | `I-xxx` |

- `id` 永远是本条 chat 的 UTC 时间戳
- `issue_id` 是目标 issue，`--new-issue` 时 = `raw-{id}`（即将创建的），`--issue` 时 = 参数值
- `idx_issue_id` 让 wt-create 和 scan 能快速按 issue 查所有相关 chat

## 写入

```
freely chat --new-issue "msg"
  → INSERT (id={ts}, chat_type='new-issue', issue_id='raw-{ts}', ...)
  → touch intake.pending

freely chat --issue raw-xxx "评论"
  → INSERT (id={ts}, chat_type='comment', issue_id='raw-xxx', ...)
  → touch intake.pending
```

## wt-create 关卡（new-issue 消费）

```
wt-create feature/raw-{ts}-{slug} --base develop
  → 提取 key = raw-{ts}

  → 查 chat-inbox:
      SELECT * WHERE id={ts} AND chat_type='new-issue' AND consumed=0
      ├─ 找到 → materialize
      │    → worktree/docs/issues/raw-{ts}/issue.md
      │    → UPDATE consumed=1, materialized_as='raw-{ts}'
      │    → 继续创建 ✓
      │
      └─ 未找到 → 查 docs/issues/raw-{ts}/
           ├─ 找到 → 已有 issue，继续创建 ✓
           └─ 未找到 → BLOCK

  → 顺便处理该 issue 的评论:
      SELECT * WHERE issue_id='raw-{ts}' AND chat_type='comment' AND consumed=0
      → 追加到 worktree/docs/issues/raw-{ts}/issue.md 的 Comments
      → UPDATE consumed=1
```

## scan 消费评论（无工位时）

scan 处理 `chat_type='comment'` 且 `consumed=0` 的条目：

```
SELECT * WHERE chat_type='comment' AND consumed=0

  → find worktrees-root/*{issue_id}*
     ├─ 找到工位 → AI 在 worktree 内追加
     │            → AI 调 chat-inbox consume
     │
     └─ 未找到 → 查 docs/issues/{issue_id}/
          ├─ raw-* 被 absorb → 递归查 I-* 的工位
          └─ 未找到/已关闭 → chat_orphan, mark consumed=1
```

## 完整链路

```
freely chat --new-issue "msg"
  → DB: (id={ts}, chat_type='new-issue', issue_id='raw-{ts}')
  → scan 放入 sources（consumed=0，AI 去重）
  → AI: wt-create feature/raw-{ts}-fix
       → wt-create 查 DB → 找到 → materialize → mark consumed=1
       → worktree/docs/issues/raw-{ts}/issue.md

freely chat --issue raw-xxx "评论"
  → DB: (id={ts2}, chat_type='comment', issue_id='raw-xxx')
  → scan: find worktree/*raw-xxx*
     ├─ 找到 → AI 在 worktree 内追加 → mark consumed=1
     └─ 未找到 → orphan, mark consumed=1
```

## 重构范围

### 新增
`chat-inbox.py` — init / add / query_by_issue / consume

### 修改
| 位置 | 改动 |
|------|------|
| `freely init` | 调 `chat-inbox init` |
| `_write_chat_to_issue` | `chat-inbox add`（chat_type + issue_id）|
| `wt-create` / `worktree-common.sh` | 提取 key，查 DB + docs/issues/ 关卡 |
| `task-source-scan.py` | 新增 `scan_chat_inbox()`（评论路由）|

### 不变
`freely chat` CLI、`scan_raw_issues`、`governance-merge-gate`、`issue-sync`、B1→B2

## 实现细节：wt-create 前置检查

### 插入位置

`docs/system/workspace/scripts/worktree/wt-create` L54（base 验证之后，git worktree add 之前）：

```bash
# L51-54: 验证 base 分支存在
if ! git show-ref --verify --quiet "refs/heads/$base" ...; then
  echo "Base branch/ref not found: $base" >&2; exit 1
fi

# >>> 新增：issue 前置检查 <<<
_require_issue_exists "$branch" || exit 1

# L56-58: 创建 worktree
target_path="$(freely_wt_resolve_target_path "$branch")"
git worktree add -b "$branch" "$target_path" "$base"
```

### Key 提取逻辑

```bash
_extract_issue_key() {
  local branch="$1"
  # raw-{14位时间戳}: raw-20260429204530
  if echo "$branch" | grep -qoE 'raw-[0-9]{14}'; then
    echo "$branch" | grep -oE 'raw-[0-9]{14}' | head -1
    return 0
  fi
  # I-{8位日期}-{4位时间}-{后缀}: I-20260429-2045-A
  if echo "$branch" | grep -qoE 'I-[0-9]{8}-[0-9]{4}-[A-Z]'; then
    echo "$branch" | grep -oE 'I-[0-9]{8}-[0-9]{4}-[A-Z]' | head -1
    return 0
  fi
  return 1
}
```

### 前置检查函数

```bash
_require_issue_exists() {
  local branch="$1"
  local key
  key="$(_extract_issue_key "$branch")"
  [[ -n "$key" ]] || return 0  # 无 key 放行（兼容旧分支名）

  case "$key" in
    raw-*)
      local ts="${key#raw-}"
      # 1. chat-inbox（new-issue，仅查 consumed=0）
      if chat-inbox query --id "$ts" --consumed 0 >/dev/null 2>&1; then
        return 0
      fi
      # 2. chat-inbox consumed=1 + docs/issues/ 存在 → 正常
      if chat-inbox query --id "$ts" --consumed 1 >/dev/null 2>&1; then
        if [[ -d "$ROOT_DIR/docs/issues/$key" ]]; then
          return 0
        fi
        # consumed=1 但 issue 缺失 → 异常恢复
        echo "警告: chat $key 已标记消费但 issue 缺失，重置" >&2
        chat-inbox reset "$ts"  # consumed=0
        return 0
      fi
      # 3. docs/issues/（已有 issue，重新开工）
      if [[ -d "$ROOT_DIR/docs/issues/$key" ]]; then
        return 0
      fi
      ;;
    I-*)
      if [[ -d "$ROOT_DIR/docs/issues/$key" ]]; then
        return 0
      fi
      ;;
  esac

  echo "拒绝创建: 未找到 issue $key" >&2
  echo "  chat-inbox (pending): $(chat-inbox query --id "${key#raw-}" --consumed 0 2>&1 || echo '无')" >&2
  echo "  docs/issues/: 无" >&2
  return 1
}
```

### materialize（wt-create 创建工位后立即执行）

```bash
_materialize_chat_if_needed() {
  local branch="$1" target_path="$2"
  local key ts
  key="$(_extract_issue_key "$branch")"
  [[ "$key" == raw-* ]] || return 0
  ts="${key#raw-}"

  # 从 chat-inbox 搬入 worktree
  if chat-inbox show "$ts" >/dev/null 2>&1; then
    local issue_dir="$target_path/docs/issues/$key"
    mkdir -p "$issue_dir"
    chat-inbox materialize "$ts" "$issue_dir/issue.md"
    chat-inbox consume "$ts" --materialized-as "$key"
    echo "materialized: chat-inbox → $issue_dir/issue.md"

    # 同时搬入该 issue 的所有待处理评论
    chat-inbox query-by-issue "$key" --type comment --pending \
      | while read -r comment_id; do
          chat-inbox materialize-comment "$comment_id" "$issue_dir/issue.md"
          chat-inbox consume "$comment_id"
        done
  fi
}
```

调用位置：`git worktree add` 成功后，`sync-tooling` 之前。



## 场景推演（10 个场景全部通过）

| # | 场景 | 结果 |
|---|------|------|
| 1 | `--new-issue` → scan → AI → wt-create → materialize | ✓ |
| 2 | `--issue raw-xxx` 评论，工位存在 | scan 找到工位，AI 追加，consume | ✓ |
| 3 | `--issue raw-xxx` 评论，无工位，issue 在 develop 已关闭 | orphan, consumed=1 | ✓ |
| 4 | `--issue raw-xxx` 评论，raw 被 absorb → 重定向 I-* | scan 递归查 I-* 工位 | ✓ |
| 5 | wt-create I-* 重新开工 | docs/issues/I-* 找到，放行 | ✓ |
| 6 | 同秒两个 chat | INSERT OR IGNORE + +1s 重试 | ✓ |
| 7 | materialize 失败（磁盘满等）| 回滚 worktree + branch | ✓ |
| 8 | AI 拿到 source 但 crash | consumed=0 不变，下次 scan 再出现 | ✓ |
| 9 | consumed=1 但 docs/issues/ 缺失 | 异常恢复：reset 为 consumed=0 | ✓ |
| 10 | 分支名无 issue key | 放行，兼容旧命名 | ✓ |

## 不变式

- **develop 零写入**：chat-inbox + wt-create materialize 都不写 develop
- **consumed 只由 AI 或 wt-create 标记**：scan 永远不标 consumed（orphan 除外）
- **工位 = issue**：wt-create 强制验证，没有 issue 不能建工位
- **原子 materialize**：失败回滚，不留半成品工位
