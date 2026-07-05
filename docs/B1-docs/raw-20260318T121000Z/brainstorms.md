# Rate Limit Recheck And Wakeup

## Trigger

Freely 的 Codex 自动切号与 backoff 已经能识别 `primary`/`secondary` 限额，但最近狗粮里暴露出一个恢复缺口：

- 某个账号因为 5 小时窗口进入冷却
- 另一个账号仍在更长窗口冷却
- supervisor 进入 sleep 后，没有在较短窗口恢复时重新唤醒并重试

结果是 runtime 可能在恢复时间已过后仍保持 `supervisor up / ai down`，让 worker 静默挂住。

## Problem

当前实现把某一轮选中的 `reset_at` 当作一次性 sleep 目标，但自治运行器不应该把“恢复时间预测”视为绝对真相。需要在 backoff 期间周期性重判：

1. 是否已有任一账号提前恢复可用；
2. 是否 stop marker 已出现；
3. 是否当前 cooldown 文件已经过期，应提前结束 sleep。

## Decision

- 为 rate-limit backoff 增加分段 sleep + 可用账号重判。
- “all_accounts_cooling_down” 不再意味着一定睡到最初选中的那一个 `reset_at`；任何保存账号一旦可用，都允许提前醒来继续下一轮。
- 用脚本级测试锁住“较短 5 小时限制恢复后必须优先回来”的行为。
