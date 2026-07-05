# 预研头脑风暴：develop-push-attempt-followthrough

## 问题陈述

Freely 已经有 `push_pending` / `push_deferred` / `push_urgency` / `resync_required` 真相面，但 merge 成功后仍可能停在“看见 debt、没有主动处理”。

这次复评后的新问题不是“要不要硬 auto-push”，而是：

1. `develop` merge 成功后，是否应自动触发一次受控 push attempt。
2. 如果这次 attempt 失败，系统如何把失败结果写回成 machine-readable followthrough truth。
3. 如何在不把网络副作用塞进 hook 的前提下，保证每次 develop merge 都被当前 followthrough 处理。

## 现有真源

- `develop-push-pending-guard-governance` 已冻结 `push_pending` / `push_deferred` 的可见性与 defer 真相。
- `develop-push-followthrough-escalation-governance` 已冻结 timely push default、lawful defer、`resync_required` 与 patrol/status 消费边界。
- 已完成 owner 明确排除了“hook/runtime 硬 auto-push”和“隐式 remote retry engine”。

## 复评结论

这次要开的不是旧 owner 的 reopen，而是新的 bounded follow-on：

- 允许：develop merge 成功后自动触发一次受控 push attempt
- 允许：attempt 失败后写回显式 `push_blocked` / blocked-reason / attempted-at / next-action truth
- 不允许：hook auto-push
- 不允许：自动重试直到成功
- 不允许：把 push 失败藏成普通 merge 成功后的静默副作用

## 设计边界

### 1. 自动触发点应是显式 merge 入口，不是 hook

最稳的落点是受保护的 merge 入口，例如 `freely pr-merge-guarded` 在 `develop` merge 成功后触发一次 `develop-push attempt`。

原因：

- merge 动作本身已经是显式 operator/runtime orchestration
- 这里触发 followthrough，不属于“隐藏在 hook 里的副作用”
- push gate 仍由现有 pre-push hook 执行，不会绕过治理链

### 2. 需要区分未尝试和尝试后被阻断

当前只有：

- `push_pending`
- `push_deferred`

这不足以表达：

- 当前 merge 是否已经触发过本轮 attempt
- attempt 是被 governance gate 阻断、还是远端/网络阻断、还是其他 push 失败

所以需要新增 `push_blocked` 或等价状态。

### 3. blocked 之后必须停在显式 followthrough，不得进入重试风暴

本轮只做：

- single controlled attempt
- explicit blocked writeback
- patrol/manager/status 继续把它当高优先级 followthrough

不做：

- daemon 化重试
- runtime 循环重推
- 对 remote/network 做退避引擎

## 候选落点

### A. laws / manager / patrol

- 增加“develop merge 成功后自动触发一次受控 push attempt”的治理语义
- 增加 `push_blocked` 的 manager 判断语义

### B. runtime

- 新增 `freely develop-push attempt`
- 把 blocked attempt 的 metadata 写回 `.freely/run`

### C. merge entrypoint

- `pr-merge-guarded` 在 `develop` merge 成功后自动触发一次 attempt

### D. tests

- attempt success
- attempt blocked by push gate / remote
- pr-merge-guarded auto-trigger
- status/live/fleet surfaces for `push_blocked`

## Promotion Gate

- 必须证明这不是回开旧 owner，而是其明确保留的 follow-on
- 必须证明 single attempt 不是 hidden auto-push
- 必须证明失败写回不会演化成 retry engine
