# Watchdog Control Plane Governance

## Trigger

Freely 当前已经在 `develop` 里具备以下能力：

- `freely ensure-manager` 负责外层拉起主管
- `runtime/freely` 能在账号不可用时 defer 给更外层 watchdog
- `manager-watchdog.sh` 能对 worker 做脚本级恢复
- `token-efficient-session-continuity-and-rotation` 已开始把 continuity / rotation / fresh_with_handoff 收成正式边界

但“watchdog”这个名字当前仍有两种混用：

1. 有时它被当成“账号切换器”
2. 有时它又被当成“所有外层监督/恢复动作的总称”

这会带来两个问题：

- 名称过窄时，会把 watchdog 锁死在 `account switch`，不利于承接 `continuity`、`context warn/rotate`、`manager bootstrap` 等监督能力。
- 名称过宽但没有分层时，又会把账号可用性、进程拉起、continuity 治理、Freely 专有 handoff 全塞进一个脚本，形成新的大泥球。

同时，旧 worktree `feature/independent-ai-watchdog-productization-20260318` 已完成“提出产品化和退休策略问题”的职责，但它留下的唯一提交仍未被新的治理线正式承接。

## Current State

当前代码与文档中，watchdog 相关能力已分散在三层：

### 1. 可复用能力层

- `docs/system/workspace/skills/ai-cli-availability-manager/SKILL.md`
- 关注点：账号可用性、限流检测、认证失败、切号、恢复集成

问题：
- skill 名字和内容目前仍偏向“AI CLI availability/account switch”
- 还没有把 “watchdog 是 umbrella control plane” 的上层命名讲清
- skill 里仍以 agent 调用视角写得较多，未明确“全局脚本也可复用 skill 脚本”这一层

### 2. Freely runtime / orchestration 层

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/manager-watchdog.sh`

这里已经承载：
- ensure-manager
- manager bootstrap handoff
- worker recovery
- 对全局账号不可用的 defer

问题：
- 一部分本可复用的账号探测/切号逻辑仍容易继续堆在 `runtime/freely`
- Freely 专有语义和可抽离能力尚未完全拆开

### 3. Governance / continuity 层

- `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/**`
- `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/**`
- `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/**`

这里已经在文档上接近形成三种不同 owner：

- account / service availability
- manager / worker runtime recovery
- continuity / session rotation

但缺少一个更高层的命名与职责图，把它们统一视为同一个外层 control plane。

## Problem

Freely 现在不是“没有 watchdog”，而是“watchdog 的命名和控制面边界还不够稳定”。

如果现在直接退休旧 worktree，而不先补这一层治理承接，会留下三类后患：

1. 后续任何关于 context monitor / continuity guard 的讨论，都可能继续争论“这算不算 watchdog”
2. `skill` 与 `runtime/freely` 的逻辑会继续双向渗透，复用能力不稳定
3. 历史 worktree retirement 会失去一个统一的 disposition 框架，只能逐条口头判断

## Direction

把 `watchdog` 正式上提为 umbrella term：

- `watchdog = outer supervision and recovery control plane`

在 umbrella 下至少拆成三类子职责：

### A. Availability Watchdog

owner:
- 可复用 skill / 脚本层

职责：
- account availability probe
- auth failure / rate limit detection
- switch account
- wait until earliest reset
- emit structured recovery state

不负责：
- Freely milestone / issue / worktree 编排
- Freely 专有 continuity artifact 写回

### B. Runtime Watchdog

owner:
- Freely runtime / project orchestration 层

职责：
- ensure manager alive
- recover expected workers
- consume availability watchdog result
- 写 manager bootstrap handoff

不负责：
- 把账号策略再重写一遍
- 替 AI 做语义压缩

### C. Continuity Watchdog

owner:
- Freely continuity governance + runtime trigger matrix

职责：
- context warn / rotate
- continuity artifact target selection
- fresh_with_handoff trigger
- resume vs restart boundary

不负责：
- account switching
- worker fleet orchestration

## Naming Judgment

不建议把现有所有能力都塞进一个字面上的 `watchdog.sh`。

更合理的是：

- `watchdog` 作为控制面总称
- 各子能力保留明确前缀，如：
  - `availability-watchdog`
  - `manager-bootstrap watchdog`
  - `continuity watchdog`

对应到 skill / script / issue 时，也保持同样分层，而不是让“watchdog”直接等于“切号”。

## Skill Boundary Judgment

你的判断是对的：Freely 应优先把“可复用能力”收进 skill，而不是继续把逻辑散落在多个 runtime entrypoint。

但 skill 只应承载：

- 可复用策略
- 通用脚本
- 参数约定
- 测试与文档真源

不应承载：

- `develop` manager worktree 假设
- Freely 的 manager bootstrap handoff 语义
- Freely 特有的 `milestone / issue / worktree fleet` 决策

因此更稳的分层是：

- skill 真源：availability / probe / switch / wait / target-agnostic restart policy
- Freely runtime：manager bootstrap / worker recovery / Freely-specific handoff

## Old Worktree Disposition

对 `feature/independent-ai-watchdog-productization-20260318` 的判断：

- status: `materialize_then_retire`
- reason:
  - 它的实现价值已大量进入 `develop`
  - 剩余独有价值主要是命名、产品化边界、历史 worktree retirement heuristic
  - 这些内容更适合作为新的治理 pre-brainstorm 输入，而不是继续保留老 worktree 作为活跃执行枝

handoff target:
- `docs/pre-brainstorms/20260319-0220--watchdog-control-plane-governance/*`

retirement precondition:
- 新 pre-brainstorm 已记录 umbrella term、skill/runtime 分层、旧 worktree disposition

retirement after:
- 旧 `20260318-1735` 研究结论被新线吸收
- cleanup 结果记录到允许的治理留痕位置

## Worktree Retirement Heuristic Update

在旧研究线基础上补一条更强的判断：

- 若历史分支的剩余价值主要是“治理命名、分层结论、retirement heuristic”，优先转交到新的 pre-brainstorm，再退休旧分支
- 若历史分支仍含未吸收实现，则不得只写文档退休，必须先决定 `promote / cherry-pick / materialize`
- 若历史分支只含纯研究文档且未进入当前 active milestone，可在完成 handoff 后退休，不必继续 restack `develop`

## Intended Landing

- `docs/pre-brainstorms/20260319-0220--watchdog-control-plane-governance/brainstorms.md`
- `docs/pre-brainstorms/20260319-0220--watchdog-control-plane-governance/candidates.md`
- `docs/pre-brainstorms/INDEX.md`

后续如继续 materialize，目标应是：

- skill 重命名 / 分层 issue
- runtime 与 skill 的脚本边界 issue
- 历史 worktree retirement/disposition issue
