# Issue: global-ai-account-watchdog-and-manager-bootstrap

- issue_id: `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `global-ai-account-watchdog-and-manager-bootstrap`
- issue-name: `global-ai-account-watchdog-and-manager-bootstrap`
- source_candidate: `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/candidates.md#c-20260318-a`
- source_brainstorm: `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 现在已经开始区分 manager、worker 和 runtime，但还缺最上层的全局恢复链：

- 当当前全局 Codex 账号不可用时，任何新的 AI 进程都起不来
- 这类恢复不应依赖 manager AI 或 worker AI
- Freely 需要纯脚本先切号，再拉起主管；主管恢复后再监督所有工位

## Scope

1. 物化 `global watchdog` 的正式职责边界。
2. 提供 CLI-first 的主管拉起入口，例如 `freely ensure-manager`。
3. 把全局账号恢复与主管拉起从 manager/worker 职责中剥离出来。
4. 提供一条 live 集成测试脚本，验证：
   - 先由脚本自己探测当前可用账号并启动监控/主管链
   - 监控链已运行后，故意切到不可用账号
   - 当前 AI 进程结束后，由 watchdog 负责恢复；不要把恢复动作交给 AI
   - 每次切号后都由脚本重新拉起新的 Codex 进程，并优先 `resume` 恢复会话
   - 最终自动切回脚本真实探测出的可用账号并恢复主管；若所有账号都不可用，则切到最早恢复账号并等待唤醒
5. 在 watchdog 拉起主管前，写入结构化 handoff，说明：
   - 哪个账号触发了 limit/不可用
   - 当前切到了哪个账号
   - 这次是立即恢复还是等待最早 reset 后恢复
   - 主管起来后优先检查哪些工位、该先判定 resume 还是 fresh_with_handoff

## Acceptance

- 文档明确区分三类 AI powerless 场景及其 owner。
- 至少存在一个纯脚本入口，可在没有任何 AI 帮助时恢复账号并拉起主管。
- live 集成测试脚本能验证“切到坏账号后自动切回好账号”的真实链路。
- live 集成测试脚本在未显式给出好账号时，也能通过真实 probe 发现当前可用账号。
- live 集成测试脚本能验证“切号 -> 新 Codex 进程启动 -> resume/续接 -> 继续监督”的真实链路。
- 主管恢复后继续只承担监督和委派，不接管全局账号切换。
- watchdog 在拉起主管前会写结构化恢复交接，而不是让主管盲启动。
- `ai-cli` / watchdog 对外暴露的 canonical identity 必须是 slot；auth email 只能作为 `auth_email` metadata，不能再被展示成当前身份。

## Completion

- `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/*`
- `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/pre-tests.md`
- `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/tasks.md`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `docs/system/workspace/skills/ai-cli-availability-manager/SKILL.md`
- `docs/system/workspace/scripts/tests/test-freely-global-account-watchdog-live`
- `docs/system/workspace/scripts/tests/test-watchdog-control-plane-skills`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/ai-cli`

## Verification

- 当前验证重点：
  - `freely ensure-manager` 是否是纯脚本，不依赖 AI
  - 当当前账号不可用时，是否能自动切到可用账号并拉起主管
  - 当 cooldown 账本过时或错误时，是否会真实 probe 所有已保存账号，而不是盲信旧账本
  - live 测试是否能覆盖两个坏账号回切到一个好账号的真实链路
  - availability watchdog 是否已经从 `runtime/freely` 中抽成可复用 skill 模块，而不是继续散落在 Freely 专有 orchestration 中
- 最新验证事实：
  - 官方帮助中心与 rate-limit 文档没有提供“多个本地保存 Codex 账号当前可用性查询”的直接接口，因此 Freely 采用脚本真实 probe 方案
  - `test-ai-cli-switch-default-tool` 已覆盖默认 `codex` 切号 UX 与切后真实账号校验
  - `test-freely-ai-account-switch` 已覆盖 `freely ai switch codex` 在未显式指定账号时主动 probe 所有已保存账号，并验证：
    - 找到可用账号时切到可用账号
    - 全部限流时切到最早恢复账号
    - probe 期间显式带代理并写回 cooldown 账本
  - `test-freely-ensure-manager` 已覆盖“先选可用账号再拉主管”的脚本回归
  - `test-freely-rate-limit-defers-to-watchdog` 继续通过，证明主动 probe 收敛后，本地 runtime 仍把 rate-limit 恢复交给 watchdog，而不是回退到本地睡眠
  - `watchdog-control-plane` 与 `ai-cli-availability-manager` 已把 availability watchdog 定义成可复用 skill 层；`runtime/freely` 现通过 `source "$WATCHDOG_AVAILABILITY_LIB"` 复用同一套 account cooldown / probe / switch / ensure-manager readiness 逻辑
  - `test-watchdog-control-plane-skills` 已覆盖 watchdog skill 是否被 runtime 与 agent 角色正式接线
  - `freely ensure-manager` 当前在 watchdog 拉起主管前，会写 manager bootstrap handoff，告知 limit/切号/恢复原因及主管优先检查面
  - 2026-03-24 continuation 新增 shared account-switch serialization：
    - 手工或自动 `freely ai switch codex` sweep 期间会持有全局 switch lock，而不是边切边让 watchdog 误 probe/误 bootstrap
    - `ensure-manager` / availability watchdog 在 probe、切号、manager bootstrap 前会先等待现有 switch sweep 完成，避免 transient unauthorized / unavailable 账号被误当成新的恢复信号
    - `test-freely-ai-account-switch-serialization` 覆盖 auto-probe sweep 全程持锁
    - `test-freely-ensure-manager-defers-during-account-switch` 覆盖 switch lock 活跃时 watchdog 延迟 probe/bootstrap，待切号结束后再恢复
  - 2026-03-24 continuation 又补齐 switch sweep 期间的剩余 race：
    - `ensure_manager_once()` 先前仍可能在 wait 之前触发 `whoami`
    - `codex_saved_accounts()` / `whoami` / `list` 读路径现在也会等待正在进行中的 switch sweep
    - `codex_probe_current_slot_now()` 现在会持有同一把 shared switch lock 覆盖整个 `codex exec` probe，避免 wait-return 后被新的手工 sweep 插入
    - `test-freely-codex-probe-defers-during-account-switch` 覆盖 watchdog probe 自身的 defer + serialization
  - 2026-03-23 当前 verification batch 在 dedicated feature worktree 中直接完成，无需引入 `pre-test-merge` 或提前要求 `post-merge acceptance`：
    - `freely ensure-manager --project <tmp-project>` 直接命令验证通过，确认 watchdog 会先切到可用账号，再发起 manager bootstrap
    - `freely start --project <tmp-project>` 最小 rate-limit 场景可直接写出 `LAST_SLOT_SWITCH_REASON="primary_rate_limit_exhausted"`，证明 runtime 仍把恢复理由写回 watchdog 接管面
  - `test-freely-rate-limit-defers-to-watchdog` 曾出现一次 3 秒边界失败，但随后单独复现与连续重跑均通过；当前判断为时间阈值边界上的 flaky，而非稳定功能回归
  - 2026-03-24 verification continuation 又暴露出两处收口缺口，并已在当前 worktree 继续修补：
    - `test-freely-rate-limit-defers-to-watchdog` 使用整秒计时，仍会偶发把 `<4s` 的正常退出误判成“本地睡眠”；当前已改成 monotonic 毫秒阈值，避免秒边界抖动
    - `ensure-manager` / earliest-reset 回归此前没有直接断言 manager bootstrap handoff artifact；当前已把 trigger/account/reason/next_action 写入测试验收面
  - 2026-03-23 晚间狗粮 continuation 暴露出一条实现缺口：
    - `all_slots_cooling_down -> earliest reset -> sleep` 路径没有显式 `reset_at + buffer`
    - wait 结束后没有重新 probe 所有 saved accounts 再决定 relaunch
    - `ensure-manager --watch` 会因为单轮 readiness pass 失败而退出控制面，现场留下 stale `ensure-manager.pid`
  - 2026-03-24 continuation writeback 已把 canonical 状态重新对齐到当前 feature worktree：
    - issue / milestone / progress / code-review 现统一表达为“continuation batch 已实现并处于 `in_verification`”
    - 当前批次不再沿用“verified-retirable”或“仍待提交”旧结论
  - 2026-03-24 slot-only cooldown identity continuation 进一步收紧了 identity 语义：
    - `ensure_codex_slot_ready_for_manager` 现在只认 `whoami.slot` 作为 cooldown identity，`whoami.account` 仅保留展示用途
    - `select_any_available_codex_slot` 只排除当前精确 slot，不再做同 family exclusion，避免把同邮箱的 `-x` 兄弟 slot 误伤
    - 已验证 `ai-cli` 的 `login`/`switch` 入口遵守显式 suffixed slot contract，不再生成或消费无后缀目录
    - 新的 focused regression `docs/system/workspace/scripts/tests/test-freely-ensure-manager-slot-alias-cooldown` 覆盖了 slot selector / manager bootstrap 路径以及 slot-only cooldown identity
  - 2026-03-25 develop live replay 进一步确认，本轮重启抖动不是 “wait for old switch/process” contract 缺失：
    - `wait_for_codex_slot_switch_idle()` 仍在 `availability-watchdog.sh` 真源里，并被 `whoami/list/probe/ensure-manager bootstrap` 路径复用
    - develop 当前 `./bin/ai whoami codex` 返回的 active slot 是 `worahe3976@outlook-com`
    - develop 当前 `./bin/ai list` 返回 15 个保存 slot，但 `.freely/run/codex-slot-cooldowns.tsv` 里只有 16 条 cooldown entry，其中 6 个真实 slot 缺账本、7 条账本 entry 指向已不存在的无后缀/旧 identity
    - 当前现场更像是 cooldown truth 没跟上 slot-first contract，watchdog 因此可能把缺记录 slot 当成“立即可用”，持续 probe/relaunch，而不是稳定进入 `all_slots_cooling_down` handoff
  - 2026-03-25 当前 dedicated continuation 又补了一条直接锁 runtime 写回的 focused regression：
    - `test-freely-rate-limit-defers-to-watchdog` 与 `test-freely-rate-limit-log-defers-to-watchdog` 现都显式断言 cooldown ledger 写入的是 suffixed slot key，而不是无后缀 account key
    - 这让 “runtime 退出后按 slot 记录 cooldown” 不再只是 `ensure-manager`/selector 间接覆盖，而是由 rate-limit supervisor 路径直接验收
  - 2026-03-25 review continuation 又补上两处边界：
    - `ensure_manager_once()` 的 idle-manager unavailable branch 现也改为按 slot cooldown identity 判断，避免 manager AI 已退场时仍用 account key 误判“当前账号可用”
    - 当 `whoami.slot` 临时缺失时，cooldown identity 会回退到 `~/.codex/active-slot`，避免 textual/structured rate-limit 退出把 cooldown 记录直接丢失
  - 2026-03-25 pre-brainstorm 收口又冻结了一条更上层的 contract rewrite：
    - 这次边界变化不再被视为“把 cooldown 账本记准一点”，而是要把 cooldown 从主恢复决策中降级出去
    - `rate limit`、`deactivated_workspace`、auth failure / invalid auth file、slot probe failure，都应统一进入 failure-driven full slot sweep
    - 真实 probe 成功前，不允许把某个 slot 的授权文件切进真实 Codex 工作位；否则无效授权会直接阻塞正在执行的 `codex exec`
    - `all slots unavailable` 时允许保留 earliest-reset 作为 debug / 排序提示，但恢复主路径应基于低频真实 reprobe，而不是继续以 cooldown ledger 为控制面真相
    - 该结论来自 `docs/pre-brainstorms/20260325-0525--watchdog-slot-sweep-without-cooldown-governance/*`，并已明确判定为同族 supporting evidence，由本 issue 吸收，不新开平行 issue
  - 2026-03-25 当前 continuation 已把上述 contract 写入能力真源并通过 focused verification：
    - `availability-watchdog.sh` 的 `ensure_codex_slot_ready_for_manager()` 现改为 current-slot probe + full saved-slot sweep；不再先信 cooldown ledger 再决定 manager bootstrap
    - `probe_all_codex_slots_and_update_cooldown()` sweep 失败时会恢复原 auth / active-slot，避免把最后一个失败 slot 留在真实 Codex 工作位；返回 usable 结果前会把 active slot 对齐回该 usable slot
    - `freely ai switch codex` 自动模式只会切到真实 probe 成功的 usable slot；`all_unavailable` 仅返回 debug hint，不再切 earliest-reset slot
    - `test-freely-ai-account-switch`、`test-freely-ensure-manager`、`test-freely-ensure-manager-earliest-reset-wait-revive` 已重写并通过，当前 focused acceptance 已对齐 slot-sweep-first recovery
  - 2026-03-25 live 狗粮又暴露出一条 CLI/metadata 漂移：
    - `slot` 才是 `.ai-auth/<slot>` 的唯一身份，但 `bin/ai whoami` 仍把 auth JWT email 输出成 `Current account`
    - 现场已出现 `Current slot != Current account` 的情形；这不是 slot 选择错误，而是 CLI 把 auth metadata 错报成了身份
    - 当前 continuation 已把 `whoami` / `switch` / `status` / `save` / `login` 的对外 contract 改成 slot-first，并新增 focused regression 锁住 “slot 标签与 auth email 不一致” 的场景
  - 2026-03-26 develop replay 又暴露出一条同族控制面缺口：
    - canonical runtime 在 manager 命中 `auth_failure` 后会停在 `stalled_without_runtime`
    - delegated interruption intake 继续堆积，但现场没有任何存活的 `ensure-manager --watch` / interruption dispatcher 继续恢复和消化
    - 当前判断：不是新 candidate，而是本 issue 的 script-owned recovery contract 仍缺一条 detached control-plane survival gate
  - 2026-03-26 当前 continuation 已补上 detached control-plane recovery：
    - `launch_manager_supervisor()`、`launch_interruption_dispatcher()`、`launch_manager_watchdog()` 已改用 `nohup ... </dev/null >/dev/null 2>&1 &`，不再依赖父 supervisor 退出后仍能保留的脆弱 background/disown 语义
    - 新增 `docs/system/workspace/scripts/tests/test-freely-auth-failure-keeps-control-plane-alive`，显式验证 manager 命中 `auth_failure` 后 `ensure-manager.pid` 与 `interruption-dispatch.pid` 仍代表 live process，且 `freely stop` 能清理
    - `test-freely-manager-watchdog-live-during-active-ai` 与 `test-freely-rate-limit-defers-to-watchdog` 继续通过，证明 detached launch 没有破坏既有 watchdog 生命周期
  - `test-freely-global-account-watchdog-live` 已真实通过：
    - `worahe3972@outlook.com -> worahe3971@outlook.com`
    - `worahe3973@outlook.com -> worahe3971@outlook.com`
  - live 测试口径已收紧为：监控脚本先启动，切到坏账号后等待当前 AI 进程结束，再验证 watchdog 是否切回脚本真实探测出的可用账号并拉起新 Codex

## Next

- 当前 continuation batch 已完成 slot-sweep-first contract 的最小实现与 feature-worktree focused 验证，当前保持 `in_verification`，等待 manager merge review。
- 当前 continuation batch 已补上 verification drift：稳定化 `rate-limit` 用例计时，并把 manager bootstrap handoff 契约收进 focused tests；本轮完成后继续保持 `in_verification`，等待 manager merge review。
- 当前 continuation batch 又补上 `auth_failure` 后 detached control-plane 存活契约；下一步进入同 issue family 的 commit / merge judgement，并在 develop replay 中确认 canonical runtime 不再掉到 `stalled_without_runtime`。
- 同族 pre-brainstorm 已把恢复 contract 进一步收紧为 `failure-driven full slot sweep`，而本轮 continuation 已把这条 contract 的最小主路径真正写回能力真源。下一轮不再是重做 contract 改写，而是继续做 code review / merge judgement / develop replay。
- 当前批次交付的 continuation contract：
  - wait 采用 `reset_at + buffer`
  - wait 期间周期性真实 probe saved accounts 是否已变得可工作
  - wait 结束后重新 probe/select，再拉起 manager
  - `ensure-manager --watch` 单轮失败后继续留在控制面重试
  - stale `ensure-manager.pid` 在 watchdog 下次启动时会被覆盖，并在 watchdog 退出时清理
- 下一步：
  - 先按新 pre-brainstorm 结论重写 watchdog contract：failure taxonomy、slot sweep 主路径、all-slots-unavailable 等待语义、以及 cooldown 的降级角色
  - 再进入 dedicated dev-loop，把 runtime / watchdog / ai-cli / tests 从 cooldown-driven recovery 改到 slot-sweep-first recovery
  - contract 改写与代码验证完成后，再由 manager 复核当前 feature worktree 的 doc/code/test 证据并决定是否 promote
