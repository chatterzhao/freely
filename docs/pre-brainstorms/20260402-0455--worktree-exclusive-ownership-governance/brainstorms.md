# Brainstorms - 20260402-0455--worktree-exclusive-ownership-governance

## Context

Freely 已经有多 worktree supervision、queue / frozen queue、same-line merge gate、PID ownership 和 session evidence，但最近自举过程中又暴露出一个更细的并发缺口：

- 多个 AI / 多个窗口会同时修改同一个 worktree，产生写入踩踏
- 多个 AI 都会看到同一个 worktree dirty，然后各自尝试 cleanup，产生抢修和误清理
- 多个 AI 可能对同一个 feature worktree 同时执行 merge / promote 到 `develop`，产生重复 merge、错误 closeout 或互相覆盖 followthrough

现有能力能回答“谁在运行、哪个 worktree dirty、merge 是否 issue-bound”，但还不能稳定回答：

- 当前谁拥有这个 worktree 的 edit 权
- 当前谁拥有这个 dirty tree 的 cleanup 权
- 当前谁拥有这条 promote lane 的 merge 权

## Why `worktree -> pid` Single Binding Is Attractive But Not Sufficient

最简单的方案是：

- 每个 worktree 维护一个 owner pid
- 同一时刻只绑定一个 AI 进程
- 别的 AI 看到已绑定就不介入

这个方案有吸引力，因为它：

- 易实现
- 易观察
- 对“同树双写”有第一层拦截

但它会把三类不同问题混在一起：

1. occupancy
   - 这个 worktree 现在有没有 AI 进程挂着

2. activity
   - 这个 AI 最近有没有真的在推进该 lane

3. authority
   - 这个 AI 现在是否仍拥有 edit / cleanup / promotion 的排它权

`worktree -> pid` 最多只能近似表达 occupancy，不能稳定表达 activity 和 authority。

## Why PID / Session Check Alone Is Not Enough

一个直接想法是：每次要介入某个 worktree 前，先检查对应 AI 进程是否绑定该 worktree，再读它的会话文件 / jsonl，判断是不是还在工作；只有没在工作时才介入。

这层探测值得保留，但单独使用不够，原因有三类：

1. `pid/session = liveness hint`，不是 `ownership truth`
   - PID 只能说明“似乎有进程”
   - jsonl / session 只能说明“最近似乎有活动”
   - 但它们不能表达“这个 AI 当前是否仍被授权继续 edit / cleanup / promote”

2. 活进程不等于可继续占有
   - AI 可能卡死、停在无关对话、等待输入、或已经偏离当前 lane
   - 会话文件可能继续增长，但增长内容和当前 worktree ownership 无关
   - 仅因为“进程还活着”就阻止接管，会把 stale owner 锁死

3. 无进程不等于可自由介入
   - 原 owner 可能刚退出，需要按 recovery / continuity 续接，而不是让新的 AI 直接抢占
   - merge / cleanup 这类动作即使当前没有 live PID，也仍可能已有 canonical owner 与未完成 followthrough
   - 如果只按“PID 不在了就谁都能上”，会把 recovery、cleanup、promotion 互相打穿

## Why "Not Working" Is Harder Than It Looks

你提到的难点是关键：即使一个 worktree 只绑定一个 pid，也还要回答“它不干活怎么办”。

这里至少有四种不同的不干活：

1. dead
   - pid 已死
   - 这是最容易判定的一类

2. stalled
   - pid 还活着，但长时间没有新 session/jsonl/continuity 证据

3. alive-but-idle
   - pid 还活着，也许会话还在增长，但当前没有推进这个 worktree 的目标
   - 例如停在闲聊、等待人工输入、或在做无关分析

4. alive-but-blocked
   - AI 不是没干活，而是在等外部条件
   - 例如等上游 merge、等测试、等人工确认

如果系统只看到“pid 还活着”，就会把 2/3/4 全都误判成“这棵树不能接管”。
如果系统只看到“很久没写文件”，又会把 4 误判成 stale。

所以“是否不干活”不能只看一个信号，至少要组合：

- pid liveness
- session/jsonl heartbeat
- continuity 最近更新时间
- 当前 lane phase
- blocker / wait reason

## Existing Truth And Gap

当前 canonical truth 已覆盖这些层面：

