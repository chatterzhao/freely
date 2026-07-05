# 预研头脑风暴：manager-stall-reentry-false-positive-supervision-thrash

## 背景

`2026-03-28` 这轮 `develop` dogfood 里，用户感知到的问题不是“Freely 完全没跑”，而是“主任务按理应已完成，但 manager 一直像在忙，又迟迟不收口”。

现场核对后，这个现象已经可以拆成两层：

1. 老问题仍在：
   - `2026-03-28 01:16:38 PDT` 与 `01:20:34 PDT` 两轮 manager AI 结束时明确记录了 `exit_reason=auth_failure`
   - 更早的 `2026-03-25` continuity / prompt 也已经把 `HTTP 402 Payment Required` 与 `deactivated_workspace` 归到同一类 Codex availability/auth 故障
2. 但这不是当前唯一阻塞：
   - 从 `2026-03-28 01:23:59 PDT` 之后，`develop` manager 的主要退出原因切成了 `operator_stop`
   - `.freely/run/preemption-state.env` 多次写出：
     - `LAST_PREEMPTION_REASON="local_continuation_reentry"`
     - `LAST_PREEMPTION_INTAKE_ID="runtime-stalled-ai-recovery"`
   - 说明当前控制面把 manager AI 判成 stalled，然后由 runtime 自己 TERM 掉重起

因此当前更值得新开预研的问题，不是“auth_failure 是否存在”，而是：

- 为什么 manager 在 canonical worker 明显仍在推进时，会持续被 `runtime-stalled-ai-recovery` 判定并重入？
- 这是否已经从“正确 stall recovery”演变成“false positive supervision thrash”？

## 问题定义

当前 `develop` manager 正在承担 supervision-only 角色。它的实际职责是：

1. 巡检 fleet / canonical lane
2. 产出 manager continuity 与 superseding worker prompt
3. 若 same-lane worker 仍 active，则保持 `queued_same_lane_busy`
4. 等待 canonical worker 继续 IBM / dev-loop，而不是自己在 `develop` 做实现

但当前 runtime stall contract 仍偏向这样一种假设：

- 当前 prompt 含 delegated continuation
- 且超过阈值没有新的 cycle-log / continuity / handoff 前进
- 那么 manager AI 很可能已经假活，应该触发 `runtime-stalled-ai-recovery`

这条假设能覆盖“prompt 已吸收 delegated continuation，但 manager 假活不产出”的场景，却没有稳定覆盖另一类合法长轮次：

- manager 已经完成本轮监督判断
- same-lane worker 仍 active，所以不会产生新的 launchable worker prompt
- manager 此时更接近 `waiting_on_worker` / `supervision_idle`
- 但当前 runtime 没有明确的 idle-safe state / heartbeat / wait contract
- 结果 `90s` 后被误判成 stalled，触发本地 continuation reentry

如果这个缺口存在，Freely 就会持续出现：

1. worker 其实在推进真实任务
2. manager 也不是无事可做，而是在重复写监督 handoff
3. 但 runtime 看不到“这是合法等待”，于是不断重启 manager
4. 最终形成 supervision thrash，而不是纯 auth failure 或纯 worker stall

## 当前现场证据

### 0. 最新冻结现场（`2026-03-28 02:06 PDT` 左右）

在完成三路 review 后，又补做了一轮 develop 现场核对，并确认 Freely 已进入“不值得继续放着空转”的状态：

- `freely live-status --project <develop>` 显示：
  - `activity_state: stalled_without_runtime`
  - `desired_runtime_state: running`
  - `last_supervisor_state: up`
  - `last_ai_state: down`
  - `last_exit_reason: starting`
- `freely fleet-status --project <develop>` 显示：
  - `develop` 当前 `sup=none ai=none`
  - canonical worker `feature/start-restart-control-plane-semantics-20260327-200651` 当前也 `sup=none ai=none`
  - canonical worker 仍是 `DIRTY`，并带 `checkpoint=true`
