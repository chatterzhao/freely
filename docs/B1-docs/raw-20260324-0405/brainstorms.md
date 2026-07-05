# 预研头脑风暴：watchdog-restart-storm-and-process-churn-detection

## 背景

这轮在“三个 loop”重构中已经把一条关键职责写清：

- watchdog 可以观察 `restart storm / rapid relaunch churn / short-window process-count growth`
- 但 watchdog 只暴露 signal
- 是否属于 dead-loop / thrash，必须交给主管在 `auto-loop` 中裁决

问题是，这条能力目前只存在于 active truth / prompt contract 中，`runtime/freely` 并没有真正实现短窗口 churn 计数、signal 暴露和 manager escalation。

## 问题定义

当前 runtime 只覆盖：

- stalled manager / worker 检测
- ensure-manager / ensure-worker 的存活恢复
- availability watchdog 的账号探测、切号、等待与恢复

但还没覆盖：

- 短窗口内 AI 进程反复被拉起
- supervisor / ai 进程数异常增长
- restart/relaunch 频次已经从“正常恢复”演变成“thrash”

如果这条 contract 不实现：

- watchdog 可能持续盲目重启
- 主管虽在语义上拥有裁决权，但 runtime 没有足够 signal 交给它
- 最终会把 dead-loop 伪装成“系统很努力在恢复”

## 目标

1. 给 runtime watchdog 增加短窗口 churn signal，而不是只靠 stall
2. 让 signal 能进入 manager-owned `auto-loop` judgement，而不是 watchdog 自裁决
3. 把 signal 暴露到 `live-status` / `fleet-status`，成为可观测证据
4. 保持与现有 availability / runtime / continuity taxonomy 一致

## 非目标

1. 不在这条预研里直接重写整套 watchdog 架构
2. 不把业务阻塞与系统 thrash 混为一谈
3. 不让 watchdog 直接宣布任务完成、cleanup 或 worker dead-loop 语义裁决
4. 不在这里顺手扩 observability UI/TUI/API 产品面

## 候选方向

1. 在 runtime 层为 manager / worker supervisor 维护短窗口启动计数与时间窗
2. 当短窗口阈值命中时，写出结构化 signal：
   - `restart_storm_suspected`
   - `process_churn_suspected`
   - `signal_window_secs`
   - `signal_count`
3. signal 进入 manager continuity / launch-state / live-status，可被主管在 `auto-loop` 中消费
4. 命中 churn signal 后，watchdog 暂停盲重启，改为等待 manager judgement / handoff

## 真相面草案

- 原始 runtime signal 真相面：`session-state.env`
  - 适合承载短窗口计数、时间窗、上次 signal 时间、最近一次 escalation 理由
  - 属于 runtime 原生观察面，`live-status` / `fleet-status` 已经会消费它
- manager continuity：只承载主管对 signal 的治理裁决
  - 例如继续恢复、冻结 lane、kill/restart worker、重判 route
  - 不应作为 restart storm 原始计数真相面
- `live-status` / `fleet-status`：只做派生观察，不自判 dead-loop

## 最小字段草案

- `RESTART_STORM_WINDOW_SECS`
- `RESTART_STORM_COUNT`
- `PROCESS_CHURN_PEAK`
- `LAST_RESTART_STORM_SIGNAL_AT`
- `LAST_RESTART_STORM_SIGNAL_REASON`
- `LAST_RESTART_STORM_ESCALATED_AT`
- `LAST_RESTART_STORM_ESCALATION_TARGET`

## 交互草案

1. runtime watchdog 记录短窗口启动/重启/进程峰值
2. 阈值命中后写 `session-state.env` signal 字段
3. `live-status` / `fleet-status` 暴露 signal
4. watchdog 不继续无限盲重启，而是把当前轮切到 manager escalation
5. 主管在 `auto-loop` 中基于 signal + prompt/jsonl/cycle tail 判断：
   - 正常 recovery
   - stale prompt / route drift
   - dead-loop / thrash
6. 裁决结果再通过 continuity / handoff 写回 runtime

