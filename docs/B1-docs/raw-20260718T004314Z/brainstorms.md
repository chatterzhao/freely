---
b1_id: B1-20260718T004314Z
phase_state: completed
source_raw: raw-20260718T004314Z
produced_candidate: C-20260718T004314Z-A
created_at: 2026-07-18
---

# B1_IBM: runtime L2120 孤儿行 source_project unbound 致 daemon start/status 静默死

## Input
raw-20260718T004314Z。2026-07-18 00:27 起 runtime 无法重启的排查产物。

## Problem（实测证据链）
1. `freely daemon start --task-mode auto` 输出仅 banner，静默 rc=1；events 停在 task_mode_written。
2. bash -x 全量 trace 终止于 manager_worker_launch_state_refresh_for_status 调用行（内部 trace 被调用点 `>/dev/null 2>&1` 吞）。
3. sourced probe 逐层缩小：refresh → reconcile_prompt_liveness → **`line 2120: source_project: unbound variable`**。
4. L2120 为孤儿行 `_agent_env="$source_project/.freely/agent-id.env"`（缩进异常 tab+空格，赋值无人消费）；git log -L 显示 commit aea0c5749（2026-06-27"fix: _agent_env defined before use"）坏编辑残留。
5. `source_project` 仅 sync-tooling 函数族有定义。set -u 下 unbound variable 是 shell 级致命错误，**绕过 `|| true` 与重定向防护**直接杀死整个进程——与本批 lane 已根修的"set -e 静默死"同类。
6. 触发条件：launch-state.env 存在且 LAST_MANAGER_CONTINUITY_* 条件满足（当前含 round-078 残留 prompts）→ 路径必达 L2120。此前 runtime 未触发是因旧 launch-state 走了 early return。

### P7（GREEN 阶段暴露的第二致命点）
删除 L2120 后 daemon status 仍死于同一 refresh 调用——`manager_reconcile_agent_id_env()` 内 `${PROJECT_ROOT}` 在 status 派发路径（startup_self_heal → refresh → reconcile）到达时尚未赋值（PROJECT_ROOT 全局仅 L3509 某些派发路径赋值），set -u 同样致命且被 `2>/dev/null` 吞。probe 设 PROJECT_ROOT 后存活证明该点：同一缺陷链第二实例。修复：函数内 `local _proj="${PROJECT_ROOT:-$SELF_ROOT}"` 回退（SELF_ROOT 脚本头部恒有值）。

## Brainstorm
### Option A: 删除 L2120 孤儿行 ✅
正确 _agent_env 逻辑在 manager_reconcile_agent_id_env() 内有默认参（`${1:-${PROJECT_ROOT}/.freely/agent-id.env}`），孤儿行纯冗余。
### Option B: 给孤儿行加 ${source_project:-} 默认
保留死代码且语义错误（该处根本不该有此赋值）。❌
### Option C: 顺带清理 launch-state 残留 prompts
状态清理属 runtime 自愈职责，代码修复后 reconcile 自会收敛；手工清状态掩盖复现路径。❌

## Decision: Option A
单行删除，根因消除。

## Candidate
- candidate_id: C-20260718T004314Z-A
- status: promoted
- milestone: M-20260718T004314Z-A
