# PRD: ai-auth-change-wake-command-lifecycle-governance

## Problem

Freely 当前把 `ai switch` 的成功路径和全局 `auth-change-wake` 紧耦合在一起，导致用户可见成功结果已经出现后，前台命令仍可能长期不退出。现场已证明这不是 OAuth 独有问题，因为 no-op `switch codex <current-slot>` 也会被同步 wake 链拖住。`login` 当前只作为同族 follow-on 风险记录，不是第一阶段硬入口。

## Product Requirement

账号命令的成功路径必须有清晰的 operator-facing lifecycle：

- 用户看到 `switch` 成功结果后，命令应在可预期时间内退出
- 后续 control-plane 唤醒不能无限阻塞前台
- wake 机制不能通过 watchdog/manager 回流到同一 success-path notify loop

## Users

- 直接执行 `bin/ai switch` / `bin/ai login` 的人类操作者
- 通过 watchdog/manager 自动触发 `ai switch` 的 Freely runtime

## Requirements

1. 为 `ai switch` 定义 bounded post-success lifecycle。
2. 为 `auth-change-wake` 定义非递归 contract。
3. 若保留 wake acknowledgement，必须 bounded 且不影响命令退出。
4. no-op switch 必须有明确语义，不能无意义地进入同样的阻塞链。
5. 现有账号恢复能力不能退化。

## Risks

- 过度异步化可能让 manager/watchdog 错过必要的 auth-change 信号。
- 仅在单点 suppress notify 可能掩盖真实 re-entrancy 缺口。
- 把当前问题误判成一般进程泄漏，可能导致修复面过宽。

## Guardrails

- 第一阶段不执行真实 `login` 回归。
- 第一阶段不执行 slot 删除或清理动作。
- 优先用 no-op switch 和现有 `list/whoami/status` 真实命令回放锁定行为。
- 修复必须带 focused regression，证明健康 watchdog recovery 仍成立。
