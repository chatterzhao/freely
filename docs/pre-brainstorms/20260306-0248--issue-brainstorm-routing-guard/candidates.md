# Candidates - 20260306-0248--issue-brainstorm-routing-guard

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_review

## Candidates

### C-20260306-1101
- title: brainstorm 路由元数据契约
- problem: 当前无法可靠判断 brainstorm 是 pre-brainstorm 还是 issue-bound brainstorm，导致脚本无法稳定兜底。
- why_now: 规则已在文档中存在，但没有执行证据字段，AI 和人类都会继续依赖模糊上下文。
- acceptance_hint: 定义最小元数据集合，至少支持两层判断：1) brainstorm 文件落位是否为 pre / issue-bound；2) 已有 issue 的研究态是否进入 issue-bound brainstorm（IBM/B）而非误回 pre-brainstorms。
- priority: P0
- status: proposed
- decision_reason: pending://research
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

### C-20260306-1102
- title: brainstorm 路由创建入口
- problem: 目前没有统一入口明确声明“这是 pre-brainstorm 还是 issue-brainstorm”，只能事后检查。
- why_now: 如果源头不约束，pre-commit 只能拦错，不能稳定引导正确路径。
- acceptance_hint: 定义一个显式入口或命令参数，创建时要求声明来源类型或 issue 路径；同时明确该入口只决定 brainstorm 文档落位，不直接替代 milestone-centered route decision。
- priority: P0
- status: proposed
- decision_reason: pending://research
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

### C-20260306-1103
- title: brainstorm 路由 pre-commit / bmad-check 兜底
- problem: 当前 hook 和检查脚本无法阻止 brainstorm 文档放错位置，也无法发现旧路径残留。
- why_now: 这是规则真正变成执行纪律的关键一层。
- acceptance_hint: pre-commit 检查 staged brainstorm 路径与元数据一致性；bmad-check 检查旧路径和必需元数据；同时避免把“有 issue/没 issue”误实现成过度简化的总路由。
- priority: P0
- status: proposed
- decision_reason: pending://research
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []


### C-20260306-1104
- title: 统一循环图中的 milestone-centered routing 修正
- problem: 现有表述仍接近 `pre-brainstorms -> candidates -> route`，会让人误以为 pre-brainstorms 结束后直接负责后续路由；这与当前收敛出的 milestone-centered routing 不一致。
- why_now: 如果主流程图和文字说明不修正，后续 AI 仍会把 candidates 误当成调度主表，导致会话启动和 auto-loop 路由理解继续偏差。
- acceptance_hint: 将流程图与文字说明统一改为 `pre-brainstorms -> candidates -> milestone -> route decision`，并明确：1) milestone 是唯一活跃任务路由面；2) issue-bound brainstorm 属于已有 issue 方向下的 `IBM/B` 子路由。
- priority: P0
- status: proposed
- decision_reason: pending://research
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []


### C-20260306-1105
- title: milestone-centered routing 对 guidance/skills 的同步对齐
- problem: 当前 `PROJECT_INTENT`、`doc-loop-execution`、`auto-loop-orchestrator`、`pre-brainstorms/README` 等仍在表达 `pre-brainstorms -> candidates -> route` 或把 `candidates.md` 当成调度主表，这与当前收敛出的 milestone-centered routing 冲突。
- why_now: 如果不先修正 guidance，后续 AI 和人类仍会按旧方法执行，导致规范、流程图和实现再次分叉。
- acceptance_hint: 明确修正文档/skills 口径为 `pre-brainstorms -> candidates -> milestone -> route decision`；移除 `candidates.md` 直接承担活跃路由的表述；补充 milestone 作为唯一活跃任务路由面的说明，并补上“已有 issue 但仍需研究时进入 issue-bound brainstorm（IBM/B）”的指导。
- priority: P0
- status: proposed
- decision_reason: pending://research
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []


### C-20260306-1106
- title: auto-loop 来源适配与上下文归一化契约
- problem: 当前只讨论了 milestone-centered routing，但还未明确 `intent/review/test/chat/github-issue/autonomous discovery/recovery` 如何被 auto-loop 组装成统一 `input_context`，导致路由器输入仍不稳定。
- why_now: 如果没有 source adapters 和 normalized context 契约，milestone-centered routing 只能停留在概念层，无法稳定服务 Freely 的自治循环与人类插话场景。
- acceptance_hint: 定义 `auto-loop` 的来源适配职责、`input_context` 最小结构，以及不同来源如何形成可供 `router(input_context, milestone_path)` 消费的统一输入。
- priority: P0
- status: proposed
- decision_reason: pending://research
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []


### C-20260306-1107
- title: doc-loop(IBM) 正式目录先行与产物落位规则
- problem: 当前对于“何时从 pre-brainstorms 转入正式 story 目录”以及 `IBM` 产物应落在哪一层，缺少明确规则，容易导致已有 issue 的 brainstorm 和正式文档继续留在 pre-brainstorms，破坏正式文档边界。
- why_now: 随着 milestone-centered routing 收敛完成，必须明确：一旦确定进入 `doc-loop(IBM)`，就应进入正式 story 文档空间，而不是继续停留在 pre-brainstorms。
- acceptance_hint: 明确规则为：已确定进入 `doc-loop(IBM)` 时，先确认 `epic-name/story-name` 并建立 `docs/epics/{epic}/{story}/`；除 milestone 外的 `IBM` 产物统一沉淀到该目录；milestone 由 `M` 单独回写。
- priority: P0
- status: proposed
- decision_reason: pending://research
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []


### C-20260306-1108
- title: auto-loop 提示词装配 + 可用 issue 双主 skill 入口模型
- problem: 当前路由研究已经收敛出 milestone-centered routing，但产品层还缺少一个足够简洁、可直接驱动 AI CLI 的入口模型；若没有明确的入口抽象，后续实现容易把全部状态分流逻辑散落到多个文档或脚本中。
- why_now: Freely 目标是自治、无交互、自动批准模式运行，实际落地需要一个既简单又不丢失状态分流精度的 AI 入口结构。
- acceptance_hint: 收敛出“auto-loop 组装提示词 + 2 main skills”模型：auto-loop 负责根据来源 skill 组装输入并发送统一提示词；提示词要求 AI 根据输入分析意图，并在 milestone 中判断是否存在**可用 issue**；若无可用 issue 则读取 `no-usable-issue-skill.md`，若有可用 issue 则读取 `has-usable-issue-skill.md`；明确这里判断的是 usable issue，而不是 issue 是否字面存在。
- priority: P0
- status: proposed
- decision_reason: pending://research
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
