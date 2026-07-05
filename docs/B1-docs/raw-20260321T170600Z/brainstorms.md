# Brainstorms: chat-triggered-worker-runtime-reactivation

## Problem

在真实狗粮中，worker 工位处于 `operator_stop` 后，`freely chat` 能把新插话写入 intake 并经 interruption dispatcher 归类，但不会把主 AI/supervisor 循环重新拉起。

表现为：
- `live-status` 显示 `activity_state: dispatch_only`
- `desired_runtime_state: stopped`
- 新 chat signal 变成 `delegated` intake
- 但没有新的 worker 主循环消费这条 signal

这会让 `freely chat` 看起来像能继续工作，实际上只是在堆积 delegated intake。

## Why It Matters

Freely 既然要求默认通过 `chat` 给 Freely 下任务，那么：
- 对 worker 工位，新的 chat signal 若需要继续当前 active issue，就必须能在正确条件下重激活 worker runtime
- 不能要求用户手动重新 `freely start` 才能让本轮 delegated continuation 真正推进

否则狗粮与用户产品面都会出现“插话成功但无人接棒”的假活性。

## Existing Truth Source Fit

这不是全新能力域，更像现有能力的缺口：
- `auto-loop-orchestrator`
- `interruption entrypoint/runtime preflight`
- `manager reactivation / patrol`
- worker side runtime re-entry

因此不应新造平行大 skill，而应扩现有 runtime/preflight/re-entry 真源。

## Scope Hypothesis

需要收敛的问题：
1. `freely chat` 在什么条件下应只写 intake，不启动 runtime
2. 在什么条件下应触发 worker runtime reactivation
3. `operator_stop`、`auth_failure`、`runtime-owned crash` 是否应区分
4. `delegated continuation` / `handoff://verification` 等 absorption target，哪些应该触发重入
5. reactivation 由谁负责：
   - chat entrypoint immediate preflight
   - interruption dispatcher
   - watchdog
6. 若当前工位已有 active AI 进程，则应走 graceful preemption / continuation，而不是重复启动第二个主循环

## Likely Direction

最可能的 canonical path 是：
- `freely chat`
- 写 intake
- 运行 interruption classification
- 若结果表明这是需要本工位继续推进的 worker-owned continuation / verification handoff，且当前 worker runtime 未运行
- 则执行 worker runtime reactivation preflight
- 再由重新拉起的 worker 主循环消费 delegated intake

## Non-Goals

- 不在本问题里重写 manager/worker 角色边界
- 不把任何 chat signal 都一律自动 start runtime
- 不用 PTY 注入解决“进程已停”的问题

## Evidence

- 2026-03-21: 在 `feature/codex-session-reentry-and-pty-input-20260321` 工位真实执行：
  - `freely stop`
  - `freely chat "继续当前 I-20260321T201000Z ..."`
- 结果：新 intake 被写成 delegated，但 `live-status` 仍是 `dispatch_only`，无 supervisor/ai 主循环接棒。
