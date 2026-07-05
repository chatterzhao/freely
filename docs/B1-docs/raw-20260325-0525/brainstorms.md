# 预研头脑风暴：watchdog-slot-sweep-without-cooldown-governance

## 背景

当前 watchdog / runtime 已经把账号语义收紧到 `.ai-auth/<slot>`，并且 canonical 真源早已承认：

- 本地 cooldown 账本会过时
- 真实可用性必须由脚本主动 probe
- 当前 slot 不可继续时，恢复动作不该依赖 manager / worker AI

但目前实现和 issue family 的默认心智仍然带着旧 contract：

- cooldown 账本仍参与 `all_slots_cooling_down -> earliest reset -> wait` 主路径
- `deactivated_workspace`、slot 失效、rate limit 等失败形态还没有统一成同一条 slot recovery contract
- 一旦把某个无效授权文件放进真实 Codex 使用位置，`codex exec` 会直接阻塞当前工作，因此“根据旧 cooldown 猜它可能可用”并不安全

这说明当前问题已经不是单纯“把 cooldown 记准一点”，而是要重新判断 cooldown 在 control-plane 里是否还应继续当核心调度真相。

## 问题定义

需要重新冻结 watchdog 的恢复 contract：

1. 真实调度真相到底是：
   - `cooldown ledger + earliest reset`
   - 还是 `failure-driven full slot sweep`
2. `rate limit`、`402 deactivated_workspace`、认证失效、workspace 失效，是否都应统一进入：
   - 标记“当前 slot 不可继续”
   - 全量 sweep 所有保存 slot
   - 找到真实可用 slot 就立即切换
3. 当所有 slot 都不可用时，runtime 应该：
   - 继续维护 cooldown/earliest-reset 排序
   - 还是只保留低频 reprobe / debug evidence，而不再把 cooldown 当恢复主真相

## 当前判断

目前更接近真实 contract 的方向是：

1. slot identity 只认 `.ai-auth/<slot-dir>`
2. 任何会让当前 slot 无法继续工作的失败，都先进入全量 slot sweep
3. 真实 probe 成功才允许把授权文件切进 Codex 工作位
4. cooldown 最多降级为调试/观测证据，不再主导恢复决策
5. 这次边界变化不需要新开独立 epic；它属于 `I-20260318-1630` 的同族 contract 改写 continuation，应由现有 watchdog issue family 吸收

## 目标

1. 冻结 “cooldown 是否退役” 的治理边界
2. 冻结 failure taxonomy 到 slot sweep recovery 的统一路由
3. 明确哪些真源需要从 `account/cooldown` 转到 `slot/probe/sweep`
4. 给后续 IBM / dev-loop 留出最小、可实现的 issue 边界

## 非目标

1. 不在本轮 pre-brainstorm 里直接重写 watchdog / runtime
2. 不在本轮直接修改 protected `develop` 上的 issue 结论
3. 不把“slot-only cooldown 修复已合并”误写成“这条 contract 已完成”

## 候选方向

1. cooldown 退役为 debug evidence
   - ledger 只保留最近失败证据或观测输出
   - 不再驱动 `earliest reset` 恢复主路径
2. 统一失败到 slot sweep
   - `rate limit`
   - `deactivated_workspace`
   - auth failure / invalid auth file
   - 当前 slot probe 明确失败
3. sweep contract 统一化
   - probe 所有保存 slot
   - 第一可用 slot 立即切换
   - 全部失败时进入低频 reprobe，而不是基于旧账本睡死
4. 将人工 `ai switch` 与 watchdog recovery 统一到同一套 slot probe / switch 主路径

## 进入 IBM 前必须冻结的问题

1. cooldown ledger 是彻底删除，还是保留为 debug / observability 输出
2. “全部 slot 不可用” 时的等待真相是：
   - 周期性真实 reprobe
   - 还是还允许用 earliest-reset 只做排序提示
3. `deactivated_workspace` 是否统一归类为 “slot unusable, switch immediately”
4. 当前 `I-20260318-1630` 能否承接这次 contract 改写，还是应 materialize 成新的同 epic issue

## 当前收口结论

本轮 pre-brainstorm 已经足够回答“新开 issue 还是同族吸收”这个首跳问题：

1. 这不是新的能力岛，而是 `global-ai-account-watchdog-and-manager-bootstrap` 内部恢复 contract 的继续收紧。
2. 旧 issue 已经拥有同一组 owner、真源、测试面与 live evidence；差别只在于此前把 `cooldown + earliest reset` 仍留在主恢复路径里。
3. 因此这条 candidate 应作为 supporting evidence 被 `I-20260318-1630` 吸收，而不是再 materialize 一个平行 issue。
4. 吸收后需要在该 issue 的 doc-loop 中显式改写：
   - `rate limit`
   - `deactivated_workspace`
   - auth failure / invalid auth file
   - slot probe failure
   这些都统一走 `failure-driven full slot sweep`，而不是继续把 cooldown 当恢复主真相。

## 真源候选

- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog`
- `docs/system/workspace/scripts/tests/test-freely-deactivated-workspace-defers-to-watchdog`
- `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`

## 生命周期判断

- 这是 Freely 自举中继续暴露出的 control-plane 共性问题
- 它与 `I-20260318-1630` 高度同族，但当前边界已经从“账本过时时增加主动 probe”推进到了“cooldown 是否退出主 contract”
- 本轮 pre-brainstorm 现已完成首跳判断：应吸收到既有 issue family，而不是 materialize 为新的 milestone-owned issue
