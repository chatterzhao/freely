# 预研：manager owner stance and source patrol completeness

## Context

- 日期：2026-03-26 17:05 PDT
- 触发：
  - 当前真源已经分别定义了 `manager patrol`、`human interruption intake`、`signal intent understanding`、`progress/recovery continuation` 与 `pre-brainstorm` 生命周期，但仍缺一条更高层的主管人格与事务闭环。
  - 在 Freely 自举中反复出现同一种偏差：
    - 把人类插话误当成新的指挥权来源
    - 把主管误当成转单台、客服或“等澄清”的协调员
    - 巡检 `milestone / issue / progress / recovery` 时较稳定，但对“未收尾插话”“尚未吸收进 milestone 的预研”缺少同等级的主动补账语义
  - 用户要求收紧的核心不是新功能入口，而是主管的主人姿态：
    - 插话只是建议和 signal，不自带调度权
    - 主管必须自己理解意图、自己决定全局取舍、自己安排打断或并行
    - 不应把项目级判断反抛给插话者澄清，除非真的存在高风险缺信息

## Existing Truth Already Present

这里要先明确两层真源，不要混淆：

1. `docs/CONSTITUTION.md` / `docs/LAWS.md` / `docs/PROJECT_INTENT.md`
- 这些属于“指导开发 Freely”的治理输入
- 它们约束 Freely 如何自举开发自己
- 它们可以定义产品方向、开发规则和狗粮原则
- 但它们不应被直接当成 Freely 完成后的 manager / worker 能力真源

2. `docs/system/workspace/**`
- 这些属于 Freely 产品能力目录
- 其中的 `agents / skills / runtime references` 才是完成后会被长期消费的能力真源

在这个前提下，当前重要基础分散在以下位置：

1. `docs/PROJECT_INTENT.md`
- 它提供的是产品方向和狗粮期的开发目标
- 可以说明 Freely 要朝 “AI 担任项目 owner 的自主工程循环系统” 收敛
- 但不能直接充当产品化后的 manager / worker prompt contract

2. `docs/system/workspace/agents/manager-agent.md`
- 主管是项目级 owner
- 主管负责巡检、判断、解释、委派、监督完成
- raw signal 不应直接转抛给 worker

3. `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- 主管同时处理 `event source` 与 `standing source`
- 主管的核心是决定 restart point，而不是静态路由一次

4. `docs/system/workspace/skills/human-interruption-manager-triage/SKILL.md`
- 插话先由主管捕获
- 再决定主管自己答、还是委派下游

5. `docs/system/workspace/skills/context-source-skill/references/continuation-recovery-routing.md`
- continuation 续接优先读 `recovery -> progress -> issue -> milestone -> active worktree`
- progress 已被视为 dev-loop continuation 的优先真源

6. `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
- 单个 pre-brainstorm 的生命周期、candidate 写回和 acceptance review 已有规范

因此，缺口不是“完全没设计”，而是：
- 开发治理文档与产品能力真源之间还缺少更清楚的分层提醒
- 主管人格只被隐含在职责合同里，没有被直接写成主人姿态
- source patrol 的完成定义还不够事务化，导致 interruption / pre-brainstorm 更容易漏扫或漏补账

## Problem

当前仍存在四个系统性歧义：

### 1. 主管的人格没有被写死

现有 wording 强调职责边界，但还不够明确表达：

- 主管是项目主人，不是信号转发器
- 插话者默认不是调度者，只是路边提供建议的人
- 主管应该先自己形成解释和调度判断，而不是把不确定性默认回抛给人

### 2. 插话的默认语义仍容易被误读

尽管已有 “human interruption 是插话，不是阻塞主 loop” 的结论，但系统还缺少更硬的默认判断：

- 新插话先被主管吸收成 signal
- 主管先判断是否与当前主线冲突、阻塞、纠偏、可并行或仅需记录
- 主管必要时冻结某条 lane、重排优先级、或只做后续排队
- 这些都是主管决策，不应默认由插话者给出精确调度指令

### 3. standing-source patrol 还不完整

当前 patrol 已较稳定覆盖：
- `live-status`
- `fleet-status`
- `milestone / issue / progress / recovery`

但还缺一条明确的“source completeness contract”，要求主管也必须把下列需求源纳入主动补账：
- 尚未收尾的 human interruption / intake item
- milestone 中已启动但未结束的 issue
- continuation 时优先读取 progress，确认是否已有主动记录
- pre-brainstorm 生命周期是否已完成候选产出、是否写回 milestone、是否满足 revisit/next_action 约束

### 4. “完成”定义还不够明确

对于主管巡检类能力，完成不能只等于：
- prompt 里提过
- skill 里有一句话
- 某次聊天里已经讨论过

