# 预研头脑风暴：operator-stop-runtime-stall-recovery-semantics

## 背景

`2026-03-28` 在把 `manager delegated continuation stall recovery` 修复合入 `develop` 后，重新启动 Freely 做 dogfood 观察，出现了一个新的表面现象：

- `develop` manager 与 canonical worker 都能成功启动
- `worker_auto_recovered=1`，说明 manager 已经能先恢复预期 worker，再进入本轮 prompt
- `pending_delegated_continuation_ids` 变成 `none`
- 但几分钟后 runtime-events 又出现：
  - `event=operator_stop_requested`
  - `event=operator_stop_signal_child`
  - `event=supervisor_cleanup ... exit_reason=operator_stop`
  - 随后又自动拉起新一轮 supervisor / AI

因此需要把问题重新定义清楚：

1. `operator_stop_requested` 在这里到底表示什么
2. 它是产品层“有意的 stop/restart 语义”，还是控制面内部恢复动作的外显日志
3. 当前这轮 stop/restart 是预期需求，还是 watchdog / stall detector 仍然存在新的误判

## 现场证据

### 1. 这次不是直接 `auth_failure`

旧日志里前两轮确实有：

- `2026-03-28T08:16:38Z ... exit_reason=auth_failure`
- `2026-03-28T08:20:34Z ... exit_reason=auth_failure`

但重新用修复后的 `develop` 启动后，这轮新现场首先表现为：

- `2026-03-28T10:27:43Z event=supervisor_started`
- `2026-03-28T10:27:48Z event=worker_auto_recovered ... recovered_workers=1`
- `2026-03-28T10:27:53Z event=ai_launch_begin`

然后才在约 3-4 分钟后出现：

- `2026-03-28T10:31:30Z event=operator_stop_requested`
- `2026-03-28T10:31:31Z event=supervisor_cleanup ... exit_reason=operator_stop`
- `2026-03-28T10:31:57Z event=supervisor_started`
- `2026-03-28T10:32:02Z event=ai_launch_begin`
- `2026-03-28T10:35:21Z event=operator_stop_requested`
- `2026-03-28T10:35:22Z event=supervisor_cleanup ... exit_reason=operator_stop`
- `2026-03-28T10:35:34Z event=supervisor_started`
- `2026-03-28T10:46:56Z event=operator_stop_requested`
- `2026-03-28T10:46:57Z event=supervisor_cleanup ... exit_reason=operator_stop`
- `2026-03-28T10:47:06Z event=supervisor_started`
- `2026-03-28T10:47:11Z event=ai_launch_begin`
- `2026-03-28T10:50:32Z event=operator_stop_requested`
- `2026-03-28T10:50:33Z event=supervisor_cleanup ... exit_reason=operator_stop`
- `2026-03-28T10:50:42Z event=supervisor_started`
- `2026-03-28T10:50:47Z event=ai_launch_begin`

所以当前主现象已经不是“manager 立即被 auth failure 打掉”，而是“manager 被 runtime 自己周期性 TERM 后重启”。

### 2. 实际触发者是 `runtime-stalled-ai-recovery`

最新 `.freely/run/preemption-state.env` 记录为：

- `LAST_PREEMPTION_MODE="graceful_term"`
- `LAST_PREEMPTION_REASON="local_continuation_reentry"`
- `LAST_PREEMPTION_INTAKE_ID="runtime-stalled-ai-recovery"`
- `LAST_PREEMPTION_PID="17215"`

这说明当前 stop 不是用户显式执行 `freely stop`，而是 runtime 内部的 stall recovery：

1. watchdog 判定 manager AI 已 stalled
2. 执行 `request_local_continuation_reentry`
3. 该函数 TERM 当前 AI pid，并写入 `local_continuation_reentry`
4. supervisor 收到信号后记录 `operator_stop_requested`

## 控制流解剖

### 1. `operator_stop_requested` 只是 supervisor 侧外显事件

