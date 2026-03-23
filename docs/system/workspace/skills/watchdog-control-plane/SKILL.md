---
name: watchdog-control-plane
description: 统一 Freely 的外层监督与恢复控制面，覆盖 availability watchdog、runtime watchdog 与 continuity watchdog 的职责边界，并提供可复用的 watchdog 脚本模块。
---

# skill:watchdog-control-plane

## 何时使用

- 需要判断某个“外层监督/恢复动作”到底属于 account、runtime 还是 continuity owner
- 需要抽离可复用 watchdog 能力，避免把策略继续堆进 `runtime/freely`
- 需要让 Freely 内部 runtime 与未来独立全局脚本共享同一套 watchdog 脚本真源

## 控制面分层

### 1. Availability Watchdog

职责：
- account availability probe
- auth failure / rate limit detection
- account switch
- earliest-reset wait / recheck
- 产出结构化恢复状态，交给上层 orchestration

代码真源：
- `scripts/availability-watchdog.sh`
- `skill:ai-cli-availability-manager` 作为窄入口说明

不负责：
- Freely 的 milestone / issue / worktree 编排
- Freely 专有 handoff 文本写回

### 2. Runtime Watchdog

职责：
- ensure manager alive
- recover expected workers
- consume manager-generated worker launch handoff and translate it into target worker runtime activation
- if the target worker is already active, trigger local continuation reentry instead of relaunching a second supervisor
- detect stalled AI processes when newer intake/continuation is pending, or when delegated continuation has already entered the manager prompt but no new continuity / handoff is emitted, then trigger runtime-owned recovery
- 消费 availability watchdog 结果
- 触发 Freely 专有 manager bootstrap handoff
- 暴露当前态控制面，让主管能直接看到活跃 pid、当前 prompt/continuity 聚焦点与 deep refs

实现承载：
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/manager-watchdog.sh`

不负责：
- 重写账号可用性策略
- 替 AI 做语义压缩

### 3. Continuity Watchdog

职责：
- context warn / rotate
- continuity artifact target selection
- `resume` vs `fresh_with_handoff` 边界
- continuity trigger matrix

事实来源：
- `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/**`
- `skill:continuity-watchdog`

不负责：
- account switch
- worker fleet recovery

## 设计规则

1. `watchdog` 是 umbrella term，不再等于“切号器”。
2. 可复用脚本优先落在 skill 下，而不是散落到多个 runtime entrypoint。
3. Freely 专有 orchestration 继续留在 runtime 层，不塞回 skill。
4. 新增 watchdog 能力时，先判断它属于 `availability / runtime / continuity` 哪一类，再决定代码落点。

## 当前模块

- `scripts/availability-watchdog.sh`
  - 提供 codex account cooldown、probe、switch、ensure-manager account readiness 等共享函数
  - 由 `runtime/freely` source 使用
- `freely live-status`
  - 提供 watchdog / runtime 当前态视图
  - 默认只展示活跃 supervisor / dispatcher / ai 与 prompt excerpt、continuity excerpt、deep refs
  - 供主管 supervision 轮次优先读取，而不是继续人肉拼 `ps + prompt + jsonl`

## 下一跳

- 若需要账号探测/切号实现细节：继续看 `skill:ai-cli-availability-manager`
- 若需要 Freely runtime 监督策略：继续看 `docs/system/workspace/scripts/runtime/freely`
- 若需要 continuity 触发边界：继续看 `skill:continuity-watchdog`