## 进入 IBM 前必须冻结的问题

1. signal 只放 `session-state.env`，还是还要同步到 `workcell-state.env`
2. manager escalation 触发后，watchdog 是完全暂停，还是进入低频观察模式
3. manager continuity 最小需要哪些字段，才能既不重复 signal 真相，又足够驱动 runtime followthrough

## 当前冻结结论

### 1. signal 真相面只放 `session-state.env`

- `session-state.env` 已经承载 runtime 原始观察信号，并被 `live-status` / `fleet-status` 消费
- `workcell-state.env` 当前职责是 `desired_runtime_state / last_supervisor_state / last_ai_state / last_exit_reason`
- restart storm / process churn 属于短窗口原始 signal，不应污染 `workcell-state.env` 的运行态镜像职责
- 因此这条能力默认不把 signal 镜像到 `workcell-state.env`

### 2. signal 命中后，watchdog 进入低频观察，不做盲重启

- 命中 signal 后，watchdog 不再继续当前轮的高频 blind relaunch
- 但也不应完全停死，否则人工插话、新 continuity、外部状态恢复都无法被及时吸收
- 更稳的语义是：
  - 先写 `session-state.env` signal
  - 触发 manager escalation
  - watchdog 进入低频观察/重查模式
  - 等待 manager continuity / handoff 决定下一步是恢复、冻结 lane、kill/restart 还是 route 重判

### 3. manager continuity 只带 signal ref 与治理裁决

- manager continuity 不重复 `RESTART_STORM_COUNT`、`PROCESS_CHURN_PEAK` 这类原始计数
- continuity 最小需要：
  - `runtime_signal_ref=session-state.env`
  - `runtime_signal_reason`
  - `runtime_signal_observed_at`
  - `restart_point`
  - `next_action`
  - `ownership`
- 也就是说，continuity 只表达“主管看到了什么 signal，以及决定 runtime 接下来怎么做”
- 原始 signal 数值仍回看 `session-state.env` 与 `live-status`

### 4. stall 与 restart storm 各判各的，不共用同一命中面

- `stall` 处理的是：AI 进程仍活着，但 prompt / cycle / continuity 已停止推进
- `restart storm / process churn` 处理的是：AI 或 supervisor 在短窗口内反复退出并被重拉
- 因此两者不应共用同一阈值或同一判据
- 建议顺序：
  1. 若 AI 仍活着，优先走现有 stall detection / recovery
  2. 若 AI 已反复退出并进入 supervisor restart churn，改由 restart storm signal 命中
  3. signal 命中后，watchdog 停止继续盲重启，把裁决权交给 manager `auto-loop`

### 5. 默认阈值先冻结成保守版本

- `RESTART_STORM_WINDOW_SECS=30`
- `RESTART_STORM_COUNT=4`
- `PROCESS_CHURN_PEAK=3`

冻结理由：

- 当前 runtime 本地 restart delay 默认是 `2s`
- 正常单次恢复或偶发两三次波动不应直接判成 thrash
- `30s / 4 次` 足以覆盖“短时间内明显重复拉起”
- `PROCESS_CHURN_PEAK=3` 则用于捕捉 supervisor / ai 异常并行膨胀，而不是单个正常 supervisor+ai 组合

## 代码与真源落点候选

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/manager-watchdog.sh`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `freely live-status` / `freely fleet-status` 对应输出面
- 相关 runtime tests

## 生命周期判断

- 这是 Freely 自举暴露出的 runtime control-plane 共性缺口
- 它不是当前“三个 loop”语义重构 issue 的一部分实现
- 它更接近 watchdog / manager supervision 家族的 follow-on implementation issue
- 当前已冻结：
  - signal 真相面写在 `session-state.env`
  - manager judgement 与 watchdog 低频观察的最小交互
  - continuity 只携带 signal ref 与 followthrough judgement
  - stall 与 restart storm 的判定面分离
  - counter/window 默认阈值
- 进入 IBM 前最后还要收紧：
  - signal 在 `live-status` / `fleet-status` 的具体展示格式
