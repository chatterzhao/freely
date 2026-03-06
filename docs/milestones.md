# Milestones

本文件是 Freely 自举开发时的主动扫描入口，用来承接已进入活跃范围的 candidate / issue。

## Milestone Policy

milestone_status_policy_version: v1

candidate_policy:
- dropped: remove from active milestone queues
- needs_research: keep in candidate_issues and route back to pre-brainstorms or issue-bound brainstorm
- promoted: bind to a milestone immediately; do not leave as long-term unbound state
- in_progress: must stay visible in milestone and matching progress evidence
- blocked: keep visible with blocker and next action

queue_policy:
- committed_issues: sequencing is clear and the item is the next active batch
- candidate_issues: belongs to the milestone, but still needs research or ordering
- completed_issues: delivered work kept for traceability within the same milestone

sequencing_policy:
- ordered_by: dependency_then_control_plane
- allow_unordered_candidates: true

routing_policy:
- no_issue_path: stay in pre-brainstorms or continue doc-loop materialization
- issue_path_present: route by issue status into issue-bound brainstorm, IBM, continuation, or completion verification

## M-20260306-workspace-routing-foundation

- title: Workspace routing foundation for Freely dogfooding
- status: active
- source_brainstorm: `docs/pre-brainstorms/20260306-0248--issue-brainstorm-routing-guard/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260306-0248--issue-brainstorm-routing-guard/candidates.md`
- intent: 把首跳路由治理候选正式纳入 milestone，避免 Freely 自己继续依赖悬空 candidate 工作
- why_now: 这批项定义 Freely 如何发现上下文、读取 milestone、并路由到下一跳 skill；如果 milestone 自身不先落盘，Freely 的狗粮链路就是断的

### committed_issues

- none currently

### candidate_issues

- none currently

### completed_issues

1. `C-20260306-1101`
- title: `lead-agent.md`
- milestone_state: completed
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- evidence: `docs/system/workspace/agents/lead-agent.md`
- completion_note: 已落地首跳中枢代理职责与首跳协议

2. `C-20260306-1102`
- title: `context-source-skill.md`
- milestone_state: completed
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- evidence: `docs/system/workspace/skills/context-source-skill/SKILL.md`
- completion_note: 已落地来源判定、milestone 扫描与 usable issue 决策规则

3. `C-20260306-1103`
- title: `no-usable-issue-skill.md`
- milestone_state: completed
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- evidence: `docs/system/workspace/skills/no-usable-issue-skill/SKILL.md`
- completion_note: 已落地 pre-brainstorm 收敛与 milestone 原子同步规则

4. `C-20260306-1104`
- title: `has-usable-issue-skill.md`
- milestone_state: completed
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- evidence: `docs/system/workspace/skills/has-usable-issue-skill/SKILL.md`
- completion_note: 已落地 usable issue 到 doc/dev-loop 的分流边界

5. `C-20260306-1105`
- title: 现有 `auto-loop-orchestrator` skill 对齐到首段闭环模型
- milestone_state: completed
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- evidence: commit `00fd970`, `docs/system/workspace/scripts/`, `docs/system/workspace/hooks/`, `bin/test-routing-foundation-loop`
- completion_note: 已把 `system/workspace` 真源、`scripts` / `hooks` 与运行时落点映射写回现有 orchestrator skill、补齐脚本与 hook 定义源，并提供最小闭环测试
