# 预研头脑风暴：worker auto-recovery race (b1 iteration)

## Discovery — Issue 价值与时效性

**Raw issue**: raw-20260503T1235Z — "fix: defer worker auto-recovery to after first AI patrol"
**来源**: GitHub #186
**提出时间**: 2026-05-03T12:39Z
**当前状态**: GitHub CLOSED；已吸收为 `I-20260503T1235Z-A`，实现完成，待 merge 到 develop

**价值判定**: 该 raw issue 已被上游 `auto-recovery-race` worktree 完整处理——root cause 已确认、fix 已实现、I-issue 已 completed。本 B1 iteration（b1）在已有分析基础上做正式 B1_IBM 物料化，作为该系统工位的治理证据留存。

## Research — 根因分析

### 故障链

```
daemon start
  → supervisor loop enters first cycle
    → manager_runtime_recover_workers_if_needed
      → reset_project_runtime_discovery_cache (清空缓存)
      → manager_runtime_launch_workers_from_latest_handoff (已标记废弃的旧路径)
        → materialize_worker_prompt_worktree_if_needed
          → worktree_path_for_branch (查 git worktree list)
          → 返回空 target (分支/worktree 尚未就绪)
        → launch 失败
    → build_prompt (首次 AI patrol，填充 fleet inventory)
```

### 关键发现

1. **`manager_runtime_recover_workers_if_needed` 在第一个 AI cycle 完成前执行**，此时 discovery cache 刚被清空，AI patrol 尚未运行，fleet inventory 未刷新
2. **废弃旧路径仍在新 cycle 中执行**：`manager_runtime_launch_workers_from_latest_handoff` 已标记为 abandoned，但调用点从未移除
3. **注释与代码不一致**：supervisor 第 18637 行注释声明 deferral 已实现，但第 18654 行的调用点从未被守卫

### 已有实现

由先行 worktree `auto-recovery-race` 完成：
- `manager_runtime_recover_workers_if_needed` 接受 `skip_continuity_recovery` 参数
- supervisor 循环在第一个 cycle 传入 `$FIRST_ROUND=true` 跳过 continuity recovery
- 首次 patrol 完成后 worker 通过 exit_contract 的 `delegate_workers` 路径 launch
- 后-AI-cycle 处理（`manager_runtime_launch_workers_after_ai_cycle_if_needed`）已存在且不受影响

### 影响范围

- 所有 daemon 重启场景（operator stop 后重启、crash 后 watchdog 重启）
- 首次 start 不受影响（无 continuity file）
- 启动时 worktree 数量越多，旧 recovery 尝试 launch 的失败 worker 越多，process churn 越严重

## Decision

本 raw issue 已被完整处理，所有分析、实现、验证均在 `auto-recovery-race` worktree 完成。本 B1 iteration 确认该 issue 价值有效、分析结论正确、实现已完成。建议：

1. Candidate `C-20260503T1235Z-A` 保持 promoted 状态
2. I-issue `I-20260503T1235Z-A` 已完成，待合并到 develop
3. 本 B1 物料化作为治理证据留存，不改变已有的上下游引用关系

## References

- 先行分析: `docs/pre-brainstorms/20260503-1235--auto-recovery-race/brainstorms.md`
- 候选: `docs/pre-brainstorms/20260503-1235--auto-recovery-race/candidates.md#C-20260503T1235Z-A`
- 实现 issue: `docs/issues/I-20260503T1235Z-A/issue.md`
- 运行时脚本: `docs/system/workspace/scripts/runtime/freely`