- PID 必须与当前 project/worktree 对齐，不能误把别的 worktree 的 pid 当成本 worktree 的 owner
- `live-status` / `fleet-status` / `baseline-status` 会暴露 runtime 当前态
- manager prompt 已要求 `dispatch_priority`、`parallel_safe`、`write_scope`
- same-lane busy guard / frozen queue 已存在
- develop merge 已要求 same-line issue / progress / review owner
- runtime 已有某些局部 claim / stale-recovery / lock pattern，可作为实现参考，而不是从零发明

但这些 truth 还停在几块分离的局部能力上：

- manager 知道自己应做项目级 ownership judgment
- worker 被要求只在 delegated target 内执行
- runtime/status 会暴露 dirty / pid / queue / recovery signal

真正缺的是把这些已有规则接成一个统一 contract：

- 谁可以把 signal 升格为 mutate authority
- 谁可以在 sibling dirty / cleanup / promotion 冲突时做最终裁决
- 哪些 machine-readable 字段要成为 runtime / status / continuity 的共同真相

## Existing Freely-Native Constraints

这个问题不能凭直觉设计，必须服从 Freely 现有的硬约束：

1. manager already owns project-level arbitration
   - `auto-loop` 是唯一 outer loop
   - completion / verification / cleanup routing 都留在 manager / auto-loop 侧
   - worker 不能把自己升级成项目级裁决者

2. worker already has locality boundary
   - worker 只执行被委派的 worktree / issue / lane
   - 不判断其他 worktree 的 merge / freeze / cleanup 策略
   - 看到 sibling dirty 最多回报 signal，而不是直接 takeover

3. runtime truth must be machine-readable and CLI-consumable
   - Freely 宪法要求状态显式且可在磁盘上检查
   - CLI first 要求核心能力必须能被程序消费
   - 法律要求 runtime/status 暴露 worktree dirty summary，供多 worktree 监督和 promotion 决策使用

4. active unresolved governance must stay milestone-visible
   - 这类 `needs_research` candidate 不能只停在聊天或临时 note
   - 必须继续挂在 active milestone candidate queue 中

更具体地说，当前 runtime 机制已经说明这个问题不能被简化成“缺一个提示词提醒”：

- manager worker launch 已按 `dispatch_priority`、`parallel_safe`、`write_scope` 排序与排队
- manager hygiene alert 会扫描 sibling worker worktree 的 dirty/checkpoint drift，并要求通过 manager delegation 收口
- manager recovery 会巡检 `desired=running` 的 worker 工位，并在 continuity 没冻结时重启或 reentry
- cleanup followthrough 已经跨 worktree 扫描 `dirty` 与 `runtime-active`

这些都证明 Freely 早就承认“项目级全局盘面”和“跨 worktree 巡检/裁决”是 manager/runtime 的职责，而不是单 worker 的私有判断。

## Existing Reusable Primitives

从当前项目能力看，最值得复用的不是某个单点脚本，而是一组已经存在的局部 primitives：

1. project-owned pid validation
   - runtime 已会校验 supervisor / ai pid 是否真的属于当前 project/worktree
   - 这说明 occupancy plane 的 project ownership 基础已经存在

2. manager worker launch conflict control
   - manager launch worker 时已经读取 `dispatch_priority`、`parallel_safe`、`write_scope`
   - 对 busy delegated worker 会进入 queue
   - 对 write_scope 冲突会排队，而不是直接并发 launch
   - 但这一层只覆盖“launch worker prompt”，还没有提升成统一 intent ownership gate

3. stale claim recovery pattern
   - interruption intake 已经有 `claim` 与 stale claim recovery
   - 说明 Freely 已接受“claim 不是永远有效，超时后要 recover”的治理模式
   - 这可直接借鉴到 cleanup / promotion lease

4. stale lock cleanup pattern
   - tool launcher 里已有 slot switch lock + stale owner pid cleanup
   - 这说明 runtime 里已存在“lock directory + owner pid + stale cleanup”的实现母型
   - 但它现在是 tool/account 级，不是 worktree/lane 级

5. continuity-driven queue truth
   - manager continuity 已能承接 queue / frozen queue / cleanup queue
   - `live-status` / `fleet-status` 也会刷新这些 truth
   - 说明 manager arbitration 有现成 artifact plane，可挂 ownership disposition

当前真正缺的是：

- 把这些 primitives 统一到 worktree/lane intent 层
- 让它们不只约束“worker launch”，而是约束“整个 mutate lifecycle”

但这些能力仍缺一个独立的 machine-readable surface：

- `exclusive lease / claim / handoff / takeover`

