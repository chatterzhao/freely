# Candidates - 20260305-0000--freely-dogfooding-governance-worktree-policy

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260305-701
- title: Worktree Root Enforcer + Permission Preflight
- problem: 项目外 worktree 规则与运行权限未形成统一执行路径，导致重复提权。
- why_now: 是“外部同级目录强约束”可持续运行的前置条件。
- acceptance_hint: 强制 `{project-name}-worktrees` 命名与同级路径检查；提供一次性 preflight 结果与修复建议。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: worktree root enforcement 已实现；混合的 permission preflight 范围过宽，不适合作为旧候选继续 materialize。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `AGENTS.md`
  - `docs/system/workspace/skills/branch-management/references/feature-worktree-flow.md`
- session_refs: []

### C-20260305-702
- title: Hook Policy Template Compiler
- problem: hooks 逻辑散落脚本，难以复用和可视化维护。
- why_now: Freely 需要把自身治理能力产品化给用户项目。
- acceptance_hint: 以单一策略源生成 `.githooks/*`，支持审计与回滚。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 当前 canonical 设计已明确 hooks 真源与运行时投影，不需要再补抽象 compiler issue。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/system/workspace/hooks/README.md`
  - `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- session_refs: []

### C-20260305-703
- title: Governance UI for Hooks/Worktree Constraints
- problem: 用户无法在可视化界面维护 hook 与约束，运维门槛高。
- why_now: 进入用户化阶段前必须建立可配置、可审计入口。
- acceptance_hint: 提供治理面板，覆盖 hook 开关、worktree 根策略、违规处理策略。
- priority: P1
- status: needs_research
- decision_reason: 方向可能仍有价值，但当前没有 CLI-first 配置内核；不应直接 materialize 成 UI issue。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260306-workspace-routing-foundation
- next_action: 继续预研，先完成 CLI-first 配置内核后再考虑 UI 层。
- revisit_trigger: 当 CLI-first 配置内核稳定后需要可视化治理界面时，再推进到 IBM。
- session_refs: []

### C-20260305-704
- title: Freely Dogfooding Governance Contract
- problem: “Freely 开发 Freely”缺少显式契约，容易出现治理例外。
- why_now: 当前正处于方法论重构期，必须先锁定行为基线。
- acceptance_hint: 在 AGENTS/Constitution 固化 dogfooding 规则并纳入门禁清单。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: dogfooding 契约已经进入入口说明与宪法级约束。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `AGENTS.md`
  - `docs/CONSTITUTION.md`
- session_refs: []
