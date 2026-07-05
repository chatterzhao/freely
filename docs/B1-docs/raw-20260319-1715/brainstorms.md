# 研究：human chat intake 与主管委派闭环

## Context

- 日期：2026-03-19 17:15 PDT
- 触发：Freely 已经把 `human chat / session evidence` 定义为 discovery source，也有 `compose-context-source-prompt.sh` 与 `test-human-chat-routing`，但当前用户插话仍只能由外部操作者手动解释，尚未形成“主管监听插话 -> 委派 pre-brainstorm worker -> candidate/milestone 更新 -> 再排班”的完整自治闭环。
- 当前已知事实：
  - `PROJECT_INTENT` 与 `LAWS` 已明确 human chat 应先进入 `doc-pre-brainstorm-execution`。
  - `context-source-skill` 已能把 chat 归类为 `source_class=discovery`。
  - `docs/system/workspace/three-loop-capability-lifecycle.md` 现已把 `human chat intake` 放进 `auto-loop` capability map，并给出 `.freely/intake/**` 这一 canonical artifact；但 reaction plane、specialized AI handling 与 canonical absorption 的深层链路仍未收敛。
  - `compose-context-source-prompt.sh` 只解决“给 AI 一份 source input prompt”，没有提供 supervisor 可长期消费的 intake 队列或命令入口。
  - `runtime/freely` / `bin/freely` 当前没有公开的 `chat` / `intake` / `interrupt` 子命令，也没有输入目录、事件账本或 intake 状态视图。
  - 主管模式已经存在，但其监督对象仍主要是 worktree / runtime / milestone，不包括显式的“人类插话待办队列”。

## 当前主问题

现在真正缺的不是“chat 算不算 discovery”，而是下面这条能力链是否可执行：

`human interruption -> durable intake -> manager observes -> classify + dedupe -> delegate worker -> pre-brainstorm artifacts -> milestone candidate/issue -> manager reschedule`

因此本条预研要回答的核心问题是：

1. 人类插话以什么 CLI-first 入口进入 Freely，才能被主管稳定捕获，而不是只存在于当前聊天线程。
2. 主管如何监控这些插话，并区分“新 discovery”“现有 issue continuation”“纯控制命令/暂停/恢复”。
3. 主管发现插话后，如何委派到 dedicated worker worktree 执行 `doc-pre-brainstorm-execution`，并跟踪它是否已经写回 candidate / milestone。
4. UI 是否需要存在；如果需要，它在这条链里只能是 intake 展示层，还是允许承担交互入口。

## 已形成的判断

### 1. 当前闭环没有真正落地完成

现状只能算“路由协议已建立”，不能算“human chat intake 闭环已完成”：

- 已有：
  - `human chat / session evidence` 的来源语义
  - pre-brainstorm / milestone / issue 的状态口径
  - `compose-context-source-prompt.sh`
  - `test-human-chat-routing`
- 未有：
  - 对外可用的 intake 命令
  - durable intake artifact / queue
  - manager 对 intake 的监督视图
  - intake 去重 / 归并 / ack 规则
  - “worker 已经吸收该插话并写回 milestone”的 completion signal

所以当前 Freely 还不能说已经支持“主管监听人的插话并自动收敛”。

### 2. 这条能力首先是 CLI first，不应先做 UI

宪法 10.1 已明确所有能力先有 CLI，UI 只是展示层。

同时，三层 loop 真源要求每项能力都要能回答：

1. 它属于哪个 loop
2. 它由哪个 owner 执行
3. 它的 canonical artifact 是什么
4. 它在 lifecycle 中对应哪个触发点

按这个口径，human chat 不应直接从“聊天线程”跳进 doc-loop；中间还缺一层 `auto-loop` intake。

因此 human interruption 的最小可行入口应该先是类似：

- `freely intake chat --project <abs_path> --message-file <abs_file>`
- 或 `freely intake chat --project <abs_path> --message "..." --author human`

它的职责不是直接做路由，而是把插话落成 durable source artifact，并触发/唤醒主管重新扫描。

UI 可以后续补，但只能是这个 CLI intake 的前端：

- UI 输入框 -> 写入同一 intake artifact / 调用同一 CLI
- UI 不能绕过 intake 账本直接把内容塞进某个 AI 会话，否则会破坏可追溯性和恢复性

### 3. human interruption 的正确站位：插话，不是阻塞主 loop

这里首先要收紧语义：人类输入在 Freely 中的默认身份是“插话”。

它的含义不是：

- 新增一条高优先级阻塞 loop
- 任何时候都要立即打断当前 worker
- 把当前 auto-loop 重新降级成“等待人类驱动”的同步会话
- 把“需要澄清”默认解释为“暂停执行，等人补充指令或意图”

它真正的站位应是：

- `human chat` 是一个外部输入 channel
- `human interruption` 是该 channel 上的一次插话 event
- `human chat intake` 是 `auto-loop` 内部的 intake / arbitration capability
- 它默认只要求被记录、被看见、被分类、被排班
- 它只有在被判定为高优先级纠偏时，才允许影响当前执行中的 worker

因此 Freely 不能把“收到人类插话”设计成“主 loop 默认阻塞，等待处理完成后再继续”。

更合理的约束是：

- 默认动作：记录到 intake，并在下一轮 manager scan 中处理
- 默认影响：不打断当前主线
- 默认结果：形成 disposition，而不是形成阻塞
- 例外情况：只有高优先级 `continuation` / 明确 `control` 才允许改变当前运行态

还要再加一条更硬的约束：

- AI 执行过程中若出现信息不足、边界摇摆、方案分歧、验收含糊，不应把“等待人类插话澄清”当作正常执行策略
- 正常策略应是主管委派新的 AI worker / sidecar 去分析、对比、收敛、补文档或做预研，再把结论回流
- 人类插话只能作为外部新增输入被吸收，不能成为 AI 主 loop 的默认依赖

### 3.1 human chat 需要先被分成两层语义

为了不和现有 `source_class` 词典冲突，human chat 不应直接被定义成新的主路由词表，而应拆成两层：

1. `source_channel`
- `human_chat`
- 只表达“输入来自哪里”

2. `intake_disposition`
- `observe`
- `control`
- `continuation`
- `discovery`
- 只表达“主管看见这条插话后应如何处置”

也就是说，`observe/control/continuation/discovery` 不是拿来替代 `LAWS 2C` 中的 `source_class`，而是 human-intake 专属的仲裁层。

### 3.2 与现有三层 loop / 主词典的映射

现有唯一主词典仍然是：

- `source_class`
- `route_kind`
- `phase_state`

因此 human-intake 的 disposition 必须显式映射回现有主词典，而不是平行存在：

1. `discovery`
- 映射到 `source_class=discovery`
- 下一跳通常是 `route_kind=pre_brainstorm`
- 进入 `doc-loop`