也就是：当前没有一个 runtime 可消费的真相面，用来明确写下“谁此刻独占这个 worktree 或这次 promote 动作”。

## Current Runtime Coverage Is Real But Partial

这个问题不是 Freely 完全没有并发治理，而是当前治理只覆盖了部分切面：

1. manager launch scheduling 已有第一层 anti-stomp
   - runtime 会按 `dispatch_priority` 排序 worker prompt
   - 会读取 `parallel_safe` 与 `write_scope`
   - 会把 busy delegated worker 和写域冲突 lane 放进 queue，而不是直接并发 launch
   - 这证明 manager-first scheduling 已存在，但它只覆盖 launch moment，不覆盖后续 cleanup / promotion followthrough

2. manager patrol 已能合法观察全 fleet，而不是只看当前工位
   - manager runtime 已会扫描 sibling worker worktree 的 dirty、checkpoint drift、expected-running state 与 down supervisor
   - 所以“看全仓 / 看全 fleet”本身不是越权，反而是 manager 的 canonical 责任
   - 真正的问题是从“观察 signal”跨到“获得 mutate authority”之间缺少明确 gate

3. cleanup followthrough 已有 safety check，但仍缺 ownership truth
   - cleanup followthrough 当前会跳过 dirty worktree，也会跳过 runtime-active worktree
   - 但它判断的是“脏不脏 / PID 活不活”，还不是“谁拥有 canonical cleanup authority”
   - 这意味着它能避免一部分误删，但还不能稳定避免 cleanup/promotion 争抢

所以当前缺口不是“要不要看别的 worktree”，而是：

- 谁可以看：manager 可以，worker 默认只把观察结果回报
- 谁可以裁决：manager
- 谁可以执行 mutate：只有持有对应 intent lease 的 owner

## Current Gap By Lifecycle Stage

按 Freely 已有 lifecycle 看，缺口集中在三段：

1. launch-time
   - 已有 `write_scope` 冲突控制
   - 但 `write_scope` 只是 handoff scheduling metadata，不是持续性的 authoritative ownership record

2. active mutation
   - worker role contract 已明确“不判断其他 worktree 的合并/冻结/清理策略”
   - 但 runtime 还没有统一 gate 去阻止 worker 因观测到 sibling dirty 就跨树 acquire mutate authority

3. post-verification promotion / cleanup
   - three-loop lifecycle 已明确 `promotion-in-flight`、`merged-not-cleaned`、`retire-ready` 主要由 manager 拥有
   - 但 cleanup followthrough 仍主要依赖 dirty/runtime-active 探测，还没显式消费 `promotion lease` / `cleanup lease`

这说明第一阶段应优先补的是 manager-owned authoritative truth，而不是把 worker 写得更聪明。

## Current Runtime Mechanics This Must Respect

这条能力不能违背当前已经稳定的 Freely 机制，至少要与下面几条兼容：

1. manager-first launch arbitration
   - worker launch 不是自由并发，而是 manager continuity 驱动
   - `write_scope` 冲突和 busy delegated worker 已会进入 queue
   - 这说明第一版 anti-stomp 不该绕开 manager，直接让 worker 自判接管

2. fleet-wide hygiene visibility
   - manager 已会巡检 sibling worker 工位的 dirty/checkpoint drift
   - 所以“看到别树 dirty”本身不是 bug；缺的是从 signal 到 mutate authorization 的桥

3. fleet-wide expected-running recovery
   - manager 已会基于 `desired=running` 和 continuity freeze truth 决定是否恢复 worker
   - 所以 takeover 不能仅按“pid 不在”或“最近没动静”草率判定

4. cleanup followthrough already crosses worktrees
   - cleanup followthrough 已会遍历其他 worktree，依据 `dirty` 和 `runtime-active` 做 remove/retain
   - 这说明 merge/cleanup 本来就不是纯本地问题；真正缺的是 ownership-aware retain/reclaim rule

## Why This Is Still An Open Gap

虽然已有全局巡检和 launch-time 排班，但反踩踏缺口仍真实存在，因为现有 truth 还停在两端：

1. occupancy-ish truth
   - pid、session、`runtime-active`
   - 回答“像不像有人在”

2. launch-time scheduling truth
   - `dispatch_priority`、`parallel_safe`、`write_scope`
   - 回答“这轮 manager 要不要先 launch / queue”

真正缺的是第三层：

