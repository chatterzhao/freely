# Candidates - 20260321-1430--external-drift-and-out-of-band-reconcile

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260321-1430-A
- title: External drift and out-of-band reconcile governance
- problem: 仓库真实状态可能被 Freely 之外的动作推进，但 `.freely` 的 intake / continuity / worktree / runtime 视图仍停留在旧状态。主管缺少一条标准能力来检测“仓库现实已经越过 Freely 记录”并做 reconcile。
- why_now: 本轮狗粮开发已经真实出现这种情况。继续依赖人工判断会让 Freely 反复尝试续接已经收口的工作，或长期保留悬空 intake / continuity / worktree 状态。
- acceptance_hint:
  - 不新造平行大 skill，优先扩已有真源
  - 主承接应是 `manager-reactivation-and-fleet-patrol` / `skill:multi-worktree-supervision`
  - 发现后的写回与收口再分流到 `milestone-planning-state-maintenance` / `worktree-maintenance-governance` / runtime recovery
  - 明确 drift 最小分类：
    - runtime drift
    - intake absorption drift
    - worktree cleanup drift
    - milestone/issue state drift
    - continuity stale drift
  - 明确主管发现 drift 后的最小 reconcile 动作
  - 至少落到现有 issue/skill/reference 之一，而不是停留在聊天建议
- priority: P0
- status: proposed
- decision_reason: 问题已真实出现，且当前预研已收敛出承接边界：它首先是主管 patrol / project-level supervision 能力，其次才分流到 state-maintenance、worktree closure 或 runtime recovery；因此应扩现有 `manager-reactivation-and-fleet-patrol` 与 `skill:multi-worktree-supervision`，而不是新造平行 skill。
- next_action: materialize 为对现有 `manager-reactivation-and-fleet-patrol` issue 与 `skill:multi-worktree-supervision` 的增强，并补 drift detection / ownership / reconcile routing 的 reference。
- revisit_trigger: 当需要把 drift classification、routing 和 writeback contract 正式落到 issue / skill / tests 时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
