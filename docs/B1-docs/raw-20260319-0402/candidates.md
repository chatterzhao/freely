# Candidates

## Priority Summary

当前候选按优先级重新收束如下：

1. `C-20260319-0402-01`
   - completion model 与 change guardrails
   - 这是问题定义层，优先级最高

2. `C-20260320-03`
   - issue acceptance 驱动的最小集成测试 substrate
   - 这是把 doc-loop 和 dev-loop 真正接起来的最小执行门

3. `C-20260320-01`
   - guardrail planner 与 validation escalation
   - 这是把 completion model 变成 runtime 决策的连接层

4. `C-20260319-0402-02`
   - machine-readable evidence interface
   - 这是把信号统一暴露给三层 loop 消费的证据面

5. `C-20260320-02`
   - bootstrap ladder 与 experiment ledger
   - 方向成立，但更像在前四者稳定后再 formalize

6. `C-20260319-0402-03`
   - doc-gardening / cleanup loop
   - 保持 `needs_research`

7. `C-20260319-0402-04`
   - 吞吐量叙事与全 agent 纯度
   - 明确 `dropped`

## C-20260319-0402-A: legacy issue

- status: `proposed`
- problem: Freely 已有 worktree/governance/doc-loop 基础，但“什么叫完成、何时升级验证、哪些风险必须人工复核、经验如何回写系统”仍分散存在，缺少统一 completion model。
- change:
  - 产出一份面向 Freely 的 completion model / change guardrails 草图
  - 把现有能力映射到 `policy -> quality gates -> risk routing -> deep validation -> decision loop`
  - 再把这些 change-lifecycle guardrails 归并到 `record system / feedback loops / invariants / cleanup` 四层
  - 标出当前缺失的自动化接口、风险分流点与治理门
- acceptance_hint:
  - 能回答 Freely 目前哪些能力已经是 agent-first，哪些仍依赖人工隐性判断权
  - 能说明某次改动何时只需基础门，何时必须升级 risk routing、deep validation 或人工复核
  - 能把这些规则映射回 Freely 三层循环，而不是停留在外部术语层
  - 后续 issue 可以按 lifecycle guardrail 缺口而不是按零散脚本推进
- decision_reason: 外部文章真正有价值的不是名词，而是把“完成条件漂移”细化成一套可分层判断的 guardrails；这使它成为当前最接近问题定义层的候选项。
- next_action: 继续 pre-brainstorm，先把 Freely 的 completion model 收束为 change-lifecycle guardrails 与四层 substrate 的映射；边界稳定前不要 materialize。
- revisit_trigger: 当 `policy / gates / risk routing / deep validation / decision loop` 可以被明确映射到 Freely 的最小可执行问题集合时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0402-A: legacy issue

- status: `proposed`
- problem: 当前 worktree discipline 很强，但 runtime、日志、dirty budget、验证状态对 agent 的读取面仍不够统一。
- change:
  - 盘点 `status`、`wt-status-all`、测试、runtime 现有输出
  - 设计统一的 machine-readable 汇总接口
  - 覆盖 benchmark / detail / experiment lineage 这类可续接证据
  - 明确哪些字段要直接服务 risk routing、哪些字段用于触发 deep validation 或人工复核
  - 让 issue acceptance、最小集成测试结果和更深验证结果都能进入同一证据接口
  - 优先补自主循环最依赖的最小字段
- acceptance_hint:
  - agent 能在少量上下文下直接拿到当前 worktree 的可执行状态摘要
  - agent 能基于结构化信号判断当前变更属于基础门通过、需要升级验证、还是需要人工复核
  - 这些结构化信号可被 outer/doc/dev 三层循环共同消费，而不是只给 dev-loop 自己看
  - 新 session 能消费这些证据继续推进，而不是只能依赖短期上下文
  - 恢复、验证、promotion 决策减少对人工解释的依赖
- decision_reason: 外部研究把问题从“状态要不要统一”推进到“统一状态是否足以支撑完成条件判断与验证升级决策”；这让本候选更接近 Freely 的执行控制面。
- next_action: 继续 pre-brainstorm，先盘点现有 status / wt-status-all / runtime 输出里哪些已经可支撑 risk routing，哪些深验证触发信号仍缺失，再决定要不要 materialize。
- revisit_trigger: 当可以明确指出哪些字段必须稳定暴露给 agent，且这些字段已经足以支持最小的 risk routing / validation escalation 决策时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0402-A: legacy issue

- status: `proposed`
- problem: 即使状态变得可读，Freely 仍缺少一个把 `change type + risk` 映射到 `required gates + escalation path` 的控制面，因此三层循环还无法稳定表现出真正的 harness 能力。
- change:
  - 定义 `change_class` / `risk_class` 的最小分类
  - 设计一个 `guardrail planner`，输入 issue/change/risk，输出本轮必须执行的 gates 与证据要求
  - 把 issue acceptance 驱动的最小集成测试纳入 planner 的默认基础门
  - 把阶梯式验证和对抗验证纳入 planner 的默认 guardrails
  - 定义何时升级到 deep validation、何时必须人工复核、何时 reroute 到 pre-brainstorm / recovery
