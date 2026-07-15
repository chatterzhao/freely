---
b1_id: B1-20260715T055018Z
phase_state: completed
source_raw: raw-20260715T055018Z
created_at: 2026-07-15
---

# B1_IBM: scan 缓存过期 + auto→listen 通用降级

## Input
- raw-20260715T055018Z: daemon start 不刷新 scan + tool_unproductive 不触发 listen

## Problem

### 缺陷 1: daemon start 不刷新 scan 缓存
`task_source_scan_regeneration_reason_for_project` 返回 1（无刷新原因）时，`append_task_source_patrol_seed_if_needed` 复用旧缓存。手工启动 daemon 后，旧缓存可能已过期（停止期间 scan 状态变化），导致 prompt 无数据。

### 缺陷 2: tool_unproductive 不触发 auto→listen
`manager_runtime_handle_exit_contract_after_ai_cycle` 中 stop_ai→listen 仅针对 `kind=="stop_ai"`。`tool_unproductive` 走 default `continue`，mode 永远 auto，形成重启循环。

## Decision

### 修复 1: start_project_runtime 清理旧 scan
在 `ensure_task_mode_gate` 后删除 `manager-task-source-scan-latest.json`。首次 `build_prompt` 的 `append_task_source_patrol_seed_if_needed` 发现文件不存在 → `bootstrap_missing_scan` → 重新 scan。

改动：1 行 `rm -f`

### 修复 2: 通用 auto→listen 降级
将 `auto + scan==0 → listen` 从 `stop_ai` case 内提到 case 外——auto 模式下，无论 AI 以何种原因退出，scan 无 ready 即切 listen。

改动：~10 行重构，提升判断层级

## Candidate
- candidate_id: C-20260715T055018Z-A
- status: promoted
- milestone: M-20260715T055018Z-A
