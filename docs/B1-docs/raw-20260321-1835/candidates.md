# Candidates - 20260321-1835--lifecycle-complete-before-merge-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260321-1835-A: legacy issue
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
- status: promoted
- decision_reason: 2026-03-27 的真实 develop merge replay 证明，这条候选不只是 supporting evidence，而是缺少独立 owner issue 的 active merge gate 缺口；必须 materialize 成 issue-bound C/M/I enforcement，才能把 “issue binding + C/M/I coherence + allowed statuses” 冻结成 develop gate。
- next_action: 在 `I-20260321-1835-A` 中收紧 develop merge gate，要求 merge 绑定具体 issue，并确保 touched candidate 与 touched owner issue 处在同一条 C/M/I 线上。
- revisit_trigger: 若后续仍出现 candidate-only merge、borrowed owner issue、或 allowed status 误判放行，则在本 issue 线继续追加 regression。
- promoted_issue_id: I-20260321-1835-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260321-1835-A/issue.md
- milestone: M-20260321-1835-A
- supporting_evidence: 2026-03-27 dogfood replay 确认 `pre-merge-commit` hook 虽已触发，但因为错误依赖 `MERGE_HEAD` 守卫而放过了 develop-bound runtime/test merge；修复方向应改为直接审查 staged merge 结果，并以真实 `git merge` 回归测试钉住该时序。
- supporting_evidence: 同轮继续确认 `absorbed` 候选当前被判得过宽，只要 `promoted_issue_path` 指向某个现存 owner issue 就足以放行 develop merge；后续 gate 应先要求“本次 merge 基于一个具体 issue”，再验证该 issue 的 `C/M/I` 链与允许状态，而不是让 candidate-only supporting evidence 直接成为通行证。
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
