# Manager Reactivation Patrol

用于主管被 runtime 拉起后，先做一轮项目级巡检，而不是直接等下一条 signal。

## 输入顺序

1. `./bin/freely live-status --project <develop>`
2. `./bin/freely fleet-status --project <develop>` 或等价工位总览
3. `docs/milestones.md`
4. 当前 relevant issue / progress / recovery / candidate artifacts

## 巡检目标

主管每轮至少检查四类“应推进但没人推进”的点位：

1. `candidate stuck`
- 仍在 `candidate_issues`
- 有明确 `next_action`
- 但没有新的 worker 在继续 pre-brainstorm / IBM materialization

2. `phase orphaned`
- `phase_state=in_ibm|in_dev|in_verification`
- 但对应 worktree 没有活跃 supervisor / ai
- 且没有 recovery / handoff 正在接管

3. `completion without closure`
- issue / verification 已完成
- 但没有 merge-up / cleanup followthrough
- worktree 仍停在 active 状态

4. `runtime visible but owner missing`
- live-status 显示 supervisor / dispatcher / ai 已下线或异常
- 但没有明确 `runtime-owned` 恢复动作

## 输出

主管必须把巡检结果加工成：

- `ownership`
  - `runtime-owned`
  - `worker-owned`
  - `manager-owned`
- `restart_point`
  - `pre-brainstorm`
  - `candidate / milestone intake`
  - `IBM`
  - `dev`
  - `verification`
  - `progress / recovery continuation`
  - `runtime supervision / cleanup`
- `next_action`
  - `delegate`
  - `runtime_recovery_requested`
  - `freeze`
  - `merge`
  - `cleanup`

## 硬规则

- 主管重激活后，不得只确认“进程活着”就算完成。
- 主管必须先做一轮 standing-source patrol，再决定这轮最重要的 worker 动作。
- issue 已 completed 但 worktree 未收口，也属于 patrol 必查项。
- 不要求每轮关闭所有 worktree；但不得让 stalled/orphaned 点位继续无人认领。