- acceptance_hint:
  - agent 不再只会“按默认流程往前跑”，而能根据风险调整验证和推进策略
  - agent 能用最低成本先暴露大部分失败，再决定是否进入更重的验证
  - 同一套 planner 可以被 outer loop 调度、被 doc-loop 预先定义、被 dev-loop 执行和回写
- decision_reason: 这是把 completion model 变成实际运行能力的关键连接层；没有 planner，前两个候选仍然更像静态分析，而不是 harness 控制面。
- next_action: 继续 pre-brainstorm，先用现有 issue 类型与验证路径做一次最小分类，再决定是否 materialize。
- revisit_trigger: 当 `change_class`、`risk_class` 与最小 gates 集合已经能稳定映射时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0402-A: legacy issue

- status: `proposed`
- problem: Freely 已有 loop 和治理，但还缺“agent 如何逐层长出闭环能力”的正式模型，也缺一层统一的实验记录面来支撑跨 session 持续推进。
- change:
  - 定义最小 bootstrap ladder：`see -> measure -> diagnose -> safe-iterate -> continuous-run`
  - 为每个阶段定义进入条件、缺失信号和下一步建议
  - 设计 experiment ledger，沉淀 benchmark、detail、实验目录、结果 lineage，供后续 session / supervisor / recovery 继续消费
- acceptance_hint:
  - 系统能判断当前 issue 或项目卡在哪一层能力，而不是只知道“还没完成”
  - 新 session 能基于统一实验记录继续前进，而不是重新阅读大量散落日志
  - Freely 可把“搭闭环”本身变成可管理、可演进的正式对象
- decision_reason: HelixVerify 文章证明，真正让 agent 变强的不是一次写对代码，而是逐层补 substrate；Freely 目前缺这条显式 bootstrapping 路径。
- next_action: 继续 pre-brainstorm，先用 Freely 自己的现状做一次 bootstrap stage 盘点，再决定 experiment ledger 应落在哪一层 artifact。
- revisit_trigger: 当五个 bootstrap stage 的边界和最小证据面已经能被稳定描述时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0402-A: legacy issue

- status: `proposed`
- problem: Freely 当前已有测试与治理，但“issue 验收标准如何第一时间落成可执行集成门”还不稳定，导致 agent 容易停留在单测或静态结果层面，闭环缺少运行时事实校验。
- change:
  - 定义 `issue acceptance -> minimal executable gate` 的最小映射规则
  - 默认优先将验收标准落成集成测试、应用级验证或等价 runtime gate
  - 规定何时只需基础集成门，何时升级到更深验证
- acceptance_hint:
  - 新 issue 不再只有自然语言验收标准，而是默认带有一个最小可执行验证门
  - agent 能直接用这道门判断当前变更是否真正触达运行时验收事实
  - 该能力可作为 harness 的第一批 substrate，而不是等到后期再补
- decision_reason: 多篇外部研究都在指向同一点：没有 issue-bound executable validation，agent 只是在“改代码”，而不是在闭环里交付应用。
- next_action: 继续 pre-brainstorm，把当前样本收束成一版 `issue type -> minimal gate -> escalation path` 规则草图，再决定是否 materialize。
- revisit_trigger: 当 issue taxonomy、acceptance taxonomy 与最小可执行 gate 的映射已经足够稳定，能形成统一规则时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0402-A: legacy issue

- status: `needs_research`
- problem: OpenAI 的经验表明，全 agent 代码库会持续产生漂移；如果 Freely 没有自动清理环，治理成本会不断上升。
- change:
  - 识别可机械检查的文档/代码漂移信号
  - 为 doc-gardening / cleanup PR 定义触发条件与最小验收
  - 优先从过期文档、未交叉链接、命名偏差、重复 helper 等模式开始
- acceptance_hint:
  - 清理动作可以周期性运行，而不是只在人工注意到时发生
  - “治理漂移”被前移到自动发现和小步修复
- decision_reason: 方向成立，但前提是 Freely 先把 lifecycle guardrails、反馈面和 enforcement 面统一，否则会过早进入“自动清理自动化”而缺少稳定基线。
- next_action: 保持 `needs_research`，等前两个更基础的 completion / guardrail 候选边界稳定后，再决定是否 materialize。
- revisit_trigger: 当反馈面和 enforcement 面已经可稳定消费后，再回看是否需要常驻 cleanup loop。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

## C-20260319-0402-A: legacy issue

- status: `dropped`
- problem: 外部案例容易把讨论带偏到“更多 PR、更少人工、全 agent 生成代码”，但这不是 Freely 当前阶段的核心成功标准。
- change:
  - 在后续相关 issue / brainstorm 中明确记录不采用项
  - 优先用“自治闭环是否稳定、是否可恢复、是否能开发真实应用”作为判断标准
- acceptance_hint:
  - 后续方案不再把吞吐量或 agent 纯度当作主卖点
  - 自治开发应用的控制面与恢复能力保持优先级高于速度叙事
- decision_reason: 这不是要 materialize 的功能项，而是一个需要被明确记录的研究排除项。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
