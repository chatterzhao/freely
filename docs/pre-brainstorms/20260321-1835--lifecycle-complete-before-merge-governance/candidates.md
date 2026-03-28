# Candidates - 20260321-1835--lifecycle-complete-before-merge-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260321-1835-A
- title: Require lifecycle closure before merge and distinguish research closure
- problem: 当前 worktree 治理已有 merge/cleanup/retirement 能力，但还缺少一条更硬的 merge gate：实现型 worktree 必须 lifecycle complete 后才能 merge；而纯研究线若结论是 `needs_research` / `dropped` / `superseded`，应允许按研究 closure 收口，而不是被错误要求走完实现链。
- why_now: 本轮在推进 active branch 时已经出现“是否可以在 issue 仍处于活跃生命周期时向上合并”的判断摇摆。如果不固定，后续会持续把“实现差不多了”误当成“可以合并了”。
- why_now: 本轮真实 `freely start + chat` 集成测试进一步证明，即使主管能被拉起并接住插话，也可能把新的项目级监督任务错误吸收到旧 cleanup continuity。若不把 lifecycle closure gate 收敛为更硬的主管判断，后续仍会把“能跑起来”误当成“可以合并了”。
- acceptance_hint:
  - 明确 merge gate 取决于 lifecycle closure，而不是实现完成感
  - 明确研究型 closure 与实现型 closure 的不同
  - 明确主管负责这层 gate，worker 不直接决定 promote
  - 明确真实集成测试下，新 signal 不得被旧 continuity 错误吸收后直接推进 merge/cleanup
  - 落点优先放在 `three-loop-capability-lifecycle`、`worktree-maintenance-governance`、`milestone-planning-state-maintenance`
- priority: P0
- status: absorbed
- adoption_type: supporting_evidence
- decision_reason: lifecycle closure、research closure 与 terminal retirement judgement 已由 `I-20260324-0405` 和现有 worktree maintenance truth 显式吸收，这条候选不再需要独立 materialization。
- next_action: 后续若出现新的 merge-before-closure 漏洞，应围绕新的 gate regression 新开 lifecycle，而不是重开本候选。
- revisit_trigger: canonical truth 再次把“实现差不多了”误当成“可以 merge / cleanup”时。
- promoted_issue_path: docs/epics/workspace-routing-foundation/three-loops-sibling-relationship-and-terminal-governance/issues/three-loops-sibling-relationship-and-terminal-governance.md
- milestone: M-20260306-workspace-routing-foundation
- supporting_evidence: 2026-03-27 dogfood replay 确认 `pre-merge-commit` hook 虽已触发，但因为错误依赖 `MERGE_HEAD` 守卫而放过了 develop-bound runtime/test merge；修复方向应改为直接审查 staged merge 结果，并以真实 `git merge` 回归测试钉住该时序。
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
