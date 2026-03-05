# Candidates - 20260305-freely-dogfooding-governance-worktree-policy

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
- status: promoted
- decision_reason: 直接支撑隔离模型和可运维性，是当前重构主线刚需。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

### C-20260305-702
- title: Hook Policy Template Compiler
- problem: hooks 逻辑散落脚本，难以复用和可视化维护。
- why_now: Freely 需要把自身治理能力产品化给用户项目。
- acceptance_hint: 以单一策略源生成 `.githooks/*`，支持审计与回滚。
- priority: P0
- status: promoted
- decision_reason: 是“模板化分发治理策略”的核心实现点。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

### C-20260305-703
- title: Governance UI for Hooks/Worktree Constraints
- problem: 用户无法在可视化界面维护 hook 与约束，运维门槛高。
- why_now: 进入用户化阶段前必须建立可配置、可审计入口。
- acceptance_hint: 提供治理面板，覆盖 hook 开关、worktree 根策略、违规处理策略。
- priority: P1
- status: promoted
- decision_reason: 与长期产品体验强相关，但依赖 P0 策略内核先稳定。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

### C-20260305-704
- title: Freely Dogfooding Governance Contract
- problem: “Freely 开发 Freely”缺少显式契约，容易出现治理例外。
- why_now: 当前正处于方法论重构期，必须先锁定行为基线。
- acceptance_hint: 在 AGENTS/Constitution 固化 dogfooding 规则并纳入门禁清单。
- priority: P0
- status: promoted
- decision_reason: 是本轮统一设计理念对齐的起点约束。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
