# Issue: global-ai-account-watchdog-and-manager-bootstrap

- issue_id: `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `global-ai-account-watchdog-and-manager-bootstrap`
- issue-name: `global-ai-account-watchdog-and-manager-bootstrap`
- verification_artifact_dir: `docs/epics/- epic-name: `workspace-routing-foundation`/- story-name: `global-ai-account-watchdog-and-manager-bootstrap`/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260318-1630/candidates.md#c-20260318-a`
- additional_source_candidates:
  - `docs/B1-docs/raw-20260323-1135/candidates.md#c-20260323-1135-a`
- source_brainstorm: `docs/B1-docs/raw-20260318-1630/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
- session_refs:
  - {tool: codex, session_id: "019d29a9-5895-74b0-aee5-b3d44d9f2390", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T03-20-57-019d29a9-5895-74b0-aee5-b3d44d9f2390.jsonl", role: "manager-closeout-audit"}
  - {tool: codex, session_id: "019d29b2-d89b-7393-9704-c7ea6cd0b526", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T03-31-19-019d29b2-d89b-7393-9704-c7ea6cd0b526.jsonl", role: "manager-closeout-audit-refresh"}
  - {tool: codex, session_id: "019d29b7-4cf6-7f23-a8d0-39f1176fad36", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T03-36-11-019d29b7-4cf6-7f23-a8d0-39f1176fad36.jsonl", role: "manager-closeout-audit-current"}
  - {tool: codex, session_id: "019d29bb-9572-74f0-99dd-3b066647ea6a", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T03-40-52-019d29bb-9572-74f0-99dd-3b066647ea6a.jsonl", role: "manager-closeout-audit-fresh-recheck"}
  - {tool: codex, session_id: "019d29c0-a278-7833-be12-65efef7889cd", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T03-46-23-019d29c0-a278-7833-be12-65efef7889cd.jsonl", role: "manager-closeout-audit-current-fresh-session"}
  - {tool: codex, session_id: "019d29f2-3953-75f2-9be9-34822f55f374", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T04-40-33-019d29f2-3953-75f2-9be9-34822f55f374.jsonl", role: "manager-closeout-audit-fleet-refresh"}
  - {tool: codex, session_id: "019d29f6-6f39-71e1-ae7a-1676f191b63c", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T04-45-09-019d29f6-6f39-71e1-ae7a-1676f191b63c.jsonl", role: "manager-closeout-audit-authoritative-refresh"}
  - {tool: codex, session_id: "019d2a17-0762-7720-80f2-03ea4786077b", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T05-20-45-019d2a17-0762-7720-80f2-03ea4786077b.jsonl", role: "manager-closeout-audit-first-jump-refresh"}
  - {tool: codex, session_id: "019d2a66-1e0b-7563-a4b7-e38b2d5d971b", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T06-47-08-019d2a66-1e0b-7563-a4b7-e38b2d5d971b.jsonl", role: "manager-closeout-audit-current-refresh"}
  - {tool: codex, session_id: "019d2c8b-59c1-7713-9f67-8ff2a6455a8c", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T16-47-03-019d2c8b-59c1-7713-9f67-8ff2a6455a8c.jsonl", role: "manager-closeout-audit-continuity-stabilization"}
  - {tool: codex, session_id: "019d2c94-db34-7012-b942-129dc5dfa98e", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/26/rollout-2026-03-26T16-57-26-019d2c94-db34-7012-b942-129dc5dfa98e.jsonl", role: "manager-closeout-audit-authoritative-fleet-refresh"}

## Why

Freely 现在已经开始区分 manager、worker 和 runtime，但还缺最上层的全局恢复链：

- 当当前全局 Codex 账号不可用时，任何新的 AI 进程都起不来
- 这类恢复不应依赖 manager AI 或 worker AI
- Freely 需要纯脚本先切号，再拉起主管；主管恢复后再监督所有工位

## Scope

1. 物化 `global watchdog` 的正式职责边界。
2. 提供 CLI-first 的主管拉起入口，例如 `freely ensure-manager`。
3. 把全局账号恢复与主管拉起从 manager/worker 职责中剥离出来。
4. 冻结 strict probe-gating contract：
   - `.ai-auth/<slot>` 与实时 probe 才是恢复真相
   - `cooldown` 不再参与任何恢复逻辑
   - slot sweep / reprobe 期间禁止拉起任何 manager / worker / AI 进程
   - 只有 watchdog 明确找到可用 slot 后，才允许恢复主管链
   - CLI / runtime 对外展示必须把 slot 作为唯一 identity；邮箱 / `account_id` 只允许作为授权元数据
5. 提供一条 live 集成测试脚本，验证：
   - 先由脚本自己探测当前可用 slot 并启动监控/主管链
   - 监控链已运行后，故意切到不可用 slot
   - 当前 AI 进程结束后，由 watchdog 负责恢复；不要把恢复动作交给 AI
   - 恢复过程中只有真实 probe 成功的 slot 才会被切进真实 Codex 工作位
   - 若所有 slot 都不可用，则保持 AI launch 阻塞，并等待 watchdog 低频检查或 inventory 变化后再唤醒主管
6. 在 watchdog 拉起主管前，写入结构化 handoff，说明：
   - 哪个 slot / 哪类失败触发了 blocked
   - 这次恢复是 probe sweep 成功还是 all-unavailable 后被唤醒
   - 当前恢复到了哪个 slot
   - 主管起来后优先检查哪些工位、该先判定 resume 还是 fresh_with_handoff

## Acceptance

- 文档明确区分三类 AI powerless 场景及其 owner。
- 至少存在一个纯脚本入口，可在没有任何 AI 帮助时恢复账号并拉起主管。
- `cooldown` 不再参与任何恢复判定、等待、排序或切换逻辑。
- 任何 slot sweep / reprobe 窗口内，都不会拉起 manager / worker / 其他 AI 进程。
- live 集成测试脚本能验证“切到坏 slot 后自动切回好 slot”的真实链路。
- live 集成测试脚本在未显式给出好 slot 时，也能通过真实 probe 发现当前可用 slot。
- live 集成测试脚本能验证“切号 -> 新 Codex 进程启动 -> resume/续接 -> 继续监督”的真实链路。
- 当所有 slot 都不可用时，watchdog 仍保持存活和可观察，但 AI launch 保持阻塞；只有后续真实 probe 或 inventory 变化发现可用 slot 后，才写 handoff 并唤醒主管。
- 主管恢复后继续只承担监督和委派，不接管全局账号切换。
- watchdog 在拉起主管前会写结构化恢复交接，而不是让主管盲启动。
- `whoami` / `switch` / `status` / `save` / `login` 的展示与 JSON 输出不会再把授权邮箱误报成“当前身份”；slot 才是当前身份锚点，auth email 只能作为 `auth_email` metadata。
- slot probe 如果因为超时被 watchdog 杀掉，partial probe output 也必须留在 `.freely/run` artifact 中，方便在 switch 结束后区分网络/代理慢、CLI 卡死、还是 `402 deactivated_workspace` 等真实返回已出现但被 timeout 截断。

## Completion

- `docs/B1-docs/raw-20260318-1630/*`
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
  - 当当前 slot 不可用时，是否会先阻塞 AI launch，再真实 probe 所有保存 slot，找到可用 slot 后才拉起主管
  - 当所有 slot 都不可用时，watchdog 是否保持存活与可观察，同时维持 no-launch gate
  - auth inventory 变化或后续真实 probe 命中可用 slot 时，是否会写 handoff 并唤醒主管
  - live 测试是否能覆盖两个坏 slot 回切到一个好 slot 的真实链路
  - availability watchdog 是否已经从 `runtime/freely` 中抽成可复用 skill 模块，而不是继续散落在 Freely 专有 orchestration 中
- 最新验证事实：
  - 官方帮助中心与 rate-limit 文档没有提供“多个本地保存 Codex 账号当前可用性查询”的直接接口，因此 Freely 采用脚本真实 probe 方案
  - `test-ai-cli-switch-default-tool` 已覆盖默认 `codex` 切号 UX 与切后真实账号校验
  - `test-freely-ai-account-switch` 的较早验证批次曾覆盖 `freely ai switch codex` 在未显式指定账号时主动 probe 所有已保存账号，并验证：
    - 找到可用账号时切到可用账号
    - 当时的旧 contract 仍会在“全部限流”场景回到 earliest-reset 语义
    - probe 期间显式带代理并写回 cooldown 账本
  - 上述 earliest-reset / cooldown-driven wording 现在只保留为被后续 slot-sweep-first rewrite 吸收的历史背景；当前 canonical contract 以 2026-03-25 strict probe-gating rewrite 及其后续 closeout judgement 为准
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
  - 2026-03-23 当前 verification batch 在 dedicated feature worktree 中直接完成，无需引入 `test-pre-merge-*` 测试批次或提前要求 `post-merge acceptance`：
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
    - `ensure_codex_slot_ready_for_manager` 现在只认 `whoami.slot` 作为 cooldown identity；授权邮箱只允许作为 `auth_email` 元数据存在
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
    - 该结论来自 `docs/B1-docs/raw-20260325-0525/*`，并已明确判定为同族 supporting evidence，由本 issue 吸收，不新开平行 issue
  - 2026-03-25 当前 continuation 已把上述 contract 写入能力真源并通过 focused verification：
    - `availability-watchdog.sh` 的 `ensure_codex_slot_ready_for_manager()` 现改为 current-slot probe + full saved-slot sweep；不再先信 cooldown ledger 再决定 manager bootstrap
    - `probe_all_codex_slots_and_update_cooldown()` sweep 失败时会恢复原 auth / active-slot，避免把最后一个失败 slot 留在真实 Codex 工作位；返回 usable 结果前会把 active slot 对齐回该 usable slot
    - `freely ai switch codex` 自动模式只会切到真实 probe 成功的 usable slot；`all_unavailable` 仅返回 debug hint，不再切 earliest-reset slot
    - `test-freely-ai-account-switch`、`test-freely-ensure-manager`、`test-freely-ensure-manager-earliest-reset-wait-revive` 已重写并通过，当前 focused acceptance 已对齐 slot-sweep-first recovery
  - 2026-03-25 `20260325-0921` supporting evidence 继续暴露出上一轮验证仍不够硬：
    - pre-tests 尚未把 “probe 期间禁止任何 AI 拉起” 与 “all-unavailable 时 watchdog alive 但 manager/worker down” 写成 acceptance hard gate
    - issue / tasks / progress / milestone 仍默认把本 story 当成“slot-sweep-first 已基本完成、等待 merge judgement”，与最新 contract 不一致
    - 当前批次因此先回 doc-loop，重写 hard gate，再进入 dev-loop 修复
  - 2026-03-25 focused verification 已补齐并通过：
    - `test-freely-ensure-manager-earliest-reset-wait-revive` 证明 all-unavailable hold 会先落到 durable availability state，再在后续真实 reprobe 找到 usable slot 后 wake manager
    - `test-freely-ensure-manager-inventory-change-wakes-watchdog` 证明 `.ai-auth` inventory 变化会触发重新检查并在写 handoff 后唤醒主管
    - `test-ai-cli-whoami-prefers-slot-identity`、`test-freely-ai-account-switch`、`test-freely-ensure-manager` 一起锁住 slot-first identity、no-launch gate 和 manager bootstrap handoff contract
  - `test-freely-global-account-watchdog-live` 已真实通过：
    - `worahe3972@outlook.com -> worahe3971@outlook.com`
    - `worahe3973@outlook.com -> worahe3971@outlook.com`
  - live 测试口径已收紧为：监控脚本先启动，切到坏账号后等待当前 AI 进程结束，再验证 watchdog 是否切回脚本真实探测出的可用账号并拉起新 Codex
  - 2026-03-26 closeout audit 追加了当前 verification gate 的 fleet / merge truth：
    - 2026-03-26 upstream absorption followthrough 再次确认当前 authoritative owner 已切到 `feature/upstream-governance-merge-prep-20260327`：`feature/develop-merge-prep-fleet-closure-20260325` 已被当前上游吸收 owner 完整覆盖（`git merge-base --is-ancestor feature/develop-merge-prep-fleet-closure-20260325 HEAD` 成功，且 `feature/develop-merge-prep-fleet-closure-20260325...HEAD = 0/26`），随后对应 worktree 与 local branch 均已删除；当前 retained fleet 因而收缩到 4 棵，writeback 提交后 `./bin/wt-status-all` 与 `./bin/wt-fleet-status` 应回到 `Summary: total=4, dirty=0` 且全部 worktree 显式 `stopped`
    - `feature/manager-scheduler-capacity-candidate-replay-20260324` 相对当前 absorption owner 仍保留未吸收本地历史（`feature/manager-scheduler-capacity-candidate-replay-20260324...HEAD = 24/266`），所以继续保持 `needs_research / retained-with-reason`，不能因为 fleet 已 clean 就误判为可直接退休
    - `git worktree list --porcelain`、`./bin/wt-status-all` 与相关 worktree `git status` 当前 authoritative fleet truth 已继续前移到 12 棵 worktree，latest stable recheck 为 `Summary: total=12, dirty=1`；当前唯一 dirty owner 只剩 `feature/develop-merge-prep-fleet-closure-20260325`。此前 continuity 里的 5-tree / 7-tree / 10-tree snapshot、旧 prompt 注入的 6-tree / 9-tree closeout inventory，以及 04:47 PDT 写下的 `dirty=3` 都不再构成当前 cleanup 真相
    - `feature/manager-scheduler-capacity-candidate-replay-20260324` 当前已 clean，继续保持 `needs_research / retained-with-reason`，但 blocker 仍是 canonical `develop` proof writeback，而不是 replay-owner-local review readiness
    - `feature/intake-absorption-closure-governance-20260326` 当前 `develop...HEAD = 3/0`、supervisor/AI 都 down 且 worktree clean；因为 canonical docs 仍缺准确 owner/phase 吸收，这轮只能保持 `supervision-needed`
    - 当前 dedicated replay owner 相对最新 `develop` 的分叉真相已前移到 `ahead 162 / behind 12`，因此这批证据只能支持 `review-ready`，不能直接支持 promote-complete / cleanup-ready
    - `feature/watchdog-auth-failure-control-plane-recovery-20260326` 与 `feature/watchdog-live-status-and-dispatcher-ready-20260326` 现已出现在 authoritative fleet 中，且提交都被 `develop` 吸收；但 disposition 不能再混写：前者当前仍缺 canonical branch owner/phase，因此是 `ownership-followthrough-needed`；后者已有 completed canonical issue、但缺 branch/worktree cleanup 留痕，因此是 `cleanup-followthrough-needed`。两者都还不能直接宣告 retired
    - `feature/latest-manager-continuity-worker-consumption-reconcile-20260326` 当前 `develop...HEAD = 11/0`，继续作为 unresolved verification/cleanup followthrough
    - `feature/watchdog-probe-early-deactivated-workspace-detect-20260326` 的 `deactivated_workspace` early-detect capability 与 verification evidence 现已被当前 owner 吸收；后续只剩 branch/worktree cleanup，不再维持独立 owner/phase
    - `feature/watchdog-slot-switch-global-launch-gate-20260326` 与 `feature/watchdog-switch-stability-and-probe-freeze-20260326` 当前分别 `develop...HEAD = 5/0` 与 `6/1`，但 canonical docs 仍缺准确 owner/phase，因此这轮只能继续保持 `supervision-needed`
    - 2026-03-25 23:41 PDT 的 develop-side fresh manager cycle 曾在新 continuity / worker prompt materialize 之前命中 `402 Payment Required` / `deactivated_workspace`；这仍是 broadened auth-failure contract 需要存在的历史证据，但在 2026-03-26 canonical proof wave 与 latest manager-continuity worker-consumption repair 之后，已不再构成当前 closeout 的主 blocker
    - `freely live-status --project ...` 已确认 delegated continuation wave 被当前工位吸收，`pending_delegated_continuation_ids=none`；因此这一轮保持 manager-owned completion verification / cleanup governance，而不是新开 replay worker
    - 2026-03-26 03:49 PDT 的 fresh recheck 再次确认 `live-status` 仍是 `last_launch_kind=fresh`、`last_rotation_reason=initial_start`，且最新 continuity 已刷新到 `.freely/run/manager-continuity-20260326-034902.md`；更早的 prompt / continuity snapshot 现在只保留 provenance 价值，不再参与当前 closeout judgement
    - 2026-03-26 03:53 PDT current fresh session 再次复核 `live-status`、`fleet-status`、`git worktree list --porcelain`、`./bin/wt-status-all` 与 `git rev-list --left-right --count develop...HEAD`，结果仍保持 7-tree / dirty=1 / `ahead 162 / behind 6`，因此路由继续固定为 manager-owned `completion_verification -> worktree-maintenance-governance`，并把最新 continuity 前移到 `.freely/run/manager-continuity-20260326-035319.md`
    - 2026-03-26 04:47 PDT current fleet-refresh session 曾把 closeout truth 更新到 10-tree / dirty=3 / `ahead 162 / behind 8`，但这一步现已被 04:57 PDT authoritative refresh supersede
    - 2026-03-26 04:57 PDT current authoritative refresh 再次复核 `live-status`、`fleet-status`、`git worktree list --porcelain`、`./bin/wt-status-all`、targeted sibling `git status --short` 与 `git rev-list --left-right --count develop...HEAD`，结果已更新为 10-tree / dirty=2 / `ahead 162 / behind 10`；因此 continuity 与 prompt 也必须前移到新的 `.freely/run/manager-continuity-20260326-045718.md` / `.freely/run/prompt-20260326-045718.txt`，避免后续会话继续消费 04:47 PDT 的 stale snapshot
    - 2026-03-26 05:26 PDT current first-jump refresh 再次复核 `live-status`、`fleet-status`、`git worktree list --porcelain`、`./bin/wt-status-all`、targeted sibling `git status --short` 与 `git rev-list --left-right --count develop...HEAD`，结果继续稳定在 10-tree / dirty=2 / `ahead 162 / behind 10`；新的 continuity / prompt 应以前移到 `.freely/run/manager-continuity-20260326-052623.md` / `.freely/run/prompt-20260326-052623.txt` 为准，并明确 scheduler candidate 当前缺的是 canonical `develop` proof writeback，而不是 replay-owner-local evidence
    - 2026-03-26 16:38 PDT current refresh 再次复核 `live-status`、`fleet-status`、`git worktree list --porcelain`、`./bin/wt-status-all`、targeted sibling `git status --short` 与 `git rev-list --left-right --count develop...HEAD`，结果继续保持 10-tree / dirty=2，但当前 replay owner 已前移到 `ahead 162 / behind 12`；新的 continuity 应以前移到 `.freely/run/manager-continuity-20260326-163850.md` 为准，并继续把 scheduler candidate 缺口固定为 canonical `develop` proof writeback blocker，而不是 replay-owner-local evidence

## Closure Judgment

- 当前 issue family 已完成 canonical replay closeout。
- `20260326-global-ai-account-watchdog-canonical-replay-verification` 已确认能力在 canonical `develop` 上 materialize，focused replay 覆盖 slot-sweep-first recovery、detached control-plane survival、dispatcher-ready gating、slot-first identity、timeout artifact preservation 与 early `deactivated_workspace` detection，未发现 reopen 证据。
- 当前 authoritative fleet truth 已收敛到 4-tree / dirty=0 / all stopped；旧的 7-tree / 10-tree / 12-tree continuity snapshot 仅保留 provenance，不再构成 blocker。
- historical note: `C-20260323-2045-A` was previously kept as an independent retained research owner while canonical `develop` still lacked the scheduler proof wave. That is no longer the current truth. Canonical candidate/milestone/progress artifacts now record it as absorbed supporting evidence, so the replay branch is retirement followthrough only, not an active owner surface.

## Next

- 本 issue 已完成；后续若 watchdog/account bootstrap 还出现新缺口，只能作为新的 runtime/dev 增量承接，不回写当前 issue。
- 当前同族后续只剩：
  - 若 scheduler 未来出现 fairness / quota / transaction 等新边界，则新开 lifecycle
  - 更广义的 interruption backlog / manager-owned absorption followthrough
- 当前批次固定下来的 contract 为：
  - probe 才是真理，cooldown 不再参与恢复逻辑
  - sweep / reprobe 窗口内所有 AI launch 都必须被阻塞
  - all-unavailable 时 watchdog 继续活着，但 manager / worker 保持 down
  - inventory 变化或后续 probe 命中 usable slot 后，先写 handoff，再恢复主管