2. `continuation`
- 映射到 `source_class=continuation`
- 下一跳由现有 continuation / recovery 规则决定
- 可能回到 `issue/progress/recovery`

3. `control`
- 不直接映射成新的业务 `source_class`
- 留在 `auto-loop`
- 由 runtime / manager 作为控制信号处理

4. `observe`
- 不应升级成新的主 `source_class`
- 只作为 intake 层的非阻塞 disposition 留痕
- 可由 manager 回答、忽略或稍后合并进别的 thread

补充：

- `observe` 不应被滥用为“当前缺信息，先挂起等人澄清”
- 如果 AI 内部需要澄清，默认应走主管再委派 AI 分析 / 预研 / 对比路径
- 只有人类主动给出新的外部输入时，才形成新的 intake event

如果不先把这张映射表写清楚，后续实现一定会长出第二套路由语义。

### 3.3 旧语义需要修订，而不是整段推翻

之前“chat / session evidence 是 discovery source”这个说法并非完全错误，但已经不够精确。

更准确的版本应是：

- raw human chat 首先是 `human_chat` 输入 channel
- 经过 intake disposition 后，它可能产出：
  - `discovery`
  - `continuation`
  - `control`
- 只有被判定为 `discovery` 的 human input，才继续沿用“chat 作为 discovery source”进入 pre-brainstorm

换句话说，不该保留“所有人类插话都天然是 discovery”的旧口径。

### 4. 主管必须监控 durable intake，而不是直接监听当前聊天线程

“监控人的插话”如果理解成直接读取交互式终端会话，会带来几个问题：

- 无法恢复
- 无法去重
- 无法跨会话追溯
- 无法在 supervisor 重启后继续处理

更合理的模型是：

1. 外部输入通过 CLI/UI 写入 durable intake artifact
2. manager cycle 在每轮扫描需求池时读取 intake 队列
3. 根据 intake item 的 `status` / `classification` / `linked_issue` / `delegation_state` 决定下一步

也就是说，主管“监控人的插话”本质上是在监控一个可恢复的 input queue，而不是盯住 stdin。

这也解释了它在三层 loop 中的归属：

- `auto-loop`
  - 负责 intake 写入、监督扫描、分类、委派、完成信号回收
  - 负责确保“插话被看见”，而不是把 loop 改造成同步阻塞等待
  - 负责在需要澄清时优先组织 AI 内部再分析/再委派，而不是停下来等人
- `doc-loop`
  - 只负责当 intake 被判定为 `discovery` 后，把它收敛为 pre-brainstorm/candidate/milestone

这里必须明确：

- `human chat intake` 不是新的第四层 loop
- 它也不是平行于 `context-source-skill` 的第二个总路由器
- 它只是 `auto-loop` 中对 human 插话做 normalize / arbitrate 的一个能力槽位
- 真正进入 `doc-loop` / `dev-loop` 的仍然是 disposition 之后的结果

### 5. intake artifact 本身需要成为状态事实源

最小字段建议：

- `intake_id`
- `created_at`
- `author`
- `channel`
- `message`
- `status`
  - `new`
  - `classified`
  - `delegated`
  - `absorbed`
  - `dropped`
- `classification`
  - `control`
  - `continuation`
  - `discovery`
- `linked_artifact`
  - pre-brainstorm path / issue path / recovery path
- `delegated_worktree`
- `session_refs`

这样主管才能回答：

- 还有哪些人类插话没处理
- 哪些已经委派但 worker 还没吸收
- 哪些已经吸收进 candidate / issue

但还要再补一条边界：

- `.freely/intake/**` 是 intake 层事实源
- 它不是新的 issue 系统
- 它不替代 `pre-brainstorms/**`、`docs/epics/**`、`docs/progress/**`、`docs/recovery/**`
- 它只保存原始插话、仲裁状态和链接关系

### 6. manager 的 completion signal 不应是“我看过了”

人类插话的完成条件应是：

- `control` 类：runtime 或 manager 已执行并留下状态回写
- `continuation` 类：已回写到现有 issue/progress/recovery
- `discovery` 类：已形成 pre-brainstorm 产物，并同步进 `docs/milestones.md`

因此“看过消息”不算完成；“被规范产物吸收并可追踪”才算完成。

同时，`absorbed` 不能只表示“写了个链接”。

最小要求还应包括：

- 若进入 `pre-brainstorm/candidate`，对应产物必须继承有效 `session_refs`
- 若进入 `issue/progress/recovery`，也必须把可追溯会话证据继续带过去
- 不允许 intake 被标记为 `absorbed`，但人类插话证据在下游产物中消失

### 7. 委派执行权必须进入 worker，而不是主管在 develop 直接写

主管位在 `develop` 只能做：

- 发现 intake item
- 判断分类
- 决定是否新建/复用 dedicated worktree
- 生成 worker handoff
- 监督 worker 是否把结果写回

真正写：

- `docs/B1-docs/<id>/brainstorms.md`
- `docs/B1-docs/<id>/candidates.md`
- `docs/milestones.md`

的必须是 worker 工位。

### 8. 现有架构分支/前端方向的关系

如果人类插话是“现在需要做前端，检查前端技术栈”，主管也不应直接把它塞进现有 architecture 分支。

应先做：

1. intake item -> `discovery`
2. 看是否已有活跃 pre-brainstorm 明确拥有这个主题
3. 若无明确 ownership，则新建 dedicated pre-brainstorm worker
4. 在 pre-brainstorm 中把“哪些旧分支/旧结论过时”作为研究输入，而不是把旧分支当成自动继续执行依据

## 候选设计方向

### A. CLI-first intake

新增一个 supervisor-facing CLI 面，例如：

- `freely intake chat --project <abs_path> --message "..."`
- `freely intake chat --project <abs_path> --message-file <abs_file>`
- `freely intake status --project <abs_path>`

最小职责：

- 把人类输入写入 `.freely/intake/`
- 返回 `intake_id`
- 触发 manager 尽快重扫，或至少让下一轮必看 intake 队列

补充判断：

- intake 不是 issue，也不是 pre-brainstorm 本身
- intake 是人类外部输入进入 Freely 的 durable source record
- 它属于 `auto-loop`，只负责把插话变成可监督、可恢复、可委派的事件

### A1. intake item 最小状态机

建议每条 intake item 至少有：

- `intake_id`
- `created_at`
- `author`
- `channel`
- `message`
- `status`
- `classification`
- `priority`
- `action`
- `linked_artifact`
- `affected_worktree`
- `session_refs`

其中：

- `status`
  - `new`
  - `classified`
  - `delegated`
  - `absorbed`
  - `dropped`
- `classification`
  - `observe`
  - `control`
  - `continuation`
  - `discovery`
- `action`
  - `non_intrusive`
  - `delegate_parallel`
  - `redirect_active_worker`

