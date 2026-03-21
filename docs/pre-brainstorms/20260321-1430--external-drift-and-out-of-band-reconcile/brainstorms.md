# 预研：external drift and out-of-band reconcile

## Context

- 日期：2026-03-21
- 触发：本轮通过狗粮开发发现，Freely 的一些真实收口动作是在 Freely 之外完成的：
  - 手工 merge / cleanup
  - 人类直接修改仓库文件
  - 不通过 Freely 的 feature worktree 开发
  - runtime 掉线后，仓库状态已经前进，但 `.freely` 中的 intake / continuity / worktree 视图仍停留在旧状态

- 现象：
  - 仓库本身可能已经 clean / merged / promoted
  - 但 Freely 仍显示：
    - delegated intake 未吸收
    - continuity 指向旧 prompt / old branch
    - worktree/fleet 仍记录已经不存在或已收口的对象
    - `desired_runtime_state=running`，但 manager/worker 实际已不在运行

## Problem

Freely 当前更擅长处理“自己发起、自己推进、自己回写”的闭环。

但用户真实使用里，存在大量 out-of-band 情况：

1. 用户不用 Freely 开发
- 直接改文件
- 直接 merge / cleanup
- 直接删分支

2. 用户部分使用 Freely，部分不用
- Freely 记录了 intake / handoff / continuity
- 但后续实现或收口是手工完成的

3. runtime 本身掉线
- 仓库状态变了
- `.freely` 状态没变
- 主管下次看见的是“悬空中的旧世界”

这会造成一种治理漂移：

- Git / docs / milestone / issue 已进入新状态
- Freely runtime / intake / continuity / worktree 视图仍停留在旧状态

如果没有专门的 reconcile 能力：
- 主管会反复 trying to continue 已经完成的工作
- 旧 intake 会长期悬空
- `live-status` / `fleet-status` 不能代表当前真实仓库

## Important Constraint

这条问题不应凭感觉新造平行能力。

优先假设它应扩展到现有主管监督/治理真源之一：

1. `manager-reactivation-and-fleet-patrol`
- 因为它已经定义主管重激活后要做 fleet patrol
- 这里可以进一步扩成：
  - 不只看“有没有 worker 在推进”
  - 还要看“Freely 记录的状态是否已经被仓库现实越过”

2. `multi-worktree-supervision`
- 因为它已经是主管读取项目级工位总览的技能
- 这里可以增加：
  - Git / docs / intake / continuity 之间的 drift check

3. `worktree-maintenance-governance`
- 因为它已经处理 fleet closure / retirement / merge chain
- 这里可以增加：
  - out-of-band merge / cleanup 后的 writeback reconciliation

4. `state-sync-and-session-evidence-governance`
- 因为它已经负责状态词典与 session evidence 规范
- 这里可以增加：
  - “旧状态已被仓库现实覆盖”时的重对齐规则

## Proposed Research Question

Freely 应该具备一条怎样的能力，来处理：

> 仓库状态被外部修改，导致 Freely 的 intake / continuity / worktree 视图悬空时，主管如何检测、对齐并恢复？

重点不是“恢复进程”本身，而是：

1. 发现 drift
- Git 已 merged / cleaned / deleted
- 但 Freely 仍显示 delegated / in-progress / active worktree

2. 判断 drift 类型
- runtime-only drift
- worktree cleanup drift
- intake absorption drift
- continuity stale drift
- milestone / issue state drift

3. 输出 reconcile 动作
- absorb old intake
- mark runtime stale and restart from fresh checkpoint
- rewrite worktree/fleet closure evidence
- update milestone / issue / candidate / continuity
- declare retained blocker when not enough evidence

## Non-Goals

- 不把这条问题直接做成“万能修复器”
- 不以删除 `.freely` 状态文件作为默认方案
- 不通过新建独立大 skill 绕过已有 manager/worktree/state-sync 真源

## Expected Result

本条预研应回答：

1. 这条能力最该扩到哪条现有真源
2. 最小输入面是什么
- `live-status`
- `fleet-status`
- git truth
- docs truth
- intake truth
- continuity truth

3. 最小输出面是什么
- drift classification
- reconcile recommendation
- required writeback targets

4. Freely 下次遇到“用户没用 Freely 开发，或者手工改了文件”时，主管不应继续假设旧状态仍为真，而应先进入 reconcile

## Current Recommendation

结论先收敛：

这条能力最适合扩到现有的 `manager-reactivation-and-fleet-patrol` / `multi-worktree-supervision` 真源中，而不是新造平行 skill。

同时，不应重复发明主管职责边界。

