# 预研：three-loop-lifecycle-dictionary-and-worktree-completion

## Context

- 日期：2026-03-23
- 触发：
  - 本轮在按 Freely 规范推进 `feature/external-codex-account-switch-integration` 时，先停在 verification / merge-ready，而没有一次性走到 `develop` merge 与 cleanup。
  - 用户进一步澄清：真正的问题不是先少了一个 completion 词典，而是 Freely 已经实现了很多能力，但 `three-loop-capability-lifecycle` 没继续把它们吸收进去，已经不再承担“整个应用所有事件、流转与分支的地图”这一职责。
- 当前共识：
  - Freely 是自治系统，不应靠人类每一步追加提醒。
  - 若用户说“按三层 loop 工作”，就应自动覆盖 worktree 生命周期，不存在 loop 之外的例外动作。
  - 三层 loop 是全应用地图，不只是高层原则摘要。
  - 所有事件、流转、终止条件、循环回跳、owner 和 skill/agent 落点，都必须能在三层 loop 里找到具体点位。
  - 在 AI 应用里，`skill` 应按传统软件模块对待，是可维护、可组合、可审计的“代码能力”，而不是零散提示词。

## Core Problem

当前项目里虽然已经有：

- `three-loop-capability-lifecycle`
- `branch-management`
- `worktree-maintenance-governance`
- `multi-worktree-supervision`
- `AGENTS.md` 入口规则

但真正的缺口不是“没几个词”，而是：

1. `three-loop-capability-lifecycle` 还不是 Freely 的全应用地图
- 它定义了很多原则和一部分能力归宿
- 但没有继续吸收后续新增的 skill / agent / runtime / worktree lifecycle 语义
- 因而当人类说“按三层 loop 工作”时，agent 仍然不知道：
  - 从哪里起跳
  - 当前为什么停
  - 下一跳是谁
  - 何时循环回流
  - 到哪里才算 terminal

2. 新能力已经很多，但没有被持续回收进 loop 地图
- 例如：
  - worktree lifecycle
  - promote / cleanup decision
  - checkpoint / hygiene intervention
  - manager restart-point routing
  - interruption / intake / delegation
  - verification 到 promote 的交界
- 这些能力虽然已经存在于 skill / agent / runtime 中，但没有全部在三层 loop 真源里形成统一流转图

3. 结果就是“按三层 loop 工作”无法直接驱动自治
- 因为它还不是完整状态机
- 只是高层框架 + 零散能力 inventory
- 中间很多流程分支、回路、终止条件和 owner handoff 仍靠人脑补

4. worktree 生命周期只是这个更大问题的一个子面
- 它当然必须收进三层 loop
- 但不应把问题缩成“只是定义 worktree completion”
- 根问题是：Freely 还没有一张持续更新的 loop map，去吸纳所有事件、行为、分支和技能落点

5. 缺少一个显式的 completion_verification 回路
- 当前很多图会直接从 dev 跳到 merge/cleanup
- 这会让 agent 分不清：
  - 什么时候是继续实现
  - 什么时候只是做 promote / replay / protected acceptance
  - 什么时候已经只剩 cleanup
- 结果就是 cycle 被白白浪费在重复开发、重复测试或停在 `merged-not-cleaned`

表面上 agent 停在：

- `in_verification`
- `merge-ready`
- `merged-not-cleaned`

本质上是因为：

- loop map 没告诉它“当前停点不是 terminal”
- 也没告诉它“下一跳是谁负责”
- 更没告诉它“这类事件属于哪层 loop、走哪条分支、何时回流”

## 2026-03-24 Continuation: 不是“三层”，而是“三个 loop”

本轮继续研究发现，当前不只是地图不够全，还存在一个更基础的表述漂移：