这样才能把“人类只是插话，但不要求确认”的语义落实为 supervisor 可计算的状态。

### A2. 为什么不是直接打进当前会话

若把插话直接注入当前正在运行的 AI CLI 会话，会带来这些问题：

- 当前工具是免交互路径，运行中不一定可安全插入新 prompt
- supervisor / AI 崩溃后会丢失插话
- 无法区分它是 observation、纠偏还是新 discovery
- 无法给 manager 做统一排队、去重和 disposition
- 无法把“已吸收进哪个工位/哪个 artifact”持久回写

因此 Freely 不应把“监听人的插话”理解成读 stdin，而应理解成监控 intake queue。

### B. Manager intake scan

在 manager 的首跳/监督 prompt 中注入：

- 当前未吸收 intake items 列表
- 最近已吸收的 intake disposition

并明确要求：

- 先判断 intake 是否高于当前 milestone continuation
- 若属于新 discovery，先委派 pre-brainstorm，不允许直接自己改仓库

### B1. manager 的四分流思考模型

主管看到一条 intake 后，不应直接问“要不要开 issue”，而应先问：

1. 这是 `observe` 吗？
- 只是问状态、碎碎念、澄清、非行动性反馈
- 默认不抢占当前 worker
- 可由主管本会话或 sidecar AI 总结回答

但这里要防止误用：

- “AI 自己不知道怎么办，所以挂起等待人来澄清”不属于健康的 `observe`
- 若问题本质上是内部分析不足，应先委派新的 AI 分析/预研 worker，而不是等待人类发新指令

2. 这是 `control` 吗？
- stop / pause / resume / freeze / focus / deprioritize
- 由 runtime 或 manager 直接处理
- 不进入 pre-brainstorm

3. 这是 `continuation` 吗？
- 对当前 issue 的纠偏、验收补充、优先级修正、重构要求
- 如果仍在现有 issue 边界内，应附着到 issue/progress/recovery
- 可能需要重定向当前 worker

4. 这是 `discovery` 吗？
- 新功能、新治理缺口、新研究题
- 应进入 pre-brainstorm，再同步 candidate / milestone

只有完成这一步，主管才知道它应落到哪个 loop / artifact。

补充约束：

- 这四分流是 human-intake 的 disposition 模型
- 不是 Freely 全系统新的统一 `source_class`
- manager 在给出 disposition 后，仍需把结果对齐回现有 `source_class/route_kind`
- 若当前问题并非来自新的 human input，而是 AI 自己在执行中遇到不确定性，优先走“AI 内部再分析/再委派”路径，不伪装成 `human interruption`

### B1.1 插话处理应是 skill，不应再造一个 agent

当前项目中：

- `agent` 表达角色边界
- `skill` 表达可复用工作能力

因此“插话处理”不应再做成新的平行 agent。更合理的结构是：

- `manager-agent`
  - 继续作为主管角色
- `skill:human-chat-intake`
  - 负责 intake item 的分类、priority、disposition 和 handoff 生成

原因：

1. 插话处理本质是主管调用的一项仲裁能力，不是一个新的长期角色。
2. 若单独引入新 agent，会和 `manager-agent` 的监督/排班职责重叠。
3. `observe/control/continuation/discovery` 的判断可被未来其他入口复用，因此更适合作为 skill。
4. 真正落仓库产物的仍是现有 worker / loop，而不是“插话 agent”自己执行。

### B2. manager 的默认抢占规则

Freely 应默认“不阻塞、不打断”，只有在继续运行会明显产出错误结果时才抢占。

建议规则：

- `observe`
  - 默认 `non_intrusive`
  - 不打断任何 worker
- `control`
  - 若影响运行安全/资源/调度，立即处理
- `continuation`
  - 若当前 worker 继续执行会明显偏离新要求，使用 `redirect_active_worker`
  - 否则允许先记入 continuity，再在下一轮接管
- `discovery`
  - 默认 `delegate_parallel`
  - 不抢占当前 milestone 主线

这和“人可以高优先级插话，但不需要确认什么”一致：高优先级不等于默认 kill 掉当前进程。

更进一步的硬边界应是：

- 插话默认是 side input，不是 stop-the-world event
- auto-loop 必须维持当前主 loop 可继续运行，除非出现明确 `control` 或高风险 `continuation`
- “被注意到”与“打断执行”必须始终分离
- “需要更多判断”与“必须等待人类回复”也必须始终分离

### B3. 主管如何“知道”有插话

这条能力的 detection 不能依赖“当前 AI CLI 会话支持交互式插入 prompt”，因为 Freely 当前主路径是免交互 supervisor 模式。

因此主管知道有插话，应来自一条独立于当前 AI CLI 进程的可恢复信号链：

1. 人类通过 CLI 或 UI 提交插话
2. 输入被写入 durable intake artifact（如 `.freely/intake/<id>/`）
3. runtime / supervisor 在磁盘上留下“存在未吸收 intake”信号
4. manager 在下一轮 prompt build 或 watch 周期中读取该信号与队列摘要

也就是说，主管不是“听见”插话，而是“看见” durable intake queue。

### B3.1 detection 的三层机制

建议拆成三层：

1. `record`
- `freely intake chat ...`
- 负责落盘 intake item

2. `signal`
- 在 `.freely/run/` 写一个轻量信号，例如：
  - `intake.pending`
  - 或 `intake-state.env`
- 目的是让 runtime 不必每次全量扫描，也能快速知道“有新插话”

3. `observe`
- manager prompt build 读取该 signal
- 若存在 pending intake，再注入队列摘要

这样有几个好处：

- 不依赖当前 AI 工具支持会话内插话
- supervisor 重启后信号仍在
- manager 不需要人再次提醒“你刚刚有插话”
- 后续 UI 和 CLI 都可复用同一 detection 路径

### B3.2 是否要立刻中断当前 manager/worker 进程

默认不需要。

建议：

- 若只是新 intake 写入：
  - 不强制 kill 当前 manager
  - 让 manager 在下一轮 prompt build 必看该队列
- 若该 intake 被判定为高优先级 `continuation`，且当前 worker 正在继续做错方向：
  - 再触发 `redirect_active_worker`

因此 detection 和 interruption 应该分离：

- detection: “主管知道有插话”
- interruption: “主管判定这条插话值得打断当前 worker”

不要把“被注意到”设计成“立刻 kill 当前进程”。

同理：

- clarification: “当前问题仍需进一步分析”
- human dependency: “系统必须等人回复才能继续”

这两者也不应默认等同。

Freely 的默认设计应是：

- 先让主管委派新的 AI 分析、预研、复核、对比方案
- 只有当问题本质上属于外部产品意图新增、授权变化或显式人类决策输入时，才被动吸收人类新插话

### B3.3 manager 的最小注意义务