`docs/system/workspace/scripts/runtime/freely` 中 `request_stop()` 会：

- 把 `DESIRED_RUNTIME_STATE_VALUE` 设为 `stopped`
- 记录 `LAST_WORKCELL_EXIT_REASON="operator_stop"`
- 记 runtime event：
  - `operator_stop_requested`
  - `operator_stop_signal_child`

并且 supervisor 只在收到 `INT TERM` 时触发 `request_stop()`。

所以 `operator_stop_requested` 并不天然等于“用户发出了产品级 stop 命令”。它只是 supervisor 收到一个 stop signal 后的统一日志语义。

进一步代码核对确认：

- `event=operator_stop_requested` 只有这一个 authoritative emit site
- `cmd_stop()` 自己不会直接写这个事件
- 只有 live supervisor 真正执行了 `trap request_stop INT TERM`，这个事件才会落盘

因此如果日志里出现 `operator_stop_requested`，至少说明两件事：

1. 当时确实存在活的 supervisor
2. 它确实收到了一个 signal，而不是单纯写了 stop marker 或停止态文件

### 2. 当前 signal 来源是 stall recovery，不是产品 stop 需求

真正触发信号的是：

- `recover_stalled_manager_ai_if_needed()`
  - 先通过 `manager_ai_runtime_recovery_reason()` 选择 stall reason
  - 然后调用 `request_local_continuation_reentry "$project" "runtime-stalled-ai-recovery"`
  - 再 `restart_manager_supervisor_preserving_handoff`

`request_local_continuation_reentry()` 本身会：

- 找到当前 AI pid
- 直接 `kill "$ai_pid"`
- 写入 preemption-state：
  - mode=`graceful_term`
  - reason=`local_continuation_reentry`
  - intake_id=`runtime-stalled-ai-recovery`

因此当前链条更准确地表示为：

`watchdog stall verdict -> local_continuation_reentry -> supervisor logs operator_stop_requested`

而不是：

`operator explicitly asked for stop -> runtime obeyed product stop contract`

### 3. 这条链本质上是控制面恢复语义

从产品语义上看，项目级 `start/stop/restart` 与全局 stop/restart 的控制面 contract 是另一条需求线，当前 canonical lane 也正在研究它。

但这次日志里的 `operator_stop_requested` 不是那条产品需求本身的证据。它更像：

- runtime 为了复用统一 supervisor 停机路径
- 把内部恢复动作映射到了同一套 stop/cleanup event 名称

也就是说，这里更像“控制面恢复动作的复用命名”，不是“用户想要的 restart/restore 功能已经在这里表达出来了”。

subagent 代码复核还确认了一条重要负边界：

- `freely stop --project <project>` 是 intended operator control surface
- 但“日志里出现 `operator_stop_requested`”这件事本身并不能证明是用户显式执行了 `freely stop`
- 同一个事件也会在 supervisor 被 runtime 内部 `TERM` 时出现

所以当前现场里看到的 `operator_stop_requested`，不能直接被解读为产品 stop 需求已经触发；还必须结合 `preemption-state.env` 与 `runtime-stalled-ai-recovery` 一起看。

## 当前判断

### 1. 这更像 runtime/control-plane 行为，而不是用户需求功能

从现有代码和日志链看，`operator_stop_requested` 在本场景里不应被解释成一个新的用户需求入口。它是内部 watchdog recovery 的副产物。

因此当前问题首先属于：

- runtime stall detection
- manager watchdog recovery
- supervisor event semantics / observability

而不是：

- project-scoped restart product contract
- global restart / restore memory product contract

### 2. 但它也暴露出产品可观测性语义不够清晰

虽然根问题更偏 runtime/control-plane，但当前日志命名会带来明显的用户认知歧义：

- 用户看到 `operator_stop_requested`
- 很容易推断成“是不是功能设计上要求它停”
- 实际上这里并不是 operator 发起的产品动作，而是 runtime 自己为了 stall recovery 在 TERM AI