- 最新 `.freely/run/manager-worker-launch-state.env` 显示：
  - `LAST_MANAGER_CONTINUITY_GENERATED=".../manager-continuity-20260328-014114.md"`
  - `LAST_MANAGER_WORKER_PROMPTS_CONSUMED=".../20260328-003441-worker-start-restart-control-plane-ibm-materialization-codex.txt"`
  - `QUEUED_WORKER_PROMPTS="...004525..., ...004859..., ...005230..., ...005619..., ...011227..., ...011652..., ...014114..."`
  - `ACTIVE_RUNNING_WORKER_COUNT="0"`
  - `UPDATED_AT="2026-03-28T09:06:32Z"`
- 最新 `.freely/run/preemption-state.env` 仍是：
  - `LAST_PREEMPTION_REASON="local_continuation_reentry"`
  - `LAST_PREEMPTION_INTAKE_ID="runtime-stalled-ai-recovery"`

因此可以把最新坏态明确冻结为：

1. manager recovery 先前很可能误杀了 lawful supervision wait
2. 经过多轮重入后，系统又进入 `queued prompts retained but active worker already gone`
3. develop manager 与 canonical worker 最终都掉成 `desired=running but no runtime`
4. 继续让 Freely 自转只会重复烧 token，而不会自然收敛出新的诊断价值

基于这一轮证据，已执行 `freely stop --project <develop>`，主动停止空转，保留现场用于后续测试设计与最小修复实验。

### 1. canonical worker 曾真实推进，但当前现场已不再是单纯 active-worker 等待

`feature/start-restart-control-plane-semantics-20260327-200651` 在本轮早些时候并不是假活空树：

- worker `live-status` 仍显示 `activity_state: ai_active`
- 该 worktree 已新增：
  - `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/**`
  - `docs/epics/workspace-routing-foundation/global-restart-restore-memory-governance/**`
  - `docs/B1-docs/raw-20260327-2006/**`
- 其中两份 issue 文档已经写成 `done_ibm`：
  - `I-20260327-2006-A`
  - `I-20260327-2006-B`

这说明 worker 不是“完全没做事”，而是已经从 pre-brainstorm 推进到了 IBM materialization。

但到最新一次现场核对时，状态又进一步恶化：

- `freely live-status --project <develop>` 显示 `activity_state: stalled_without_runtime`
- `manager-worker-launch-state.env` 显示：
  - `ACTIVE_RUNNING_WORKER_COUNT="0"`
  - `QUEUED_WORKER_PROMPTS="...004525..., ...004859..., ...005230..., ...005619..., ...011227..., ...011652..., ...014114..."`
- `freely fleet-status` / `./bin/wt-fleet-status` 也显示 develop manager 与 canonical worker 当前都处于 `desired=running` 但 supervisor/AI 都已 down

所以当前不能再把问题仅表述成“active worker 正常运行，但 manager 被误杀”。

更准确的说法是：

1. 最初 thrash 很可能始于合法 supervision wait 被误判
2. 但在反复 `local_continuation_reentry` 之后，系统已经演化到另一种坏状态：
   - manager continuity / queued prompts 还留在控制面
   - 真实 worker 已不在运行
   - develop manager 自己也再次 stalled
3. 因而当前研究对象应扩成：`manager stall recovery` 与 `manager-worker-launch-state` 的契约失配，导致 false positive 与 stale queue 可以串联出现

### 2. manager 的新增价值在快速下降

`develop` manager 近几轮主要在重复做同一件事：

- 继续确认 canonical owner 仍是 `feature/start-restart-control-plane-semantics-20260327-200651`
- 重写 superseding worker prompt
- 把 dispatch state 写成 `queued_same_lane_busy`
- 维持“same-lane worker 已运行，所以不要再开新 writer”

从 runtime 角度看，它确实有产物输出，但这些产物在语义上接近“监督侧重复确认”，而不是新一轮 substantive route shift。

### 3. manager 被 runtime 自己反复打断

当前 `develop` 的 `.freely/logs/runtime-events.log` 已显示一串模式：