主管一旦看到 pending intake，至少要产出一条 disposition：

- `observe and ignore for now`
- `answer without delegation`
- `delegate parallel pre-brainstorm worker`
- `attach to current issue continuity`
- `redirect active worker`

只有这样，系统才算真的“注意到了插话”，而不是只是把一条消息落盘。

### B3.4 不应把“注意到插话”设计成提示词约定

CLI/UI 可以在提交插话时附带标准化元信息，但不应把“这是人类插话，请调用某 skill”当成唯一 detection 机制。

原因：

- 这类提示词只对本次会话有效，不是 durable state
- 若当前 manager/worker 进程未消费该 prompt，插话就会失效
- 多轮对话中，后续 event 很难判断是在补充、纠偏还是推翻前一判断
- supervisor 重启后无法仅凭 prompt 文本恢复未吸收事项

因此，提示词约定最多只能作为 handoff 内容的一部分，不能代替 `.freely/intake/**` 与 `.freely/run/**` 的状态事实源。

### B4. 多轮人类对话应建模为 thread/event，而不是一条 message 覆盖一切

若人类连续在一个会话里多次插话，Freely 不应把它们都压扁成单条 intake message，也不应要求每条都立刻 materialize 为独立 issue。

更合理的模型是：

- `thread`
  - 表示同一条人类插话主题线
- `event`
  - 表示线程中的一次发言或补充

建议最小 artifact：

- `.freely/intake/threads/<thread_id>/meta.env`
- `.freely/intake/events/<event_id>/meta.env`
- `.freely/intake/events/<event_id>/message.txt`

其中：

- 每次 `freely intake chat ...` 产生一个新 `event`
- 若显式指定 `--thread <thread_id>`，则把 event 追加到已有 thread
- 若未指定 thread，则创建新 thread
- manager/skill 的 disposition 应优先作用在 thread 上，而不是只作用在单个 event 上

这样主管才能回答：

- 这次新输入是在补充现有 thread，还是开启新主题
- 当前 thread 是否已稳定到可以变成 pre-brainstorm / issue
- 当前 event 是否推翻了 thread 先前 disposition，需要 redirect active worker

### B4.1 多轮 thread 的状态与聚合规则

建议 thread 级别也有自己的状态字段：

- `thread_status`
  - `open`
  - `classified`
  - `delegated`
  - `absorbed`
  - `closed`
- `current_classification`
- `current_action`
- `linked_artifact`
- `affected_worktree`
- `latest_event_id`

而 event 级别负责保存原始发言和局部判断。

推荐规则：

- thread 的 `current_*` 由最新未吸收的有效 event 决定
- 若新 event 只是补充说明，不推翻之前边界，则沿用 thread disposition
- 若新 event 明显改变方向，则更新 thread disposition，并在需要时触发 redirect
- 只有 thread 被吸收进 issue / pre-brainstorm / recovery 后，相关 event 才能一起视作 absorbed

### B4.2 `jsonl_path` 不应强制每条 event 都有，但 thread 应始终可追踪

`jsonl_path` 很有价值，但不应被设计成所有人类插话都必须具备的硬门槛。

更合理的是：

- 如果插话来自有持久会话记录的入口：
  - 记录 `session_refs`
  - 尽量附带 `jsonl_path`
- 如果插话来自纯 CLI `--message` / UI 输入框：
  - 允许没有 `jsonl_path`
  - 仍然必须有 durable `event_id`, `thread_id`, `message.txt`

因此，应坚持的是“可追踪引用”，不是“必须有 jsonl_path”。

建议字段口径：

- `session_refs`
  - 可为数组
  - 每项可含：
    - `tool`
    - `session_id`
    - `jsonl_path`
    - `role`

其中：

- thread 级别可聚合多个 `session_refs`
- event 级别只记录其直接来源
- 对于同一人类连续会话，后续 event 可以复用同一 `session_id/jsonl_path`
- 若是新入口产生的补充输入，则新增一条 `session_refs` 记录，而不是覆写旧值

### B4.3 主管对多轮 thread 的注意义务

主管不仅要知道“有新 event”，还要知道“这个 event 属于哪个 thread，是否改变既有 disposition”。

因此下一轮 manager queue scan 至少要看到：

- pending threads 数量
- 每个 thread 的最新 event 摘要
- thread 当前 disposition
- 是否存在需要重新仲裁的 changed thread

只有做到 thread 级别可见，Freely 才不会在多轮对话里不断重复开新 candidate 或漏掉纠偏。

### B4.4 真实的人类碎碎念还需要一层 intake session

仅有 `thread/event` 还不够贴近真实使用。现实中，人类往往会在一个连续会话里不断碎碎念，其中可能混杂：

- 状态追问
- 新想法
- 对现有 issue 的纠偏
- 完全无关的另一个主题

因此 Freely 不应把“一个人类会话”直接等同于“一个 thread”，更不应等同于“一个 issue / 一个 worktree”。

更合理的是三层：

- `intake session`
  - 表示一次连续的人类输入会话
  - 例如一个 CLI attach 会话、一个 UI chat panel、一个持续复用的 jsonl 会话
- `thread`
  - 表示该 session 中被主管识别出的某个主题线
- `event`
  - 表示 session 中的一次原始发言或系统切分后的子片段

关系应是：

- 一个 session 可包含多个 thread
- 一个 thread 可聚合多个 event
- 一个 thread 最终才可能链接到某个 issue / pre-brainstorm / worktree

这能避免把“连续碎碎念”错误地绑定到单一工位或单一问题。

### B4.5 是否需要专门的人类碎碎念会话

建议：需要一个稳定复用的 `intake session` 概念，但不必要求用户手工频繁新建会话。

推荐设计：

- CLI-first 默认存在一个项目级 `human-intake` 会话
- 后续人类插话默认追加到该 session
- runtime/manager 基于内容把新 event 归并或拆分到不同 thread
- 当检测到上下文明显切换时，可自动新建 session，但应保留对旧 session 的引用

也就是说：

- session 应尽量稳定复用
- thread 应按主题自动拆分
- issue/worktree 只在 thread 稳定后才建立映射

这样更符合现实中的使用习惯，也更利于 supervisor 做持续吸收。

### B4.6 `jsonl_path` 的正确归属：优先是 session 级，而不是每条 event 级

若底层存在 jsonl 或等价会话日志，最自然的做法不是要求每个 event 都有一条独立 `jsonl_path`，而是：

- `intake session` 持有主 `jsonl_path`
- `event` 只记录自己在该 session 中的定位信息
  - 例如 `offset`
  - `message_index`
  - `timestamp`
- `thread` 则聚合来自同一 session 或多个 session 的相关 event

因此更合理的字段关系是：

- session:
  - `session_id`
  - `jsonl_path` 可选
  - `channel`
  - `opened_at`
  - `last_event_at`
