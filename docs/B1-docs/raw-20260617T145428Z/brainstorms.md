# Brainstorm: freely-db-cli syntax error + AGENTS.md entry flow + hook message

## Discovery

### Source
- raw-20260617T145428Z28Z（GitHub issue #2932）
- 发现方式：daemon 重启时 `ensure_freely_db` 所有 CLI 操作（db.ping 等）均失败

### Bug 1: freely-db-cli IndentationError

`docs/system/workspace/scripts/runtime/freely-db-cli` 第 282 行 `_task_update_params` 函数：

```python
def _task_update_params(args):
    p = {"task_id": args["task_id"]}
              "worktree", "branch", ...  # ← for k in ( 缺失
```

`for k in (` 前缀被意外删除。所有 CLI 操作（`db.ping`、`chat.add`、`session.upsert` 等）解析为 `IndentationError` 直接退出，导致 `ensure_freely_db()` 的 health check 失败。

**影响范围**：40 个 worktree 全部包含此 bug。但 freeely-db daemon 是独立运行的 Python 进程（不经过 CLI），所以 daemon 本身的 SQLite 操作不受影响。只有当 daemon 重启、`ensure_freely_db` 试图通过 CLI 做健康检查时才会触发。

**根因链**：
1. 某次提交中 `for k in (` 被意外删除（可能在重构或合并冲突解决时）
2. 所有基于 develop 创建的 worktree 继承此 bug
3. daemon 是独立进程，bug 长期未被发现
4. daemon 重启时 `ensure_freely_db` → `freely-db-cli db.ping` → IndentationError → 判定 daemon 未运行 → 尝试启动新 daemon → 旧 daemon 已在运行 → 启动超时失败

### Bug 2: AGENTS.md 流程缺少 feedback 入口

AGENTS.md §核心开发流程的原始结构：

```
阶段1: 问题发现（scan / chat / 平台 issue）  ← feedback 不在此
阶段2: 创建 raw issue（freely feedback / chat --new-issue）  ← feedback 被埋在括号里
```

对比 feat-execution skill 的正确流程：`feedback → wt-create → B1_IBM → ...`

feedback 是整条链路的第一个入口节点，不应该压在"创建 raw issue"的子选项里。且入口是"或"关系：
- feedback → 新问题摄入，创建 raw issue
- scan → 发现已有 raw issue 继续
- scan → 发现已有工位，直接进入继续

### Bug 3: pre-commit hook 拦截提示不指向 skill

develop 提交被 hook 拦截时，提示只有机械操作（`wt-create`、`sync-tooling`），不告知 AI 应该调用哪个 skill。AI 看到纯机械命令的自然反应是"绕过这个限制"，而不是"找到正确的流程规范"。

对比同一 hook 的 `FREELY_SKIP_IBM_GATE` 拦截消息，正确地指向了 `skill:freely-doc-B1_IBM-execution` 和 `skill:freely-doc-B2_IBM-execution`。

## Research

### 1. 为什么 freely-db-cli 的 bug 传播到 40 个 worktree 而未被发现

- `ensure_freely_db()` 只在 daemon 启动时调用（`start_project_runtime`）
- daemon 进程存活期间不会重新调用 `ensure_freely_db`
- 所有 SQLite 操作通过 Unix socket 直达 daemon，不经过 CLI
- 最后一个有正确 CLI 的 daemon 进程覆盖了整个开发周期

### 2. 为什么 Agent 在 hook 拦截后选择绕过而不是读规则

旧 hook 消息的逻辑链：
```
你被拦了 → 用 wt-create → 用完后 wt-close
```

缺失的环节：**为什么不直接 commit、为什么要走完整流程、走哪个 skill**

新消息的逻辑链：
```
你被拦了 → 读 AGENTS.md §核心开发流程 → 调 skill:freely-fix-execution / skill:freely-feat-execution → skill 里有完整约束和执行步骤
```

## Decision

三个修复均为低风险单行/文档修改：

| Bug | 修复 | 文件 | 行数 |
|---|---|---|---|
| freely-db-cli syntax | 补回 `for k in (` | `freely-db-cli` | 1 行 |
| AGENTS.md flow | 重构入口为"或"分支，显式列出 feedback | `AGENTS.md` | ~25 行 |
| Hook message | 指向 skill，加反绕过警告 | `pre-commit.sh` | ~10 行 |

**决策：promote**。三个 bug 根因明确，修复简单，无争议。