- `2026-03-28T08:23:59Z event=operator_stop_requested`
- `2026-03-28T08:24:00Z event=supervisor_cleanup ... exit_reason=operator_stop`
- `2026-03-28T08:24:08Z event=supervisor_started`
- 后续 `08:27:29Z`、`08:31:02Z`、`08:34:12Z`、`08:37:53Z`、`08:41:01Z`、`08:44:42Z` 反复出现同型 `operator_stop`

并且 `.freely/run/preemption-state.env` 当前最新仍是：

- `LAST_PREEMPTION_MODE="graceful_term"`
- `LAST_PREEMPTION_REASON="local_continuation_reentry"`
- `LAST_PREEMPTION_INTAKE_ID="runtime-stalled-ai-recovery"`

这说明这些 stop 不是用户显式 `freely stop`，而是 runtime 自己触发的 manager stall recovery。

### 4. 当前 stall detector 缺少 idle-safe 分支

`docs/system/workspace/scripts/runtime/freely` 当前相关逻辑是：

1. `manager_ai_runtime_recovery_reason()` 依次判断：
   - `manager_ai_stalled_with_pending_intake`
   - `manager_ai_prompt_superseded_by_new_intake`
   - `manager_ai_stalled_after_delegated_continuation_prompt`
2. 一旦命中，就会：
   - `write_manager_bootstrap_handoff(...)`
   - `request_local_continuation_reentry "$project" "runtime-stalled-ai-recovery"`
   - `restart_manager_supervisor_preserving_handoff "$project"`

其中 `manager_ai_stalled_after_delegated_continuation_prompt()` 的关键条件是：

- manager AI 仍在
- 当前 prompt 带 `Delegated continuation handoff`
- 当前 cycle-log 与 prompt-file 都超过阈值未更新
- 若已有更新后的 continuity，则只有在 `manager_continuity_has_unconsumed_launchable_worker_prompt` 成立时才继续判 stalled

这条判断仍然默认：

- “delegated continuation 进入 prompt 后，若长期无新 continuity / launchable worker prompt，就应当恢复”

但对当前 `queued_same_lane_busy` 场景，这个前提并不总成立：

- same-lane worker 已经在跑
- manager 本轮未必应该再生成 launchable prompt
- 此时“没有 launchable worker prompt”是正常监督结果，不一定是 stall

### 5. launch-state 真相其实已经部分存在，但 stall detector 还没稳定消费它

当前并不是完全没有 runtime state 可用。

`develop` 当前的 `.freely/run/manager-worker-launch-state.env` 已经同时写出：

- `ACTIVE_RUNNING_WORKER_COUNT="1"`
- `LAST_MANAGER_WORKER_PROMPTS_CONSUMED="...003441..."`
- `QUEUED_WORKER_PROMPTS="...004525..., ...004859..., ...005230..., ...005619..., ...011227..., ...011652..., ...014114..."`
- `UPDATED_AT="2026-03-28T08:57:47Z"`

在最初现场里，这至少说明两件事：

1. runtime 已经知道“当前确实有 active worker 在跑”
2. runtime 也已经知道“后续 prompt 只是排队，不是每一轮都 launchable”

因此当前缺口未必是“完全缺一个新 artifact”，更可能是：

- stall detector 当前只会问“有没有 unconsumed launchable worker prompt”
- 但不会问“当前 continuity 的正常结论是否正是 same-lane busy + active worker already running”

也就是说，最可能缺的不是数据采集，而是 runtime recovery 在判 stalled 时没有消费现有 `manager-worker-launch-state` 的 queue/busy truth。

而在最新现场里，这个缺口又暴露出第二层风险：

- queue truth 可能会持续保留
- 但 runtime 没有在 stall recovery 后强制核对“queued prompt 对应的 canonical worker 是否仍存活”
- 结果就可能出现：
  - `QUEUED_WORKER_PROMPTS` 仍在
  - `ACTIVE_RUNNING_WORKER_COUNT="0"`
  - manager 仍沿用旧的 delegated continuation prompt 继续被判 stalled

