# Brainstorm - 20260410-1835--codex-limit-triggered-slot-recovery-and-real-bin-ai-verification

一句话范围：本 worktree 只负责收紧切号/runtime 的顶层验收标准, 用手工真实测试证明切号是否符合要求, 并修复/重构所有与切号、cooldown、启动恢复、`bin/ai xx` 命令面相关的 bug。

## Problem

Freely 当前在 Codex 账号真实不可用时，`freely start` 的启动恢复链没有稳定兑现“当前 slot 刚刚因为 limit 失败，则内部恢复必须排除它并继续探测后续 slot”的语义。此外，和这条链直接相关的 `bin/ai xx` 真实命令面、cooldown、launch confirmation、startup recovery 仍存在需要系统排查和重构的点。

本条预研只处理 runtime / command / recovery 本体：

- 真实执行 `bin/ai xx` 相关命令，而不是只看 mock/unit
- 故意切到真实 limit slot，再启动 `freely`
- 观察 runtime/logs/live-status/fleet-status
- 找出切号、cooldown、launch confirmation、startup recovery 的 bug 和可优化点
- 为修改后验收保留同一套真实复现与回归路径

## Scope

1. 梳理 `bin/ai` 所有相关命令的真实命令面：
   - `init`
   - `list`
   - `whoami codex`
   - `status codex`
   - `switch codex`
   - `switch codex <slot>`
   - `login codex apikey`
   - `save codex`
   - `delete codex <slot>`
2. 区分两类切号语义：
   - 用户直接执行 `bin/ai switch codex`：不应无条件忽略 current slot
   - `codex exec` 真命中 limit 后触发的内部恢复：必须带着“刚失败 current slot”上下文排除当前号
3. 覆盖真实启动链：
   - 手工切到真实不可用/limit slot
   - `freely start`
   - 观察 `live-status`、cycle log、runtime-events、状态文件
4. 修复和重构相关路径：
   - manager bootstrap recovery
   - saved-slot inventory / cooldown
   - launch-time confirmation
   - after-failure slot selection context
5. 补 runtime 级测试，使“limit-triggered internal recovery”与“manual switch”语义不再混淆。

## Out Of Scope

- 不在本条预研中重新设计整个 testing governance / merge gate 体系
- 不把“用户手动执行 switch”强行改成自动跳过当前号
- 不把 URL/OAuth inventory 提升为比真实 `codex exec` 更强的 truth
- 不在本条预研中解决所有 adapter/ACP 长期路线，只记录对本问题的边界影响

## Confirmed Facts

1. 真实故障已复现：
   - 切到真实坏号后启动 `freely`
   - runtime 进入 `dispatch_only`
   - `last_exit_reason` 为 `primary_rate_limit_exhausted`
   - cycle log 有真实 Codex usage limit 报错
2. 当前 repo 中“跳过当前 slot”的能力只部分存在：
   - 选择器 `select_next_codex_slot()` / `select_any_available_codex_slot()` 会跳过 current identity
   - 但 `freely start` 走到 `ensure_codex_slot_ready_for_manager()` 时，没有把 after-failure 语义作为统一不变量继续传下去
3. `bin/ai --dry-run switch codex` 当前仍可能返回 `candidate_slot == current_slot`，这说明它表达的是 inventory 视角，不是“刚失败后的内部恢复”视角
4. URL/OAuth inventory 可以快，但和真实 `codex exec` 可用性并不总一致；真实 limit 触发后，不能再把刚失败 slot 当作普通候选
5. limit 检测当前分两层：
   - 优先吃结构化 usage / reset 信息
   - fallback 才靠日志字符串匹配 `usage limit|try again`
   fallback 具备脆弱性，不能作为唯一可信面
6. 当前 Codex 默认 adapter 仍是 `direct`；ACP 不是这次问题的主故障面，但需要检查它是否复用了同一恢复语义。
7. 用户要求本 worktree 不讨论“为什么测试体系没兜住”，这里只负责把相关命令、切号行为、启动恢复和真实验收跑透并修好。
8. 本条预研已进一步收紧调用策略：
   - 切号相关的实际可用性判定，不再接受 URL / OAuth / curl 面作为主调用链
   - 真实 `codex exec "hi"` 现在是唯一可接受的运行时 truth
   - 旧的 inventory / OAuth helper 可以暂留实现，但不能继续作为 `switch`、`freely start`、watchdog recovery、status 刷新 的主调用路径
