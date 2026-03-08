# Milestones

本文件是 Freely 自举开发时的主动扫描入口，用来承接已进入活跃范围的 candidate / issue。

## Milestone Policy

milestone_status_policy_version: v2

candidate_policy:
- dropped: remove from active milestone queues
- needs_research: keep in candidate_issues and route back to pre-brainstorms or issue-bound brainstorm
- promoted: bind to a milestone immediately; do not leave as long-term unbound state
- blocked: keep visible with blocker and next action

queue_policy:
- committed_issues: sequencing is clear and the item is the next active batch
- candidate_issues: belongs to the milestone, but still needs research or ordering
- completed_issues: delivered work kept for traceability within the same milestone

phase_state_policy:
- `phase_state=in_ibm`: keep the issue visible in `committed_issues` with `issue_path` and `next_action`; do not require `progress`
- `phase_state=done_ibm`: keep the issue visible in `committed_issues` with `issue_path` and a clear handoff into dev-loop
- `phase_state=in_dev`: keep the issue visible in `committed_issues` and require matching `progress`
- `phase_state=blocked_dev`: keep the issue visible with blocker, next action, and current execution context
- `phase_state=in_verification`: keep the issue visible until completion evidence is written back
- `phase_state=completed`: move the issue to `completed_issues` with evidence

session_policy:
- full `session_refs` live in candidate / issue / progress / recovery artifacts
- milestone may keep `active_session_ref` as a summary, but `issue_path` is the canonical detail pointer

sequencing_policy:
- ordered_by: dependency_then_control_plane
- allow_unordered_candidates: true

routing_policy:
- no_issue_path: stay in pre-brainstorms or continue doc-loop materialization
- issue_path_present: route by `phase_state` into issue-bound brainstorm, IBM, continuation, dev-loop, or completion verification

## M-20260306-workspace-routing-foundation

- title: Workspace routing foundation for Freely dogfooding
- status: active
- source_brainstorm: `docs/pre-brainstorms/20260306-0248--issue-brainstorm-routing-guard/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260306-0248--issue-brainstorm-routing-guard/candidates.md`
- intent: 把首跳路由治理候选正式纳入 milestone，避免 Freely 自己继续依赖悬空 candidate 工作
- why_now: 这批项定义 Freely 如何发现上下文、读取 milestone、并路由到下一跳 skill；如果 milestone 自身不先落盘，Freely 的狗粮链路就是断的

### committed_issues

1. `I-20260307-1201`
- title: 源分类、milestone-owned issue 与派生 worktree 路由治理
- milestone_state: committed
- phase_state: `in_ibm`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/issues/source-routing-and-derived-worktree-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/candidates.md`
- next_action: 继续在 IBM 环内校准状态联动口径，并在 issue 完成 `done_ibm` handoff 后再推进 dev-loop

2. `I-20260308-0101`
- title: 状态联动、流程标识词典与 session evidence 传播治理
- milestone_state: committed
- phase_state: `in_ibm`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/candidates.md`
- next_action: 在治理文档与 skills 中统一流程标识词典、状态联动矩阵与 session evidence 传播规则

### candidate_issues

- none currently

### completed_issues

1. `C-20260306-1101`
- title: `lead-agent.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/lead-agent-bootstrap.md`
- evidence: `docs/system/workspace/agents/lead-agent.md`
- completion_note: 已落地首跳中枢代理职责与首跳协议

2. `C-20260306-1102`
- title: `context-source-skill.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/context-source-skill-bootstrap.md`
- evidence: `docs/system/workspace/skills/context-source-skill/SKILL.md`
- completion_note: 已落地来源判定、milestone 扫描与 usable issue 决策规则

3. `C-20260306-1103`
- title: `doc-pre-brainstorm-execution.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/doc-pre-brainstorm-execution-bootstrap.md`
- evidence: `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
- completion_note: 已落地 docs 前置收敛环，负责 pre-brainstorm 产物与 milestone 原子同步

4. `C-20260306-1104`
- title: `doc-ibm-execution.md` 与 `dev-loop-execution.md` 的外循环接驳边界
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/doc-loop-dev-loop-handoff-bootstrap.md`
- evidence: `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`, `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
- completion_note: 已收紧 issue-bound `IBM+G` 与 `DDD` 的接驳边界，状态交换统一回流给 auto-loop

5. `C-20260306-1105`
- title: 现有 `auto-loop-orchestrator` skill 对齐到首段闭环模型
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/auto-loop-orchestrator-bootstrap.md`
- evidence: `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`, `docs/system/workspace/scripts/README.md`, `docs/system/workspace/scripts/tests/test-routing-foundation-loop`, `docs/system/workspace/hooks/pre-commit.sh`
- completion_note: 已把 `system/workspace` 真源、`scripts` / `hooks` 与运行时投影映射写回 orchestrator，并补齐最小闭环测试

6. `I-20260308-1631`
- title: 阶段前缀式主进度标识治理
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/stage-prefixed-progress-identifier/issues/stage-prefixed-progress-identifier.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1630--stage-prefixed-progress-identifier/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1630--stage-prefixed-progress-identifier/candidates.md`
- evidence: `docs/LAWS.md`, `docs/PROJECT_INTENT.md`, `docs/milestones.md`, `docs/system/workspace/skills/context-source-skill/SKILL.md`, `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`, `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
- completion_note: 已把 `phase_state` 收敛为 Freely 自举阶段的主执行标识，并统一 `done_ibm -> in_dev` handoff 与 milestone 路由口径

7. `I-20260308-1931`
- title: 业务阻塞状态与系统崩溃恢复定位治理
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/business-block-vs-system-crash-recovery/issues/business-block-vs-system-crash-recovery.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1930--business-block-vs-system-crash-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1930--business-block-vs-system-crash-recovery/candidates.md`
- evidence: `docs/LAWS.md`, `docs/system/workspace/skills/context-source-skill/SKILL.md`, `docs/system/workspace/skills/recovery-subagent-governance/SKILL.md`, `docs/milestones.md`
- completion_note: 已明确分层业务阻塞与系统崩溃恢复，禁止用 `blocked_*` 伪造系统事件交接，并统一恢复定位顺序与最小字段口径
