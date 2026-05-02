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

## First-hop route judgment (2026-03-19)

### Demand pool scan

- `docs/milestones.md`
  - 已存在更高优先级的 committed issue 处于 `in_verification`、`in_ibm` 与 `in_dev`
  - 但当前 `20260319-0220--watchdog-control-plane-governance` 尚未写入 active milestone，属于需要补齐映射的新 discovery
- progress / recovery
  - 当前仓库尚未启用与本问题对应的 `docs/progress/**` 或 `docs/recovery/**`
  - 因此不能把本轮问题伪装成 continuation
- review / test
  - 已有 `test-watchdog-control-plane-skills` 等验证覆盖现有 watchdog skill 接线
  - 目前没有新的失败测试或 code-review 直接要求进入 dev-loop
- human chat / session evidence
  - 当前会话明确要求进入 Freely 首跳闭环，并核对 watchdog control plane 研究线的路由
  - `docs/pre-brainstorms/CONVERGENCE.md` 已记录旧工位 `materialize_then_retire` 的 handoff 证据
- github issue
  - 本轮未发现新的 github issue 输入
- `docs/PROJECT_INTENT.md`
  - 本轮问题属于治理命名、监督控制面与 worktree retirement 承接，仍符合“从 chat / session evidence / 治理漂移中发现问题，再先收敛为 candidate”的产品方向

### Route judgment

- source_class: `discovery`
- current_pool: `human chat / session evidence` with milestone sync and disposition backfill required
- route_kind: `pre_brainstorm`
- target_skill: `doc-pre-brainstorm-execution`
- selected_tool: `codex`
- why_selected:
  - 当前需要直接修改仓库内的 pre-brainstorm 与 milestone 产物
  - 当前剩余工作是把已吸收的治理结论重新绑定到正式 milestone / issue / skill，而不是直接继续实现
  - 当前运行工具已经是 `codex`，按首跳协议必须在本会话内继续第二跳，而不是只输出 `next_prompt`

### Why not a new IBM issue

1. umbrella taxonomy、skill/runtime 边界与 retirement disposition 的主要内容已经分别被现有正式 issue 和 `watchdog-control-plane` skill 吸收，不适合再重新物化成一个新的单体 IBM issue。
2. 当前缺的不是更多研究，而是把候选与已有 `I-20260318-1630`、`I-20260318-1408`、`I-20260319-0018` 及 `watchdog-control-plane` skill 的承接关系写清。
3. 旧 worktree retirement 已在 `docs/pre-brainstorms/CONVERGENCE.md` 留痕；当前需要的是 disposition 对齐与归档，而不是重开 issue。

### Binding result

- `C-20260319-0220-A`
  - 已被 `docs/system/workspace/skills/watchdog-control-plane/SKILL.md` 与 `I-20260318-1630` / `I-20260318-1408` / `I-20260319-0018` 吸收
  - disposition: archive，不新开 IBM
- `C-20260319-0220-B`
  - availability 与 runtime extraction 已被 `watchdog-control-plane`、`ai-cli-availability-manager`、`runtime/freely` 与 `I-20260318-1630` 吸收
  - continuity extraction 已确认进入稳定 issue `I-20260319-0018` 的 IBM 收口
  - disposition: promote 到既有 issue，下一跳走 `doc-ibm-execution`
- `C-20260319-0220-C`
  - 已被 `docs/pre-brainstorms/CONVERGENCE.md` 的 `materialize_then_retire` handoff 与当前 brainstorm 的 retirement heuristic 吸收
  - disposition: archive，不新开 IBM

### Workspace judgment

- current_worktree: `feature/watchdog-control-plane-governance-20260319`
- workspace_action: `continue_current_worktree`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`

### Next recommended action

- 继续作为 `pre_brainstorm` 留在 `docs/pre-brainstorms/20260319-0220--watchdog-control-plane-governance/`
- 把 A / C 从 active candidate queue 收口为 archive trace
- 把 B 提升并绑定到 `I-20260319-0018`，从 active candidate queue 移出
- 当前 pre-brainstorm 已完成 binding 和 archive，不再继续扩研究 scope
- 下一跳改为在 `I-20260319-0018` 中执行 `doc-ibm-execution`
- 待 `I-20260319-0018` 收口后，若无新增未吸收实现，再把本 pre-brainstorm 整体转入归档/退休
- 若后续发现新的未吸收实现或新的治理漂移，再重新进入 `doc-pre-brainstorm-execution`