- event:
  - `event_id`
  - `session_id`
  - `event_seq`
  - `message.txt`
  - `session_refs`
- thread:
  - `thread_id`
  - `source_sessions`
  - `current_classification`
  - `linked_artifact`

这样设计有几个好处：

- 同一连续会话不用反复新建 jsonl
- 后续 event 可以自然引用“之前那个 jsonl”
- manager 能把一个 session 里的不同主题拆成不同 thread
- worker handoff 时既可引用 thread，也可回溯到原始 session log

### B4.7 session、thread、issue、worktree 的分工边界

建议明确这四层不要混淆：

- session
  - 原始人类输入容器
  - 解决“人一直在说”这件事
- thread
  - 主题收敛容器
  - 解决“这些话在说哪个问题”
- issue / pre-brainstorm
  - 规范产物容器
  - 解决“这个问题在系统中的正式表达是什么”
- worktree
  - 执行容器
  - 解决“谁在哪个隔离工位做这件事”

因此正确流向应是：

`session -> event -> thread -> disposition -> issue/pre-brainstorm -> worktree`

而不是：

`session -> 直接某个 worktree`

### B4.8 主管对 session 的最小职责

主管不仅要扫描 pending event，也要维护 session 健康度。

最小职责应包括：

- 识别一个 session 中是否出现多个主题 thread
- 避免把无关碎碎念错误附着到当前活跃 issue
- 当 session 太长或主题漂移严重时，自动 rollover 到新 session
- 在 handoff 中同时提供：
  - thread summary
  - 原始 session refs

这样 worker 既有被收敛过的任务边界，也保留原始上下文可查。

### C. Worker handoff for discovery intake

新增或补强一类标准 handoff：

- 来源：human intake item
- 输出目标：pre-brainstorm + milestone sync
- 完成后必须回写 `intake_id -> linked_artifact`

### C1. continuation 类插话的 redirect 模型

`continuation` 类插话不是新开 issue，也不总是新开 pre-brainstorm。

当它影响当前正在运行的 worker 时，建议允许一条显式 redirect 路径：

1. manager 判定该 intake 为 `continuation`
2. 确认受影响的 `affected_worktree`
3. 由 runtime 终止对应 worker 进程
4. 写一份新的 handoff：
   - 保留旧 `session_refs`
   - 指向旧 cycle log / jsonl
   - 附带新的 intake summary
   - 明确这是“同 issue 边界内的纠偏”，不是新 discovery
5. 以 fresh/resume 合适路径重启该 worker

也就是说，“终止当前进程 + 旧会话文件地址 + 新提示词”是需要存在的，但它应只用于 `continuation` 高优先级纠偏，而不是所有插话的默认处理方式。

这里还应明确：

- `redirect_active_worker` 是例外治理动作，不是 human-intake 的默认成功路径
- 若当前 worker 没有明显跑偏，优先写 continuity / handoff，等下一轮自然接管

### C2. discovery 类插话的标准处理

若 intake 被判定为 `discovery`：

1. 不默认打断当前活跃 worker
2. manager 判断是否存在可复用的活跃 pre-brainstorm ownership
3. 若无，则新建 dedicated worker worktree
4. worker 执行 `doc-pre-brainstorm-execution`
5. 产出：
   - `docs/B1-docs/<id>/brainstorms.md`
   - `docs/B1-docs/<id>/candidates.md`
   - `docs/milestones.md` candidate 同步
6. 回写 intake：
   - `status=absorbed`
   - `linked_artifact=<brainstorm/candidate/milestone>`

这样“人的插话”才算被系统正式吸收。

### D. Optional UI later

若后续需要 UI：

- UI 提供 chat/intake 面板与队列状态
- 但它只调用同一 intake CLI / 同一 artifact 层
- UI 不新增业务逻辑，不自带另一套路由系统

### D1. UI 的正确角色

UI 可以存在，但只应承担：

- 输入框
- intake inbox 列表
- disposition 展示
- linked artifact / affected worktree 展示

不应承担：

- 绕过 CLI 的直接 agent 注入
- 独立的路由逻辑
- 独立的 issue materialization 逻辑

换句话说，UI 是 intake 的展示层，不是另一套 supervisor。

## 深化收敛（2026-03-19 夜间补充）

### 关键修订 1：主管不是解释者，主管是 notice + claim + delegate 的调度者

前文把 manager 写得过重了，容易滑向“主管自己负责理解并解释每条插话”。这不符合 Freely 当前角色边界。

更准确的模型应是：

- `manager-agent`
  - 第一时间注意到 pending human interruption
  - `claim` 该 interruption，防止多轮 supervisor 重扫时重复委派
  - 判断 reaction mode
  - 立即委派专门 AI 去处理
  - 决定处理产物最后应吸收到哪个 canonical pool
- 专门 AI（可 materialize 为 `skill:human-interruption-handling` 所驱动的 worker）
  - 负责深度理解人类插话的真实意图
  - 负责调用需要的技能、读取上下文、判断与当前 issue/worktree 的关系
  - 负责生成“加工过的插话产物”
  - 负责把结果写回或 handoff 给下游 canonical owner

因此主管的“第一时间介入”不等于“主管本工位把文档解释和产物都写完”。

主管的最小动作应是：

- notice
- claim
- choose reaction mode
- delegate specialized AI
- decide final absorption target

### 关键修订 2：human interruption 需要分成 reaction plane 与 artifact plane

之前的表述更像在讨论单一 intake 状态机，但真正需要的是两层：

1. `reaction plane`
- 回答“当前正在运行的系统现在怎么响应这条插话”
- 关注 active worker / active run / immediate routing

2. `artifact plane`
- 回答“这条插话最终沉淀成什么，之后其他 AI 从哪里发现它”
- 关注 canonical pool、continuity、candidate、issue、recovery

如果不分开，就会产生两种常见失败：

- 只做 reaction，不做 artifact，导致插话体验很灵敏，但后续 AI 看不到
- 只做 artifact，不做 reaction，导致插话被当作慢速文档输入，用户感知机械

Freely 正确的主链应是：

`human interruption -> manager notice/claim -> choose reaction -> delegate specialized AI -> refined interruption artifact -> absorb into canonical pool`

补充收敛：

- 前文关于 `thread/event/session` 的探索可保留为未来扩展参考，但不应再视为当前 MVP 的前置条件
- 当前更高优先级的是先收紧 `reaction chain + specialized AI + canonical absorption`
- 只有当单条 interruption item + resolution artifact 无法支撑真实多轮插话时，才应升级到更复杂的会话建模

### 关键修订 3：reaction mode 应对应“主管调度动作”，而不是新的全局主词典

参考 `openclaw` 的 queue / steer 体系后，可以借鉴它的 reaction 语义，但不能照搬其 session-only 架构。

`openclaw` 的可借鉴点：