1. “三层循环”这个中文说法很容易把 `doc-loop` 和 `dev-loop` 听成被 `auto-loop` 包含的内层。
2. `PROJECT_INTENT`、部分 pre-brainstorm、以及若干 issue / verification 文档里出现了 `outer / inner`、`三层`、`层级` 之类的口径，会进一步强化这种误读。
3. 一旦 AI 读成“包含关系”，就更容易继续犯这些错：
   - 把 `doc-loop` 当成 `dev-loop` 的上游父层，而不是并列 sibling loop
   - 把 verification / writeback / cleanup 误说成第四层，或误挂到错误 loop
   - 把某个局部 loop 的跳出误判成整个主题已完成

当前需要冻结的更正是：

- 应称为“**三个 loop**”，不是“**三层**”。
- `auto-loop` 是外层编排 / patrol / routing / governance loop。
- `doc-loop` 与 `dev-loop` 是两个并列执行 loop，不是上下包含关系。
- `completion verification`、`recovery`、`cleanup governance` 是 `auto-loop` 负责路由和收口的阶段/路径，不是新增 loop，也不是 `doc/dev` 的子层。
- 某个 loop 的一次内循环跳出，只代表这一轮要回交给 `auto-loop` 重判；不代表主题已经终止。
- 只有当 `auto-loop` 观察到：
  - 当前 issue lifecycle 已闭合
  - 必要 testing closeout 已完成
  - worktree / branch lifecycle 已进入 `retired`
  - 且没有待续接的 canonical owner
  才能判当前主题从 active lifecycle 退出。

## 2026-03-24 Continuation: 改动范围与 owner 收敛

这次改动面很大，不能直接全仓替换 `三层` / `inner` / `outer`。

初步词面审计结果：

- `rg -l "三层|three-loop|Three-Loop|three loop|three loops|doc-loop|dev-loop|auto-loop" docs AGENTS.md`
- 当前命中约 `221` 个文件
- 其中同时混有：
  - 产品真源
  - 当前仍 active 的 pre-brainstorm / issue / pre-tests / code review
  - 已吸收的历史研究、历史验证与旧日志说明

因此这次不能做“全仓统一替换”；必须先区分“仍会影响当前自治判断的真相面”与“只保留历史语境的证据面”。

先按三类分层：

