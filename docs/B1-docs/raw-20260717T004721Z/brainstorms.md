---
b1_id: B1-20260717T004721Z
phase_state: completed
source_raw: raw-20260717T004721Z
produced_candidate: C-20260717T004721Z-A
created_at: 2026-07-16
---

# B1_IBM: valid_sse_watchdog_pid_for_project 参数反转致活 watchdog 永判 invalid

## Input

- 来源：2026-07-16 runtime 排查（storm 病理调查中发现的独立缺陷）
- 现象：每次 status / self-heal / reconcile 对**活着的** sse-watchdog 触发 `startup_self_heal_stale_pid_cleared role=sse_watchdog`（误清 pid 文件）与 reconcile 误杀；2026-07-16/17 事件日志中每个 supervisor 启动周期均出现

## Problem

`docs/system/workspace/scripts/runtime/freely` ~L3570：

```bash
valid_sse_watchdog_pid_for_project() {
  local pid="$1" project="$2"      # ← 参数反转
  pid_matches_project "$pid" "$project" "runtime/sse-watchdog.sh --project" || return 1
```

所有调用方（`runtime_pid_valid_for_role`、`reconcile_control_plane_processes_for_active_runtime`、`sse_watchdog_pid_for_project`、`cmd_ensure_sse_watchdog_watch` 等）都按家族约定传 `(project, pid)`。反转后 `pid_matches_project` 拿项目路径当 pid 做 `kill -0`，恒失败 → 活进程永判 invalid。`fe8df8be9`（2026-06-23，SSE Watchdog 引入提交）带入，潜伏 3 周。

同族对照：`valid_ensure_manager_watchdog_pid_for_project`、`valid_interruption_dispatcher_pid_for_project` 均为 `(project, pid)` 顺序——本函数是唯一反例。

## Brainstorm

### Option A：改调用方传参顺序适配本函数
- 反对：违反函数族约定，调用方分散多处，改动面反而大且易再错

### Option B：改函数签名对齐家族约定 `(project, pid)`
- 单点修复，语义与家族一致；函数体内三处引用变量名不动（pid/project 交换声明即可）

## Decision: Option B

单行声明修复 + 回归断言（对活 sse-watchdog valid 判定必真）。

## 边界

- 只改 `valid_sse_watchdog_pid_for_project` 声明行；不改 sse-watchdog 生命周期逻辑、不改其他 valid_* 函数
- 与 raw-20260717T004620Z（已合并）、raw-20260717T004654Z（bridge）零重叠

## Candidate

- candidate_id: C-20260717T004721Z-A
- status: promoted
- milestone: M-20260717T004721Z-A