3. lifecycle ownership truth
   - 回答“谁现在有权继续 edit / cleanup / promotion”
   - 即使 worker 已经 launch、pid 还活着、merge actor 看到了 dirty tree，也还要过这一层

如果没有这第三层，就仍会出现两类踩踏：

- launch 后 ownership 漂移，但系统只能看到 pid 仍活着
- merge/cleanup followthrough 需要跨树判断时，系统只能看到 dirty/runtime-active，却看不到 canonical owner

## Three-Loop And Role Boundary

这个问题不只是 worktree 本地机制，而是 Freely 自身三层职责的缺口：

1. auto-loop / manager
   - 负责项目级盘面感知
   - 负责 lane 排班、ownership arbitration、queue / frozen queue / cleanup queue
   - 负责决定谁能 acquire / renew / handoff / release 某个 intent lease

2. doc-loop worker / dev-loop worker
   - 负责在已分配的 issue / worktree / lane 内推进
   - 不负责自行裁决跨 worktree ownership
   - 不应因为“看见别的 worktree 脏了”就直接越权 cleanup / merge / takeover

3. verification / cleanup followthrough
   - 虽然可能发生在多个 worktree 之间，但 owner 仍应由 manager 显式指定
   - 不能退化成任何 worker 看到问题就顺手处理

也就是说：

- ownership arbitration 是 manager 职责
- worker 只消费已裁决好的 ownership
- runtime 负责把这层裁决 materialize 成 machine-readable truth

## Freely-Native Restatement

如果按 Freely 自己的工作机制重述，这个 anti-stomp 问题应这样分层：

1. `auto-loop`
   - 唯一有资格做项目级 arbitration
   - 负责把 raw signal 加工成 `ownership + restart_point + next_action`
   - 负责把跨 worktree dirty / merge / cleanup 问题重新路由，而不是让当前 worker 自扩 scope

2. `manager-agent`
   - 是 `auto-loop` 的项目级执行人格
   - 负责：
     - 读取 `live-status` / `fleet-status`
     - 判断 ownership
     - 生成 manager continuity
     - 生成 worker prompt
     - 维护 queue / frozen queue / cleanup queue

3. `worker-agent`
   - 是 doc-loop / dev-loop / verification evidence worker
   - 只在被委派的 target 内 mutate
   - 看到别的 worktree dirty，最多上报 signal，不直接 takeover

4. runtime
   - 不做业务判断
   - 但要把 manager 的 arbitration truth 变成 machine-readable / enforceable surface

## Merge Cleanliness Is Still Valid, But Mutation Must Re-Route

这里最容易设计错的点，是把“全仓 cleanliness 检查”误当成问题源头。

其实全仓检查本身是合理的，因为：

- manager 本来就负责 fleet patrol
- promotion / cleanup 本来就需要看 project-level dirty / busy summary
- 忽略 sibling worktree 的 dirty / busy 会导致误删和错误 closeout

真正要改写的不是“要不要看全仓”，而是“看到了之后谁有权继续 mutate”：

1. inspect is allowed
   - merge actor / manager 可以看全仓 dirty / busy / queue / runtime state

2. mutate is not implied
   - 看到 sibling dirty，不等于当前 actor 自动获得 cleanup authority

3. arbitration must bounce back to manager
   - 若当前 actor 没有对应 cleanup / promotion lease，就只能：
     - 冻结当前 promotion
     - 写 signal / blocker
     - 请求 manager 重新排班或显式 handoff

4. cleanup followthrough also needs ownership truth
   - 即使是 cleanup followthrough 这种看似“系统顺手做掉”的路径，也不能只凭 `dirty=false && pid=down` 就删除 worktree
   - 仍要回答：当前有没有未完成的 cleanup / promotion owner、有没有 takeover in flight、是否只是 runtime 暂停而非 authority 释放

## Minimum Authoritative Fields

为避免再退化成模糊 prompt 约定，建议定义两个最小结构。

### A. occupancy record

最小字段：

- `target_worktree`
- `target_branch`
- `role_hint`
- `current_tool`
- `supervisor_pid`
- `ai_pid`
- `session_id`
- `jsonl_path`
- `last_heartbeat_at`
- `last_continuity_at`
- `phase_state`
- `blocked_reason`

用途：

- 只回答“谁在这里、最近是否活着、当前处于什么 phase”

### B. intent lease record

最小字段：

- `lease_kind`
  - `edit`
  - `cleanup`
  - `promotion`
- `lease_target`
  - worktree path / branch / issue / integration target
