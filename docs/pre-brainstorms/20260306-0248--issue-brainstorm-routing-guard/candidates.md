# Candidates - 20260306-0248--issue-brainstorm-routing-guard

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_review

## Convergence

- 最终工作产物应收敛为：
  - 1 个首跳中枢代理：`lead-agent.md`
  - 1 个来源适配与上下文判定 skill：`context-source-skill.md`
  - 2 个第二跳 workflow skills：`no-usable-issue-skill.md`、`has-usable-issue-skill.md`
  - 1 个现有 `auto-loop-orchestrator` skill 对齐项
- 主链应显式对齐为：
  `sh/ps1 -> external AI CLI tool -> lead-agent -> context-source-skill -> usable-issue decision -> no-usable-issue-skill | has-usable-issue-skill -> doc-loop(IBM+G) | dev-loop(DDD)`
- 产物类型只分为 `agent` 与 `skill`
- 命名不再使用 loop 前缀；名称表达职责，目录表达归属，元数据表达可调用范围
- `docs/system/workspace/` 统一暴露 Freely 能力；`bin/`、`.githooks/` 视为运行时落点
- 正式落点路径：
  - `docs/system/workspace/agents/lead-agent.md`
  - `docs/system/workspace/skills/context-source-skill/SKILL.md`
  - `docs/system/workspace/skills/no-usable-issue-skill/SKILL.md`
  - `docs/system/workspace/skills/has-usable-issue-skill/SKILL.md`
  - `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
  - `docs/system/workspace/scripts/` 定义 `sh` / `ps1` 启动与编排脚本
  - `docs/system/workspace/hooks/` 定义 hook 规范或模板；`.githooks/` 作为安装产物
- 当前先不把 hook/script 放回主收敛；先把首段闭环主链和 4 个文档型产物写清。

## Candidates

### C-20260306-1101
- title: `lead-agent.md`
- problem: 当前还缺少一个明确的首跳 AI 中枢代理说明，定义从 `sh/ps1` 启动外部 AI CLI 工具后，到底由谁承担首段闭环编排职责。
- why_now: 如果没有 `lead-agent` 这一层，启动器、来源适配、usable issue 判定和第二跳 skill 会继续混在一起，无法形成统一主链。
- acceptance_hint: 创建 `docs/system/workspace/agents/lead-agent.md`，明确：1) 它由启动后的外部 AI CLI 工具执行；2) 它位于 `sh/ps1` 与 `context-source-skill` 之间；3) 它负责首跳接管、治理前置与委托，不负责自己扫描需求池；4) 它负责调用后续 skill，而不是内嵌所有来源判定细节；5) 它不替代 `doc-loop-execution` / `dev-loop-execution`。
- priority: P0
- status: promoted
- decision_reason: 这是两层 auto-loop 机制的中枢；本轮纠偏后已明确它是“首跳接管与委托者”，而不是需求池扫描器。
- promoted_issue_path: pending://issue-materialization
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs: []

### C-20260306-1102
- title: `context-source-skill.md`
- problem: 当前缺少一个供 `lead-agent` 使用的来源适配与上下文判定规则文件，无法稳定把 `<source input>` 转换成 usable issue 判断和下一跳分支编排决策。
- why_now: 首跳不是直接执行业务工作，而是先做来源适配、上下文识别和基于来源的编排；如果没有这一层，首跳 AI 只能重新自由发挥。
- acceptance_hint: 创建 `docs/system/workspace/skills/context-source-skill/SKILL.md`，明确：1) 它负责扫描 `milestone/progress/recovery/review/test/chat/github-issue/intent` 需求池；2) AI 应在此 skill 下自主判断来源优先级，而不是由脚本硬编码；3) 如何做 usable issue 与 issue 边界判定；4) 如何区分 `pre-brainstorm`、`issue-bound brainstorm`、`issue continuation`；5) 如何结合任务强度、工具优先级、工具可用性列表选工具；6) 不把 doc/dev-loop 细节塞到该 skill。
- priority: P0
- status: promoted
- decision_reason: 这是 `lead-agent` 的核心依赖文件，也是两层模型里真正承载“找活、解释上下文、决定下一跳”的一层。
- promoted_issue_path: pending://issue-materialization
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs: []

### C-20260306-1103
- title: `no-usable-issue-skill.md`
- problem: 当前没有一个正式的第二跳执行指南，指导“没有 usable issue”时如何继续前置研究、如何写 `pre-brainstorms` 产物、以及如何同步 milestone。
- why_now: 这是下游 AI 命中“无可用 issue”时的唯一标准工作入口；如果不先固化，仍会退回口头解释。
- acceptance_hint: 创建 `docs/system/workspace/skills/no-usable-issue-skill/SKILL.md`，明确：1) 无稳定 issue 边界时继续停留 `pre-brainstorms`；2) 如何产出 `brainstorms.md` / `candidates.md`；3) 如何将 candidate 原子同步进 milestone；4) milestone 绑定后如何回写 candidate 状态；5) 它不承载执行态，只负责把问题收敛到 candidate + milestone。
- priority: P0
- status: promoted
- decision_reason: 这是第二跳执行层里“无可用 issue/无稳定边界”分支的标准工作法，负责 pre-brainstorm -> candidate -> milestone 的闭环。
- promoted_issue_path: pending://issue-materialization
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs: []


### C-20260306-1104
- title: `has-usable-issue-skill.md`
- problem: 当前没有一个正式的第二跳执行指南，指导“已经命中 usable issue”时如何进一步进入正式 issue 工作流，以及何时应调用 `doc-loop-execution` 或 `dev-loop-execution`。
- why_now: 如果这一层不写清，最容易把“已有 usable issue”误实现成固定 doc-loop 路径，破坏宪法/法律已经固定的 doc/dev-loop 分层。
- acceptance_hint: 创建 `docs/system/workspace/skills/has-usable-issue-skill/SKILL.md`，明确：1) 它用于“已有稳定 issue 边界”；2) 它不替代 doc/dev-loop；3) 何时进入 issue-bound IBM 的 `B/M`，何时进入 `dev-loop-execution`；4) test/review/chat 等来源命中后应先重做边界判定，再决定是 issue-bound brainstorm 还是 continuation；5) issue-bound brainstorm / story 目录 / milestone 回写的边界。
- priority: P0
- status: promoted
- decision_reason: 这是第二跳执行层里“有可用 issue”分支的标准工作法；本轮纠偏后已明确它是正式 issue 工作流入口，而不是“直接开发”快捷路径。
- promoted_issue_path: pending://issue-materialization
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs: []


### C-20260306-1105
- title: 现有 `auto-loop-orchestrator` skill 对齐到首段闭环模型
- problem: 当前 `PROJECT_INTENT` 与现有 `auto-loop-orchestrator` skill 之间仍有断层，尚未显式说明 `sh/ps1 -> external AI CLI tool -> lead-agent -> context-source-skill -> no/has-usable-issue-skill -> doc/dev-loop` 这条实现链。
- why_now: 如果不把现有 orchestrator skill 一起对齐，后续实现会出现“脑中模型”和规范文案两套说法并存。
- acceptance_hint: 更新 `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`：1) 首跳由 `system/workspace/scripts` 中定义的 `sh` / `ps1` 启动外部 AI CLI 工具；2) AI CLI 工具进入 `docs/system/workspace/agents/lead-agent.md`；3) `lead-agent` 调用 `context-source-skill`；4) `context-source-skill` 产出下一跳决策并进入 `no-usable-issue-skill` / `has-usable-issue-skill`；5) `doc-loop-execution` / `dev-loop-execution` 继续保持正式领域工作流；6) hook 定义源位于 `system/workspace/hooks`，`.githooks/` 作为安装产物。
- priority: P0
- status: promoted
- decision_reason: 这是把本次预研结论真正接回现有 orchestrator skill 与项目意图的收口项。
- promoted_issue_path: pending://issue-materialization
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs: []
