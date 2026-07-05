---
b1_id: B1-20260704T064539Z
phase_state: completed
source_raw: raw-20260704T064539Z39Z
source_url: https://github.com/chatterzhao/freely/issues/3726
produced_candidate: C-20260704T064539Z-A
created_at: 2026-07-04
---

# B1_IBM: 统一 ACP session 管理 + Bridge 解耦

## Input
- raw-20260704T064539Z39Z (GitHub #3726)
- 关联: raw-20260704T080808Z08Z (多 bridge 并行, GitHub #3727)

## Problem

12 个分散的 session 操作调用点。agent_working 无 slot 列。Bridge 与 session 耦合（7 处）。

## 解耦: 三层架构

```
L1 Bridge Infrastructure (freely shell)
  _ensure_acp_bridge_running(project, base_tool)  ← 显式 base_tool
  _acp_bridge_socket(project, base_tool)           ← per-tool socket
  本期: 单 bridge, 签名预留

L2 Session Management (agent_working.py)
  acp_session_connect(project, raw_key, role, agent_id, slot, ...)
    → base_tool = slot.split('-')[0]
    → bridge = _acp_bridge_socket(project, base_tool)

L3 Agent Logic (watchdog, freely)
  只传 slot, 不知道 bridge 存在
```

## Session 决策树

```
acp_session_connect(project, raw_key, role, agent_id, slot, message?, force_new?)

  # ── 0. 显式要求 new ──
  force_new? → session/new  (gate review, 跨 base_tool, 用户显式)

  # ── 1. 有 session_id? ──
  查 agent_working → 有 session_id?
  ├─ 有 + alive + msg  → prompt
  ├─ 有 + alive no msg → return id
  ├─ 有 + dead + msg   → resume → ok → prompt
  │                              → fail → fallback new + log
  └─ 有 + dead no msg  → resume → ok → return
                                  → fail → fallback new + log

  # ── 2. 无 session，创建新 session ──
  #     两种 new: fork (同 base_tool) 优先于 session/new
  无 session_id
  ├─ 同 base_tool + mgr 有 session → fork(Mgr)
  │   fork 失败 → fallback new + log
  └─ 跨 base_tool → new + log
```

### fork 条件：同 base_tool，非同 slot

```
fork 只要求 ACP binary 相同。同 base_tool 不同 slot 完全可以 fork:
  Manager:  opencode-apikey-ds-flash 
  Worker:   opencode-apikey-openai-gpt
  → 同 base_tool = opencode → fork ✅ (不同 slot 不影响 fork)

fork 不行的只有跨 base_tool:
  Manager:  opencode-*
  Worker:   claude-*
  → base_tool 不同 → fork ❌ → session/new
```

### 两种 new

| 类型 | 场景 | 日志 |
|------|------|------|
| **fork** (优先) | 同 base_tool，无 session | 正常，不记日志 |
| **session/new** (主动) | 跨 base_tool，force_new，gate review | `"using new: {reason}"` |
| **session/new** (兜底) | resume 失败，fork 失败，未知异常 | `"falling back to new after {op} failed: {err}"` |

### 设计原则

**能 fork 必须 fork (同 base_tool):** 继承 context，缓存命中。不同 slot 也能 fork——slot 决定 model/provider，不影响 fork。

**resume 不预检 slot:** 不判断 slot 是否变了。直接尝试 resume——同 base_tool 不同 slot 可能成功，失败了自然回退 new + 日志。

**回退兜底:** 任何操作意外失败 → new + 日志。保证不阻塞，方便调试。

## 本期关键改动

### 1. agent_working 加 slot 列
```sql
ALTER TABLE agent_working ADD COLUMN slot TEXT DEFAULT '';
```

### 2. _ensure_acp_bridge_running 接受显式 base_tool
```bash
# Before: 内部取 AGENT_AI_TOOL
_ensure_acp_bridge_running() { local base_tool="${AGENT_AI_TOOL%%-*}"; }
# After
_ensure_acp_bridge_running() { local project="$1" base_tool="${2:-claude}"; }
```

### 3. _acp_bridge_socket 加 base_tool 参数 (本期忽略)
```bash
_acp_bridge_socket() { local project="$1" base_tool="${2:-}"; echo "/tmp/freely-acp-{hash}.sock"; }
```

### 4. acp_session_connect() 统一入口
```python
def acp_session_connect(project, raw_key, role, agent_id, slot,
                        message=None, force_new=False):
    """统一 session 操作选择。active detection + fallback safety net."""
```

### 5. 删除 watchdog 分散逻辑
- `_should_use_fork()`, `_create_reviewer_session()`
- `_acp_session_new/fork/resume/prompt` (4 wrappers)
- `_handle_needs_*` 中的 session 分发 if/elif

### 6. 命名修正
`CLAUDE_SESSION_ID_CURRENT` → `TOOL_SESSION_ID_CURRENT`

## Candidate
- candidate_id: C-20260704T064539Z-A
- status: promoted
- milestone: M-20260704T064539Z-A
