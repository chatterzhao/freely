# Candidates - 20260304-0000--research-redo-owner-tool-alignment

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260304-601
- title: Owner Loop Contract
- problem: 外循环状态机尚未固化为契约。
- why_now: 是 AI 自治闭环可执行的核心。
- acceptance_hint: 定义发现/路由/执行/恢复/回流状态与输入输出。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: Owner loop 契约已由现有 auto-loop、lead-agent 与三层循环真源吸收。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
  - `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- session_refs: []

### C-20260304-602
- title: Gate Contract
- problem: 门禁点已分散存在，缺少统一契约。
- why_now: 没有统一门禁会导致回归与质量漂移。
- acceptance_hint: 定义 Ring/SSOT/验收/集成测试/独立监理 Gate。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 门禁契约已被现行法律执行与状态同步治理吸收。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/system/workspace/skills/laws-enforcer/SKILL.md`
  - `docs/B2-docs/ibm/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- session_refs: []

### C-20260304-603
- title: Recovery Contract
- problem: 续接与桥接恢复规则缺少结构化协议。
- why_now: 自治运行稳定性取决于恢复机制。
- acceptance_hint: 明确触发条件、写回字段、重启策略。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 恢复契约已由 session lifecycle 与 watchdog 真源吸收。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/B2-docs/ibm/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
  - `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- session_refs: []

### C-20260304-604
- title: Issue Discovery + Router 内核实现
- problem: 发现与路由能力仍停留在文档层，未形成可执行内核。
- why_now: 是 ADD 外循环稳定运行的前置能力。
- acceptance_hint: 覆盖意图/review/test/chat/github/milestone/progress 的发现与分流规则执行。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 发现与路由内核已由 source-routing 与 context-source 真源承接。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/B2-docs/ibm/source-routing-and-derived-worktree-governance/issues/source-routing-and-derived-worktree-governance.md`
  - `docs/system/workspace/skills/context-source-skill/SKILL.md`
- session_refs: []

### C-20260304-605
- title: Sub-agent 批次编排器
- problem: 并行委托约束已在宪法定义，但缺少可执行编排模块。
- why_now: 关系到吞吐、等待语义与失败回退的稳定性。
- acceptance_hint: 落地批次等待、失败回退、审计记录与最大并发策略。
- priority: P1
- status: needs_research
- decision_reason: 方向重要但需先明确当前阶段并发范围与最小可行边界。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260306-workspace-routing-foundation
- next_action: 继续预研，确定 sub-agent 批次编排的最小边界后再决定是否 materialize。
- revisit_trigger: 当 Freely 需要支持并行委托时，再推进到 IBM。
- session_refs: []

### C-20260304-606
- title: Promotion & Cleanup Enforcer
- problem: 分支提升链与分支/worktree清理尚未形成统一执行器。
- why_now: 宪法对提升与清理有硬约束，需系统化执行避免治理漂移。
- acceptance_hint: 自动校验 `feature -> pre-develop -> develop` 与合并后清理动作记录。
- priority: P1
- status: dropped
- adoption_type: superseded
- decision_reason: promotion 与 cleanup 已由 worktree-maintenance-governance 主线吸收。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/B2-docs/git-worktree/worktree-maintenance-governance/issues/worktree-maintenance-governance.md`
  - `docs/system/workspace/skills/branch-management/SKILL.md`
- session_refs: []

### C-20260304-607
- title: Doc Contract Compiler
- problem: Story 验收标准尚未编译为可执行检查项，门禁难以自动化执行。
- why_now: 是从“文档约束”走向“机器可执行门禁”的关键转换点。
- acceptance_hint: 将验收项映射为检查任务，并接入集成测试门禁与放行流程。
- priority: P0
- status: absorbed
- adoption_type: supporting_evidence
- decision_reason: issue-level acceptance、pre-tests executable contract 与相关 checklist/gate 已被后续 IBM acceptance 真源吸收，这条旧候选不再需要独立 materialization。
- promoted_issue_path: docs/B2-docs/ibm/ibm-pretests-executable-acceptance-quality-governance/issues/ibm-pretests-executable-acceptance-quality-governance.md
- milestone: M-20260306-workspace-routing-foundation
- session_refs: []