1. 必须改的 active truth
- `docs/PROJECT_INTENT.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- 当前仍 active 的 pre-brainstorm / candidate / issue / pre-tests / skill 真源
- 这些地方若继续保留“层级/包含关系”暗示，会直接误导后续自治

2. 应同步改的 active lifecycle 文档
- 当前 milestone 仍在跟踪的 candidate
- 当前 issue family 的 IBM / PRD / pre-tests / code review
- 这些地方不一定都要大改图，但至少要与新的 sibling-loop 口径一致

3. 历史证据面
- 已关闭/已吸收的老 brainstorm、老 code review、历史日志说明
- 原则上不做全量词面清洗
- 只有当它们仍在被当作现行真相引用时，才补必要澄清

owner 上也要先收清：

- 这条“地图补全 + 三个 loop 关系纠偏”不应再开并行 milestone owner。
- 当前最合适的 milestone owner 仍是 `C-20260319T110500Z-A`。
- `20260323-0241` 继续作为该 owner 下的 active continuation 研究面，承接“地图补全、事件链、sibling-loop 关系和 terminal 语义”这些更细的收敛。
- 在 milestone 未明确吸收前，不应直接把这条 continuation 当成独立待 materialize 主线。

## Proposed Model

### 1. 三层 loop 必须升级为全应用事件地图

所有能力、事件、行为都必须落在三层 loop 中，而且要写到可执行级别，不只是概念级别：

- `auto-loop`
  - 来源扫描
  - event intake
  - worktree/workcell 监督
  - routing
  - restart-point routing
  - promote decision
  - cleanup decision
  - fleet closure
  - runtime continuity / recovery
- `doc-loop`
  - pre-brainstorm
  - candidate
  - milestone intake
  - issue materialization
  - IBM + G
- `dev-loop`
  - implementation
  - tests
  - review
  - verification writeback
  - promotion-ready evidence

对每一类事件，都要能在地图中回答：

- 入口是什么？
- 当前属于哪层 loop？
- owner 是谁？
- 调用哪个 skill / agent？
- 成功后回流到哪一跳？
- 失败 / 阻塞 /分叉 时走哪条逻辑分支？
- terminal state 是什么？

结论：
- 三层 loop 不是摘要，而是 Freely 的总状态机 / 总地图
- worktree lifecycle 不是第四层 loop
- 它只是这张地图里的一个能力面，由 `auto-loop` 编排、`doc-loop` / `dev-loop` 消费

### 2. 统一词典是地图的一部分，不是全部

当前仍然需要统一词典，但它只是为了让地图可执行：

- `active`
  - 当前 worktree 仍在承载生命周期，不可删除
- `merge-ready`
  - feature worktree 内 verification 已完成，但尚未向目标分支 promote
- `merged-not-cleaned`
  - 已并入目标分支，但本地 worktree / branch 还未退役
- `retire-ready`
  - 已满足 cleanup 门槛，可以删除本地 worktree / branch
- `completed`
  - 当前这棵 worktree 的生命周期已经闭环，cleanup 已完成

对应结论：
- “一个 worktree 开发完毕”的默认含义，应该是 `completed`
- 对普通实现型 `feature/*` worktree，默认必须走到删除 worktree / branch，才叫真正完成
- 若因明确原因保留，只能叫 `merged-not-cleaned` 或 `retire-ready`，不能笼统叫“做完”

但更关键的是：

- 这些词必须嵌到 loop map 的节点里
- 不是单独在别处定义完就结束

### 2.5 强制 worktree 下的建模原则

既然 Freely 强制 `feature/*` 使用 dedicated worktree，那么真正需要建模的不是“issue 自己在空中流转”，而是三类对象的联动：

1. `signal`
- 一次插话、一次 patrol 发现、一次 review finding、一次 test failure、一次 runtime anomaly
- 它只负责说明“为什么这一轮被唤醒”

2. `lifecycle record`
- canonical 文档面上的 candidate / issue / progress / recovery / milestone
- 它负责说明“当前问题边界已经走到哪一层 loop”

3. `worktree execution cell`
- branch + worktree + runtime/session + ownership 的组合
- 它负责说明“这一轮动作到底在哪棵树里执行、由谁执行、还能不能继续、何时可以删除”

因此：

- `signal` 决定 first hop
- `lifecycle record` 决定当前 loop phase
- `worktree execution cell` 决定真实执行容器

这三者必须一起更新，不能只更其中一个。

如果只更新 issue / milestone，而不更新 worktree state：
- manager 不知道该唤醒哪棵树
- cleanup 不知道哪棵树已闭环

如果只看 worktree，而不看 lifecycle record：
- 就会把 dirty/clean 误当作业务完成度
- 也会把 research tree、companion tree 和实现树混在一起

结论：
- 在 Freely 里，“流转发生在 worktree 上”这句话是对的
- 但更精确地说，是发生在 `signal -> lifecycle record -> worktree execution cell` 的联动上
- `three-loop-capability-lifecycle` 需要同时画出这三层，不然事件图仍然不完整

### 3. “按三层 loop 工作”必须成为统一触发入口

用户只要说：

- `按三层 loop 工作`

就自动等价于：

- 按 Freely 规范
- 按 task lifecycle
- 按 worktree lifecycle
- 直到当前轮应该达到的闭环终点

这不是同义词游戏，而是因为：

- 这些表述本来就都属于同一张 loop map
- 不应再让 agent 维护平行语义

### 4. 每层 loop 必须落成 agent / skill 模块

既然 Freely 是 AI 应用，那么三层 loop 的执行面必须落实到 agent / skill：

- `agent`
  - 决定 route / owner / next hop
- `skill`
  - 作为可维护模块承载具体能力

skill 在这里应视为传统软件的功能模块：

- 是代码能力
- 是模块边界
- 不是可有可无的提示拼接

### 5. 必须补“事件 -> loop 节点 -> owner -> next hop”总表

当前最缺的不是再讲原则，而是建立一张总表，覆盖：

- 所有主要事件
- 所有主要行为
- 所有状态流转
- 所有分支条件
- 所有回流点
- 所有终止条件

例如至少要覆盖：

- human interruption
- standing-source patrol
- event source intake
- pre-brainstorm
- candidate promotion / drop / needs_research
- milestone intake
- issue materialization
- IBM done / blocked
- dev
- verification
- merge
- cleanup
- recovery
- checkpoint / hygiene
- worktree retire / keep
- merged finding -> new worktree

否则三层 loop 还不能真正驱动自治。

### 5.5 必须补“worktree-first event chain”

最小可执行链路至少要能完整表示下面这条标准路径：

```text
human interruption
-> durable intake
-> manager notice / classification
-> restart-point routing
-> decide: reuse current worktree | create new feature worktree | stay manager-only
-> worker handoff
-> doc-loop or dev-loop inside the selected worktree
-> verification evidence
-> manager promote decision
-> protected branch acceptance / replay if needed
-> verified-retirable
-> branch delete / worktree delete / remote branch disposition
-> cleanup evidence
-> next patrol sees lifecycle closed
```

这里最关键的不是“画一条箭头”，而是每一步都要回答：

- 事件发生在哪里
- canonical 记录写到哪里
- worktree 是复用、派生、冻结还是退休
- 下一跳 owner 是 manager、worker 还是 runtime

如果这条链画不全，Freely 就仍然会停在：

- `in_verification` 但没人接 promote
- `merged-not-cleaned` 但没人接 cleanup
- `needs_research` 但 worktree 被错误长期保留

### 5.6 worktree 生命周期应该建成独立子状态机

issue 的 `phase_state` 不够表达 execution cell 的真实状态，还需要并列的 worktree lifecycle vocabulary。建议最少区分：

- `planned`
  - signal 已确认需要 dedicated worktree，但尚未创建
- `provisioning`
  - 正在通过 `branch-management` 创建或进入正确 worktree
- `active`
  - 当前 worktree 承担 doc-loop 或 dev-loop 执行
- `frozen`
  - 因上游依赖、dirty budget、runtime unavailable 或 manager sequencing 暂停推进
- `verification-ready`
  - worker 已形成最小验证证据，等待 manager 进入 promote / completion routing
- `promotion-in-flight`
  - 正在 merge-up、merge-prep、replay 或 protected acceptance
- `merged-not-cleaned`
  - 目标分支已吸收，但 branch/worktree/remote disposition 尚未完成
- `retire-ready`
  - 已满足 cleanup gate，只差执行 branch/worktree 删除和留痕
- `retired`
  - 本地 worktree 和 branch 已删；若有远程也已删或 retained-with-reason

这样才不会把：

- issue 的 `completed`
- worktree 的 `merged-not-cleaned`
- manager 的 `retire-now`

误当成同一个状态。

### 5.7 创建、复用、删除 worktree 的决定点必须显式化

用户这次点得很准。既然是强制 worktree，就不能只说“最后 cleanup 一下”，必须明确：

1. 哪里创建
- 在 `auto-loop` restart-point routing 之后
- 当 manager 判定当前 signal 需要 worker-owned doc/dev execution，且现有 worktree 不可安全复用时
- 由 `branch-management` 创建 dedicated feature worktree

2. 哪里复用
- 当前 signal 被判定为现有 issue continuation
- 且已有 active worktree 对应该 issue / chain
- 且 runtime/dirty/ownership 都允许继续

3. 哪里冻结
- 在 `multi-worktree-supervision` 或 `worktree-maintenance-governance`
- 典型原因是 parent 未进要求路径、checkpoint 超预算、runtime down、blocked 只允许 doc continuity

4. 哪里删除
- 不在 worker 自己随手删
- 必须在 manager 判定 `verified-retirable` 之后
- 由 cleanup / retirement handoff 进入 `branch-management` cleanup lifecycle 执行
- 删除动作本身仍属于三层 loop 地图中的正式节点，而不是“扫尾杂事”

### 5.8 最小事件矩阵应该覆盖“什么时候新开树”

当前很多歧义其实都来自“这轮到底该不该新开 worktree”。总地图里至少要固定以下判断：

- `new discovery`
  - 默认新开或进入 dedicated research/doc worktree
- `issue continuation`
  - 默认回到已有 active worktree
- `worker-local interruption`
  - 默认优先复用当前 worker worktree，不重开 sibling
- `verification failure on protected branch`
  - 默认回到来源 feature worktree；若来源树已退休，则新开 repair worktree
- `merge-prep integration bug`
  - materialize 为 merge-prep/discoverd fix；必要时新开 dedicated repair worktree
- `research finished`
  - 不保留旧 research tree，写回 canonical 后退休
- `merged finding after promote`
  - 不在 `develop` 上直接修；回来源 feature worktree 或新开 repair worktree

如果这些点不在总地图里写死，AI 每轮都要重新猜“是复用旧树，还是新开树”，自治就不稳定。

### 5.9 还必须补“省周期关键点”

真正能让 Freely 少绕圈的，不只是图画全，而是要在图里写明默认决策：

- issue continuation 且 active tree 还在
  - 默认复用当前树，不新开 sibling
- docs 已足够进入实现
  - 默认直接进 `dev-loop`，不重复跑 IBM
- 当前只剩 promote / replay / protected acceptance
  - 默认进 `completion_verification`，不是再回 `dev-loop`
- verification 失败但边界没变
  - 默认回同一 issue / 同一 active tree 修，不重开 discovery
- verification 暴露了新边界
  - 默认回 `pre-brainstorm`，不硬塞进当前 issue
- cleanup gate 已过
  - 默认立即退休 tree，而不是长期挂在 `merged-not-cleaned`

这些 gate 必须直接写进 lifecycle 真源，否则“图很全”但执行还是会绕远路。

### 6. Agent / skill owner 需要显式化

未来要让 Freely 自治不再“人说一步动一步”，至少需要：

- `manager-agent`
  - 负责 loop-level route / next hop / closure 判断
- `branch-management`
  - 承载 workspace / branch lifecycle 执行语义
- `worktree-maintenance-governance`
  - 承载 disposition 判定与 fleet closure
- `three-loop-capability-lifecycle`
  - 承载总地图、总词典和总映射

若这些 owner 不清楚，主管就会在 verification 后停住。

## Likely Landing

这条问题更像一个治理能力缺口，落点应优先在：

1. `docs/system/workspace/three-loop-capability-lifecycle.md`
- 升级为全应用事件地图
- 增加“事件 -> loop 节点 -> owner -> next hop -> terminal state”总表
- 明确 worktree lifecycle、promotion、cleanup、recovery、checkpoint 等都属于三层 loop 组合，而不是例外流程

2. `docs/LAWS.md`
- 定义地图节点使用的状态词典与门槛
- 定义哪些状态允许停，哪些状态必须自动继续

3. `docs/system/workspace/skills/branch-management/**`
- 明确它只是 loop map 中 workspace lifecycle 的执行模块
- 不再把 promote / cleanup 语义游离在总地图之外

4. `docs/system/workspace/skills/worktree-maintenance-governance/**`
- 明确 disposition 词典必须与三层 loop 地图节点一致

5. 项目级 `AGENTS.md`
- 只保留入口提醒：
  - 用户说“按三层 loop / 按 Freely 规范 / 按生命周期”时，直接进入这张地图，而不是再临时解释语义

## Expected Result

这条预研应最终收敛成：

1. 三层 loop 成为真正的总地图
- 所有事件、行为、流转、分支、回流、终止条件都能找到具体点位

2. 统一词典
- 所有涉及“做完 / 收口 / 完成 / retire”的词都成为地图节点的一部分，而不是散落说明

3. 统一触发
- 以后只要说“按三层 loop 工作”，agent 就能知道从哪里起、在哪里循环、为什么不能停、何时才是 terminal

4. worktree-first execution map
- 以后只要看到一个 signal，agent 就能同时回答：
  - 当前 canonical lifecycle record 是什么
  - 当前执行 worktree 是哪棵
  - 该复用、创建、冻结、promote 还是删除哪棵树
