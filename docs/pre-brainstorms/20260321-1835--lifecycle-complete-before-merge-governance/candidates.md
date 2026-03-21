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
- status: proposed
- decision_reason: 这是 Freely 用 Freely 自举时直接暴露的治理缺口，而且会影响所有后续 worktree 的 promote/cleanup 判断，值得先作为能力缺口固定。
- next_action: 判断它应作为对现有 worktree/lifecycle 真源的增强来 materialize，而不是新增平行 merge skill。
- revisit_trigger: 当 merge readiness、research closure 与 lifecycle closure 的关系能被稳定写成统一 gate wording 时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