因此当前需要冻结的不只是 `same-lane busy`，还包括：

1. 哪些 queued prompt 仍然代表可等待的 lawful worker
2. 哪些 queued prompt 在 active worker 消失后应重新变成 launchable
3. manager stall detector 在看到 `queued>0 && active=0` 时，应该 reroute 到 relaunch worker / recovery，而不是继续沿用“supervision wait”的解释

### 6. 当前测试覆盖偏向“该恢复时会恢复”，缺少“合法等待时不应恢复”

## 最新收敛

在冻结 `develop` 现场后，已在能力真源 [freely](/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260328-0154-feature-manager-stall-local-continuation-reentry-research/docs/system/workspace/scripts/runtime/freely) 上落最小 runtime 修复，并补齐针对本轮真实风险的离线测试。

当前最小修复包含三条约束：

1. `manager_ai_stalled_after_delegated_continuation_prompt()` 只会让“当前或更新的 continuity”抑制 stall recovery，不再让旧 continuity 跨轮次吞掉当前 prompt 的恢复。
2. `manager_continuity_waiting_on_active_busy_worker()` 对 stale runtime worktree refs、缺失 prompt file、无法解析的 target worktree 都转为保守失败，不再允许“一条 busy worker + 一条坏 prompt”整体伪装成 lawful wait。
3. 对同轮 prompt / continuity 的时间边界放宽到 `>=`，避免因为文件时间粒度过粗，把本来合法的 same-round supervision wait 误打成 stall。

已通过的新增 targeted tests：

- `test-freely-manager-delegated-continuation-active-worker-wait-does-not-recover`
- `test-freely-manager-delegated-continuation-mixed-busy-and-launchable-recovers`
- `test-freely-manager-delegated-continuation-older-busy-continuity-recovers`
- `test-freely-manager-delegated-continuation-busy-and-stale-prompt-recovers`
- `test-freely-manager-worker-launch-relaunches-stale-queued-prompt`

同时回归通过的相关既有 tests：

- `test-freely-manager-delegated-continuation-stall-recovery`
- `test-freely-manager-stall-recovery`
- `test-freely-manager-stall-recovery-unconsumed-launchable-prompt`
- `test-freely-manager-generated-handoff-stall-recovery`
- `test-freely-manager-worker-launch-busy-worker-queue`

当前结论更新为：

- `same-lane busy` 的 lawful wait 已有一个最小、保守、可测试的 runtime contract。
- “旧 continuity 抑制当前恢复” 与 “busy worker 掩盖 stale prompt” 这两类新退化已被测试冻结。
- `develop` 仍应继续保持停机，直到这条 lane 完成 code review / merge 决策；当前没有理由恢复 live dogfood。

当前脚本级测试里，已经能看到：

- `test-freely-manager-stall-recovery`
- `test-freely-manager-delegated-continuation-stall-recovery`
- `test-freely-manager-stall-recovery-unconsumed-launchable-prompt`
- `test-freely-manager-generated-handoff-stall-recovery`

这些都在验证：

- prompt stalled 后 recovery 会触发
- generated handoff / launchable prompt stalled 后 recovery 会触发

但当前没看到对应的负向用例去冻结：

- canonical worker 已 active
- manager launch-state 明确是 `queued_same_lane_busy`
- manager 没有新的 launchable worker prompt，本轮只是合法等待 worker
- 此时 `recover_stalled_manager_ai_if_needed` 不应触发

如果这条 negative test 不存在，当前 false positive 很容易在“真 stall recovery 逻辑一直通过”的情况下混进 `develop` dogfood。

### 7. 现在不应继续在线 dogfood，而应先转向离线测试锁边界

到这一步，证据面已经足以支撑预研判断：

- 三个 loop 的方法论本身没有发现根本性错误
- manager stall detector 与 launch-state truth 存在契约失配
- 当前 live 现场已经从“更干净的误判 wait”恶化到“stale queue + worker down”

所以后续最稳的路线不应再是继续放 develop runtime 自跑，而是：

