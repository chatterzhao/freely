# Candidates - 20260306-0113--standard-worktree-prompts-and-fallback-boundary

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260306-0113-A: legacy issue
- title: 标准 `git worktree` 提示统一
- problem: 规范入口和 hook 提示仍混有 helper 心智、抽象占位符或不可移植路径，导致用户与 AI 更难形成统一的标准 worktree 心智。
- why_now: `test-pre-merge-*` 临时测试批次语义收紧后，开发主路径已经回到 `develop`；此时必须同步把创建 feature worktree 的用户提示收敛为行业通用写法。
- acceptance_hint: 所有规范入口统一以 `cd <your-project-name-path>` + `git worktree add -b ... ../<your-project-name>-worktrees/... develop` 为主路径；helper 退居辅助；hook 仅承担兜底提示。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 标准 worktree 提示已统一到 hooks、AGENTS 和 branch-management reference。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `AGENTS.md`
  - `docs/system/workspace/skills/branch-management/references/feature-worktree-flow.md`
- session_refs: []