9. 用户已明确要求“方法可以留下，但调用统一走 exec truth”；因此本 worktree 的后续修改不是只补 fallback，而是要完成主路径重构。
10. 当前 runtime lane 的收口结论：
   - watchdog manager bootstrap 已改成只吃 exec probe/sweep 作为选槽真源
   - `codex_inventory_truth()` 现只读 availability cache，不再触发 OAuth refresh/sweep
   - `codex_oauth_probe_single_slot()` / `codex_oauth_sweep_all_slots()` 仍保留，用于遗留诊断/单测，不在 `switch`、`freely start`、watchdog bootstrap 主链上
11. 新增真实命令面发现：
   - `bin/ai status codex` 在 real env 中会同步扫所有 saved slots；当前真实一轮约耗时 `1m56s`
   - 旧实现复用了会 promote candidate 的 sweep helper，导致 `status` 可能把当前 auth 从坏号直接切到另一个可用 slot；这属于副作用越界，必须修成 report-only
12. 新增真实失败谱系：
   - 同一坏号既可能最终报真实 usage limit，也可能先长时间出现 websocket / certificate / MITM 类网络噪音
   - 因此真实恢复与验收不能假设“坏号 = 立即 rate_limit”；必须按真实 `codex exec` 输出分类 `rate_limit` / `network_failure`
13. 对当前号的最新收口：
   - 若当前 account/apikey 在真实 `codex exec` 中报 `network_failure` / `timeout` / `unauthorized` / `subscription_expired` 等不可用状态，而 saved slots 里仍有其他候选，恢复链不得在当前号上终止
   - 必须继续真实尝试后续 saved slots / 其他 slot kinds；只有当根本没有其他 saved candidates 时，才允许返回 `current_auth_unusable` 或 `current_auth_rate_limited`
14. 新增 3 分钟真实 runtime 证据：
   - 手工切到 `account-worahe1001@outlook-com-1` 后直接启动 `freely`
   - cycle log 持续出现 websocket / certificate / reconnect 错误
   - 3 分钟后 supervisor 与 ai 仍存活，`whoami codex` 仍是坏号
   - 说明当前 active-runtime 设计会把这类网络异常长期挂在当前 slot 上，而不是及时判当前测试 slot 不可用并推进到下一个 slot
15. 最新闭环缺口已经定位：
   - 当前坏 slot 已能在 active runtime 中被快速判为 `network_failure` 并终止 codex 子进程
   - 但 feature / worker worktree 的 `freely start` 后续没有合法的“继续尝试下一个 slot”执行者
   - 原设计默认把这一步交给 `ensure-manager`
   - 而 `ensure-manager` 又被限制为 protected manager worktree，导致 feature 工位上的真实启动恢复验收链不闭环
16. 关于测试环境 lane 的最新边界：
   - `test-pre-merge-*` 只属于 `premerge-integration`
   - 它可以承接主线前集成验证，但不能替代 merge 后 canonical protected worktree 上的 `post-merge-followthrough`
   - 因此这次 runtime lane 仍必须保证 dedicated feature / worker worktree 自己就能完成真实 `freely start` 坏号恢复闭环，而不是把可验证性寄托给 `test-pre-merge-*`
17. 用户最新再次澄清了启动/切号语义：
   - `freely start` 的正常路径应当是“直接使用当前 slot 启动”，而不是一开始就做全量健康检查
   - 只有在真实使用过程中命中 `limit` / `auth_failure` / `network_failure` 等失败后，才触发内部自动切号
   - 自动切号不是手工 `switch` 的全量 sweep 语义；它应跳过刚失败 current slot，并在找到第一个真实可用 slot 后立即停止
   - 手工 `bin/ai switch codex` 才允许全量扫号、刷新 cooldown 与 availability
18. 用户同时明确要求默认取消后台/定时扫号设计：
   - Codex 的真实 `exec` 探测会消耗 token
   - `watchdog_probe_current_slot` / 周期性 availability 探测不应继续作为默认 runtime 设计
   - 默认只保留人工命令触发、真实失败后按需恢复，或极少数明确诊断入口
19. active runtime 与 probe/switch 的网络失败语义必须继续拆开：
   - `bin/ai switch codex` / availability probe 中的 reconnect / TLS / certificate fatal 仍属于 slot test fast-fail，可立即杀掉当前测试进程并尝试下一个 slot
   - `freely start` 的 active codex cycle 中出现同类证据时，默认按 `execution_network_transient|persistent` 处理，不能直接升级成 `same_tool_slot_recovery`
   - 否则宿主环境级 TLS/证书问题会被误判成 slot 坏号，导致 runtime 在 saved slots 间持续漂移