- `steer`
- `followup`
- `collect`
- `interrupt`

它们在 `openclaw` 中是运行时 queue mode：

- `steer`: 运行中注入当前 active run；流式时在下一个 tool boundary 生效
- `followup`: 当前 turn 结束后，用 queued payload 开新 turn
- `collect`: 多条消息先入 followup queue，再合并成一轮
- `interrupt`: 清掉当前 lane backlog，并 abort active run，再由新消息重启

相关实现与文档证据：

- `docs/concepts/queue.md`
- `docs/concepts/agent.md`
- `src/auto-reply/reply/get-reply-run.ts`
- `src/auto-reply/reply/agent-runner.ts`
- `src/agents/pi-embedded-runner/runs.ts`

但 `Freely` 和 `openclaw` 的差异必须明确：

- `openclaw` 主要解决“单 session 会话中，新 user message 如何影响 active run”
- `Freely` 还必须解决“这条插话最终进入哪个治理池、被哪个 worker/worktree 吸收”

因此在 Freely 中，这 4 个词应表达 `reaction mode`，而不是替代 `source_class/route_kind`。

### 修订后的 reaction mode 语义

建议 reaction mode 统一为 5 种：

1. `steer`
- 含义：当前 active worker 不必死亡，但其下一段工作必须立刻改向
- 适用：插话与当前 issue 强相关，且继续原方向会偏航

2. `followup`
- 含义：当前 worker 先收尾，插话在当前轮后立即进入下一轮处理
- 适用：插话重要，但不值得立刻修改当前执行轨迹

3. `collect`
- 含义：单条插话暂不稳定，需与后续补充一并加工，再产出统一 artifact
- 适用：连续碎碎念、边界尚未稳定、多条消息互为补充

4. `interrupt`
- 含义：当前 active worker 必须立刻停止，并以这条插话主导 replacement handoff
- 适用：继续运行会明显产出错误结果，或人类给出明确 stop/立即改向输入

5. `noise`
- 含义：插话应被记录、可追溯，但当前不应改变执行，也不应 materialize 成正式工作项
- 适用：纯情绪、碎片提醒、低信号闲聊、与当前项目边界无关的旁噪

注意：

- `noise` 不等于丢弃；它仍需被 notice、claim、留痕，并允许后续重新升级
- `collect` 不等于忽略；它要求专门 AI 产出聚合 digest
- `steer` 不等于 `interrupt`；是否杀进程取决于当前工具/worker 是否支持安全重定向

### 每种 reaction mode 的 Freely 落地链路

#### A. `steer`

适用：当前 active issue/worktree 仍然正确，但执行方向要立刻修正。

链路：

1. human interruption durable 写入 `.freely/intake/**`
2. manager notice + claim
3. manager 识别 `affected_worktree` / `affected_issue`
4. manager 不自己深度解释，而是委派专门 AI 产出 `steer handoff`
5. 该 handoff 至少包含：
   - 插话意图摘要
   - 与当前 issue 的关系
   - 哪些旧计划失效
   - 下一段工作该如何改向
6. 若当前工具支持安全 in-run 注入，则在 worker 的下一安全边界使用新 handoff 改向
7. 若当前工具不支持安全注入，则走 `fresh_with_handoff` / replacement worker
8. 该插话同时被吸收到当前 `issue/progress/recovery` continuity
9. intake 标记为 absorbed，并指向 continuity artifact

关键点：

- `steer` 的本质是“ownership 不变，方向变化”
- 它不必默认 kill 当前进程

#### B. `followup`

适用：当前 run 可自然结束，但插话应在下一轮被优先处理。

链路：

1. 写入 intake
2. manager notice + claim
3. manager 选择 `followup`
4. manager 立即委派专门 AI，产出 followup interpretation / handoff
5. 当前 worker 不被打断，继续到自然边界
6. 当前轮结束后，manager 以该 handoff 启动下一轮专门处理
7. 根据处理结果把插话吸收到 canonical pool
8. intake absorbed

关键点：

- `followup` 不是“稍后再说”
- 它是“已被主管接住，等待当前安全边界后立即处理”

#### C. `collect`

适用：连续多条插话属于一个未稳定主题，直接处理会过早或碎片化。

链路：

1. 多条插话逐条写入 intake
2. manager 每次都 notice + claim，但 reaction 选择 `collect`
3. 专门 AI 周期性读取相关 interruption items，产出 `interruption digest`
4. digest 至少包含：
   - 聚合后的主题摘要
   - 是否互相补充或冲突
   - 当前是否已达到可执行边界
   - 建议下一跳
5. 当 digest 稳定后，再升级为：
   - 新 discovery
   - 当前 issue continuation
   - control/runtime action
   - noise
6. 原始 intake items 统一链接到 digest，再一起关闭或继续等待

关键点：

- `collect` 必须生成中间加工产物，而不是只做原始消息堆积
- 这也是最适合专门 AI 深度解释的模式

#### D. `interrupt`

适用：当前 worker 继续执行会明显出错，或人类给出明确 stop / 立即改向命令。

链路：

1. 写入 intake
2. manager notice + claim
3. manager 识别 reaction=`interrupt`
4. manager 委派专门 AI 生成 replacement handoff
5. runtime 终止对应 worker 进程
6. 启动 replacement worker / replacement session
7. replacement worker 使用新的 handoff 启动
8. 后续将插话吸收到 `issue/progress/recovery` 或新的 `pre-brainstorm`
9. intake absorbed，并记录 replacement linkage

关键点：

- `interrupt` 必须伴随 replacement chain
- 只有 abort 没有 replacement handoff，不算处理完成

#### E. `noise`

适用：当前不应改变执行，也不应马上 materialize 成正式工作项。

链路：

1. 写入 intake
2. manager notice + claim
3. 专门 AI 确认该条目当前仅属低信号旁噪或无行动价值
4. 产出简短 resolution note：
   - why classified as noise
   - 是否需要后续重新评估
5. 写入 manager continuity 或 interruption resolution artifact
6. intake 标记为 dropped/noise-resolved，但保留追溯 link

关键点：

- `noise` 也需要 AI 处理结论，不是 silently ignore
- 否则“人类总是被正确对待”无法成立

### 加工后的 interruption artifact 应如何被后续 AI 对待

这里需要明确“加工产物”不是最终统一落在一个池里，而是分三层：

1. 原始收件层：
- `.freely/intake/**`
- 保存原始插话、reaction、claim、delegate、resolution link

2. 加工解释层：
- `interruption resolution artifact`
- 可落在 `.freely/intake-resolutions/**` 或项目级 continuity 等价落点
- 保存专门 AI 的解释结论、reaction mode、absorption target、delegate outcome

3. canonical pool：
- 按类型进入现有正式池

按类型的 canonical absorption：

- 新 discovery
  - `docs/B1-docs/**`
  - `docs/milestones.md`
