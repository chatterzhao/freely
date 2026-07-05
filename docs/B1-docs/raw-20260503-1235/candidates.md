# Candidates - 20260503-1235--auto-recovery-race

## Candidate Issues

### C-20260503-1235-A: legacy issue

- title: `Defer manager_runtime_launch_workers_from_latest_handoff to after first AI patrol cycle`
- status: `promoted`
- adoption_type: `code_change`
- decision_reason: Root cause 已确认——`manager_runtime_recover_workers_if_needed` 在第一个 AI cycle 完成前调用 `manager_runtime_launch_workers_from_latest_handoff`（已标记为废弃旧路径），此时 fleet cache 未填充，worker launch 必然失败。该旧路径调用从未被移除，注释与代码不一致。
- promoted_issue_path: `docs/issues/I-20260503T1235Z-A/issue.md`
- milestone: `M-20260306-workspace-routing-foundation`
- source_brainstorm: `docs/B1-docs/raw-20260503-1235/brainstorms.md`
- session_refs:
  - {tool: ccds, session_id: "20260503-auto-recovery-race", role: "author"}
- next_action: 已完成实现，合并到 develop。
- revisit_trigger: 若修改后仍出现启动期 worker launch 失败，或后续重构移除了 `manager_runtime_launch_workers_from_latest_handoff`，则重新评估。

---

## Implementation Plan

### 1. 修改点：`manager_runtime_recover_workers_if_needed` 函数

**文件**: `docs/system/workspace/scripts/runtime/freely`

**当前代码**（第 15042-15052 行）：

```bash
manager_runtime_recover_workers_if_needed() {
  local project="$1" repo_root wt_path branch desired_state role_hint exit_reason supervisor_state recovered latest_continuity_file normalized_project normalized_wt_path
  ...
  reset_project_runtime_discovery_cache "$project"
  latest_continuity_file="$(latest_generated_manager_continuity_file_for_project "$project")"
  recovered="$(manager_runtime_launch_workers_from_latest_handoff "$project")"
  ...
```

**改为**：添加 `skip_continuity_recovery` 参数，控制是否执行 continuity-based recovery：

```bash
manager_runtime_recover_workers_if_needed() {
  local project="$1" repo_root wt_path branch desired_state role_hint exit_reason supervisor_state recovered latest_continuity_file normalized_project normalized_wt_path
  local skip_continuity_recovery="${2:-false}"  # ← 新增参数
  ...
  # continuity-based recovery (废弃旧路径): 仅当非首次 patrol 时执行
  if [[ "$skip_continuity_recovery" != "true" ]]; then
    reset_project_runtime_discovery_cache "$project"
    latest_continuity_file="$(latest_generated_manager_continuity_file_for_project "$project")"
    recovered="$(manager_runtime_launch_workers_from_latest_handoff "$project")"
    [[ "$recovered" =~ ^[0-9]+$ ]] || recovered=0
  fi
  ...
```

> 注意：`latest_continuity_file` 在函数后半部分（terminal exit contract 处理、freeze 检测中也有引用。如果 `skip_continuity_recovery=true` 时跳过了赋值，这些引用会使用空值。需要验证这些后续使用在空值时是否安全。

### 2. 修改点：supervisor 主循环的调用处

**当前代码**（第 18654 行）：

```bash
    # Process terminated workers once per cycle (not every watchdog tick)
    manager_runtime_recover_workers_if_needed "$PROJECT_ROOT" >/dev/null || true
```

**改为**：传入 FIRST_ROUND 作为 skip flag：

```bash
    # Process terminated workers once per cycle (not every watchdog tick)
    # On first cycle, skip continuity-based recovery — fleet cache not populated yet.
    # Workers are launched via post-AI-cycle handler (delegate_workers exit contract).
    manager_runtime_recover_workers_if_needed "$PROJECT_ROOT" "$FIRST_ROUND" >/dev/null || true
```

同时更新第 18637-18640 行的注释，使其准确反映当前实际行为：

```bash
    # FIRST_ROUND guard: continuity-based worker recovery (manager_runtime_launch_workers_from_latest_handoff)
    # is skipped on the first cycle because the fleet cache isn't populated until build_prompt runs.
    # Startup recovery created 3+ simultaneous ACP sessions
    # (manager + workers) collapsing the bridge in <60s.
    # Workers are launched via post-AI-cycle handler (delegate_workers exit contract).
```

### 3. 验证 `latest_continuity_file` 在 skip 分支中的引用安全

在 `manager_runtime_recover_workers_if_needed` 中，`latest_continuity_file` 在以下位置被引用：

| 行号 | 用途 | 受 skip 影响？ |
|------|------|----------------|
| 15050 | 赋值为 continuity-based recovery 的输入 | 跳过赋值 → 空值 |
| 15140 | `manager_continuity_explicitly_freezes_worker_project` 检测 | 空值 → `continue` 条件为 false → 走正常 recovery 路径 |

