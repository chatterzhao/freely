---
name: freely-watchdog-control-plane
description: >-
  统一 Freely 外层监督与恢复控制面。覆盖 availability、runtime、continuity
  三类 watchdog 的职责边界，提供可复用的 watchdog 脚本模块。

  Use when: 需要整体理解或修改 watchdog 架构，排查自主运行异常。
  触发词："watchdog"、"监督"、"恢复"、"avail"、"runtime died"。
---

# skill:freely-watchdog-control-plane

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
- reset buffer 与 cooldown_elapsed 后的真实 re-probe
- 产出结构化恢复状态，并写出 manager bootstrap handoff 供 runtime/manager 恢复链消费

代码真源：
- `scripts/availability-watchdog.sh`
- `skill:freely-ai-cli-availability-manager` 作为窄入口说明

不负责：
- Freely 的 milestone / issue / worktree 编排
- manager bootstrap handoff 的消费与后续 supervisor / fleet 编排

### 2. Runtime Watchdog

职责：
- ensure manager alive
- recover expected workers
- consume manager-generated worker launch handoff and translate it into target worker runtime activation
- if the target worker is already active, trigger local continuation reentry instead of relaunching a second supervisor
- detect stalled AI processes when newer intake/continuation is pending, or when delegated continuation has already entered the manager prompt but no new continuity / handoff is emitted, then trigger runtime-owned recovery
- detect stalled active workers after delegated continuation has already entered the worker prompt but cycle log / closeout no longer advances, then trigger worker-side runtime recovery
- detect restart storms / rapid relaunch churn / unexpected short-window process-count growth as dead-loop suspicion signals, then escalate the signal to manager-owned `auto-loop` judgement instead of blindly relaunching forever
- 消费 availability watchdog 结果
- 触发 Freely 专有 manager bootstrap handoff
- 暴露当前态控制面，让主管能直接看到活跃 pid、当前 prompt/continuity 聚焦点与 deep refs

实现承载：
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/manager-watchdog.sh`

不负责：
- 重写账号可用性策略
- 替 AI 做语义压缩
- 独自判定“这条 lane 是否业务上已死循环”；watchdog 只负责发现 churn / stall signal，terminal judgement 仍回到 manager

### 3. Continuity Watchdog

职责：
- context warn / rotate
- continuity artifact target selection
- `resume` vs `fresh_with_handoff` 边界
- continuity trigger matrix

事实来源：
- `docs/B2-docs/token-efficient-session-continuity-and-rotation-governance/**`
- `skill:freely-continuity-watchdog`

不负责：
- account switch
- worker fleet recovery

## 设计规则

1. `watchdog` 是 umbrella term，不再等于“切号器”。
2. 可复用脚本优先落在 skill 下，而不是散落到多个 runtime entrypoint。
3. Freely 专有 orchestration 继续留在 runtime 层，不塞回 skill。
4. 新增 watchdog 能力时，先判断它属于 `availability / runtime / continuity` 哪一类，再决定代码落点。
5. restart storm / process churn 是 runtime watchdog 的 signal，不是 worker 自报；一旦命中阈值，应交由主管在 `auto-loop` 中判断是正常 recovery、旧 prompt 漂移，还是 dead-loop / thrash。

## 当前模块

- `scripts/availability-watchdog.sh`
  - 提供 codex account cooldown、probe、switch、ensure-manager account readiness 等共享函数
  - 由 `runtime/freely` source 使用
- `freely live-status`
  - 提供 watchdog / runtime 当前态视图
  - 作为 day-1 `current-state plane`，默认只展示活跃 supervisor / dispatcher / ai、prompt excerpt、continuity excerpt、最小 acceptance 摘要与 deep refs
  - 供主管 supervision 轮次优先读取，而不是继续人肉拼 `ps + prompt + jsonl`
  - signal surface 可以暴露 stall / churn / dead-loop suspicion，但 terminal completion / delete judgement 仍必须沿 `acceptance_ref` 回 artifact plane

## 下一跳

- 若需要账号探测/切号实现细节：继续看 `skill:freely-ai-cli-availability-manager`
- 若需要 Freely runtime 监督策略：继续看 `docs/system/workspace/scripts/runtime/freely`
- 若需要 continuity 触发边界：继续看 `skill:freely-continuity-watchdog`

## Runtime Watchdog 现行机制锚点（2026-07-17 对齐）

- **supervisor 存活**：`supervisor-heartbeat` mtime（2s touch / `SUPERVISOR_HEARTBEAT_TIMEOUT_SECS=120` 超时 / 新生宽限 `SUPERVISOR_STARTUP_HEARTBEAT_GRACE_SECS=15`，以 supervisor.pid mtime 判代际）
- **判死动作**：verified teardown（TERM→KILL 兜底 + kill -0 验证消亡），禁止裸 TERM（daemon 有意忽略无 stop-marker 的 TERM）；不可杀 → `manager_watchdog_supervisor_kill_failed` + 本 tick 不拉新
- **storm/churn 检测**：`RESTART_STORM_WINDOW_SECS=120` / `RESTART_STORM_COUNT=10` / `PROCESS_CHURN_PEAK=3`；supervisor 死亡由 ensure-manager 侧 `record_supervisor_death_for_storm_window` 记入窗口；命中即升级 manager bootstrap handoff（advisory，不自动动作）
- 完整真源见 `three-loop-capability-lifecycle.md` §Runtime 监督面机制真源
