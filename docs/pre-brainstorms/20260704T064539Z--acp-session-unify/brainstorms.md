---
b1_id: B1-20260704T064539Z
phase_state: completed
source_raw: raw-20260704T064539Z
source_url: https://github.com/chatterzhao/freely/issues/3726
produced_candidate: C-20260704T064539Z-A
created_at: 2026-07-04
---

# B1_IBM: 统一 ACP session 管理方法

## Input
- raw-20260704T064539Z (GitHub #3726)

## Problem

三个 agent role 的 ACP session 创建逻辑分散在多处，参数传递不一致，agent_working 记录不完整。

### session 创建的三条路径

| 路径 | Manager | Worker | Reviewer |
|------|---------|--------|----------|
| session/new | `_persist_session_anchor_early` → agent_assign (每 cycle) | watchdog_sse._acp_session_new | `_ensure_reviewer_agent` |
| session/fork | - | watchdog_sse._acp_session_fork | - |
| session/resume | - | - | - (不写 agent_working) |

### 当前 agent_assign 调用对比

| 参数 | Manager | Worker | Reviewer |
|------|:---:|:---:|:---:|
| raw_key | `__manager__` ✓ | from issue ✓ | from issue ✓ |
| role | `manager` ✓ | `worker` ✓ | `reviewer` ✓ |
| agent_id | `manager_01` ✓ | from pool ✓ | `reviewer_01` ✓ |
| session_id | `CLAUDE_SESSION_ID_CURRENT` (可能空!) | ✓ | ✓ |
| worktree | ✓ | ✓ | **未写** |
| branch | ✓ | ✓ | **未写** |
| slot | **未写** | 未确认 | 未确认 |
| test_worktree/test_branch | **未写** | 未确认 | **未写** |

### 命名问题

`CLAUDE_SESSION_ID_CURRENT` 存的是当前 tool 的 session ID（opencode/claude/codex/cline 都可能），不应带 CLAUDE 前缀。应改为 `TOOL_SESSION_ID_CURRENT`。

## Brainstorm

### Option A: 在 agent_working.py 中增加统一封装

新增 `acp_session_register()` 函数，session/new 和 session/fork 都调用它：

```python
def acp_session_register(project, raw_key, role, agent_id, session_id,
                         slot="", worktree="", branch="",
                         test_worktree="", test_branch=""):
    """所有 ACP session 创建的统一入口"""
    agent_assign(project, raw_key, role, agent_id,
                 session_id=session_id, slot=slot,
                 worktree=worktree, branch=branch,
                 test_worktree=test_worktree, test_branch=test_branch)
```

三个 role 差异仅在于 raw_key 来源和必填参数：
- Manager: raw_key=`__manager__`, slot 从 agent-table 取
- Worker: raw_key 从 worktree issue 绑定取
- Reviewer: raw_key 从 worktree issue 绑定取

### Option B: 在 freely 中增加 shell 封装

用 bash 函数封装统一调用，处理 role 差异。

问题：worker 的 session 是 watchdog_sse.py (Python) 创建的，manager 的是 shell 创建的——跨语言，shell 封装不到 Python 侧。

### Option C: 最小改动——补全缺失参数

不动架构，只补全 Manager 和 Reviewer 遗漏的参数。

问题：无法解决根本矛盾——三个调用点三套逻辑，每次新增 agent 都要手动对齐。

## Decision: Option A

在 `agent_working.py` 中增加 `acp_session_register()` 统一入口，三个调用点改为调用它。同时：
- 重命名 `CLAUDE_SESSION_ID_CURRENT` → `TOOL_SESSION_ID_CURRENT`
- Manager 写入时补全 slot、session_id
- Reviewer 补全 worktree、branch

## Candidate
- candidate_id: C-20260704T064539Z-A
- status: promoted
- milestone: M-20260704T064539Z-A
