# Candidates - 20260306-0248--issue-brainstorm-routing-guard

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_review

## Convergence

- 最终工作产物应收敛为：
  - 1 个首跳中枢代理：`auto-loop-lead-agent.md`
  - 1 个来源适配与工具选择 skill：`context-source-skill.md`
  - 2 个第二跳 workflow skills：`no-skill.md`、`has-skill.md`
  - 1 个 `auto-loop-orchestrator` / guidance 对齐项
- 当前先不把 hook/script 放回主收敛；先把两层 auto-loop 机制和 4 个文档型产物写清。

## Candidates

### C-20260306-1101
- title: `auto-loop-lead-agent.md`
- problem: 当前虽然已经收敛出两层 auto-loop 机制，但还缺少一个明确的首跳 AI 中枢代理说明，定义首个 AI 工具启动后到底承担什么职责。
- why_now: 如果没有 `lead-agent` 这一层，`context-source-skill.md`、`no-skill.md`、`has-skill.md` 会被误写成同一层入口，导致首跳编排和第二跳执行再次混淆。
- acceptance_hint: 创建 `auto-loop-lead-agent.md`，明确：1) 它由首个 AI 工具执行；2) 它负责调用 `context-source-skill.md`；3) 它负责生成下一跳 AI 工具调用指令；4) 它不替代 `doc-loop-execution` / `dev-loop-execution`。
- priority: P0
- status: promoted
- decision_reason: 这是两层 auto-loop 机制的中枢；不先明确它，后续所有 skill 层级都会继续混乱。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

### C-20260306-1102
- title: `context-source-skill.md`
- problem: 当前缺少一个供 `lead-agent` 使用的来源适配与工具选择规则文件，无法稳定把 `<source input>` 转换成下一跳 AI 工具调用指令。
- why_now: 你已经明确首跳不是直接执行业务工作，而是先做来源适配和工具调用装配；如果没有这一层，首跳 AI 只能重新自由发挥。
- acceptance_hint: 创建 `context-source-skill.md`，明确：1) chat/review/test/github-issue/recovery 等来源输入如何组织；2) 如何结合任务强度、工具优先级、工具可用性列表选工具；3) 如何生成第二跳调用指令；4) 不把 doc/dev-loop 细节塞到该 skill。
- priority: P0
- status: promoted
- decision_reason: 这是 `lead-agent` 的核心依赖文件，也是两层模型里真正承载来源适配的一层。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

### C-20260306-1103
- title: `no-skill.md`
- problem: 当前没有一个正式的第二跳执行指南，指导“没有可用 issue”时如何继续前置研究、如何写 `pre-brainstorms` 产物、以及如何同步 milestone。
- why_now: 这是下游 AI 命中“无可用 issue”时的唯一标准工作入口；如果不先固化，仍会退回口头解释。
- acceptance_hint: 创建 `no-skill.md`，明确：1) 无可用 issue 时继续停留 `pre-brainstorms`；2) 如何产出 `brainstorms.md` / `candidates.md`；3) 如何将 candidate 原子同步进 milestone；4) 什么情况下停止前置研究并回流。
- priority: P0
- status: promoted
- decision_reason: 这是第二跳执行层里“无可用 issue”分支的标准工作法。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []


### C-20260306-1104
- title: `has-skill.md`
- problem: 当前没有一个正式的第二跳执行指南，指导“已经命中可用 issue”时如何进一步进入正式 issue 工作流，以及何时应调用 `doc-loop-execution` 或 `dev-loop-execution`。
- why_now: 如果这一层不写清，最容易把“已有 issue”误实现成固定 doc-loop 路径，破坏宪法/法律已经固定的 doc/dev-loop 分层。
- acceptance_hint: 创建 `has-skill.md`，明确：1) 它用于“已有可用 issue”；2) 它不替代 doc/dev-loop；3) 何时进入 `doc-loop-execution`，何时进入 `dev-loop-execution`；4) issue-bound brainstorm / story 目录 / milestone 回写的边界。
- priority: P0
- status: promoted
- decision_reason: 这是第二跳执行层里“有可用 issue”分支的标准工作法，也是最容易与 doc/dev-loop 混淆的一层，必须单独固化。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []


### C-20260306-1105
- title: `auto-loop-orchestrator` / guidance 对齐到两层 auto-loop 模型
- problem: 当前 `PROJECT_INTENT`、`auto-loop-orchestrator` 与本预研内部新增模型之间仍有断层，尚未显式说明 `lead-agent -> context-source -> no/has-skill -> doc/dev-loop` 这条实现链。
- why_now: 如果不把 guidance 和现有 orchestrator 一起对齐，后续实现会出现“脑中模型”和规范文案两套说法并存。
- acceptance_hint: 统一文档与 orchestrator 表述：1) 首跳由 `sh/ps1` 启动首个 AI 工具；2) 首个 AI 工具执行 `auto-loop-lead-agent.md`；3) `lead-agent` 调用 `context-source-skill.md` 生成第二跳指令；4) 第二跳再进入 `no-skill.md` / `has-skill.md`；5) `doc-loop-execution` / `dev-loop-execution` 继续保持正式领域工作流。
- priority: P0
- status: promoted
- decision_reason: 这是把本次预研结论真正接回宪法/法律/项目意图的收口项。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
