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

还有一个实现细节必须面对：

- OpenAI/Codex 当前没有可直接拿来查询“这组本地保存账号里谁现在可用、谁何时恢复”的官方本地 CLI。
- 帮助文档和 rate-limit 文档能说明“usage limit 会在某个窗口恢复”，但不能直接替 Freely 返回本机多个保存账号的实时可用矩阵。
- 所以 Freely 不能把本地 cooldown 账本当真理；账本只能做排序提示，真实可用性必须由脚本主动 probe。

另一个关键问题是：`AI 无能为力` 不能混成一个桶，至少要分三类。

## AI-Powerless Taxonomy

### 1. 全局 AI 服务不可用

这类问题的特征是：不是某个单独会话坏了，而是任何新的 AI 进程都起不来。

典型包括：
- 全局账号限额
- 认证失效 / token 失效
- AI 服务网络不可达
- 登录态损坏，导致任何新 `codex exec` / `iflow` 都无法工作

owner:
- `global watchdog`

required action:
- 全局切号 / 全局等待 / 全局健康检查
- 恢复后再启动主管

### 2. 当前 AI 会话不可延续

这类问题的特征是：服务本身未必不可用，但当前这条响应链已经结束，不能再靠当前 AI 自己继续。

典型包括：
- 响应已经结束
- `context compacted` 后需要新进程续接
- fresh session rotation
- 需要带新提示词重新启动工具
- 需要 cron / 定时唤醒 / 外部事件触发

owner:
- 当前工位 `runtime / scripts`

required action:
- 写 continuity
- 重新发起新进程
- 带角色提示和 handoff 续接

### 3. 其他工位 AI 进程已退出

这类问题的特征是：不是全局账号挂了，而是某个 worker 自己已经死了，它不可能再自己启动自己。

典型包括：
- 某个 worker supervisor 退出
- 某个 worker AI 进程异常消失
- 主管仍活着，但被监督工位已经 `down/down`

owner:
- `manager runtime` 先做脚本恢复
- 若脚本恢复后仍异常，再交给 `manager AI` 告警和重排

required action:
- 脚本拉起该 worker supervisor
- 主管随后只看恢复结果和下一步编排

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

补充：
- 第 1 类问题由 `global watchdog` 处理
- 第 2 类问题由当前工位 `runtime` 处理
- 第 3 类问题由 `manager runtime` 先处理，只有失败后才升级给 `manager AI`

## Capability Shape

- `freely ensure-manager`
  - 不依赖当前 AI 会话
  - 先检查全局账号可用性
  - 必要时执行 `freely ai switch ... --yes`
  - 账号恢复后再执行 `freely start --project <develop>`
- `global account selection`
  - 有可用账号则立即切
  - 若账本显示全部不可用，则逐个真实 probe 已保存账号
  - probe 都失败时才选最早恢复账号
  - 睡眠期间周期重检，不睡死
- `manager handoff`
  - 主管只接收已经恢复后的结果状态
  - 不接管切号与主管自拉起
- `worker outage recovery`
  - manager runtime 先脚本恢复缺席 worker
  - manager AI 只在脚本恢复不足时做告警与编排

## Boundary

这条能力必须明确：

- `global watchdog` 管全局账号和主管存活
- `manager runtime` 管 worker fleet 监督与 worker 掉线脚本恢复
- `worker runtime` 管自己工位的会话续接
- `manager AI` / `worker AI` 都不负责 AI 无能为力的恢复动作

## Intended Landing

- `docs/pre-brainstorms/`
- `docs/LAWS.md`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/scripts/runtime/freely`
- 新的全局 watchdog/ensure 脚本

## Verification Notes

- 官方帮助中心和 rate-limit 文档没有提供“查询多个本地 Codex 登录账号当前可用性”的直接入口；因此 Freely 采用脚本真实 probe。
- 真实验证口径应是：
  1. 先起 `ensure-manager --watch`
  2. 切到坏账号
  3. 让当前 Codex 进程结束
  4. 观察 watchdog 是否切回好账号并拉起新 Codex
- 2026-03-18 的 live 验证中，`worahe3972@outlook.com -> worahe3971@outlook.com` 与 `worahe3973@outlook.com -> worahe3971@outlook.com` 两条链均通过。