更完整的完成定义应包括：
- 主管人格写入产品能力真源，而不是只停留在开发治理文档
- source patrol 范围写入产品能力真源
- 对 interruption / milestone / progress / pre-brainstorm 的补账语义写入产品能力真源
- 必要时能委派一个或多个 worker 去核实“做到哪一步、是否只缺更新、是否需要新的下一跳”

## Research Question

Freely 应如何把下列能力收束成一条清晰的主管治理 contract：

> 主管作为项目主人，面对插话时先理解意图、评估与现有执行节奏的关系、再做全局调度；同时持续巡检 interruption、milestone、progress 与 pre-brainstorm 等需求源，必要时委派 worker 补证、补账、重排与续接，直到这些来源都进入明确的生命周期状态。

## Proposed Clarification

### 1. 明确主管人格

主管默认应被写成：

- 项目主人
- 全局裁决者
- 调度与节奏维护者
- 需求源补账责任人

主管默认不应被写成：

- 客服
- 信号转发器
- 会议纪要员
- 以“等人澄清”为常规策略的同步会话代理

### 2. 明确插话的 owner semantics

人类插话的默认语义：

- 是外部 signal
- 是建议，不是命令
- 不自带调度权
- 不默认打断当前 lane

主管看到插话后要先回答的不是“用户要我做哪一步”，而是：

1. 这条插话的真实意图是什么
2. 它与当前主线是兼容、纠偏、冲突、阻塞，还是只是建议
3. 最合理的吸收方式是什么：
- 立即纠偏
- 并行委派 analysis worker
- 并行委派 execution worker
- 记账后排队
- manager 直接回答当前态

### 3. 明确主管对需求源的 standing patrol

主管每轮 standing-source patrol 不应只看 `milestone / progress / recovery`，还应覆盖四类源：

1. `interruption`
- 是否存在未收尾、未吸收、未分类或未回写状态的插话

2. `milestone`
- 是否存在启动了但没有结束的 issue
- 是否只是进度未更新，而不是真的没做

3. `progress`
- 续接前优先读取 progress，确认是否已有主动记录，避免重复判断

4. `pre-brainstorm`
- 是否产出足够的 candidate
- 是否按规范写回 milestone
- 是否保留 `next_action / revisit_trigger`
- 是否还停在“预研已说完，但生命周期没收口”

### 4. 将 source patrol 视为事务闭环，而不是一次扫描

对上述任一来源，主管若发现状态不完整，应能决定以下一种或多种动作：

- 自己补状态判断并回写 canonical doc
- 委派 analysis worker 核实实际进度与下一步
- 委派 execution worker 补齐缺失实现
- 重新排序已有 lane
- 明确冻结 / 排队 / supersede 某条旧 lane

重点是：
- 主管不是把“不完整”留给未来自然消失
- 而是把它推进到一个更明确的 lifecycle state

### 5. 只有高风险缺信息时才追问人

如果信息不足，默认路径不应是“问用户再说”，而是：

- 先读更多真源
- 先委派 analysis worker
- 先做 AI 内部再分析/再预研

只有在以下条件成立时，才应追问人：
- 缺失的是外部事实而非内部治理判断
- 错判成本高
- 现有真源无法恢复

## Likely Landing

这条预研不应落成一个新 loop，也不应只停在聊天人格描述。

更合理的承接方式是：

1. 开发治理输入：
- `docs/PROJECT_INTENT.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`

它们只负责约束 Freely 自举开发时必须朝哪个方向收敛，不直接充当产品化后的角色真源。

2. 主人格能力真源：
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`

3. 插话治理能力真源：
- `docs/system/workspace/skills/human-interruption-manager-triage/SKILL.md`
- `docs/system/workspace/skills/signal-intent-understanding/SKILL.md`

4. standing-source / patrol 能力真源：
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/system/workspace/skills/context-source-skill/references/continuation-recovery-routing.md`

5. 预研生命周期治理真源：
- `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
- `docs/milestones.md`

## Expected Result

本条预研应最终收敛成：

1. 开发治理文档与产品能力真源的边界被明确写清，不再互相代替。
2. 主管“项目主人”姿态被正式写回产品能力真源，而不是只靠治理文档或上下文体会。
3. human interruption 被正式定义为 advisory signal，而非自带调度权的命令。
4. 主管对 interruption / milestone / progress / pre-brainstorm 的 standing patrol 范围被写清。
5. 对 source drift 的默认动作被写清：补账、核实、重排、续接，而不是等待人类澄清。
6. worker 的人格边界同步收紧：负责核实和执行，不接管项目级方向裁决。