1. 先在脚本测试里冻结负向边界
2. 再做最小判据实验
3. 最后才决定 runtime 真源应消费现有 launch-state，还是显式新增 `waiting_on_worker` 契约

## 当前最小 materialization 结果

在停止 develop runtime 空转后，已经先做了一轮最小实现与离线验证，目标不是“一次性彻底修完 control plane”，而是先把最危险的误杀边界锁住：

### 已落的最小 runtime 变更

`docs/system/workspace/scripts/runtime/freely` 当前已补一个非常窄的 helper：

- `manager_continuity_waiting_on_active_busy_worker()`

它的语义不是“只要看到 active worker 就 suppress recovery”，而是更保守的：

1. 基于当前 continuity 的 worker prompt 集合逐个看 target worktree
2. 已消费且仍 active 的 prompt 视为已在执行，不构成新 launchable demand
3. 未消费 prompt 若对应 `active + delegated-continuation-busy` worker，视为 lawful wait
4. 只要存在任何一个未消费 prompt 不属于上述 lawful wait，就不能 suppress recovery

随后 `manager_ai_stalled_after_delegated_continuation_prompt()` 在 delegated continuation aging 路径上先消费这层 truth：

- 如果 continuity 当前只是“等待 active busy worker”，则不触发 `local_continuation_reentry`
- 如果 continuity 里还混有其他仍应 launch / relaunch 的 prompt，则仍保持现有 recovery 能力

这轮实现还顺手把该函数结尾补成显式 `return 0`，避免 shell 函数只靠隐式最后命令状态来表达 stalled 结果。

### 新增测试边界

本轮新补了三条关键测试：

1. `test-freely-manager-delegated-continuation-active-worker-wait-does-not-recover`
   - 冻结：合法等待 active busy worker 时，manager 不得被 stall recovery 误杀
2. `test-freely-manager-delegated-continuation-mixed-busy-and-launchable-recovers`
   - 冻结：即便 continuity 里有一个 active busy worker，只要还混有其他真 launchable prompt，recovery 仍必须触发
3. `test-freely-manager-worker-launch-relaunches-stale-queued-prompt`
   - 冻结：`QUEUED_WORKER_PROMPTS` 残留、但 target worker 已不在运行时，manager launch path 应重新发起 launch，而不是把 stale queue 永久留在控制面

另外还顺手清理了一个已有测试环境噪音：

- `test-freely-manager-stall-recovery-unconsumed-launchable-prompt`
  - 补建 worker `.freely/run` 目录，避免出现无关的 `find: No such file or directory`

### 当前已跑通过的相关测试