**第 15140 行的行为分析**：
```bash
if manager_continuity_explicitly_freezes_worker_project "$project" "$wt_path" "$latest_continuity_file"; then
```
当 `latest_continuity_file` 为空时，`manager_continuity_explicitly_freezes_worker_project` 第 2 行有守卫：
```bash
[[ -n "$continuity_file" && -f "$continuity_file" ]] || return 1
```
空值会导致 return 1（false），所以不会误判为 frozen。这是安全的。

**结论**：跳过后 `latest_continuity_file` 为空对后续逻辑无负面影响。

### 4. 后-AI-cycle 处理（已存在，无需修改）

第 19110-19146 行的现有逻辑负责在 AI cycle 结束后通过 exit contract launch worker：

```bash
exit_contract_action="$(project_runtime_handle_exit_contract_after_ai_cycle ...)"
...
if [[ "$exit_contract_action" == "delegate_workers" ]]; then
  manager_runtime_launch_workers_after_ai_cycle_if_needed "$PROJECT_ROOT" ... 
fi
```

这是**新路径**，不受本次修改影响。首次 AI patrol 完成后，如果 AI 产出了 `delegate_workers` exit contract，worker 会通过此路径被 launch。

### 5. 与现有 `manager_runtime_launch_workers_after_ai_cycle_if_needed` 的关系

| 维度 | manager_runtime_launch_workers_from_latest_handoff (旧路径) | manager_runtime_launch_workers_after_ai_cycle_if_needed (新路径) |
|------|------|------|
| 触发时机 | 每个 cycle 开始前 | AI cycle 完成后，exit_contract == delegate_workers |
| 输入源 | continuity markdown (awk regex) | exit_contract 的 WORKER_PROMPTS_CSV |
| 是否废弃 | 是，已标记 abandoned | 是，当前推荐路径 |
| 本修改 | 首 cycle 跳过，后续保留作为兼容兜底 | 不修改 |

新路径已经在正常工作，旧路径保留为兼容兜底（处理非 delegate_workers 场景下的 worker recovery）。

### 6. "First Patrol Complete" 的检测机制

`FIRST_ROUND` 变量在第 18603 行初始化为 `true`，在第 19104 行（AI cycle 结束后）设置为 `false`：

```bash
# 第 18603 行（cycle 开始前）
local FIRST_ROUND=true

# 第 19104 行（cycle 结束后）
FIRST_ROUND=false
```

这个变量天然适合作为"是否已完成首次 patrol"的信号。使用 `FIRST_ROUND` 作为 guard 不需要引入新的状态变量或文件标记。

### 7. Edge Cases 分析

| 场景 | 行为 | 正确性 |
|------|------|--------|
| 首次启动（无 continuity file） | `manager_runtime_launch_workers_from_latest_handoff` 返回 0，skip 无影响 | ✅ |
| 重启（有 continuity file） | 首 cycle skip，第二 cycle 正常 recovery | ✅ |
| 首次 AI cycle 失败（auth error） | 第 19104 行仍设置 `FIRST_ROUND=false`，第二 cycle recovery 执行 | ✅ — 即使首轮失败，daemon 已在运行，cache 可用 |
| Terminal exit contract 处理 | 不受 skip 影响，仍在每个 cycle 执行 | ✅ |
| Worker supervisor state reconciliation | 不受 skip 影响，仍在每个 cycle 执行 | ✅ |
| ACP bridge mode | deferral 在 supervisor 层，不涉及 AI adapter | ✅ |
| 多次重启、restart storm | 首 cycle skip，第二 cycle recovery 有 restart_storm 守卫 | ✅ |

### 8. 测试计划

#### 新增测试

**测试 1：首次 cycle 不触发 continuity recovery**
- 设置场景：已有 continuity file + 可恢复 worker prompt
- 验证：首次 cycle 中 `manager_runtime_launch_workers_from_latest_handoff` 不被调用
- 验证：第二次 cycle 中该函数被调用

**测试 2：terminal exit contract 处理在首次 cycle 不受影响**
- 设置场景：已有 terminal exit contract 的 worker worktree
- 验证：首次 cycle 中 `materialize_manager_worker_terminal_continuation` 仍被调用

**测试 3：后-AI-cycle worker launch 正常工作**
- 现有测试验证 `manager_runtime_launch_workers_after_ai_cycle_if_needed` 的行为
- 确认修改不破坏此路径

#### 回归测试

- `test-freely-manager-runtime-recovery` 系列测试应全部通过
- `test-freely-manager-worker-launch-*` 系列测试应全部通过
- 重点关注 `test-freely-manager-runtime-recovery-skips-*` 系列的 freeze/conflict 检测

### 9. 修改文件清单

| 文件 | 修改类型 | 说明 |
|------|----------|------|
| `docs/system/workspace/scripts/runtime/freely` | 修改 | 第 15042 行函数签名添加参数；第 15049-15052 行添加 guard；第 18637-18640 行注释更新；第 18654 行传递 FIRST_ROUND |