所以它也带出一个 secondary question：

- supervisor event 是否需要区分
  - 用户显式 stop
  - runtime-owned recovery stop

如果不区分，后续调试和产品语义讨论会长期混淆。

## 暂时性结论

当前最合理的中间结论是：

1. `operator_stop_requested` 在这轮现场里不是需求本身，而是 runtime stall recovery 的日志表征
2. 修复后的 `same-lane busy` 边界已经初步奏效，因为 manager 能先恢复 worker，且不再把 delegated continuation backlog 长时间卡在 pending
3. 但 watchdog 仍然在 3-4 分钟后把 manager 判成 stalled，说明剩余问题已经从“active worker 合法等待”转移到更深一层：
   - manager 在成功吸收 delegated continuation 后，到底什么状态算“合法长轮次”
   - 什么状态才该判成 stalled
   - 当前 cycle-log / prompt mtime contract 是否仍把某类合法 manager 工作误判成假活

## 更深一层的流程判断

### 1. 这不是产品 stop loop，而是 runtime 监督 loop 在自杀式重入

从 `PROJECT_INTENT` 与 `three-loop-capability-lifecycle` 的定义看：

- `auto-loop` 是 outer orchestration / governance loop
- `doc-loop` 与 `dev-loop` 是 sibling execution loops
- worker 可以在 sibling loop 内持续推进
- `auto-loop` 只负责监督、路由、completion / cleanup judgement，而不是要求每几十秒都必须产出新的 canonical artifact

当前 manager 正处在这种“outer supervision while worker is active”的位置：

- `develop` manager runtime 活着
- canonical worker runtime 也活着
- `worker_auto_recovered=1`
- `pending_delegated_continuation_ids=none`
- `active_running_worker_count=1`

因此从三个 loop 的站位看，manager 合法地处在一个“监督 + 长轮次思考 + 等待 worker 继续推进”的状态，本身不应该自动等价为 stall。

### 2. 真正的 heartbeat 目前过于依赖 cycle-log 静态输出

当前 runtime 链路是：

1. supervisor 在 `develop` 上启动一轮 manager AI
2. `monitor-ai-cli.sh` 只是把外部 AI CLI 的 stdout/stderr 追加到 `cycle-*.log`
3. manager watchdog 每隔 `10s` 执行一次 `ensure_manager_once()`
4. 只要发现 manager supervisor 和 AI pid 都活着，就进入 `recover_stalled_manager_ai_if_needed()`
5. delegated continuation 场景下，stall detector 目前主要看：
   - 最新 `cycle-*.log` mtime
   - 最新 `prompt-*.txt` mtime
   - 再结合 continuity 文件做少量合法等待豁免
6. 一旦 `cycle_log` 与 `prompt_file` 都超过 `MANAGER_AI_STALL_THRESHOLD_SECS=90` 未更新，就触发：
   - `runtime-stalled-ai-recovery`
   - `local_continuation_reentry`
   - `operator_stop_requested`

这意味着当前 heartbeat 不是：

- AI pid 仍活着
- session/jsonl 仍在推进
- worker 仍活着且 manager 处于 supervision-only 合法等待

而是高度依赖“最近 90 秒内 cycle log 有没有新字节”。

### 3. 现场更像“合法长静默 + 粗粒度 stall detector”

现场 mtime 与复现实证共同表明：

- `cycle-20260328-033534.log` 在 `03:35:39` 启动后，最后一次 mtime 是 `03:37:45`
- 对应这轮 `operator_stop_requested` 发生在 `03:39:23`
- `cycle-20260328-034706.log` 在 `03:47:11` 启动后，对应 `operator_stop_requested` 出现在 `03:50:32`
- `preemption-state.env` 同时记录 `runtime-stalled-ai-recovery -> local_continuation_reentry`

这说明当前问题并不是“manager 真的已经死掉且无人察觉”，而更像：

