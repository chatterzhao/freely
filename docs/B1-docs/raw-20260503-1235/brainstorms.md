# 预研头脑风暴：worker auto-recovery at startup fires before bridge/cache ready (GitHub #186)

## 背景

Issue #186 报告了一个 daemon 启动时的竞态问题：manager 的 worker auto-recovery 在 AI patrol 首次完成之前触发，此时 fleet cache 尚未填充，导致 worker launch 失败，进而引发 process churn / restart storm。

### 现场时间线

```
12:34:42 supervisor started
12:34:45 ACP bridge started
12:34:47 worker launch FAILED  ← auto-recover tried to launch worker!
12:34:47 target= (empty)       ← worktree cache not populated yet
```

从 supervisor 启动到 worker launch 失败仅间隔 5 秒，远短于一轮 AI patrol 的耗时。

## Root Cause 分析

### 故障链

```
daemon start
  → supervisor loop enters first cycle
    → select_launch_kind (确定本轮 launch 模式)
    → manager_runtime_recover_workers_if_needed   ← 第 18654 行
      → reset_project_runtime_discovery_cache       ← 清空缓存
      → manager_runtime_launch_workers_from_latest_handoff  ← 第 15051 行（旧路径）
        → materialize_worker_prompt_worktree_if_needed
          → worker_prompt_resolved_worktree
            → worktree_path_for_branch              ← 用 git worktree list 查分支
            → 返回空 target                          ← 分支/worktree 尚未就绪
        → launch 失败
    → build_prompt                                  ← 第 18680 行（首次 AI patrol 在此）
      → append_fleet_supervision_if_needed           ← 填充 fleet inventory
```

### 关键代码位置

**1. supervisor 主循环 (`freely` 第 18615-19198 行)**

```
18637: # Worker auto-recovery deferred to after first AI patrol cycle.
18638: # Startup recovery created 3+ simultaneous ACP sessions
18639: # (manager + workers) collapsing the bridge in <60s.
18640: # Workers now launched via post-AI-cycle handler only.
...
18654: manager_runtime_recover_workers_if_needed "$PROJECT_ROOT" >/dev/null || true
```

**矛盾点**：第 18637-18640 行的注释声明"auto-recovery 已推迟到首次 AI patrol 之后"，但第 18654 行仍然在每个 cycle（包括第一个 cycle）都调用 recovery。注释描述的是**期望状态**，但代码**未实际实现**。

**2. recovery 函数 (`freely` 第 15042 行)**

```bash
manager_runtime_recover_workers_if_needed() {
  ...
  reset_project_runtime_discovery_cache "$project"        # ← 清空 fleet cache
  latest_continuity_file="$(latest_generated_manager_continuity_file_for_project "$project")"
  recovered="$(manager_runtime_launch_workers_from_latest_handoff "$project")"  # ← 旧路径
  ...
  # 后半部分：处理 terminal exit contract、followthrough materialization（非竞赛相关）
}
```

**3. `manager_runtime_launch_workers_from_latest_handoff` 的设计注释**

```bash
# PREVIOUS APPROACH (abandoned):
#   manager_runtime_launch_workers_from_latest_handoff parsed worker
#   prompts from continuity markdown (awk regex). This was fragile:
#   - AI output format variations broke the regex parser
#   - Multi-layer gate checks (stale refs, launchable, etc.) filtered
#     out valid workers
```

**关键**：这已经是标注为"废弃旧路径"的代码。新路径是 `manager_runtime_launch_workers_after_ai_cycle_if_needed`（第 11996 行），它在 AI cycle 完成后通过 exit_contract 的 WORKER_PROMPTS_CSV 来 launch worker。

**4. 后-AI-cycle 处理 (`freely` 第 19110-19146 行)**

```bash
exit_contract_action="$(project_runtime_handle_exit_contract_after_ai_cycle ...)"
case "$exit_contract_action" in
  ...
  delegate_workers|continue|"")
    ;;
esac
if [[ "$exit_contract_action" == "delegate_workers" ]]; then
  manager_runtime_launch_workers_after_ai_cycle_if_needed "$PROJECT_ROOT" ...  # ← 新路径
fi
```

### 根本原因总结

1. **`manager_runtime_recover_workers_if_needed` 在第一个 AI cycle 完成前执行**，此时：
   - discovery cache 刚被 `reset_project_runtime_discovery_cache` 清空
   - AI patrol 尚未运行，fleet inventory 未刷新
   - 旧 continuity file 中的 worker prompt 可能引用不存在的分支或 worktree

2. **废弃旧路径 (`manager_runtime_launch_workers_from_latest_handoff`) 仍在新 cycle 中执行**。虽然已有多处注释说明它已被替代，但调用点从未移除。

3. **注释与代码不一致**：第 18637 行的 deferral 注释是 2026-05-01 左右设计新路径时写的，但旧路径的调用点未被删除或加上 FIRST_ROUND 守卫。

## 影响范围

- 所有 daemon 重启场景：无论是 operator stop 后重启，还是 crash 后由 watchdog 重启
- 首次 start 场景不受影响（无 continuity file → `manager_runtime_launch_workers_from_latest_handoff` 返回 0）
- 启动时 worktree 数量越多，旧 recovery 尝试 launch 的失败 worker 越多，process churn 越严重