- `holder_kind`
  - `manager`
  - `worker`
  - `runtime`
- `holder_ref`
  - worker prompt path / continuity ref / session ref
- `granted_by`
  - manager continuity artifact
- `acquired_at`
- `heartbeat_at`
- `status`
  - `active`
  - `queued`
  - `frozen`
  - `handoff_pending`
  - `stale_candidate`
- `takeover_policy`
  - `manager_review_required`
  - `runtime_reclaim_allowed`
  - `explicit_handoff_only`

用途：

- 回答“谁现在有权 mutate 哪种 intent”

## Manager-Owned Arbitration Rules

为避免踩踏，建议把下面几条收成 manager-only contract：

1. 跨 worktree arbitration 只能由 manager 做
   - worker 不得自行决定别树是否 stale / 是否可 merge / 是否应 cleanup

2. 发现别树 dirty 不是执行授权
   - 只是 signal
   - 下一跳必须回 manager continuity / cleanup queue

3. merge cleanliness 发现 blocker 后不能直接跨树修
   - 当前 merge actor 只能：
     - freeze 当前 promotion
     - 上报 dirty target
     - 请求 manager arbitration

4. stale takeover 必须有 artifact
   - 不允许自然语言里说“我来接管了”就算完成

5. queue / frozen / cleanup queue 必须和 lease truth 对齐
   - 队列只是显示面
   - lease 才是执行授权面

## Worker Locality Enforcement

worker 默认只能在自己的 delegated target 内 mutate。

这条规则应同时体现在三层：

1. prompt layer
   - `Worktree`
   - `Branch`
   - `intent_kind`
   - `intent_target`

2. runtime layer
   - runtime 读取 worker prompt 时校验：
     - 当前 mutate intent 是否只落在 delegated target
     - 若是 cleanup / promotion，是否存在 active lease

3. governance layer
   - review / verification / merge followthrough 明确把跨树越权视为治理错误，而不是“帮忙修了点脏树”

## Merge Cleanliness Reinterpretation

当前全仓 cleanliness 规则需要从：

- `dirty exists -> current actor may need to fix it`

改成：

- `dirty exists -> current actor must report it to manager arbitration`

然后 manager 才决定：

1. `retain-with-reason`
   - 本轮显式跳过，不影响当前 lane

2. `delegate-cleanup`
   - 单独派 cleanup worker

3. `freeze-promotion`
   - 当前 merge lane 先冻结，等待 cleanup closeout

4. `same-owner-continue`
   - 只有在当前 actor 已持有该 dirty target 的 cleanup/promotion authority 时，才允许继续

这里要特别强调一条：

- “merge 前检查所有 worktree 是否干净”本身不是问题
- 问题是当前 merge actor 在发现 sibling dirty 后，缺少 ownership-aware routing
- 正确动作应是 `report -> arbitration -> delegated owner acts`
- 而不是 `discover -> current actor mutates sibling`

## First Deliverable Shape

第一批能力不必一步到位重写所有路径，建议拆成三个 owner：

1. occupancy surfacing
   - 把 `occupancy record` 显示到 `live-status` / `fleet-status`

2. manager-issued intent lease
   - continuity / worker prompt / cleanup queue 增加 `intent_kind` / `intent_target`

3. blocking enforcement for high-risk actions
   - `cleanup`
   - `promotion`
   - same-worktree `edit`

## Worker Locality Rule

当前真实风险之一正是：某个 worker 在自己的工位里执行时，也能看到别的 worktree dirty、别的 lane 未 cleanup、甚至别的分支准备 merge，然后顺手介入。

这类行为默认应视为越权，除非 manager 显式委派。

建议默认规则：

1. worker 默认只看自己的 assigned worktree / issue / lane
2. worker 即使观测到其他 worktree dirty，也只能：
   - 写 signal
   - 回报 manager
   - 请求 arbitration
3. worker 不得直接：
   - acquire 别的 worktree 的 cleanup lease
   - acquire 别的 worktree 的 promotion lease
   - 代表别的 worktree 做 merge-prep / closeout

这条 locality rule 不是新增价值观，而是把现有 worker contract 机器化：

- 现有 prompt/handoff 已有 `Worktree:`、`Branch:`、`write_scope`
- 现有 manager/worker 分工已经要求 worker 不判断别树 merge / cleanup 策略
- 新增 lease 只是把“自然语言上的不要越权”提升成 runtime 可消费的 gate

## Merge And Global Cleanliness Problem