- 当前 issue continuation
  - `issue`
  - `progress`
  - `recovery`
- runtime / control
  - runtime state / manager continuity
- noise
  - interruption resolution note / manager continuity

因此：

- `.freely/intake/**` 是短期事件池，不应成为长期主治理池
- 真正长期可发现的池，仍应是既有 canonical artifacts

### 其他 AI 何时使用“加工后的插话产物”

不是所有 AI 都持续扫描所有 interruption artifact，而应按类型消费：

1. `pre-brainstorm worker`
- 只在 interruption 已被升级为 discovery candidate 后消费

2. `current issue worker`
- 只在 interruption 被加工为 continuation handoff 后消费

3. `runtime / recovery worker`
- 只在 interruption 被加工为 control / recovery signal 后消费

4. `manager-agent`
- 持续看到 intake queue 与未 absorbed 的 interruption resolution artifact
- 用于监督 claim、delegate、absorption 是否完成

因此 Freely 不应让“所有 worker 持续阅读所有 interruption artifact”。

更合理的是：

- manager 持续阅读 interruption queue / resolution queue
- 业务 worker 只读取已经分发到自己 loop/ownership 的加工结果

### 对 `openclaw` 的深层借鉴边界

从 `openclaw` 可借鉴的是：

- reaction mode 不是抽象词，而是有真实运行时链路
- `steer/followup/collect/interrupt` 对应不同 active-run 处理方式
- system 不把所有插话都同等对待

不应直接照搬的是：

- `openclaw` 的 session-centric queue 直接等同于 Freely 的 project governance model
- `user message` 直接作为最终 worker 输入，不再经过主管委派与 canonical absorption

Freely 需要在 `openclaw` 的 reaction plane 之上，再增加：

- manager notice / claim
- specialized AI interpretation
- canonical absorption

这正是 Freely 与 openclaw 的产品差异。

## 需要回答的问题

1. intake artifact 应落在 `.freely/intake/`、`docs/B1-docs/CONVERGENCE.md`，还是别的路径？
2. intake item 的分类由 runtime 预分类，还是完全由 manager/AI 分类？
3. `steer/followup/collect/interrupt/noise` 是否足够表达 Freely 的 reaction plane；它们与 canonical `source_class/route_kind` 的映射真源应放在哪里？
4. detection signal 应落在 `.freely/run/` 的什么形式，才能让 manager 稳定知道“有插话”而不依赖会话内交互？
5. manager 如何对 intake 与 milestone continuation 排优先级，避免“任何插话都抢占当前验证”？
6. specialized AI 的最小角色边界应是什么：独立 worker、skill 驱动的 worker，还是某个现有 doc-loop worker 的变体？
7. `steer` 与 `interrupt` 的 runtime 边界应如何定义：哪些情况允许同工位改向，哪些情况必须 replacement worker？
8. 如果 human chat 明确点名“检查前端架构分支是否过时”，这类输入在 CLI 上应如何表达为 discovery，而不是直接命令式改代码？
9. `collect` 的聚合产物应如何定义：单个 digest 文件、resolution artifact，还是 manager continuity 中的 structured block？
10. 原始 intake、interruption resolution artifact、canonical pool 三层之间的 link schema 应如何定义，才能确保可追溯又不长出第二套 issue 系统？
11. 哪些旧口径需要被精确修订，例如“chat / session evidence 是 discovery source”，以免继续误导首跳路由？
12. 需要哪些最小测试，才能证明：
   - intake 可写入
   - manager 能检测到 pending intake
   - manager 可 claim 并立即委派 specialized AI
   - `steer` / `followup` / `collect` / `interrupt` / `noise` 各自走到正确 reaction chain
   - specialized AI 可产出 interruption resolution artifact
   - canonical absorption 正确发生
   - 完成状态可回写且不会重复委派

## 初步结论

- Freely 当前没有实现好 human chat intake 的完整能力闭环。
- 正确方向不是先做 UI，而是先补一条 CLI-first、durable、可恢复的 `intake -> manager notice/claim -> specialized AI -> interruption resolution artifact -> canonical absorption` 闭环。
- 这条能力属于 `auto-loop` 与 `doc-loop` 的接缝：
  - intake / notice / claim / delegate / reaction 在 `auto-loop`
  - canonical absorption 视类型进入 `doc-loop` 或 continuation/recovery
- human interruption 的默认站位是“插话 side input”，不是阻塞主 loop 的同步 gate。
- 因此系统要求是“插话必须被看见和仲裁”，不是“插话必须先处理完，主 loop 才能继续”。
- 同样，AI 执行过程中的不确定性默认应通过主管再委派 AI 分析解决，而不是等待人类补充指令或意图。
- 主管的职责应收紧为：notice、claim、choose reaction、delegate、choose canonical absorption target；主管不是深度解释者。
- 深度解释应由 specialized AI 完成，它通过 skill 调用与上下文读取产出 interruption resolution artifact。
- `steer/followup/collect/interrupt/noise` 应表达 reaction plane，而不是替代现有 `source_class/route_kind` 的主词典。
- 主管知道有插话，不能依赖交互式 prompt 注入；必须依赖 durable intake artifact + runtime signal + manager queue scan。
- `.freely/intake/**` 应是短期事件池，不应直接膨胀成长期主治理池；长期可发现事实仍应回到 canonical artifacts。
- 业务 worker 不应持续读取所有 interruption artifacts；manager 负责持续监督，业务 worker 只读取已经分发给自己 loop/ownership 的加工结果。
- 人类插话不应默认打断正在运行的 worker；reaction 需要在 `steer/followup/collect/interrupt/noise` 之间做 AI 判断。
- AI 的澄清需求不应默认转化为对人的同步依赖；默认应转化为新的 AI 分析/预研/复核委派。
- `openclaw` 值得借鉴的是 reaction chain，而不是其 session-only queue 直接等同于 Freely 的项目治理模型。
- 完整实现前，任何“主管正在监听人类插话”的说法都只能算概念成立，不能算产品能力已交付。

## 深度评审后的收口结论（进入能力设计前）

### 当前预研是否达标

结论：**已经接近达标，可以进入能力设计；但还不适合直接实现，必须先把文中的旧探索正式降权。**

已经足够稳定的部分：

- 主链已经稳定到 `CLI-first intake -> manager notice/claim -> specialized AI handling -> interruption resolution artifact -> canonical absorption`。
- `reaction plane` 与 `artifact plane` 的区分已经明确。
- manager 的职责边界已经收紧为编排，而不是深度解释。
- `openclaw` 的可借鉴点已经收紧到 reaction chain，而不是整体架构照搬。

仍需显式降权的旧探索：