1. manager AI 进程仍活着
2. worker 也仍活着
3. delegated continuation 已经被当前 manager prompt 吸收
4. 但 manager 在一个合法的 supervision round 中没有持续往 `cycle-*.log` 打出新字节
5. watchdog 于是把“无新输出”过度近似成“stall”

从三个 loop 的定义看，这类长静默 supervision round 本身并不违反系统设计；真正有问题的是 runtime 用来判定它是否 still healthy 的 heartbeat 合同太粗。

### 4. 这更像 suboptimal heuristic / bug，而不是需求要求它这样

把设计文档和实现对齐后，当前结论已经可以更明确：

- `PROJECT_INTENT` 与 `three-loop-capability-lifecycle` 要求 `auto-loop` 做 outer orchestration / judgement，而不是要求每个 manager 监督轮次都必须在短窗口内吐出新的 runtime-visible artifact
- `watchdog-control-plane` 要求 watchdog 在 stall / churn 时提供 signal，但 terminal judgement 仍回 manager；对 restart storm 已经是“signal + observe delay”，不是“直接无限 TERM”
- `continuity-watchdog` 明确区分“watchdog 负责恢复进程”和“AI 负责语义 continuity”，因此 watchdog 不应该仅凭 stdout/stderr 静默就替 AI 宣判该轮 supervision 已失效

所以这次反复 `operator_stop_requested` 更像：

- 一个 runtime/control-plane 层面的 heuristic 过粗
- 表现形式是 manager delegated-continuation supervision round 被误判成 stalled
- secondary issue 是 event naming 让人误以为这是产品级 `operator stop`

换句话说，当前更像“不够稳的实现 + 可观测性语义歧义”，而不是“产品按设计就该每 90 秒自杀式重入一次”。

### 5. 当前实现也不是最优解

就现有 runtime 设计而言，`manager_ai_stalled_after_delegated_continuation_prompt()` 的实现不算最优，原因有三点：

1. 它把 `cycle-*.log` mtime 当成 primary heartbeat，但 `monitor-ai-cli.sh` 只是 stdout/stderr 搬运层，不能稳定代表 manager 是否仍在合法 supervision 中。
2. 它虽然已经对 `active busy worker` 做了一层 lawful-wait 豁免，但豁免真相仍然过窄，无法覆盖“manager 正在监督 active worker、但没有新 log 输出”的健康长轮次。
3. 它对这类 stall 直接走 `request_local_continuation_reentry + TERM + restart`，而不是像 restart storm 那样先 signal / surface / observe，再把 judgement 交还给 `auto-loop`。

因此实现上至少存在一个明显的 asymmetry：

- 对“明显抖动”的 runtime：系统已经有更保守的 signal-first 处理
- 对“可能只是静默监督”的 runtime：系统反而直接强制 TERM

这不是一个理想的风险分配。

## 低回归修复方向

当前最稳的修法，不应该是“先把 90 秒改大”或“先大改三个 loop 合同”，而应该分三层推进。

### 1. 先补负向测试，冻结合法长静默边界

在动 runtime 前，应该先补一条直接命中本案的负向测试：

- manager AI alive
- active worker count > 0
- latest prompt 是 delegated continuation / supervision round
- `cycle-*.log` 静默超过阈值
- 但没有更强证据表明 worker 已死、launchable prompt 积压、或 AI pid 不存在
- 这时 `recover_stalled_manager_ai_if_needed` 不应直接触发 `local_continuation_reentry`

没有这条测试，任何“放宽 stall detector”的修法都容易把真 stall 也一起放掉。

### 2. 优先做窄修，不先全局调阈值

更低回归的方向是给 delegated-continuation supervision 增加更强的 idle-safe contract，例如：

- 当 manager AI 仍活着
- 且当前 prompt 明确处于 delegated continuation supervision
- 且 active worker truth > 0
- 且没有 unconsumed launchable worker prompt / stale queue / dead worker evidence
- 则把这轮状态视为 `supervision_wait`，不直接走 runtime-stalled-ai-recovery

