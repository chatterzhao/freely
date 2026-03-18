# Global AI Account Watchdog

## Trigger

当前 Freely 已经把 manager / worker / runtime 的边界收得更清楚，但还有一个更上层的问题：

- Codex / iflow 等 AI 进程真正能否继续工作，取决于全局账号是否仍可用。
- 一旦当前全局账号打到限额，主管 AI 和 worker AI 都可能同时失活。
- 这时不能再依赖任何 AI 做“切号并重启”，因为 AI 本身已经发不出下一条命令。

这说明“账号切换 + 主管拉起”不属于 manager，也不属于 worker，而是更外层的全局脚本职责。

## Problem

当前设计仍有一个上层缺口：

1. `runtime/freely` 里已经有 account switch 逻辑，但它仍然依附于某个具体项目 supervisor。
2. 若全局账号不可用时，所有依赖这个账号的新 AI 进程都无法启动。
3. 若此时主管 supervisor 也不存在，就没有任何 AI 或项目级 runtime 可以继续发起恢复。
4. 因此，必须有一个完全不依赖 AI 的全局 watchdog，先恢复账号，再拉起主管。

## Decision

Freely 需要新增一个比主管更外层的 global control-plane：

1. `global ai account watchdog`
   - 读取全局 AI 账号池状态
   - 在全局账号不可用时切到可用账号
   - 若所有账号都不可用，切到最早恢复账号并等待
2. `manager bootstrap`
   - 在账号可用后，由脚本拉起 `develop` 上的主管 supervisor
   - 主管 AI 启动后才开始读取 fleet 并监督 worker
3. `role boundary`
   - manager 不负责切号
   - worker 不负责切号
   - project runtime 不应承担“全局账号生命线”这个职责
   - 这件事应由 global watchdog 独立执行

## Capability Shape

- `freely ensure-manager`
  - 不依赖当前 AI 会话
  - 先检查全局账号可用性
  - 必要时执行 `freely ai switch ... --yes`
  - 账号恢复后再执行 `freely start --project <develop>`
- `global account selection`
  - 有可用账号则立即切
  - 否则选最早恢复账号
  - 睡眠期间周期重检，不睡死
- `manager handoff`
  - 主管只接收已经恢复后的结果状态
  - 不接管切号与主管自拉起

## Boundary

这条能力必须明确：

- `global watchdog` 管全局账号和主管存活
- `manager runtime` 管 worker fleet 监督
- `worker runtime` 管自己工位的会话恢复
- `manager AI` / `worker AI` 都不负责 AI 无能为力的恢复动作

## Intended Landing

- `docs/pre-brainstorms/`
- `docs/LAWS.md`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/scripts/runtime/freely`
- 新的全局 watchdog/ensure 脚本