- `test-freely-manager-delegated-continuation-active-worker-wait-does-not-recover`
- `test-freely-manager-delegated-continuation-mixed-busy-and-launchable-recovers`
- `test-freely-manager-delegated-continuation-stall-recovery`
- `test-freely-manager-stall-recovery-unconsumed-launchable-prompt`
- `test-freely-manager-semantic-loop-status-surface`
- `test-freely-manager-worker-launch-busy-worker-queue`
- `test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
- `test-freely-manager-worker-launch-relaunches-stale-queued-prompt`

### 当前判断

截至这一步，可以把问题收敛成：

1. 最危险的 false-positive supervision thrash 边界已经有最小防线
2. `queued prompts` 与 worker liveness 之间的 stale-state 问题也已有一条离线回归保护
3. 但这还不等于“control plane 问题全修完”

后续仍需继续核对的，是不是还存在更深层的 manager/worker launch-state 漂移、以及是否需要把这轮最小修复正式 materialize 为 milestone-owned issue / IBM，而不是一直停留在 pre-brainstorm 研究态

## 与既有 issue / pre-brainstorm 的关系

这条新问题与下列已存在家族相邻，但并不等价：

1. `20260323-1705--manager-delegated-continuation-stall-recovery`
   - 该条关注的是“delegated continuation 进入 prompt 后假活无产出”
   - 当前问题则更窄：manager 已经给出监督结论，但在 `same-lane busy` 等合法等待态里仍被误杀
2. `20260324-0405--watchdog-restart-storm-and-process-churn-detection`
   - 该条关注 restart storm signal 与 manager escalation
   - 当前问题更像“restart storm 的一个上游诱因”：stall detector 误判合法监督态，主动制造 churn
3. `20260327-1845--manager-consumed-continuity-resume-routing-drift`
   - 该条关注 manager resume 后回到 generic patrol
   - 当前问题更偏向 runtime stall contract 本身的过度激进，不是 route narrowing 漂移
4. `I-20260322-0412 worker-active-reentry-for-manager-delegated-continuation-governance`
   - 已解决 active worker 被 manager 新 intake 命中时如何 reentry
   - 当前问题不是 worker reentry 缺失，而是 manager 自己缺少 `waiting_on_worker` 的稳定 contract

## 核心假设

### 假设 A：当前缺的是 manager supervision idle-safe contract

runtime 现在能识别：

- 有新 intake 需要 manager 吸收
- prompt 已 superseded
- delegated continuation prompt 后长时间无产出

但还不能识别：

- “manager 本轮已完成 lawful supervision judgement，当前只是等待 active worker”

因此最可能缺的是一个显式状态：

- `manager_waiting_on_worker`
- `same_lane_busy_wait`
- `supervision_idle_after_handoff`

名称可再议，但它必须能让 runtime 区分：

- 假活 stall
- 合法等待

### 假设 B：当前 heartbeat 真相面不足

当前 stall 判断主要依赖：

- cycle log mtime
- prompt file mtime
- continuity / worker-prompt 生成状态

但 manager 在长轮监督里可能做的是：

- 读 fleet
- 对齐 branch-local continuity
- 保持 same-lane busy judgement
- 暂时不再写新 continuity

如果没有更细的 heartbeat / explicit wait marker，仅靠文件 mtime 容易把合法长轮判成假活。

### 假设 C：`queued_same_lane_busy` 需要成为一等 runtime truth

当前 same-lane busy 只在 manager continuity / worker prompt 里作为监督结论出现。

但 runtime stall recovery 需要的是更直接的 control-plane truth：

- 当前 lane 是否已有 active lawful writer

### 假设 D：queue truth 还需要和 active-worker liveness 一起解释

最新现场显示，仅有 queue/busy truth 还不够。runtime 还需要知道：

- queued prompt 所依赖的 canonical worker 是否仍在跑
- 若已不在跑，queued prompt 是不是应被重新评估为 launchable
- stall recovery 是否应该优先把 manager 带回“重新核对 queue/liveness”的分支，而不是继续把旧 delegated continuation prompt 当作唯一事实源

否则系统会从“误判 lawful wait”进一步退化成“lawful wait 被误杀后，留下 stale queue + no worker + stalled manager”的双重失配。
- 当前 continuity 是否已经被消费成“同 lane 合法等待”，而不是“还有 launchable prompt 未发出去”

## 代码级评审结论

### 结论 1：误判窗口确实存在，而且根因更像“判据没有消费完整 truth”

`docs/system/workspace/scripts/runtime/freely` 里的 `manager_ai_stalled_after_delegated_continuation_prompt()` 当前只在一种情况下把“新 continuity 比 prompt 更新”继续视为 stall：

- `manager_continuity_has_unconsumed_launchable_worker_prompt "$project" "$continuity_file"`

这条判断对“确实还有 launchable prompt 没被消费”的场景是合理的，但它没有对称消费另一类 truth：

- `manager-worker-launch-state.env` 已经记录 `ACTIVE_RUNNING_WORKER_COUNT>0`
- 当前 continuity 对应 prompt 集合处于 `QUEUED_WORKER_PROMPTS`
- 这些 queued prompt 是 `worker_project_busy_with_delegated_continuation` 导致的 same-lane busy，而不是 dispatch 漏发

这意味着 runtime 当前能看到“还有 launchable prompt 才算 stalled”，但还看不到“本轮监督结论本来就是 active worker + same-lane busy wait，因此不应恢复”。如果现场确实处于后者，当前 stall detector 就会把 lawful wait 误杀成 stall。

### 结论 2：launch-state 观察面已经部分具备 idle-safe 所需真相

`write_manager_worker_launch_state()` 与 `manager_worker_launch_state_refresh_for_status()` 已经把这几层 truth 固化到状态文件：

- `LAST_MANAGER_CONTINUITY_GENERATED`
- `LAST_MANAGER_WORKER_PROMPTS_GENERATED`
- `LAST_MANAGER_CONTINUITY_CONSUMED`
- `LAST_MANAGER_WORKER_PROMPTS_CONSUMED`
- `QUEUED_WORKER_PROMPTS`
- `ACTIVE_RUNNING_WORKER_COUNT`
- `AVAILABLE_NEW_WORKER_SLOTS`

而 `manager_runtime_launch_workers_from_latest_handoff()` 在处理 prompt 时，也已经显式区分：

- active worker
- same-lane busy worker
- parallel-safe / write-scope 冲突
- queue vs launch

所以当前更像“recover 路径没有复用 launch 路径已知的 queue/busy 语义”，而不是完全缺一套控制面状态。

### 结论 3：现有测试覆盖明显偏正向，缺负向冻结

当前脚本测试已经覆盖：

- delegated continuation stall 应触发恢复
- generated handoff stall 应触发恢复
- unconsumed launchable prompt 应触发恢复
- active worker 在 manager launch 时应走 reentry，而不是重新起 supervisor
- live-status / fleet-status 在 active worker 存在时应保守清除 semantic-loop suspicion

但还没看到一个直接冻结 `recover_stalled_manager_ai_if_needed()` 的负向用例，条件大致应是：

- manager prompt 含 delegated continuation
- prompt / cycle log 已过阈值
- latest continuity 已更新
- `ACTIVE_RUNNING_WORKER_COUNT=1`
- 相关 prompt 只存在于 `QUEUED_WORKER_PROMPTS`
- queued 原因来自 same-lane busy / active worker 占位
- 期望：`recover_stalled_manager_ai_if_needed` 返回 false，不写 `preemption-state.env`

没有这类测试时，后续即使做“避免误杀”的修复，也容易在保住正向恢复的同时再次把 lawful wait 判错，或者反过来过度放宽导致真 stall 被漏检。

## 三个 loop 视角下的风险评审

### 1. auto-loop / doc-loop / dev-loop 边界本身没有错，错在 supervision contract 太粗

从 `CONSTITUTION`、`LAWS` 和 `three-loop-capability-lifecycle` 看，当前设计要求是：

- `auto-loop` 负责 outer orchestration / governance
- `doc-loop` 和 `dev-loop` 只产出 evidence
- verification / recovery / cleanup 只是 route，不是新 loop

所以 manager 在 `develop` 上做 supervision-only 是符合三条 loop 设计的。问题不在 loop 边界，而在 runtime 没有给 auto-loop manager 一个足够稳定的“等待 active worker”合同。

### 2. 当前行为有退化 risk：监督抖动会吞噬真正的 worker 推进窗口

一旦 manager 被频繁 `local_continuation_reentry`：

- supervisor/AI 会话不断轮换
- 新 continuity / prompt 会重复生成
- queue 语义被不断覆盖
- 人类和 runtime 都更难判断 canonical worker 是否真正被阻塞

这不是纯观测噪声，而是 control-plane churn；继续放大下去，会直接伤害 auto-loop 的完成判定与 cleanup judgment。

### 3. 修复时最大的回归风险不是“修不好”，而是把真 stall 一起吞掉

当前 recovery 还负责几类真问题：

- pending intake 长时间未吸收
- delegated prompt 被更新 intake supersede
- continuity 生成了可 launch 的 worker prompt，但 manager 假活没消费

如果后续为了避免 same-lane busy 误杀而粗暴加一条“只要有 active worker 就不恢复”，就会把“active worker 存在，但 manager 侧确实还有新的 launchable prompt / superseding intake 未吸收”的真 stall 一起吃掉。这是后续 materialization 必须严防的回归面。

## 下一步研究焦点

1. 冻结 idle-safe contract 的最小判据：它应基于 `manager-worker-launch-state.env` 现有字段，还是需要新增一个显式的 `waiting_on_worker` truth。
2. 证明这个 contract 不会压掉三类真恢复：`pending_intake`、`superseded_by_new_intake`、`unconsumed_launchable_worker_prompt`。
3. 在进入 IBM 之前先补齐 negative test 设计，避免后续实现只靠现场日志回归。
- manager 当前是否只是等待这个 writer，而不是期待新 handoff
- 该等待态的最大允许静默窗口是多少

如果这些仍只是 prompt/continuity 语义，而不是 runtime 可直接消费的 state truth，误判就很难避免。

### 假设 D：问题可能是“已有 state 未被使用”，而不是“完全缺 state”

新补的现场证据表明，`manager-worker-launch-state.env` 已经暴露：

- active worker count
- launched prompt
- queued same-lane prompts

因此下一轮研究要优先回答：

- `manager_ai_stalled_after_delegated_continuation_prompt()` 是否应该直接读取 launch-state，识别 `queued_same_lane_busy + active_running_worker_count>0`
- 还是必须额外引入新的 wait-state / heartbeat 才足够稳

## 进入 candidate 前需要冻结的问题

1. 这条缺口应归类为：
   - same-family follow-on of `manager-delegated-continuation-stall-recovery`
   - 还是新的 runtime control-plane candidate
2. `waiting_on_worker` / `same-lane busy wait` 的 canonical truth 应落在哪里：
   - `session-state.env`
   - `manager-worker-launch-state.env`
   - `workcell-state.env`
   - 还是新的 runtime-owned wait-state artifact
3. stall detector 的放宽条件应基于：
   - explicit wait state
   - heartbeat writeback
   - worker alive + same-lane ownership proof
   - 上述几者的组合
4. 若 availability/auth 仍处于 `probing`，它是否应抑制本类 stall recovery，避免两套恢复机制彼此踩踏
5. manager 在 supervision-only round 允许静默多久，才不至于被误判为 stall
6. 当前 `manager-worker-launch-state.env` 是否已经足够承载 idle-safe judgement，只是 `manager_ai_stalled_after_delegated_continuation_prompt()` 尚未消费它
7. 是否应先补一条 negative regression test，冻结 `queued_same_lane_busy + active worker` 不触发 manager reentry

## 当前最小冻结结论

1. 当前现象已经不能只归因于 `auth_failure`
   - `auth_failure` 是持续老问题
   - 但 `operator_stop + local_continuation_reentry + runtime-stalled-ai-recovery` 已构成独立控制面问题
2. canonical worker 当前确实在推进真实任务
   - 因此“主任务没动”不是事实
3. 当前最可疑的缺口是：
   - manager supervision phase 缺少 idle-safe / waiting-on-worker contract
4. restart storm 目前更像次生症状
   - 若这个 false positive 不消除，restart storm 只会继续被 stall detector 自己制造
5. 当前回归面存在明显负向用例缺口
   - 在补齐 “same-lane busy 合法等待时不应恢复” 前，任何 stall recovery 改动都容易再次误伤 supervision-only round

## 下一步研究

1. 对齐 `manager_ai_stalled_after_delegated_continuation_prompt()` 与 `manager_continuity_has_unconsumed_launchable_worker_prompt()` 的完整判据
2. 抽样 `develop` manager 最近几轮 cycle-log，确认每次被 TERM 前是在读现场、在写 continuity，还是已进入纯静默等待
3. 比对 current `develop` 与 canonical worker worktree 的状态面：
   - `session-state.env`
   - `manager-worker-launch-state.env`
   - `workcell-state.env`
   - `preemption-state.env`
4. 研究是否已有旧 issue 能合法吸收这条缺口；若不能，再 materialize 成新的 runtime control-plane candidate
