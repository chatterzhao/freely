# Brainstorm: cli-wrapper-packaging-and-regression-surface-governance

## Boundary

本 owner 只处理本轮 CLI 审计确认的三类包装层问题：

1. runnable wrapper 缺失 executable bit
2. `freely ai --help` 帮助输出前的 shell 噪音
3. `test-ai-cli-switch-triggers-auth-change-wake` 的 worktree / 环境不稳定

## Why This Is A Separate Lifecycle

- 这些问题都发生在命令入口和回归入口层，而不是 runtime/control-plane 深层语义。
- 如果先去修 runtime 或 bootstrap，后续测试仍可能建立在不稳定 wrapper 上，继续放大假阳性或环境耦合。
- 因此应先把“命令真能跑、测试真在测真实入口”这层收稳，再进入更深的 owner。

## Initial Repair Direction

1. 只给已确认应 direct-exec 的 wrapper 补 executable bit。
2. 把 `ai-cli` help heredoc 改成不会触发 command substitution 的安全写法。
3. 查清 auth-change wake 测试为什么会在某些 worktree 首跑缺失 `wake.log`，优先收敛成 deterministic fixture。
