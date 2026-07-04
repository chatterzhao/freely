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

### 1. Session 全生命周期

ACP session 有 5 种操作：

| 操作 | 触发者 | 触发时机 | agent_working |
|------|--------|---------|:---:|
| `session/new` | run-acp-prompt.py | launch_kind=fresh, resume 失败回退, fork 失败回退 | 各处离散 |
| `session/fork` | run-acp-prompt.py, watchdog_sse.py | launch_kind=fork, worker/reviewer 从 manager fork | 各处离散 |
| `session/resume` | run-acp-prompt.py | launch_kind=resume, session/prompt 失败回退 | **不写** |
| `session/prompt` | watchdog_sse.py | 向 alive session 投递消息 | 不写 |
| `session/close` | run-acp-prompt.py | AI cycle 结束 | agent_release |

### 2. 三个角色的 session 创建调用链

```
Manager:
  daemon cycle → _persist_session_anchor_early() (freely, shell)
    → agent_assign(raw_key="__manager__", role="manager", ...)

Worker:
  watchdog_sse._handle_needs_worker() (Python)
    → agent_get_session() 查活 session → session/prompt
    → 死 → _acp_session_fork(from manager) → agent_assign(...)
    → fork 失败 → _acp_session_new() → agent_assign(...)
    → 都没有 → delegate to Manager

Reviewer:
  watchdog_sse._handle_needs_reviewer() (Python)
    → agent_get_session() 查活 session → session/resume+prompt
    → 死 → session/new → agent_assign(update_only=True)
```

### 3. agent_working 表结构和写入逻辑

表结构: `raw_key | worktree | branch | test_worktree | test_branch | manager_id | worker_id | reviewer_id | created_at | updated_at`

{role}_id 列存格式: `agent_NN:session_id`（reviewer 可用逗号拼接多个）

DB upsert 逻辑 (freely_db_manager.py):
- **INSERT**: 新 raw_key → 写入 worktree, branch, test_worktree, test_branch + {role}_id
- **UPDATE**: 已有 raw_key → 只更新 {role}_id 列，**不更新** worktree/branch（这意味着如果创建时这俩为空，后续 UPDATE 也补不上）
- **reviewer_id 特殊处理**: APPEND 模式（逗号拼接），不覆盖已有 reviewer

### 4. 参数缺失详表

| 调用点 | raw_key | role | agent_id | session_id | slot | worktree | branch | 问题 |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|------|
| Manager (freely:4052) | ✓ | ✓ | ✓ | **可能空** | **未传** | ✓ | ✓ | session_id 在 agent_assign 时 CLAUDE_SESSION_ID_CURRENT 可能未设置 |
| Worker watchdog fork | ✓ | ✓ | ✓ | ✓ | **未传** | **未传** | **未传** | agent_assign 只传 (raw_key, role, agent_id:session_id)，不传 worktree/branch/slot |
| Worker watchdog new | ✓ | ✓ | ✓ | ✓ | **未传** | **未传** | **未传** | 同上 |
| Worker freely:5992 | ✓ | ✓ | ✓ | **未传** | **未传** | ✓ | **未传** | Phase 1 dual-write，只有 worktree |
| Reviewer watchdog | ✓ | ✓ | ✓ | ✓ | **未传** | **未传** | **未传** | update_only=True，不传 worktree/branch/slot |
| Reviewer _ensure_reviewer_agent | ✓ | ✓ | ✓ | ✓ | **未传** | **未传** | **未传** | 走 bridge socket 直接创建，不传 worktree/branch |

### 5. session/resume 不更新 agent_working

session/resume 复用已有 session，理论上不需要更新。但以下场景会导致 session_id 过时：
- bridge 重启后 session 丢失 → run-acp-prompt.py fallback 到 session/new → 新 session_id
- 此时 agent_working 里存的仍是旧 session_id

### 6. 命名问题

`CLAUDE_SESSION_ID_CURRENT` 出现在 3 个文件 11 处，存的是任意 tool 的 session ID（opencode/claude/codex/cline），不应带 CLAUDE 前缀。

## Brainstorm

### 核心问题：没有统一的 session 注册入口

session 创建 → agent_working 写入 这一对操作分散在 5 个调用点，每个点的参数完整度不同。应该是：**任何 session/new 或 session/fork 成功后，自动触发 agent_working 写入**。

### 方案 A: Python 统一入口 `acp_session_register()`

在 `agent_working.py` 增加：

```python
def acp_session_register(project, raw_key, role, agent_id, session_id,
                         slot="", worktree="", branch="",
                         test_worktree="", test_branch=""):
    """ACP session/new 或 session/fork 成功后的统一入口。
    
    所有 agent role 的 session 创建都调用此函数写入 agent_working。
    role 差异仅在于 raw_key 的语义:
      - Manager:  "__manager__" (无 raw issue 绑定)
      - Worker:   从 worktree issue 提取
      - Reviewer: 从 worktree issue 提取
    """
    # 从 agent-table 自动补充 slot（如果未传）
    if not slot:
        slot = _resolve_slot_from_agent_table(project, role, agent_id)
    
    agent_assign(project, raw_key, role, agent_id,
                 session_id=session_id, slot=slot,
                 worktree=worktree, branch=branch,
                 test_worktree=test_worktree, test_branch=test_branch)
```

调用点改为：
- Manager `_persist_session_anchor_early`: 调用 `acp_session_register`
- Worker watchdog `_handle_needs_worker`: fork/new 成功后调用
- Reviewer watchdog `_handle_needs_reviewer`: new 成功后调用
- Reviewer `_ensure_reviewer_agent`: 调用 `acp_session_register`

### 方案 B: 在 acp-bridge.py 层拦截

在 acp-bridge.py 的 `session/new` 和 `session/fork` handler 中，成功后自动写 agent_working。

优点：所有调用点自动覆盖，不需要逐个改。
问题：acp-bridge.py 不知道 raw_key、role、slot 等业务语义。需要调用方在 params 中传入。

### 方案 C: 最小改动补全参数

不动架构，只补缺失参数。

问题：5 个调用点各补一遍，下次新增 agent 又要补一遍。

## Decision: 方案 B（acp-bridge.py 拦截）+ 方案 A（Python 统一入口）组合

方案 B 补全 session/new 和 session/fork 的 params 传递，方案 A 提供统一写入函数。

具体：
1. `agent_working.py` 增加 `acp_session_register()` 统一入口
2. `acp-bridge.py` 的 session/new 和 session/fork handler 在成功后调用 `acp_session_register`（从 params 中取 raw_key/role/agent_id/slot/worktree 等）
3. 调用方（run-acp-prompt.py、watchdog_sse.py、freely shell）在 params 中传入完整参数
4. `CLAUDE_SESSION_ID_CURRENT` → `TOOL_SESSION_ID_CURRENT`
5. DB upsert 修复：UPDATE 时也更新 worktree/branch/test_*

### session/resume 的处理

session/resume 不创建新 session，但需要更新 agent_working 中的 session_id（防止 bridge 重启导致 session_id 变化）。在 agent_working.py 增加：

```python
def acp_session_update(project, raw_key, role, agent_id, session_id):
    """session/resume 成功后更新 session_id"""
    agent_assign(project, raw_key, role, agent_id, session_id=session_id)
```

## Candidate
- candidate_id: C-20260704T064539Z-A
- status: promoted
- milestone: M-20260704T064539Z-A