20. 新增真实 rate-limit 回归证据：
   - 手工切到 `account-worahe1001@outlook-com-1` 后启动 `freely`
   - 当前 active cycle 首次失败已重新落回 `primary_rate_limit_exhausted`，不再把证书/TLS 噪音直接记成 `slot_switch_reason=network_failure`
   - 之后出现的 `watchdog_probe_current_slot` / `probe_recovery_slots` 证据，实际来自 after-failure slot recovery 复用 watchdog probe helper，不是 idle 周期性后台扫号
   - 这说明“active cycle 网络分类”与“after-failure 顺序探测后续 slots”现在已经是两条不同链，但日志命名仍容易让人误判成 periodic probe
21. 最新真实 `freely start` 验收已经闭环：
   - 坏号 `account-worahe1001@outlook-com-1` 启动后，首轮真实失败落成 `primary_rate_limit_exhausted`
   - worker supervisor 随后按 `after_failure_exec_recovery_slot_probe` 顺序真实测试后续 saved slots
   - 遇到 `timeout` / `network_failure` 会立即结束当前测试并继续下一个 slot
   - 找到第一个真实可用 slot `apikey-codex-a1002-1` 后立即停止恢复 sweep，并继续 `fresh_with_handoff`
22. 最新真实手工 `bin/ai switch codex` 证据已经确认：
   - 无 slot 参数时，会按 saved inventory 全量 sweep
   - 当前号 `apikey-codex-a1006-1` 会被显式纳入 probe，并不会被无条件跳过
   - 即使中途已经发现可用 slot，也会继续扫完整个 inventory，最后才 promote 第一个可用 slot
   - 这与“自动恢复找到首个可用即停止”的语义已经明确分开
23. 最新真实命令面验收已覆盖并回滚：
   - `init`、`list`、`whoami codex`、`status codex`、`switch codex`、`switch codex <slot>` 已真实执行
   - `login codex apikey` 已使用真实已有 apikey 凭据创建临时 provider `e2e-cmd-20260410-temp`
   - `save codex` 已真实生成第二个临时 slot
   - `delete codex <slot>` 已真实删除两个临时 slot，并确认 inventory 无残留
   - 所有测试后当前认证已还原并通过真实 `whoami codex` 验证为 `apikey-codex-a1006-1`
24. 最新进程与清场证据：
   - `freely stop` 后未残留 supervisor / dispatcher / monitor / codex child
   - 切号恢复链中的测试 codex child 会在 network/tls/certificate 失败时被及时杀掉
   - 本轮唯一额外观察到的卡住现象来自手工 `bin/ai status codex` 的长时 real-env probe，不是 runtime 切号恢复造成的残余进程泄露

## Root Cause Direction

### A. 语义混淆

当前实现把下面两件事混在一起了：

1. “用户要求执行一次 `switch codex`，看看 inventory 里现在谁可用”
2. “当前 slot 刚刚因为真实 limit 失败，runtime 正在做 after-failure recovery”

这两种场景不应复用同一选择语义。

### B. after-failure 上下文没有沿启动链传递

runtime supervisor 会在 `codex exec` 失败后记录 `primary_rate_limit_exhausted` / `secondary_rate_limit_exhausted`，也会给 active slot 写 cooldown，但后续 manager bootstrap 重新进入 `ensure_codex_slot_ready_for_manager()` 时，没有把“上一个 slot 刚失败”当作强约束输入继续传递。

### C. inventory hint 与 launch truth 层级不清

OAuth / URL inventory 适合低成本筛选，但不能覆盖“刚刚真实失败”的局部事实。当前链路对两种 truth 的层级约束还不够硬。

### D. 多真值并存导致运行时语义漂移

当前 `switch`、watchdog、`freely start`、`status` 的部分路径仍然先调用 OAuth/URL sweep，再在部分条件下 fallback 到 exec。

这会带来两个直接问题：

1. 用户看到的“当前可用 / 候选可启动”并不总是来自真实执行面
2. 同一条切号链在不同入口上可能走不同 truth，导致恢复语义和日志证据不一致

因此这次不仅要修 `after-failure`，还要把主调用链收敛成 exec-only。

### E. 当前号失败被错误当成全局终止

`switch codex` 的 live-auth 前置探测原本把“当前 live apikey 不可用”直接映射为 launch_blocked。这个映射只在“根本没有其他 saved slots 可继续尝试”时成立；一旦 inventory 中还有其他 saved 候选，这种提前返回就会把单 slot 的网络抖动误判成全局无解。