- 文中早期的 `observe/control/continuation/discovery`，不应再作为 reaction mode 继续扩张；它只可保留为吸收后的 canonical 去向参考。
- 文中早期的 `thread/event/session`，应明确视为未来扩展，而不是当前 MVP 前置。
- “所有 human chat 都先算 discovery source” 的旧说法，应只保留在最终 absorption 为 discovery 的场景。

因此，当前文档的正确阅读方式应是：

- raw interruption：`.freely/intake/**`
- current-run reaction：`steer/followup/collect/interrupt/noise`
- final absorption：回到 discovery / continuation / control / resolution-note 等 canonical pools

### Freely 能力落地的最小模块边界

若进入正式设计，建议按低耦合方式拆成 4 层：

1. `runtime/scripts`
- 命令面：
  - `freely intake chat`
  - `freely intake status`
  - 后续如确有必要，再补 `claim/resolve`
- 负责：
  - durable intake 落盘
  - detection signal
  - manager prompt surfacing
  - 进程级 kill/restart/fresh_with_handoff
- 不负责：
  - 深度解释
  - 业务吸收

2. `manager-agent`
- 负责：
  - notice
  - claim
  - choose reaction
  - delegate specialized AI
  - choose absorption target
  - 监督 completion
- 不负责：
  - 深度解释
  - 直接写 pre-brainstorm / milestone / issue

3. `skill:human-interruption-handling`
- 作为 specialized AI 的核心能力模块
- 输入：
  - raw intake
  - 当前 issue/worktree/milestone/runtime 上下文
  - manager 选定的 reaction
- 输出：
  - `interruption resolution artifact`
  - `intent_summary`
  - `worker_handoff`
  - `absorption_recommendation`
  - `link_schema`
- 负责：
  - 深度解释
  - skill 级上下文读取
  - 生成后续可消费的 bridge artifact
- 不负责：
  - 直接取代下游 doc/dev skills

4. 既有业务 skills
- discovery -> `skill:doc-pre-brainstorm-execution`
- continuation -> 既有 continuation/recovery/doc/dev 路径
- control -> runtime / manager continuity
- noise -> resolution note / continuity

这套拆法满足：

- CLI first
- skill 收口
- manager 只编排
- downstream 继续复用既有技能，而不是长第二套系统

### 建议的 artifact 分层

建议固定三层，而不是试图用一个目录承载全部语义：

1. 原始输入层
- `.freely/intake/**`
- 只保存 raw interruption 与最小状态

2. 加工桥接层
- `.freely/run/interruption-resolution/**`
- 保存 specialized AI 生成的 resolution artifact / digest / handoff

3. 正式治理层
- discovery -> `docs/B1-docs/**` + `docs/milestones.md`
- continuation -> `issue/progress/recovery`
- control -> runtime state / manager continuity
- noise -> resolution note / continuity

约束：

- 原始输入不直接冒充正式 issue
- bridge artifact 不长期替代 canonical pool
- 业务 worker 不持续轮询 `.freely/intake/**`

### 每种 reaction mode 的 Freely 落地链路

#### `steer`

- 语义：ownership 不变，但当前活跃工位接下来必须改方向。
- 链路：
  1. raw interruption 落盘
  2. manager `notice + claim`
  3. manager 选择 `steer`
  4. specialized AI 生成 `steer handoff`
  5. runtime 根据工具能力二选一：
     - 安全注入 handoff
     - `fresh_with_handoff` 重启同工位 worker
  6. 当前 worker 只消费自己 handoff
  7. 后续吸收到当前 issue/progress/recovery

#### `followup`

- 语义：当前 run 先自然结束，下一轮马上处理。
- 链路：
  1. raw interruption 落盘
  2. manager `notice + claim`
  3. manager 选择 `followup`
  4. specialized AI 生成 followup artifact
  5. 当前 worker 不被 kill
  6. 当前 run 结束后，manager 以该 artifact 启动下一轮处理

#### `collect`

- 语义：单条插话不足以稳定解释，先聚合再处理。
- 链路：
  1. 每条 interruption 单独落盘
  2. manager 对每条都 `notice + claim`
  3. reaction 设为 `collect`
  4. specialized AI 产出 `interruption digest`
  5. digest 稳定后再决定 absorption 去向

#### `interrupt`

- 语义：当前 run 继续下去会明显错，必须立刻替换。
- 链路：
  1. raw interruption 落盘
  2. manager `notice + claim`
  3. manager 选择 `interrupt`
  4. specialized AI 生成 replacement handoff
  5. runtime kill 当前 worker
  6. runtime 启动 replacement worker/session
  7. replacement worker 只消费 replacement handoff

#### `noise`

- 语义：已被看见并解释，但当前不应进入业务主线。
- 链路：
  1. raw interruption 落盘
  2. manager `notice + claim`
  3. specialized AI 生成 resolution note
  4. 写入 continuity / resolution artifact
  5. intake 标记为 resolved-noise，但保留追溯 link

### worker 何时看到加工后的 interruption artifact

原则：**按 ownership 定向消费，不做全局广播。**

- `manager-agent`
  - 持续读取 intake queue 与 unresolved resolution artifacts
- `pre-brainstorm worker`
  - 只读取已加工为 discovery handoff 的 artifact
- `current issue / dev worker`
  - 只读取已加工为 steer/followup/interrupt handoff 的 artifact
- `runtime`
  - 只读取 process-control 所需 signal / handoff

因此默认机制应是：

- manager 看全局
- specialized AI 做加工
- 业务 worker 只看发给自己的结果

而不是：

- 所有 worker 自己持续扫 `.freely/intake/**`

### 进入实现前必须先固定的 4 件事

1. reaction 词典
- MVP 只用 `steer/followup/collect/interrupt/noise`

2. specialized AI skill 契约
- 输入什么
- 输出什么
- link schema 怎么写

3. runtime 动作矩阵
- 哪些情况注入
- 哪些情况 `fresh_with_handoff`
- 哪些情况 kill + replacement

4. artifact 放置策略
- raw intake 放哪
- resolution artifact 放哪
- 最终 absorption 放哪

只有这 4 件事固定下来，human interruption 才算从“预研想法”真正进入“Freely 能力设计”。

## Materialization Update

- `I-20260319-1715` 已物化为正式 issue：`docs/epics/workspace-routing-foundation/human-chat-intake-and-manager-delegation/issues/human-chat-intake-and-manager-delegation.md`
- canonical 文档工位挂起说明：`feature/prebrainstorm-human-chat-canonical-20260320-0023` 只重复物化了 human-chat issue 包，独立 verification/review 不足，且祖先历史混入 `CLI TUI` / `project-resolution` 能力线；后续只允许人工摘取真正独有的 human-chat 文档差异到 `feature/human-chat-intake-supervision-20260319-1030`，不得把本工位作为独立 promote 来源。
- 后续对这条能力的收口应从 issue / verification 继续，不应再回退到 pre-brainstorm 作为主执行入口。
