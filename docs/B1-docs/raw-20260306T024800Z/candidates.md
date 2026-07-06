# Candidates - 20260306-0248--issue-brainstorm-routing-guard

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_review

## Convergence

- 最终工作产物应收敛为：
  - 1 个首跳中枢代理：`lead-agent.md`
  - 1 个来源适配与上下文判定 skill：`context-source-skill.md`
  - 3 个领域执行 skills：`doc-pre-brainstorm-execution.md`、`doc-ibm-execution.md`、`dev-loop-execution.md`
  - 1 个现有 `auto-loop-orchestrator` skill 对齐项
- 主链应显式对齐为：
  `sh/ps1 -> external AI CLI tool -> lead-agent -> context-source-skill -> doc-pre-brainstorm-execution | doc-ibm-execution | dev-loop-execution`
- 产物类型只分为 `agent` 与 `skill`
- 命名不再使用 loop 前缀；名称表达职责，目录表达归属，元数据表达可调用范围
- `docs/system/workspace/` 统一暴露 Freely 能力；`bin/`、`.githooks/` 视为运行时落点
- 正式落点路径：
  - `docs/system/workspace/agents/lead-agent.md`
  - `docs/system/workspace/skills/context-source-skill/SKILL.md`
  - `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
  - `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
  - `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
  - `docs/system/workspace/scripts/` 定义 `sh` / `ps1` 启动与编排脚本
  - `docs/system/workspace/hooks/` 定义 hook 规范或模板；`.githooks/` 作为安装产物
- 当前先不把 hook/script 放回主收敛；先把首段闭环主链和 `lead-agent/context-source-skill/pre-brainstorm/doc/dev` 这组核心能力写清。

## Candidates

### C-20260306T024800Z-A: legacy issue
- title: `lead-agent.md`
- problem: 当前还缺少一个明确的首跳 AI 中枢代理说明，定义从 `sh/ps1` 启动外部 AI CLI 工具后，到底由谁承担首段闭环编排职责。
- why_now: 如果没有 `lead-agent` 这一层，启动器、来源适配、usable issue 判定和第二跳 skill 会继续混在一起，无法形成统一主链。
- acceptance_hint: 创建 `docs/system/workspace/agents/lead-agent.md`，明确：1) 它由启动后的外部 AI CLI 工具执行；2) 它位于 `sh/ps1` 与 `context-source-skill` 之间；3) 它负责首跳接管、治理前置与委托，不负责自己扫描需求池；4) 它负责调用后续 skill，而不是内嵌所有来源判定细节；5) 它不替代 `doc-ibm-execution` / `dev-loop-execution`。
- priority: P0
- status: promoted
- decision_reason: 这是两层 auto-loop 机制的中枢；本轮纠偏后已明确它是“首跳接管与委托者”，而不是需求池扫描器。
- promoted_issue_path: `docs/B2-docs/ibm/bootstrap-routing-foundation-artifacts/raw-20260306-1101issues/lead-agent-bootstrap.md`
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs: []

### C-20260306T024800Z-A: legacy issue
- title: `context-source-skill.md`
- problem: 当前缺少一个供 `lead-agent` 使用的来源适配与上下文判定规则文件，无法稳定把 `<source input>` 转换成 usable issue 判断和下一跳分支编排决策。
- why_now: 首跳不是直接执行业务工作，而是先做来源适配、上下文识别和基于来源的编排；如果没有这一层，首跳 AI 只能重新自由发挥。
- acceptance_hint: 创建 `docs/system/workspace/skills/context-source-skill/SKILL.md`，明确：1) 它负责扫描 `milestone/progress/recovery/review/test/chat/github-issue/intent` 需求池；2) AI 应在此 skill 下自主判断来源优先级，而不是由脚本硬编码；3) 如何做 usable issue 与 issue 边界判定；4) 如何区分 `pre-brainstorm`、`issue-bound brainstorm`、`issue continuation`；5) 如何结合任务强度、工具优先级、工具可用性列表选工具；6) 不把 doc/dev-loop 细节塞到该 skill。
- priority: P0
- status: promoted
- decision_reason: 这是 `lead-agent` 的核心依赖文件，也是两层模型里真正承载“找活、解释上下文、决定下一跳”的一层。
- promoted_issue_path: `docs/B2-docs/ibm/bootstrap-routing-foundation-artifacts/raw-20260306-1101issues/context-source-skill-bootstrap.md`
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs: []

### C-20260306T024800Z-A: legacy issue
- title: `doc-pre-brainstorm-execution.md`
- problem: 当前缺少一个真正按“工作能力”命名的 pre-brainstorm 执行 skill，导致“没有 usable issue”这种路由条件被误建模成技能本体。
- why_now: `pre-brainstorm` 是独立的文档工作环，不只是路由结果；如果不把它抽成正式执行 skill，`context-source-skill` 与中间 handoff skill 会继续重叠。
- acceptance_hint: 创建 `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`，明确：1) 它属于 docs 工作的一种前置形态；2) 负责前置研究收敛；3) 产出 `docs/B1-docs/raw-<id>/brainstorms.md` 与 `candidates.md`；4) candidate 必须原子同步进 `docs/milestones.md`；5) 它不产出正式 issue-bound `brainstorms/prd/pre-tests/tasks`。
- priority: P0
- status: promoted
- decision_reason: `pre-brainstorm` 本身是独立执行环；用“没 issue”来命名 skill 会把路由条件和工作能力混在一起。
- promoted_issue_path: `docs/B2-docs/ibm/bootstrap-routing-foundation-artifacts/raw-20260306-1101issues/doc-pre-brainstorm-execution-bootstrap.md`
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs: []


### C-20260306T024800Z-A: legacy issue
- title: `doc-ibm-execution.md` 与 `dev-loop-execution.md` 的外循环接驳边界
- problem: 当前 issue-bound 文档环与开发环的接驳边界还不够硬，容易被中间层 handoff 设计重复描述，侵入正式 loop 职责。
- why_now: `doc-loop` 与 `dev-loop` 是宪法/法律已经固定的正式内循环；外循环应该编排它们，而不是再造一层“有 issue skill”去部分重复它们。
- acceptance_hint: 收紧 `docs/system/workspace/skills/doc-ibm-execution/SKILL.md` 与 `docs/system/workspace/skills/dev-loop-execution/SKILL.md` 的外循环接驳说明，明确：1) `context-source-skill` 负责决定进哪个环；2) `doc-ibm-execution` 负责 issue-bound `IBM+G` 与里程碑同步；3) `dev-loop-execution` 负责 `DDD`、测试、progress/milestone 回写；4) 两者的状态交换、阻塞、完成结果要回流给 `auto-loop`。
- priority: P0
- status: promoted
- decision_reason: 真正稳定的执行能力应该直接是 `doc-ibm-execution` 和 `dev-loop-execution`；“有 usable issue”只是路由判定，不该长期存在为独立 skill。
- promoted_issue_path: `docs/B2-docs/ibm/bootstrap-routing-foundation-artifacts/raw-20260306-1101issues/doc-loop-dev-loop-handoff-bootstrap.md`
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs: []


### C-20260306T024800Z-A: legacy issue
- title: 现有 `auto-loop-orchestrator` skill 对齐到首段闭环模型
- problem: 当前 `PROJECT_INTENT` 与现有 `auto-loop-orchestrator` skill 之间仍有断层，尚未显式说明 `sh/ps1 -> external AI CLI tool -> lead-agent -> context-source-skill -> pre-brainstorm/doc-loop/dev-loop` 这条实现链。
- why_now: 如果不把现有 orchestrator skill 一起对齐，后续实现会出现“脑中模型”和规范文案两套说法并存。
- acceptance_hint: 更新 `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`：1) 首跳由 `system/workspace/scripts` 中定义的 `sh` / `ps1` 启动外部 AI CLI 工具；2) AI CLI 工具进入 `docs/system/workspace/agents/lead-agent.md`；3) `lead-agent` 调用 `context-source-skill`；4) `context-source-skill` 直接编排进入 `doc-pre-brainstorm-execution`、`doc-ibm-execution` 或 `dev-loop-execution`；5) 各 loop skill 的状态交换、阻塞、完成结果回流给 `auto-loop`；6) hook 定义源位于 `system/workspace/hooks`，`.githooks/` 作为安装产物。
- priority: P0
- status: promoted
- decision_reason: 这是把本次预研结论真正接回现有 orchestrator skill 与项目意图的收口项。
- promoted_issue_path: `docs/B2-docs/ibm/bootstrap-routing-foundation-artifacts/raw-20260306-1101issues/auto-loop-orchestrator-bootstrap.md`
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs: []