这比全局把 `MANAGER_AI_STALL_THRESHOLD_SECS` 调大更稳，因为：

- 不会把真正的 pending-intake stall 一起放宽
- 不会影响 worker-side stall detector
- 不会改变 restart storm / churn 既有 contract

### 3. 复用已有 signal-first 模式，而不是继续直接 TERM

如果后续证据表明“manager 长静默是否健康”仍然难以仅凭本地 truth 判定，那么更稳的第二层修法是：

- 把这类 delegated supervision quiet-period 先表面化成 runtime signal
- 复用 restart-storm 那套 `surface + observe_delay + manager judgement` 模式
- 避免 watchdog 直接把可疑静默等价为必须 TERM 的 stall

这样既保留 watchdog 的发现职责，也更贴合三个 loop 的 owner 边界。

### 4. 单独处理命名歧义，不和 stall 修复绑死

`operator_stop_requested` 的可观测性歧义是真问题，但不应该和 stall detector 修复硬绑在一个补丁里。

更稳的节奏应是：

1. 先修 false-positive / suboptimal stall contract
2. 再补 runtime event naming 或额外字段，让“explicit operator stop”与“runtime-owned recovery stop”可区分

这样能避免一次补丁同时碰 runtime 行为和对外事件 contract，降低回归面。

## 当前结论

到这一步，可以把问题定性为：

- 不是产品要求 manager 每 90 秒在 delegated-continuation supervision 中自杀式重入
- 更像 runtime stall detector / heartbeat contract 的 bug 或至少 suboptimal heuristic
- 当前实现不是最优，因为它对“静默监督”过早采用了最激烈的恢复动作
- 最安全的修法是：先补负向测试，再做 delegated-supervision 特定的窄豁免或 signal-first 化，而不是粗暴调大阈值或重写整个 watchdog
- `cycle-20260328-034706.log` 在 `03:47:11` 启动后，最后一次 mtime 是 `03:48:56`
- 对应这轮 `operator_stop_requested` 发生在 `03:50:32`
- 也就是说并不是 cycle log 完全不写，而是“先写一段，再静默超过 `90s` 后被 recovery 杀掉”

这和当前 `90s` stall 门槛正好发生碰撞。

结合 `monitor-ai-cli.sh` 的实现，这个静默并不代表 child 已死；它只代表外部 AI CLI 在那段时间没有新的 stdout/stderr 输出。若 manager 正在处理一个大 prompt、做较长的监督判断、或等待内部工具返回，这种静默完全可能是合法的。

因此目前更像：

- `cycle log quiet >= 90s`
- 被 runtime 当作 `manager_ai_stalled_after_delegated_continuation_prompt`
- 进而触发自恢复杀进程

而不是已经有证据说明 manager 真正 dead。

## 背后流程为什么会走到这里

### 1. manager 还没完成新的 canonical continuity 生产

当前 live/runtime truth 显示：

- 最新 prompt 已经滚到 `prompt-20260328-034706.txt`
- 但最新 manager continuity 仍然停在 `manager-continuity-20260328-014114.md`

这说明从 `01:41 PDT` 之后，manager 虽然反复被拉起多轮 fresh cycle，但还没有再成功完成一轮“产出新 continuity -> 写回 -> 吸收 delegated continuation”的闭环。

所以当前不是“manager 正常完成多轮，只是日志怪”；而是它确实长期没完成新的 manager-level semantic writeback。

### 2. prompt 里还在反复注入一个很大的 delegated continuation backlog

最新 prompt 现场还有两个关键信号：

- prompt 大约 `30KB / 171` 行
- `Delegated continuation handoff` 里仍然包含一长串历史 delegated intake
- `live-status` 现在还显示：
  - `intake_active_items: 85`
  - `intake_delegated_items: 85`
  - `last_consumed_delegated_continuation_ids` 仍是一串很长的历史 backlog

