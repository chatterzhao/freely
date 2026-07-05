# Candidates - 20260321-0257--worktree-fleet-governance-closure

## Context
- Source brainstorm: ./brainstorms.md
- Status: promoted

## Candidates

### C-20260321-0257-A
- title: Worktree fleet governance closure mode
- problem: Freely 当前已经有 worktree 维护技能，但还缺项目级 fleet closure 模式，无法系统性核对“所有 worktree 的 pre-brainstorm / candidate / milestone / issue / review / tests / git ancestry / cleanup 状态是否闭环”，也无法稳定执行“沿父链逐级向上 merge 到 develop，再 cleanup”的治理流程。
- why_now: 当前仓库同时存在 research、implementation、merge-prep、governance 和 stacked parent-child worktree；继续靠人工经验做 closure，已经暴露出冲突标记残留、候选生命周期未闭环、以及需要逐级 merge 的链路判断。
- acceptance_hint:
  - 扩展 `skill:worktree-maintenance-governance`，新增项目级 fleet closure 模式
  - 明确每棵 worktree 的最小核查面：candidate、milestone、issue lifecycle、tests、git ancestry、cleanup readiness
  - 明确对 parent-child 依赖链执行 `child -> parent -> merge-prep-from-develop -> develop`
  - 明确只有 `verified-retirable` 才能 cleanup
  - 至少有一条 skill / prompt / test 级证据，保证未来 Freely 能按此流程执行
- priority: P0
- status: promoted
- decision_reason: 这是通过狗粮开发直接发现的治理缺口。现在不收编成 skill，后续每次大批量 worktree 收口都会重复踩同一类问题。
- promoted_issue_path: docs/B2-docs/git-worktree/worktree-fleet-governance-closure/issues/worktree-fleet-governance-closure.md
- legacy_id_mapping: I-20260321-0257  # 历史遗留的 issue id
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