### F. bounded network retry 设计边界放错了

当前 runtime 对 execution-network failure 的主设计是：

1. 让当前 codex 进程自己卡在 reconnect / websocket / 证书错误里
2. 等它自然退出后，把失败记成 `execution_network_transient` / `persistent`
3. manager bootstrap 在 backoff 结束后优先 relaunch 当前 slot，而不是继续试其他 slot

这对“全局网络暂时抖动且没有其他候选”的宿主级故障有意义，但对“正在做 slot 可用性测试 / 切号恢复”的场景是错误设计，因为：

1. 当前 slot 已经给出明确的 network/certificate failure 证据
2. 继续留在当前 slot 只会浪费时间，不会增加可信度
3. 用户要求的 recovery 目标是前进到下一个 slot，而不是陪当前 slot 无限重连

因此需要把设计拆成两类：

1. `slot-local failure during availability testing / switch / startup recovery`
   - 一旦命中 reconnect / certificate / websocket fatal 等信号，就立即判当前测试 slot 不可用
   - 立即杀掉本次测试/启动用的 codex 子进程
   - 立刻推进到下一个 saved slot / 其他 slot kind
2. `host-global outage / no alternate candidates`
   - 只有在没有其他 saved candidates，或多个 slot 都表现出同类宿主网络故障时，才允许保留 bounded network retry/backoff

### G. worker runtime 把 slot recovery 外包给 protected manager，破坏了本地验收闭环

当前实现把 slot-local failure 后的“继续试下一个 slot”主要放在 `ensure-manager` / manager control plane 里，这在 manager protected worktree 中成立，但在 dedicated feature / worker worktree 中会出问题：

1. `freely start` 在 feature worktree 里是真实可执行的验收入口
2. 这类工位默认不是 protected manager worktree，不能合法直接跑 `ensure-manager`
3. 如果 worker supervisor 在 slot-local failure 后直接退出，并等待 manager control plane 接手，就会出现：
   - 当前坏 slot 被杀掉了
   - 但本地 runtime 不再继续前进
   - 真实 `freely start` 验收无法证明“自动试下一个 slot”

因此设计需要修改为：

1. manager worktree 仍可保留外部 control-plane recovery
2. worker / feature worktree 的 same-tool slot-local recovery 必须在本地 supervisor 内闭环
3. 只有 same-tool candidates 全部耗尽，才允许继续交给更高层 fallback / cross-tool / waiting judgement

### H. runtime recovery 错把“自动恢复”实现成“全量 sweep”

最新真实验证暴露出另一层设计偏差：当前 worker-local recovery 虽然已经不再卡死在坏号上，但仍复用了 `probe_all_codex_slots_and_update_cooldown()` 这类全量 sweep helper，导致：

1. `freely start` 一旦进入恢复，就顺手把大量 slot 全都真实 probe 一遍
2. 恢复时延与 token 消耗被手工 `switch codex` 的语义绑架
3. runtime 还会留下 `watchdog_probe_current_slot` 之类后台 probe 痕迹，说明默认常驻扫描并未真正退出

这与用户要求不一致。正确拆分应是：

1. `freely start`
   - 直接使用当前 slot
   - 不做开局全量健康检查
2. `automatic recovery after actual failure`
   - 只在真实使用已失败后触发
   - 跳过刚失败 current slot
   - 逐个尝试后续 slot
   - 找到第一个真实可用 slot 就停止
3. `manual switch codex`
   - 才执行全量 sweep
   - 刷新 cooldown / availability cache
4. `background periodic probing`
   - 默认关闭
   - 不能作为 runtime 正常路径

## Open Questions

1. Codex direct 与 ACP adapter 是否共享同一条 slot recovery helper；若共享，是否需要同样强化 after-failure 语义
2. `switch codex` 在非 dry-run 下是否应该继续保持“有一个可用就可停”的行为，还是内部 helper 应在 after-failure 模式下完成全量探测和 cooldown 刷新
3. 是否需要为“刚失败 slot”引入单独的 launch-time exclusion 参数，而不是只依赖 cooldown 文件推断
4. limit fallback 若只剩日志字符串，是否要把该结果显式标记为 lower-confidence，并促使后续 recheck
5. unsaved current live apikey 且同时存在 saved apikey slots 时，manual `switch codex` 是否也要先显式 probe 当前 live auth，再决定是否继续 sweep；当前规则已明确“不能无条件忽略 current”，但这部分仍需继续实测收口
6. `execution_network_transient` / `execution_network_persistent` 当前是否仍默认“重试当前 slot”，以及应如何改为“slot-local network failure during recovery 直接杀进程并前进；只有 host-global outage 才 backoff 原地重试”