这说明当前 manager 每次 fresh launch 并不是只处理一个新 continuation，而是在不断重新消费一个历史 backlog。虽然 active prompt 视角下 `pending_delegated_continuation_ids=none`，但语义上这些 delegated item 并没有被真正 absorb/close 掉。

这会带来两个叠加效应：

1. manager prompt 体量和监督复杂度被旧 backlog 放大
2. 一旦 manager 没来得及产出新的 continuity，就会在下一轮 fresh launch 继续把同一批 backlog 再喂一次

也就是说，当前 stop loop 很可能不是单纯 watchdog 门槛太小，而是：

- stale delegated backlog 吸收链没有真正收口
- 导致每轮 prompt 都被历史 continuation 家族拖大
- 再叠加 `90s` 的 output-based stall detector

### 3. 因而这更像 runtime contract 缺口，不是现成需求功能

目前更接近的根因画像是：

- `operator_stop_requested` 只是 recovery side effect
- “周期性 stop” 也不像产品要求
- 真问题在于 runtime contract 没有清楚地区分：
  - 合法长静默的 manager supervision round
  - 真 stalled / dead manager round

同时，delegated intake lifecycle 也没有在 runtime 层形成足够稳的收口机制，导致监督 prompt 长期带着旧 backlog 反复重进。

## 当前测试与文档缺口

现有测试更偏向验证“该恢复时会恢复”或“active busy worker 合法等待时不应恢复”：

- 已有负向保护：`latest continuity` 明确等待 active busy worker 时，不应触发 recovery
- 已有正向保护：存在 launchable / stale prompt target 时，应触发 delegated continuation stall recovery

但还没有看到一条直接冻结当前现场的测试：

- manager AI 仍活着
- active worker 也活着
- manager prompt 仍是 delegated continuation prompt
- cycle log 在一个较长监督轮次里静默超过 `90s`
- 但这段静默本身不应立即等价为 stall

所以即使当前观察强烈指向“heartbeat contract 过粗”，现有测试矩阵也还没有把这条合法长静默场景钉死。

## 下一步研究方向

1. 把这条问题拆成两层 owner，而不是混成一个“operator_stop”现象：
   - A. manager stall detector / heartbeat contract
   - B. delegated intake backlog absorption / prompt inflation
   - C. supervisor event naming semantics（不要把 runtime-owned recovery stop 和 operator-explicit stop 混成一个观测词）
2. 在 runtime 设计上补清楚“什么才算 manager progress”：
   - 只靠 `cycle-*.log` mtime 很可能不够
   - 需要判断是否引入 session/jsonl heartbeat、AI pid age + active worker truth，或显式 `supervision_wait` state
3. 在 observability 上区分：
   - user-explicit stop
   - runtime-owned recovery stop
4. 判断 follow-on 应如何 materialize：
   - 若主要是 watchdog 判据问题，归 `runtime recovery / stall governance`
   - 若主要是 delegated intake 长期不吸收，归 `manager interruption absorption / backlog convergence`
    - 若主要是事件命名误导，归 `runtime observability semantics`

## 设计需求还是 bug

### 1. 当前行为不属于明确需求

现有设计真源没有任何一处要求：

- manager 在 delegated-continuation supervision 中必须每 `90s` 产出新的 `cycle log` 字节
- 否则 runtime 就应直接 `TERM` 当前 AI 并重入

相反，设计真源强调的是：

- `auto-loop` 是 outer orchestration / judgement
- watchdog 负责发现 stall / churn signal
- terminal judgement 仍然回到 manager / `auto-loop`

因此，“manager + worker 都活着，只因为 manager 监督轮次短时静默就触发 `local_continuation_reentry`”不符合当前产品/架构意图。

### 2. 这更像 bug，至少也是过粗 heuristic

如果从故障分类上细分，这更接近：

- primary: runtime stall-detector false positive
- secondary: observability semantics 不清晰
- tertiary: delegated backlog / prompt inflation 可能在放大静默窗口