你提到的另一个关键点是：当前某些 merge/promotion 行为会看全仓 worktree cleanliness，但这个检查还缺少 ownership awareness。

于是会出现两类坏行为：

1. blind global hygiene action
   - worker 为了满足 merge gate，看到别的 worktree 不干净，就直接去处理
   - 结果是 merge actor 越权跨树 cleanup

2. blind merge despite active owner
   - worker 只看“现在需要 merge”
   - 没先确认目标 worktree / related cleanup lane 是否已有 active worker 在处理
   - 结果是重复 merge / 重复 cleanup / followthrough 覆盖

因此“merge 前检查全仓是否干净”本身没有错，错的是缺少下一层规则：

- 发现脏树时，不等于当前 merge actor 可以直接介入
- 发现别的 lane dirty，只能触发 manager arbitration
- 只有 manager 指定的 cleanup owner 才能处理该 dirty lane

## Refined Problem Split

这个并发问题不应混成一个“worktree busy”布尔值，而应拆成三个 lease：

1. edit lease
   - 目标：单个 worktree 的实现/文档写入
   - 风险：两个 AI 同时改同一棵树

2. cleanup lease
   - 目标：dirty tree 收口、checkpoint、cleanup followthrough、retirement
   - 风险：多个 AI 同时“帮忙处理脏树”，导致误删、重复 cleanup、错误改写 continuity

3. promotion lease
   - 目标：同一 worktree / branch / owner issue 的 merge-prep、verification、promote 到 `develop`
   - 风险：多个 AI 同时 merge、重复 closeout、相互覆盖 verification 结论

## Refined Direction: Occupancy Plane + Intent Lease Plane

最佳方向不是单一排它文件，也不是单一 pid 绑定，而是两层真相面：

### 1. Occupancy plane

回答“谁挂在这棵树上”：

- current pid / supervisor pid / ai pid
- current tool / session_id / jsonl path
- last heartbeat
- last continuity update
- current phase / blocker

这一层是观测面，不直接做最终裁决。

### 2. Intent lease plane

回答“谁拥有哪种排它权”：

- 谁拥有 edit lease
- 谁拥有 cleanup lease
- 谁拥有 promotion lease

这层才是 gate。

这样可以避免一个常见误伤：

- 同一个 worktree 上允许多个 AI 正常存在
- 但不允许它们同时持有相同 intent 的独占权

## Concurrency Matrix

“一个 worktree，同时多个 AI 正常的”这一点需要被显式允许，而不是一刀切禁止。

建议的并发矩阵：

1. read + read
   - 允许

2. read + review
   - 允许

3. read + edit
   - 允许，但 edit 只有一个 owner

4. review + edit
   - 允许，但 review 不得顺手改树

5. edit + edit
   - 默认禁止，除非明确拆分为不同 worktree

6. cleanup + edit
   - 默认禁止

7. promotion + edit
   - 默认禁止

8. promotion + read/review
   - 允许，但只有 promotion owner 可以真正 merge / closeout

换句话说：

- 一个 worktree 可以有多个 observer
- 但同一种 mutate intent 只能有一个 owner

不要把方案停在“介入前看看 PID”。

更稳的方向是两层判断：

1. Probe-first
   - 介入前先看：
     - project/worktree 对齐过的 supervisor / AI pid
     - `workcell-state.env`
     - continuity / queue / cleanup queue
     - session_id / jsonl 最近活动
   - 这层只负责判断：
     - 当前 owner 似乎 still-live
     - 当前 owner 可能 stale
     - 当前需要 recovery，而不是直接 takeover

2. Lease-first
   - 真正决定“能不能介入”的，不是 PID，而是 runtime 维护的 lease truth
   - 每个 lease 至少需要：
     - `lease_kind`: `edit | cleanup | promotion`
     - `lease_target`: worktree path / branch / issue / integration target
     - `holder`: manager / worker / tool / session
     - `acquired_at`
     - `heartbeat_at`
     - `continuity_ref`
     - `takeover_policy`
   - 介入者必须先 claim / acquire lease；拿不到 lease 就进入 queue / frozen queue / recovery path

## Lease Rules

### 1. Edit lease

- 同一 worktree 任一时刻只允许一个 writer lease
- 没有 edit lease 的 AI：
  - 可以读
  - 可以 review
  - 不能直接写
- 若 owner stale：
  - 先走 recovery judgement
  - 再决定 renew、handoff 或 force-takeover

### 2. Cleanup lease

