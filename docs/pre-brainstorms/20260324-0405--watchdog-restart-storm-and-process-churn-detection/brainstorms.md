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
- 在进入 IBM 之前，需要先冻结：
  - signal 真相面写在哪里
  - signal 与 stall contract 如何并存
  - manager judgement 与 watchdog pause/retry 的最小交互
