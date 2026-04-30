# Brainstorm — Chat Inbox SQLite 架构

## 为什么需要 chat-inbox

`freely chat --new-issue` / `--issue <id>` 是人机插话入口。
之前直接写 `docs/issues/`，落在 daemon 所在分支（develop，protected），污染受保护分支。

## 核心思路：chat-inbox 是 fallback，不是默认

插话时先判断目标 issue 是否已有 worktree：

```
freely chat --new-issue "msg"
  → 新 issue，必然没有 worktree
  → chat-inbox（暂存，等 scan 消费后建工位）

freely chat --issue xxx "评论"
  → 扫描 worktree 列表，查找 docs/issues/xxx/issue.md
     ├─ 找到 → 直接追加评论到 worktree（不经过 chat-inbox）
     └─ 未找到 → chat-inbox（暂存，等 scan 消费）
```

chat-inbox 只处理两种 fallback 场景：
1. 新建 issue（天然没有工位）
2. 评论一个找不到工位的 issue（可能已 merge 或工位已删除）

## 工位扫描逻辑

```bash
# 在 _write_chat_to_issue 的评论分支中
_find_issue_in_worktrees() {
  local target="$1"  # raw-xxx 或 I-xxx
  local worktrees_root="$project/../freely-worktrees"

  for wt in "$worktrees_root"/*/; do
    [[ -d "$wt" ]] || continue
    [[ -f "$wt/docs/issues/$target/issue.md" ]] || continue
    echo "$wt"
    return 0
  done
  return 1
}
```

## SQLite Schema（仅 fallback 用）

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

## 写入逻辑（_write_chat_to_issue 改动）

```
--new-issue:
  → chat-inbox add（always，新 issue 无工位）

--issue xxx:
  → _find_issue_in_worktrees(xxx)
     ├─ 找到 worktree
     │    → 直接 cat >> worktree/docs/issues/xxx/issue.md（不经过 chat-inbox）
     │    → 如果是 raw-* 且已 absorbed，重定向到 I-*
     │
     └─ 未找到
          → chat-inbox add --type issue-id:xxx（fallback）
```

## 消费逻辑（task-source-scan.py，不变）

chat-inbox 中的 pending 项由 scan 消费，与之前设计一致。

## 重构范围

### 新增
| 文件 | 职责 |
|------|------|
| `chat-inbox.py` | SQLite 操作：init/add/list/consume/show |

### 修改
| 调用方 | 改动 |
|--------|------|
| `freely init` | 调 `chat-inbox init` 建表 |
| `_write_chat_to_issue` — new-issue | → `chat-inbox add` |
| `_write_chat_to_issue` — 评论 | → 先扫工位，找到直接写；未找到 → `chat-inbox add` |
| `task-source-scan.py` | 新增 `scan_chat_inbox()` |

### 不变
| 组件 | 原因 |
|------|------|
| `freely chat` CLI | 用户接口不变 |
| `scan_raw_issues` / `scan_linked_issues` | 继续扫 `docs/issues/` |
| `governance-merge-gate` | 验证 `docs/issues/` |
| AI agent | 只读 scan JSON + `docs/issues/` |
| `issue-sync` | 从 `docs/issues/` 同步 |
| B1→B2 全流程 | unchanged |

## 完整链路

```
freely chat --new-issue "msg"
  → chat-inbox add（无工位，暂存）
  → scan → AI 建工位 → docs/issues/raw-{id}/issue.md

freely chat --issue raw-xxx "评论"
  → 扫工位
     ├─ 找到 → 直接写 worktree/docs/issues/raw-xxx/issue.md
     └─ 未找到 → chat-inbox add（暂存）
```