- dirty tree 不应被“谁先看到谁就顺手修”
- cleanup 必须绑定明确 owner，并写 cleanup continuity
- 其他 AI 即使发现 dirty，也只记录 signal，不直接做 cleanup mutate

### 3. Promotion lease

- 对同一个 `worktree/branch/issue -> develop` 路径，同一时刻只允许一个 promotion owner
- merge gate 除了校验 same-line issue / progress / review，还应能看到：
  - 当前 merge actor 是否持有 promotion lease
  - 是否存在未完成的 cleanup / verification followthrough

## Activity And Staleness Heuristics

对于“占坑但不干活”，建议不要靠单一阈值，而要做分层判断：

1. hard stale
   - pid 不存在
   - lease heartbeat 超时
   - 可直接进入 reclaim candidate

2. soft stale
   - pid 存在
   - 但 session/jsonl 和 continuity 长时间无更新
   - 进入 manager review，而不是直接抢占

3. blocked-but-owned
   - continuity 明确写了 blocker / wait reason
   - 即使近期没有文件改动，也不应自动回收 lease

4. suspicious occupancy
   - pid 活着，但 session/hash/heartbeat 不再对应当前 worktree lane
   - 需要强制写一条 takeover / repair artifact 后才能接管

会话 hash 可以作为辅助证据，但不应成为唯一 gate。原因是：

- hash 变化不一定代表业务推进
- hash 不变也不一定代表失活
- 它更适合做“最近内容是否在变”的旁证，而不是 ownership 真相

## Takeover Conditions

不能允许无限持锁，所以需要 takeover policy：

1. stale pid
   - 进程死了，且 lease heartbeat 超时

2. stale continuity
   - continuity 停留太久，无新证据

3. explicit handoff
   - manager / worker 已明确把 lane 移交给别的 owner

4. forced takeover with artifact
   - takeover 必须写 machine-readable handoff / takeover artifact
   - 不能只在自然语言里说“我来接管”

## Product Surface Candidates

- `.freely/run/leases/*.env` 或单一 `leases.json`
- `.freely/run/occupancy/*.env` 或扩展现有 `workcell-state.env`
- `freely live-status --project <wt>` 暴露当前 worktree lease
- `freely fleet-status --project <repo>` 暴露冲突 lease / stale lease / waiting takeover
- worker prompt 在现有 `write_scope` 外增加：
  - `lease_kind`
  - `lease_target`
  - `lease_mode`: `acquire | renew | handoff | release`
- manager continuity 显式记录：
  - active leases
  - queued claimants
  - takeover reason

## Phase-1 Contract Freeze

如果这条线要继续向 issue materialization 收敛，第一阶段建议先冻结下面这些 contract，而不是再停留在抽象讨论。

### 1. Authority split

- manager
  - 唯一可裁决 `acquire / renew / handoff / reclaim` 的角色
  - 唯一可把 sibling dirty / merge blocker 从 signal 转成 delegated mutate authority
- worker
  - 只能消费已写明 `Worktree / Branch / intent_kind / intent_target` 的 handoff
  - 发现 sibling dirty / stale 只能 report，不直接 mutate
- runtime
  - 不负责业务语义判断
  - 但负责持久化 occupancy / lease truth，并在高风险路径执行 gate

### 2. Phase-1 authoritative fields

第一版先冻结这些字段，不额外扩大：

- occupancy
  - `target_worktree`
  - `target_branch`
  - `role_hint`
  - `supervisor_pid`
  - `ai_pid`
  - `session_id`
  - `last_heartbeat_at`
  - `last_continuity_at`
  - `phase_state`
  - `blocked_reason`
- intent lease
  - `lease_kind`
  - `lease_target`
  - `holder_kind`
  - `holder_ref`
  - `granted_by`
  - `acquired_at`
  - `heartbeat_at`
  - `status`
  - `takeover_policy`

### 3. Phase-1 stale and takeover rules

- `hard-stale`
  - pid 无效，且 lease heartbeat 超时
  - runtime 可标成 reclaim candidate，但最终 reclaim 仍需 manager artifact
- `soft-stale`
  - pid 仍活着，但 session / continuity 长时间无更新
  - 只能进入 manager review，不能自动抢占
- `blocked-but-owned`
  - continuity 明确写 blocker / wait reason
  - 不允许仅因“最近没改文件”就回收 lease
- `explicit-handoff`
  - 当前 owner 或 manager 写出 handoff artifact
  - 新 owner 才能 acquire

