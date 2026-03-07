# Candidates - 20260306-0016--freely-githooks-install-mode

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260306-001
- title: Freely 托管 hooks 默认落在 `.freely/.githooks`
- problem: 如果直接把 hooks 装到 `.git/hooks`，Freely 难以稳定升级、审计和管理，也不利于前端展示当前治理状态。
- why_now: 这是 Freely 管理用户项目的基础治理能力，需要先定义默认托管模式。
- acceptance_hint: 明确 `.freely/.githooks` 为默认事实源，`core.hooksPath` 指向该目录，并说明升级覆盖边界。
- priority: P0
- status: promoted
- decision_reason: 是整个 hooks 产品化管理路径的基础前提。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

### C-20260306-002
- title: Hooks 托管模式前端开关与用户接管退出路径
- problem: 用户如果不满意 Freely 托管的 hooks，需要一个清晰、可逆、不会被升级覆盖的退出路径。
- why_now: 没有退出路径会让 hooks 治理显得侵入性过强，不利于用户接受。
- acceptance_hint: 前端开关支持切换到 `.git/hooks`；切换时提供复制指引或复制动作；进入用户接管模式后，Freely 停止自动覆盖。
- priority: P0
- status: promoted
- decision_reason: 直接关系到产品可接受性和长期维护边界。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
