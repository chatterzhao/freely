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
- 关联: raw-20260704T080808Z (多 bridge 并行)

## 当前耦合点 (7 处)

| # | 位置 | 耦合方式 | 问题 |
|---|------|---------|------|
| 1 | `_ensure_acp_bridge_running` freely:14034 | `base_tool="${AGENT_AI_TOOL:-claude}"` 内部取 Manager tool | 不能为其他 tool 启 bridge |
| 2 | daemon start freely:22152 | `_ensure_acp_bridge_running "$project"` 无 base_tool | 只启一个 bridge |
| 3 | cycle check freely:22241 | 同上 | 同上 |
| 4 | worker launch freely:13178 | `_manager_bridge_socket` 硬编码 | worker 只能用 Mgr bridge |
| 5 | watchdog `_acp_rpc` line 34 | `_acp_bridge_socket(project)` 无 base_tool | 所有操作同一 bridge |
| 6 | reviewer session freely:18770 | 硬编码 `/tmp/freely-acp-{hash}` | 同上 |
| 7 | `_acp_bridge_socket` freely:13910 | project_hash only | 不支持多 bridge 命名 |

## 解耦: 三层架构

```
Layer 1: Bridge Infrastructure (freely shell)
  _ensure_acp_bridge_running(project, base_tool)  ← 显式 base_tool 参数
  _acp_bridge_socket(project, base_tool)           ← per-tool socket
  socket: /tmp/freely-acp-{hash}.sock              (本期单 bridge)
          /tmp/freely-acp-{hash}-{base_tool}.sock  (下期多 bridge)

Layer 2: Session Management (agent_working.py)
  acp_session_connect(project, raw_key, role, agent_id, slot, ...)
    → base_tool = slot.split('-')[0]
    → bridge = _acp_bridge_socket(project, base_tool)
    → new/fork/resume/prompt 都走这个 bridge
    → 不知道 bridge 细节，只传 slot

Layer 3: Agent Logic (watchdog, freely)
  Manager:  acp_session_connect(_, '__manager__', 'manager', _, manager_slot)
  Worker:   acp_session_connect(_, raw_key, 'worker', _, worker_slot, message=task)
  Reviewer: acp_session_connect(_, raw_key, 'reviewer', _, reviewer_slot, message=review)
  不知道 bridge 存在，只传 slot
```

## 本期关键改动

### 1. _ensure_acp_bridge_running 接受显式 base_tool

```bash
# Before: 内部从 AGENT_AI_TOOL 取
_ensure_acp_bridge_running() {
  local project="$1"
  local base_tool="${AGENT_AI_TOOL:-claude}"  # ← Manager 的 tool

# After: 显式传入
_ensure_acp_bridge_running() {
  local project="$1" base_tool="${2:-claude}"
```

### 2. _acp_bridge_socket 接受 base_tool（本期忽略）

```bash
_acp_bridge_socket() {
  local project="$1" base_tool="${2:-}"
  # 本期: 忽略 base_tool，始终返回唯一 socket
  echo "/tmp/freely-acp-$(_acp_bridge_short_hash "$project").sock"
  # 下期: echo "/tmp/freely-acp-$(_acp_bridge_short_hash "$project")-${base_tool}.sock"
}
```

### 3. 调用方变化

```
daemon start:
  Before: _ensure_acp_bridge_running "$project"
  After:  _ensure_acp_bridge_running "$project" "${AGENT_AI_TOOL%%-*}"

worker launch:
  Before: _manager_bridge_socket="$(_acp_bridge_socket "$manager_project")"
  After:  _worker_bridge="$(_acp_bridge_socket "$manager_project" "$worker_base_tool")"
          # 本期 worker_base_tool == manager_base_tool（同 tool）→ 同一 socket → 行为不变

watchdog session:
  Before: bridge = _acp_bridge_socket(project)
  After:  bridge = _acp_bridge_socket(project, base_tool)
          # 本期所有 agent 同 tool → 同 socket → 行为不变
```

## Session 决策树

```
acp_session_connect(project, raw_key, role, agent_id, slot, message?, force_new?)
  → (session_id, operation_used)

  force_new? → session/new
  agent_working 有 session_id?
  ├─ 有 + slot 匹配
  │   ├─ alive + msg → prompt
  │   ├─ alive no msg → return id
  │   ├─ dead + msg  → resume → prompt
  │   └─ dead no msg → resume
  ├─ 有 + slot 不匹配 → new (安全)
  └─ 无 → 同 tool + mgr 有 session → fork(Mgr) : new

  任何操作失败 → 降级 new + 日志
```

## Candidate
- candidate_id: C-20260704T064539Z-A
- status: promoted
- milestone: M-20260704T064539Z-A
