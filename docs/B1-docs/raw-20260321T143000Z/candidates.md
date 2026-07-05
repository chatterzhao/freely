# Candidates - 20260321-1430--external-drift-and-out-of-band-reconcile

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260321T143000Z-A: legacy issue
- title: External drift and out-of-band reconcile governance
- problem: 仓库真实状态可能被 Freely 之外的动作推进，但 `.freely` 的 intake / continuity / worktree / runtime 视图仍停留在旧状态。主管缺少一条标准能力来检测“仓库现实已经越过 Freely 记录”并做 reconcile。
- why_now: 本轮狗粮开发已经真实出现这种情况。继续依赖人工判断会让 Freely 反复尝试续接已经收口的工作，或长期保留悬空 intake / continuity / worktree 状态。
- acceptance_hint:
  - 不新造平行大 skill，优先扩已有真源
  - 主承接应是 `manager-reactivation-and-fleet-patrol` / `skill:multi-worktree-supervision`
  - 发现后的写回与收口再分流到 `milestone-planning-state-maintenance` / `worktree-maintenance-governance` / runtime recovery
  - 不重复定义主管职责；沿用现有 `manager-agent` 边界，只新增 drift detection / explain / delegate / supervise-completion 检查面
  - 明确 drift 最小分类：
    - runtime drift
    - intake absorption drift
    - worktree cleanup drift
    - milestone/issue state drift
    - continuity stale drift
  - 明确主管发现 drift 后的最小 reconcile 动作
  - 至少落到现有 issue/skill/reference 之一，而不是停留在聊天建议
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 本轮研究结论已被吸收到新的 `manager-watchdog-trigger-and-drift-reconcile-governance` issue 中，后续以该 issue 生命周期为准，不再把本候选保留成平行推进线。
- next_action: 通过新的 issue 在主管巡检真源中落下 `external drift / out-of-band reconcile` 检查面，并保持本预研仅作为历史追溯输入。
- revisit_trigger: 若未来需要单独拆出 runtime-level drift detector，而不只是主管 patrol 语义增强，再重新开启新预研。
- promoted_issue_path: `docs/B2-docs/ibm/manager-watchdog-trigger-and-drift-reconcile-governance/issues/manager-watchdog-trigger-and-drift-reconcile-governance.md`
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- superseded_by:
  - `docs/B2-docs/ibm/manager-watchdog-trigger-and-drift-reconcile-governance/issues/manager-watchdog-trigger-and-drift-reconcile-governance.md`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