### 4. Phase-1 blocking order

第一阶段只对最危险的 mutate 路径做 blocking：

1. same-worktree `edit`
2. `cleanup`
3. `promotion`

其余路径先 advisory：

- read / review 并发
- fleet patrol / cleanliness inspection
- stale-candidate surfacing

### 5. Phase-1 merge cleanliness rewrite

第一版不取消全仓 cleanliness 检查，但把后续动作改写为：

1. `discover sibling dirty`
2. `record blocker + target`
3. `route back to manager arbitration`
4. manager 决定：
   - `retain-with-reason`
   - `delegate-cleanup`
   - `freeze-promotion`
   - `same-owner-continue`

### 6. Phase-1 non-goals

- 不要求所有 worker-only prompt 都立即消费 lease
- 不在第一版重写全部 merge / cleanup 脚本
- 不把 read-only 多 AI 共存误判成冲突
- 不让 runtime 自己决定语义级 takeover

## Suggested Delivery Order

为了尽量贴合现有 runtime，而不是一次性重写，建议按下面顺序落：

1. status surfacing first
   - 先把 occupancy / lease 暴露到 `live-status` / `fleet-status`
   - 先让 manager 和人工都看得到冲突与 stale candidate

2. manager continuity writeback second
   - continuity / worker prompt 增加 `intent_kind`、`intent_target`、lease disposition
   - 先把 arbitration truth 写出来，再要求更多路径消费

3. blocking only on highest-risk mutations
   - same-worktree `edit`
   - `cleanup`
   - `promotion`

4. then extend into cleanup followthrough and merge-prep retention logic
   - 让跨树巡检继续保留
   - 但把真正的 mutate / retire / promote 判断切到 ownership-aware gate

## First Delivery Suggestion

第一阶段不要直接上最重的 blocking 设计，建议按这个顺序：

1. 先把 occupancy truth 补全到 status surface
2. 再加 advisory lease conflict detection
3. 最后只对高风险动作上 blocking lease：
   - cleanup
   - promotion to `develop`
   - same-worktree edit acquire

这样能先减少踩踏，同时避免过早把正常多 AI 观察/审阅流量也拦死。

## Minimal Architecture-Aligned Materialization

为了最大化复用当前项目能力，第一版不必新造复杂系统，可优先这样落：

1. occupancy truth
   - 扩展 `workcell-state.env` 或相邻 runtime 状态文件
   - 增加最近 heartbeat、continuity ref、observed session/jsonl ref

2. intent lease truth
   - 新增 `.freely/run/leases/`
   - 每个 lease 文件只描述一个 target + kind + holder + heartbeat

3. manager arbitration writeback
   - manager continuity 显式写 active lease / queued claimant / takeover reason

4. runtime enforcement
   - 先在 manager worker launch path 上消费 lease
   - 再在 cleanup / promotion path 上消费 lease
   - 最后再决定是否把 lease 校验推进到 merge gate

## Non-Goals

- 不把它退化成单纯“看 PID 在不在”
- 不把它退化成“大家自觉别同时改”
- 不一次性重写全部 runtime / supervision / merge gates
- 不把所有 read-only inspection 都算成冲突

## Open Questions

1. lease canonical truth 最适合放在每个 worktree 自己的 `.freely/run/leases/`，还是项目级汇总面？
2. promotion lease 的最小 target 应是 `worktree_path`，还是 `issue + integration_target`？
3. cleanup lease 是否应覆盖 checkpoint commit，还是只覆盖 cleanup / retirement / merge followthrough？
4. stale owner takeover 的默认阈值应该基于 pid、jsonl 心跳、continuity 更新时间，还是三者组合？
5. merge gate 是否要在第一阶段先做 advisory-only lease check，再升级成 blocking gate？

## Current Judgement

最佳方向不是“只看对应 AI 工具进程和会话文件有没有在工作”，而是：

- 用 PID / session / continuity 做 probe-first health check
- 用 machine-readable lease 做最终 ownership gate

只有这样，Freely 才能同时避免：

- 活进程假占坑
- 死进程后随意抢占
- 多 AI 同时 cleanup / merge 的互相踩踏

当前更具体的冻结结论是：

- 这是 manager-owned arbitration gap，不是 worker 自觉问题
- 这是 runtime-consumable truth gap，不是单纯 prompt 文案问题
- 第一阶段不需要禁止多 AI 共存，只需要禁止未授权的 mutate intent 并发
