# 预研：manager reactivation and fleet patrol

## Context

- 日期：2026-03-21
- 触发：当前 Freely 已经具备 manager supervisor、`freely live-status`、`fleet-status`、`ensure-manager --watch`、interruption dispatcher 和 worktree 维护类 skill。
- 已有能力：
  - runtime 层可通过 `ensure-manager --watch` 与 supervisor 循环维持 manager 工位运行
  - manager-agent 已定义项目级监督、委派、merge / cleanup 判断
  - `multi-worktree-supervision` 已定义项目级工位当前态与排班观察面
  - `worktree-maintenance-governance` 已定义 worktree audit / merge-prep / retirement handoff
- 缺口：
  - 现在更像“主管如果被拉起，就知道该怎么判断”
  - 但还缺一条更明确的能力，要求主管定期重新激活并主动巡检“哪些点位没有 worker 在推进”

## Problem

工作停滞不一定表现为进程死掉。

更常见的情况是：

1. 某个 phase 没有 worker 在推
- pre-brainstorm 有 candidate，但没人继续 materialize
- IBM / issue 已 ready，但没人进入 dev-loop
- issue 已完成实现，但 verification / promote / cleanup 没人收口

2. 某个 worker 已经退出，但状态仍挂在进行中
- `phase_state=in_dev`
- 实际没有 supervisor / ai 在跑
- 也没人做 recovery / handoff

3. 某个 worktree 已经只剩治理收尾
- issue 生命周期走完
- 但 worktree 没 merge-up
- 或 merge 了但没 cleanup

4. 某个新 signal 已进入系统，但没有被主管重新吸收
- human chat / interruption / runtime anomaly / worker-discovered gap
- 只是被记录，不代表已经重新进入正确 restart point

这说明：
- “主管活着”不等于“fleet 在被持续监督”
- 还需要一条更明确的 fleet patrol 能力，定期检查：
  - 现在谁在干活
  - 哪些应该有人干但没人干
  - 哪些已经做完但没人收口

## Why Existing Capabilities Are Not Enough

### `ensure-manager --watch`

它解决：
- manager 进程是否被重新拉起

它不解决：
- 主管被拉起后，是否主动做一轮项目级巡检
- 是否发现“没有 worker 在推进的 phase”

### `freely live-status`

它回答：
- 当前 supervisor / dispatcher / ai 是否活着
- 当前 prompt / continuity 在聚焦什么

它不直接回答：
- 整个 fleet 哪些 active issue / candidate / worktree 当前没有 owner
- 哪些 completed issue 仍没 cleanup

### `multi-worktree-supervision`

它更偏：
- 当前态观察
- checkpoint / dirty / runtime / freeze / integration 节奏

但还没有显式收束：
- patrol cadence
- stalled / orphaned phase 的发现规则
- “没有 worker 在推进”的标准

### `worktree-maintenance-governance`

它更偏：
- 单树审计
- merge / retire / closure

它不是主管定期巡逻规则本身。

## Proposed Direction

需要新增一条更明确的治理能力，暂定方向：

- `manager_reactivation_patrol`

它不替代现有 skill，而是位于其上层：

1. 确保主管被重新激活
- 通过 `ensure-manager --watch` 保证进程存在

2. 主管每轮先做 fleet patrol
- 先读 `live-status`
- 再读 `fleet-status`
- 再读 milestones / candidates / issue / progress / recovery

3. 巡检“没人推进”的点位
- candidate stuck
- issue done_ibm 但没进入 dev
- in_dev / in_verification 但无 runtime / 无 worker
- completed 但无 merge / cleanup

4. 发现后做 owner 判定
- runtime-owned
- worker-owned
- manager-owned

5. 输出下一步动作
- delegate worker
- request runtime recovery
- freeze
- merge
- cleanup
- reopen pre-brainstorm / IBM / verification

## Possible Acceptance Shape

1. manager supervision 真源中明确：
- 主管不是被动等 signal，而是定期 patrol fleet

2. 至少定义一条 stalled / orphaned 判定规则
- phase 有状态，但没有活跃 worker / runtime
- 或生命周期已走完但没有收口动作

3. `live-status + fleet-status + milestones/issue artifacts` 的组合读取顺序被固定

4. 当发现无人推进时，主管必须：
- 指定 restart point
- 指定 ownership
- 指定下一个 worker / runtime 动作

## Open Questions

1. 这条能力应落为：
- 新 skill
- 还是扩展 `multi-worktree-supervision`
- 或扩展 `worktree-maintenance-governance`

2. patrol cadence 是：
- 每轮 manager loop 默认执行
- 还是单独 watchdog / patrol worker

3. “没有 worker 在推进”的最小判定是否应结合：
- `live-status`
- `fleet-status`
- issue / progress / milestone phase_state
- continuity / recovery evidence

## Provisional Decision

更倾向于：

- 不新建一个完全独立的大 skill
- 而是 materialize 一个治理 issue，把：
  - manager reactivation
  - fleet patrol
  - stalled/orphaned phase detection
  - delegate / merge / cleanup followthrough

统一收束成主管监督协议的下一步增强。