它不是“为了保证功能正确而必须这样”的必要行为，更像“为了尽快抓 stall 而采用了过粗 proxy，结果把合法 supervision round 也杀掉了”。

## 当前实现是不是最优

结论是否定的。至少从风险分配上看，它不是最优实现。

### 1. stall detector 对弱证据过于激进

`manager_ai_stalled_after_delegated_continuation_prompt()` 当前主要用：

- manager AI pid 存在
- delegated continuation 已进入 prompt
- `cycle-*.log` mtime 超过阈值
- `prompt-*.txt` mtime 超过阈值

来推断“manager 已 stalled”。

这相当于把“最近没有新的 stdout/stderr”近似成“监督链已失效”。对一个允许长监督轮次的 outer loop 来说，这个 proxy 太弱。

### 2. 对真正高风险抖动反而更保守

runtime 里已经存在更保守的 restart-storm / process-churn 处理：

- 先记录 signal
- 写 manager bootstrap handoff
- `observe_delay`
- 暂停 blind relaunch，等待 manager judgement

也就是说，系统对“明显抖动”的 pathological case 已经采用 signal-first，而对“可能只是静默监督”的 case 却直接 TERM。这种风险分配并不理想。

### 3. 观测词复用会误导调试

`operator_stop_requested` 既会出现在：

- 用户显式 `freely stop`
- runtime-owned recovery 触发 supervisor trap

这会让外层观察者误以为系统是在执行业务级 stop/restart 需求。命名本身不是主因，但它放大了误判成本。

## 如何修而不引入回归

### 原则

不要先做大范围策略改动。尤其不要：

- 先把 `MANAGER_AI_STALL_THRESHOLD_SECS` 全局调大
- 先把 delegated continuation recovery 整体关掉
- 先把 observability rename 和行为修复揉成一个补丁

这些做法都容易把“误判少了”与“真 stall 被放过了”混在一起。

### 推荐顺序

1. 先补负向测试，冻结当前真实风险边界
   - `active manager`
   - `active worker`
   - delegated continuation 已进入当前 manager prompt
   - manager 处于 supervision-only 合法等待
   - `cycle log` 静默超过 `90s`
   - 预期：不得直接触发 `runtime-stalled-ai-recovery`

2. 再做窄修，不做全局阈值放宽
   - 只在 delegated-supervision 场景引入 idle-safe contract
   - 或把这类 quiet-period 从“直接 recovery”降级为“signal-first / observe-only”
   - 前提是不能削弱已有“真 stall + stale launchable prompt / superseded intake”恢复能力

3. 最后再拆 observability 语义
   - 让 runtime-owned recovery stop 与 explicit operator stop 在事件命名或附加字段上可区分
   - 这一层应单独改，避免影响行为判断

### 低回归修法候选

当前看风险最低的方向有两个：

1. delegated-supervision idle-safe contract
   - 当 manager AI 存活
   - 当前 prompt 是 delegated continuation supervision
   - active worker count > 0
   - 且没有更强证据表明 launchable prompt stale / intake superseded / worker runtime missing
   - 则不要直接进入 `local_continuation_reentry`

2. signal-first 复用 restart-storm 模式
   - 对“manager quiet-period suspicion”先记录 signal 与 handoff
   - 允许短暂 observe window
   - 如果 quiet-period 持续且又出现更强 stall 证据，再进入 recovery

这两个方向都明显优于“把阈值从 90 调到 180/300”这种全局放宽。

## 结论收敛

截至本轮研究，可以把结论压缩为：

1. 这不是产品需求要求的 stop/restart 语义。
2. 这更像 runtime stall detector 对 delegated-supervision quiet-period 的 false positive，至少也是过粗 heuristic。
3. 当前实现不是最优，因为它把弱 heartbeat proxy 当成强 stall 证据。
4. 最稳的后续不是立刻改大逻辑，而是先补负向测试，再做 delegated-supervision 专属窄修，最后再单独处理 event naming / observability。