现有 `manager-agent` 已经明确规定：
- 主管负责巡检、判断、解释、委派、监督完成
- 主管不直接做 doc-loop / dev-loop 实现
- 一旦进入“要做事”，应交给 worker、maintenance worker 或 runtime owner

所以这条预研新增的不是“主管也能修复 drift”，而是：
- 主管如何识别 `external drift`
- 主管如何把 drift 结构化成 `ownership + restart_point + next_action`
- 主管随后应把哪类 drift 委派到哪条已有能力

原因：

1. 这条问题首先是主管巡检问题，不是单纯 worktree cleanup 问题
- 触发点是：主管看到的 `live-status / fleet-status / milestone / issue / continuity` 已经落后于仓库现实
- 第一动作应是 `detect + classify + ownership + restart_point`
- 这正属于 manager patrol / project-level supervision 的边界

2. `worktree-maintenance-governance` 更适合承接发现后的局部治理动作
- 例如：
  - out-of-band merge / cleanup 之后的 fleet closure writeback
  - 需要 merge / retire / cleanup disposition 的工位核对
- 但它不是“主管每轮先判断仓库现实是否已经越过 Freely 记录”的首入口

3. `state-sync-and-session-evidence-governance` 更适合承接词典和写回规则
- 例如：
  - intake / continuity / runtime_state / session evidence 的规范字段
  - stale evidence 的写回口径
- 但它不是 standing-source patrol 的主职责承接点

4. `milestone-planning-and-state-maintenance` 更像发现 drift 后的专门委派对象
- 当 drift 主要表现为：
  - candidate / issue / milestone / completed queue 没同步
  - 已完成但未回写 milestone
- 此时主管应把它识别为 state-maintenance 问题并委派，而不是自己长期手工 reconcile

## Non-Redundant Boundary

这条能力必须遵守现有主管定义，不新增以下错误语义：

1. 不把主管变成 repair worker
- 主管不直接修改业务实现、不直接补 worker 级长期产物

2. 不把主管变成 runtime operator
- 账号切换、重启、等待、attach/resume 失败后的恢复，仍属于 `runtime-owned`

3. 不把主管变成万能 reconcile 脚本
- 主管只做：
  - `detect`
  - `classify`
  - `explain`
  - `delegate`
  - `supervise completion`

4. 对用户的输出应先是状态解释，再是委派决定
- 主管先告诉用户：
  - 发生了哪类 drift
  - 为什么当前 Freely 视图已不可信
  - 这件事将委派给谁处理
- 然后再由对应 owner 执行对齐

## Recommended Shape

推荐的能力结构：

1. 主承接真源：
- `manager-reactivation-and-fleet-patrol`
- `skill:multi-worktree-supervision`

2. 发现后的二级分流：
- `skill:milestone-planning-state-maintenance`
  - 负责 candidate / issue / milestone / progress / cleanup 的状态 reconcile
- `skill:worktree-maintenance-governance`
  - 负责 out-of-band merge / cleanup / retirement / fleet closure 核对
- `runtime-owned recovery`
  - 负责 supervisor down / continuity stale / attach/resume 不成立时的恢复动作

3. 不新增 parallel big skill
- 这条能力应被表述为：
  - `manager patrol` 新增 `external_drift / out_of_band_reconcile` 检查面
  - 而不是新增一个与 manager / supervision / maintenance 并列的大 skill

## Drift Classification Draft

主管在 patrol 中至少应区分：

1. `runtime_drift`
- `desired_runtime_state=running`
- 但 supervisor / ai / dispatcher 已下线
- 且仓库真相已经继续前进

2. `intake_absorption_drift`
- intake / delegated item 仍悬空
- 但相关 issue / docs / git truth 已显示该工作已被吸收或完成

3. `worktree_cleanup_drift`
- Freely 仍记录 active/retire-pending worktree
- 但 git/worktree/branch truth 已 merged / removed / cleaned

4. `continuity_stale_drift`
- 现存 continuity/session evidence 指向旧 branch / old prompt / old path
- 但当前可续接的真实执行上下文已经变化

5. `state_writeback_drift`
- candidate / issue / milestone / verification / cleanup 之间存在 canonical artifacts 不一致
- 例如 issue 已完成但 milestone 未 completed，或 cleanup 已完成但 issue 仍 in_verification

## Reconcile Output Draft

主管发现 drift 后，输出不应只是“有问题”，而应至少包含：

- `drift_kind`
- `ownership`
  - `runtime-owned`
  - `manager-owned`
  - `worker-owned`
- `restart_point`
  - `fleet patrol`
  - `candidate / milestone maintenance`
  - `worktree audit / closure`
  - `runtime recovery`
- `required_writebacks`
  - `milestones.md`
  - issue/progress/recovery
  - `.freely` runtime/session state
  - worktree/branch cleanup evidence
