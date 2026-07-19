---
b1_id: B1-20260719T101009Z
phase_state: completed
source_raw: raw-20260719T101009Z
source_url: https://github.com/chatterzhao/freely/issues/4010
produced_candidate: C-20260719T101009Z-A
created_at: '2026-07-19'
---

# B1: 跨 base_tool 的 session 创建——fork vs new

## 证据

daemon 日志：
```
worker_launch: contract_kind=delegate_workers
manager bridge socket not found; falling back to --agent mode (opencode)
worker session-id capture timed out after 30s
```

opencode bridge pid/socket/log 全无——从未启动。

## 全仓排查

### 路径 1: Worker fork (L13258-13266) ❌

```bash
_worker_slot=$("$PROJECT_ROOT/bin/agent-table-query" --get-slot worker_01)
_worker_base="${_worker_slot%%-*}"     # → "opencode"
_manager_bridge_socket="$(_acp_bridge_socket "$manager_project" "$_worker_base")"
# → /tmp/xxx-opencode.sock ← Manager 用的是 claude，不是 opencode！
```

查 socket 不存在 → fallback agent mode → 但 opencode bridge 未启动 → session/new 也超时。

### 路径 2: Reviewer session (L19137) ❌

```bash
_bridge_socket="$(_acp_bridge_socket "$PROJECT_ROOT")"  # 默认 Manager tool
```

Reviewer 用 cline，Manager 用 claude → socket 是 claude 的 → cline session/new 发到了 claude bridge → 失败。

### 路径 3: Python acp_session_connect (agent_working.py L87-172) ✅

```python
if base_tool == mgr_base or not mgr_base:
    # same → try fork
else:
    # cross-tool → new
return _do_new(...)
```

## 设计原则

不管什么 role（worker/reviewer/未来新增），跨 base_tool 统一处理：
- **同 tool** → fork from Manager bridge
- **不同 tool** → ensure target bridge running → session/new

## Fix

### L13258-13266: Worker fork 路径

```bash
# 改前
_worker_base="${_worker_slot%%-*}"
_manager_bridge_socket="$(_acp_bridge_socket "$manager_project" "$_worker_base")"

# 改后
_worker_base="${_worker_slot%%-*}"
_mgr_base="${AGENT_AI_TOOL%%-*}"
if [[ "$_worker_base" == "$_mgr_base" ]]; then
    # same tool → fork from Manager bridge
    _manager_bridge_socket="$(_acp_bridge_socket "$manager_project" "$_mgr_base")"
else
    # cross-tool → ensure Worker bridge, session/new
    _ensure_acp_bridge_running "$manager_project" "$_worker_base" || { ... }
    _manager_bridge_socket="$(_acp_bridge_socket "$manager_project" "$_worker_base")"
fi
```

### L19137: Reviewer session 路径

```bash
# 改前
_bridge_socket="$(_acp_bridge_socket "$PROJECT_ROOT")"

# 改后
_reviewer_base="${_reviewer_slot%%-*}"
_mgr_base="${AGENT_AI_TOOL%%-*}"
if [[ "$_reviewer_base" != "$_mgr_base" ]]; then
    _ensure_acp_bridge_running "$PROJECT_ROOT" "$_reviewer_base" || { ... }
fi
_bridge_socket="$(_acp_bridge_socket "$PROJECT_ROOT" "$_reviewer_base")"
```

## 不受影响

Manager 自身只用一个 tool，不涉及跨 tool。
acp_session_connect (Python) 已正确处理。