## Verification Plan

1. 在本 worktree 中真实执行 `bin/ai xx` 命令面，记录命令返回与副作用
2. 先切到真实 limit slot，再 `freely start`
3. 连续观察：
   - `freely live-status`
   - `freely fleet-status`
   - `.freely/logs/runtime-events.log`
   - `.freely/logs/cycle-*.log`
   - `.freely/run/workcell-state.env`
4. 修复后重复同一路径，确认：
   - internal recovery 排除刚失败 current slot
   - 启动前不再把该 slot 重新当作 launch candidate
   - 用户手动 `bin/ai switch codex` 语义未被误改
   - `bin/ai status codex` 只刷新 availability ledger，不再偷偷切换当前 auth
5. 用脚本测试把 manual switch 与 limit-triggered recovery 两条语义分开锁死。
6. 对所有切号相关主路径补一条更高优先级验收：
   - `switch codex`
   - `freely start`
   - watchdog bootstrap recovery
   - `status codex` 的实时 probe
   都必须只使用真实 `codex exec "hi"` 作为可用性 truth，而不是 URL / curl / OAuth sweep。
7. 对 live current auth 的失败语义补独立验收：
   - 无 saved slots 时，`network_failure` 仍应阻断并显式报 `current_auth_unusable`
   - 有 saved slots 时，同一失败必须继续 sweep 其他 candidates，而不是提前退出
8. 对 active runtime 再补一条更硬的真实验收：
   - 当当前测试 slot 在真实 `freely start` / active codex cycle 中出现 reconnect / certificate / websocket fatal
   - supervisor 必须在有后续 candidates 时尽快杀掉当前 codex 子进程
   - 不允许等待当前坏号无限重连；必须继续试下一个 slot
   - 在 dedicated feature / worker worktree 中，这个“继续试下一个 slot”必须由本地 supervisor 自己完成，而不是依赖 protected manager worktree
9. 对启动与恢复语义再加一条反向约束：
   - `freely start` 不得在正常启动前主动扫完整个 saved slots 列表
   - 自动恢复不得复用手工 `switch codex` 的全量 sweep 行为
   - runtime 默认不得保留后台/定时 Codex availability probe
10. 对真实命令面再加一条回归要求：
   - `login/save/delete` 这类会改认证状态的命令必须带真实回滚与 `whoami codex` 复验
   - `status codex` 必须保持 report-only，不得因刷新 availability ledger 而偷偷切换当前 auth
10. 对真实命令面测试再加一条执行纪律：
   - 所有会修改 live auth 的 `bin/ai xx` 测试都必须先记录原始 current slot
   - 测试结束后必须串行恢复到原始 slot，并再次用真实 `whoami codex` 复核
   - 不允许并发执行 `switch` / `whoami` 造成 auth 漂移后再继续下一轮实验

## Exit Criteria

1. 当前 worktree 内已有真实命令面与真实启动复现证据
2. runtime 修复把“after-failure 排除当前失败 slot”收成硬约束，而不是选择器偶然行为
3. 测试能明确区分 manual switch 与 internal recovery
4. 修改后能再次通过真实坏号启动 Freely 的回归验收
5. 切号相关主路径已完成 exec-only 重构；旧 URL / OAuth helper 不再作为主调用链
6. dedicated feature / worker worktree 中的真实 `freely start` 已能在 slot-local failure 后本地自动前进到下一个 slot，不再依赖 protected manager control plane 才能闭环
7. `freely start` / 自动恢复 / 手工 `switch codex` / 后台 probe 四种语义已明确拆开，且默认 runtime 不再用全量 sweep 或定时扫号冒充自动恢复
8. 所有真实 `bin/ai xx` 验证结束后，auth 状态已恢复到测试前记录的原始 slot，并有真实 `whoami codex` 证据
9. active runtime 的 reconnect / TLS / certificate fatal 不再直接走 slot-local marker 通道；它必须落到 `execution_network_*` 分类，避免环境级故障触发连续切号
10. 真环境 rate-limit 回归中，`probe_recovery_slots` 仍会在 after-failure recovery 中顺序尝试后续 saved slots；这不是 periodic scan，但后续应继续收紧日志/命名，避免与默认后台 probe 语义混淆
