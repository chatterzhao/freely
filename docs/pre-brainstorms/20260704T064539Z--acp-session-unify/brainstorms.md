---
b1_id: B1-20260704T064539Z
phase_state: completed
source_raw: raw-20260704T064539Z
source_url: https://github.com/chatterzhao/freely/issues/3726
produced_candidate: C-20260704T064539Z-A
created_at: 2026-07-04
---

# B1_IBM: 统一 ACP session 管理 + Bridge 解耦

## Input
- raw-20260704T064539Z (GitHub #3726)
- 关联: raw-20260704T080808Z (多 bridge 并行, GitHub #3727)

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

  force_new? → session/new    (gate review, 跨 tool, 用户显式)

  查 agent_working → 有 session_id?

  ├─ 有
  │   ├─ slot 不同? → new + log("slot changed: {old} → {new}")
  │   │              主动检测，不浪费时间 resume
  │   │
  │   └─ slot 相同
  │       ├─ alive + msg  → prompt
  │       ├─ alive no msg → return id
  │       ├─ dead + msg   → resume → ok → prompt
  │       │                         → fail → new + log("resume failed: {err}")
  │       └─ dead no msg  → resume → ok → return
  │                                 → fail → new + log("resume failed: {err}")
  └─ 无
      ├─ 同 tool + mgr 有 session → fork(Mgr)
      │   fork 失败 → new + log("fork failed: {err}")
      └─ 跨 tool → new + log("cross-tool, using new")
```

### 设计原则

**主动检测 (主路径):** slot 变了直接 new，日志清晰记录原因。不浪费 time+cost 尝试必然失败的 resume。

**回退兜底 (安全网):** resume/fork 意外失败 → new + 日志。即使同 slot 理论上应该成功，runtime 也可能出问题（bridge 重启等），兜底保证不阻塞。

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
