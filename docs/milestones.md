# Milestones

本文件是 Freely 自举开发时的主动扫描入口，用来承接已进入活跃范围的 candidate / issue。

## Milestone Policy

milestone_status_policy_version: v2

candidate_policy:
- dropped: remove from active milestone queues
- needs_research: keep in candidate_issues with `next_action` and `revisit_trigger`, and route back to pre-brainstorms or issue-bound brainstorm; do not silently drop it from active scans
- promoted: bind to a milestone immediately; do not leave as long-term unbound state
- blocked: keep visible with blocker, next action, and revisit trigger

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
- unresolved candidate or issue never disappears just because the current round chose another priority; keep it in the appropriate queue with an explicit restart condition

## M-20260306-workspace-routing-foundation

- title: Workspace routing foundation for Freely dogfooding
- status: active
- source_brainstorm: `docs/pre-brainstorms/20260306-0248--issue-brainstorm-routing-guard/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260306-0248--issue-brainstorm-routing-guard/candidates.md`
- intent: 把首跳路由治理候选正式纳入 milestone，避免 Freely 自己继续依赖悬空 candidate 工作
- why_now: 这批项定义 Freely 如何发现上下文、读取 milestone、并路由到下一跳 skill；如果 milestone 自身不先落盘，Freely 的狗粮链路就是断的

### committed_issues

1. `I-20260327-1115`
- title: OAuth slot inventory sweep and launch-time confirmation governance
- milestone_state: committed
- phase_state: `done_ibm`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260327-1115--oauth-api-usage-query-refactor/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260327-1115--oauth-api-usage-query-refactor/candidates.md`
- next_action: 当前 OAuth `wham/usage` 预研已完成 materialization；下一步进入 dev-loop，把 unified sweep、availability cache、cooldown overwrite 和 launch-time confirmation 写回 capability truth，不再停留在 pre-brainstorm

### completed_issues

1. `I-20260307-1201`
- title: 源分类、milestone-owned issue 与派生 worktree 路由治理
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/issues/source-routing-and-derived-worktree-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/code-reviews/20260316-first-hop-second-hop-verification.md`
  - `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/code-reviews/20260326-source-routing-canonical-replay-verification.md`
- completion_note: 首跳来源分层、IBM/progress 边界、derived worktree 规则与同工具第二跳 contract 已收口；旧 dirty sibling blocker 已被 canonical 4-tree fleet truth 消除，不再构成未完成项

2. `I-20260319-0018`
- title: Token-efficient session continuity and rotation governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-0018--token-efficient-session-continuity-and-rotation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0018--token-efficient-session-continuity-and-rotation/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-token-efficient-session-continuity-and-rotation-governance.md`
  - `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/code-reviews/20260326-token-efficient-session-continuity-and-rotation-canonical-verification.md`
- completion_note: continuity trigger matrix、manager-vs-worker continuity targets、fallback-only session evidence refs 与 warn/rotate/fresh-with-handoff 边界已共同写回 canonical truth sources；后续官方 compaction primitive 或 continuity schema 演进另开 lifecycle

3. `I-20260319-0148`
- title: Context-compaction continuity guard salvage
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/context-compaction-continuity-guard-salvage/issues/context-compaction-continuity-guard-salvage.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-0148--context-compaction-salvage-and-retirement/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0148--context-compaction-salvage-and-retirement/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-context-compaction-continuity-guard-salvage.md`
  - `docs/epics/workspace-routing-foundation/context-compaction-continuity-guard-salvage/code-reviews/20260326-context-compaction-continuity-guard-salvage-canonical-verification.md`
- completion_note: 旧 context-compaction 分支独有的 continuity guard 字段、prompt 提醒与测试锁定已被 canonical `develop` 吸收；本地也不再保留旧 feature branch，后续 continuity 演进回到主线 issue family

2. `I-20260321-0217`
- title: Claude Code tool profiles and Codex MCP session evidence governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/claude-code-codex-mcp-runtime-governance/issues/claude-code-codex-mcp-runtime-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-2145--cc-tool-profiles-and-concurrent-session-continuity/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-2145--cc-tool-profiles-and-concurrent-session-continuity/candidates.md`, `docs/pre-brainstorms/20260321-0148--cc-codex-session-evidence-resolution/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/claude-code-codex-mcp-runtime-governance/code-reviews/20260321-cc-codex-runtime-governance-verification.md`
  - `docs/epics/workspace-routing-foundation/claude-code-codex-mcp-runtime-governance/code-reviews/20260326-cc-codex-runtime-canonical-replay-verification.md`
- completion_note: `cc` / `cc-use-codex-cli` fixed top-level profiles、双层 session evidence 与 focused regressions 已在当前 develop-facing absorption owner 上保持通过；后续 protected replay 属于 sweep-level promote，不再阻塞 issue 完成

3. `I-20260321-1745`
- title: Active lifecycle boundary and dogfooding capability discovery
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/active-lifecycle-boundary-and-dogfooding-capability-discovery/issues/active-lifecycle-boundary-and-dogfooding-capability-discovery.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1745--active-lifecycle-boundary-and-dogfooding-capability-discovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1745--active-lifecycle-boundary-and-dogfooding-capability-discovery/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/active-lifecycle-boundary-and-dogfooding-capability-discovery/code-reviews/20260321-active-lifecycle-boundary-and-dogfooding-capability-discovery-verification.md`
  - `docs/epics/workspace-routing-foundation/active-lifecycle-boundary-and-dogfooding-capability-discovery/code-reviews/20260326-active-lifecycle-boundary-canonical-replay-verification.md`
- completion_note: active-vs-historical lifecycle 边界与狗粮能力发现原则已稳定写回 `three-loop-capability-lifecycle` 和 `PROJECT_INTENT`；后续更高层产品架构讨论另开 lifecycle，不回灌此 issue

4. `I-20260322-1801`
- title: pre-test-merge responsibility, usage, and lifecycle governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/candidates.md`
- evidence:
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
  - `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
  - `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
  - `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
  - `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/code-reviews/20260322-pre-test-merge-responsibility-usage-and-lifecycle-governance-verification.md`
- completion_note: 历史 issue/path 仍沿用 `pre-test-merge` 命名，但当前 canonical 真义已收敛为 `test-pre-merge-*` 测试批次前缀族；其职责边界、stale / retire / rebuild 语义与 replay 默认策略已写回真源，后续 lifecycle management capability 保持独立，不与职责定义混成同一 issue

5. `I-20260321-1515`
- title: Remote branch retirement governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/issues/remote-branch-retirement-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1515--remote-branch-retirement-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1515--remote-branch-retirement-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/code-reviews/20260321-remote-branch-retirement-governance-verification.md`
  - `docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/code-reviews/20260326-remote-branch-retirement-canonical-replay-verification.md`
- completion_note: remote branch disposition 已并入 cleanup/retirement contract，并在当前 absorption owner 上继续通过 focused interruption cleanup regression；后续 status surface 扩展另开 lifecycle

6. `I-20260321-0257`
- title: Worktree fleet governance closure
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/worktree-fleet-governance-closure/issues/worktree-fleet-governance-closure.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-0257--worktree-fleet-governance-closure/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-0257--worktree-fleet-governance-closure/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/worktree-fleet-governance-closure/code-reviews/20260321-worktree-fleet-governance-closure-verification.md`
  - `docs/epics/workspace-routing-foundation/worktree-fleet-governance-closure/code-reviews/20260326-worktree-fleet-governance-closure-canonical-replay-verification.md`
- completion_note: `fleet_closure` 能力与 canonical inventory writeback 已稳定收敛到 4-tree / dirty=0 / all stopped；retained-vs-retired judgement 已冻结为 protected/control、retained research owner、active develop-facing absorption owner 三类，后续 research materialization 不再阻塞本 issue 完成

7. `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/candidates.md`, `docs/pre-brainstorms/20260325-0525--watchdog-slot-sweep-without-cooldown-governance/candidates.md`, `docs/pre-brainstorms/20260325-0921--watchdog-strict-slot-probe-gating-and-wake-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/code-reviews/20260326-global-ai-account-watchdog-canonical-replay-verification.md`
  - `docs/progress/workspace-routing-foundation/p-global-ai-account-watchdog-and-manager-bootstrap.md`
- completion_note: global watchdog/bootstrap contract 已在 canonical `develop` 通过 replay，slot-sweep-first recovery、no-launch gate、all-unavailable hold、inventory-change wake、slot-only identity、dispatcher-ready gate 与 timeout/deactivated-workspace artifact 全部稳定；scheduler retained research 与更广义 interruption followthrough 另由后续 lifecycle 承接

2. `I-20260326-1815`
- title: IBM pre-tests executable acceptance quality governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/issues/ibm-pretests-executable-acceptance-quality-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260326-1733--ibm-pretests-real-environment-acceptance-quality/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260326-1733--ibm-pretests-real-environment-acceptance-quality/candidates.md`
- evidence:
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
  - `docs/progress/workspace-routing-foundation/p-ibm-pretests-executable-acceptance-quality-governance.md`
  - `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/code-reviews/20260326-ibm-pretests-executable-acceptance-quality-governance-verification.md`
- completion_note: IBM 真源现在要求 `pre-tests.md` 默认写出可恢复的 executable acceptance contract，并对 Freely 自治能力明确 integration、application-native real-environment、end-to-end dogfood 三类 post-merge 验收面；verification review 模板统一与 machine-readable schema 继续留给后续 lifecycle

3. `I-20260326-1915`
- title: Deep-refactor fleet sequencing governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/issues/deep-refactor-fleet-sequencing-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260326-1825--deep-refactor-fleet-sequencing/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260326-1825--deep-refactor-fleet-sequencing/candidates.md`
- evidence:
  - `AGENTS.md`
  - `docs/progress/workspace-routing-foundation/p-deep-refactor-fleet-sequencing-governance.md`
  - `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/code-reviews/20260326-deep-refactor-fleet-sequencing-governance-verification.md`
- completion_note: broad/deep refactor 前的 fleet sequencing audit 已固定为开发 Freely 的入口 gate，并已用真实 stop、merge-prep 与 governance-check 结果验证；后续若要升级成自动化或更高等级规则，应由新的 lifecycle 承接

4. `I-20260326-1835`
- title: Manager owner stance and source-patrol completeness governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-owner-stance-and-source-patrol-governance/issues/manager-owner-stance-and-source-patrol-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260326-1705--manager-owner-stance-and-source-patrol/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260326-1705--manager-owner-stance-and-source-patrol/candidates.md`
- evidence:
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/agents/worker-agent.md`
  - `docs/system/workspace/skills/human-interruption-manager-triage/SKILL.md`
  - `docs/system/workspace/skills/signal-intent-understanding/SKILL.md`
  - `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
  - `docs/system/workspace/skills/context-source-skill/references/continuation-recovery-routing.md`
  - `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
  - `docs/progress/workspace-routing-foundation/p-manager-owner-stance-and-source-patrol-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-owner-stance-and-source-patrol-governance/code-reviews/20260326-manager-owner-stance-and-source-patrol-governance-verification.md`
- completion_note: 已把开发治理输入与运行期能力真源的边界写清，并把 manager owner stance、advisory interruption semantics、以及 interruption / milestone / progress / pre-brainstorm 的 standing-source completeness 直接收敛进产品能力真源；后续若要继续把这套 contract 扩成更强的 runtime 事务面，应通过新 lifecycle 承接。

3. `I-20260322-0445`
- title: Latest manager continuity worker consumption governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0445--latest-manager-continuity-worker-consumption/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0445--latest-manager-continuity-worker-consumption/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-latest-manager-continuity-worker-consumption-governance.md`
  - `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260322-latest-manager-continuity-worker-consumption-verification.md`
  - `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260326-latest-manager-continuity-worker-consumption-canonical-replay-verification.md`
- completion_note: canonical `develop` 已重新对齐 latest continuity / latest worker prompt generated-consumed truth，并通过当前 continuity parser focused regression；后续 queue / frozen / reentry 演进另开 lifecycle

4. `I-20260326-0445`
- title: Manager-delegated intake absorption closure governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-delegated-intake-absorption-closure-governance/issues/manager-delegated-intake-absorption-closure-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260326-0445--manager-delegated-intake-absorption-closure/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260326-0445--manager-delegated-intake-absorption-closure/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-manager-delegated-intake-absorption-closure-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-delegated-intake-absorption-closure-governance/code-reviews/20260326-manager-delegated-intake-absorption-closure-verification.md`
- completion_note: manager-owned delegated intake absorbed closure 已进入 canonical `develop`，focused regressions 与 live-status surface 均未回退；worker-side delegated lifecycle 仍按既有 issue family 独立推进

5. `C-20260324-0405-A`
- title: Watchdog restart-storm and process-churn signal implementation
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/watchdog-restart-storm-and-process-churn-governance/issues/watchdog-restart-storm-and-process-churn-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260324-0405--watchdog-restart-storm-and-process-churn-detection/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260324-0405--watchdog-restart-storm-and-process-churn-detection/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-watchdog-restart-storm-and-process-churn-governance.md`
  - `docs/epics/workspace-routing-foundation/watchdog-restart-storm-and-process-churn-governance/code-reviews/20260324-watchdog-restart-storm-and-process-churn-verification.md`
- completion_note: restart-storm / process-churn signal 的 runtime helper、`session-state.env` 真相面、manager escalation 与 `live-status` / `fleet-status` 暴露已在 same-family issue 中完成并验证；该 candidate 不再保留为 active dev handoff

6. `I-20260320-1945`
- title: Watchdog live status surface and manager supervision
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-1945--watchdog-live-status-surface-and-manager-supervision/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-1945--watchdog-live-status-surface-and-manager-supervision/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
- completion_note: `freely live-status` 的主管监督接线与 status surface 已进入 canonical truth；后续若继续扩 JSON / watch / scoring，应新开 lifecycle

7. `I-20260320-2105`
- title: Baseline-status command and status family governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/baseline-status-command-and-status-family-governance/issues/baseline-status-command-and-status-family-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-2105--status-family-baseline-rename-and-future-aggregation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-2105--status-family-baseline-rename-and-future-aggregation/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/baseline-status-command-and-status-family-governance/issues/baseline-status-command-and-status-family-governance.md`
- completion_note: `baseline-status` 命名迁移与 `status` family 聚合入口已经完成；后续 JSON family 输出或 watch 模式应通过新 lifecycle 承接

8. `I-20260324-0405`
- title: 三个 loop 的并列关系与 terminal governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/three-loops-sibling-relationship-and-terminal-governance/issues/three-loops-sibling-relationship-and-terminal-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-1105--three-loop-capability-lifecycle-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-1105--three-loop-capability-lifecycle-governance/candidates.md`, `docs/pre-brainstorms/20260323-0241--three-loop-lifecycle-dictionary-and-worktree-completion/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-three-loops-sibling-relationship-and-terminal-governance.md`
  - `docs/epics/workspace-routing-foundation/three-loops-sibling-relationship-and-terminal-governance/code-reviews/20260324-three-loops-sibling-relationship-verification.md`
- completion_note: active truth、agent / skill 与 runtime-facing contract 已统一到 `auto-loop` outer + `doc-loop` / `dev-loop` sibling 的模型；继续把它留在 `in_dev` 会制造假待办

9. `I-20260322-0115`
- title: CLI-first entrypoint and observability surface unification
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/issues/cli-first-entrypoint-and-observability-surface-unification.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-cli-first-entrypoint-and-observability-surface-unification.md`
  - `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`
- completion_note: shared front-door submit helper 与 CLI-first backend contract 已完成并验证；后续若继续扩 Tauri 渲染层，应新开 lifecycle

10. `I-20260322-0135`
- title: Integration-acceptance-first IBM and verification governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/integration-acceptance-first-verification-governance/issues/integration-acceptance-first-verification-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0135--integration-acceptance-first-ibm-and-verification/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0135--integration-acceptance-first-ibm-and-verification/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-integration-acceptance-first-verification-governance.md`
  - `docs/epics/workspace-routing-foundation/integration-acceptance-first-verification-governance/code-reviews/20260322-integration-acceptance-first-verification-governance-verification.md`
- completion_note: `pre-tests.md` 作为 issue-level acceptance 控制面与 integration-first 口径已收回真源；结构化 verification review 模板若继续扩展，应另开 lifecycle

11. `I-20260322-0228`
- title: Manager delegation after sufficient patrol evidence governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-delegation-after-sufficient-patrol-evidence-governance/issues/manager-delegation-after-sufficient-patrol-evidence-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0228--manager-delegation-after-sufficient-patrol-evidence/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0228--manager-delegation-after-sufficient-patrol-evidence/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-manager-delegation-after-sufficient-patrol-evidence-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-delegation-after-sufficient-patrol-evidence-governance/code-reviews/20260322-manager-delegation-after-sufficient-patrol-evidence-governance-verification.md`
- completion_note: patrol evidence 充足后必须切 concrete worker delegation 的阈值语义已经稳定落盘；后续若 runtime 仍出现只巡检不委派，应进入新的 delegation-mechanism lifecycle

12. `I-20260322-0412`
- title: Worker active reentry for manager-delegated continuation governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0412--worker-active-reentry-for-manager-delegated-continuation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0412--worker-active-reentry-for-manager-delegated-continuation/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-worker-active-reentry-for-manager-delegated-continuation-governance.md`
  - `docs/epics/workspace-routing-foundation/worker-active-reentry-for-manager-delegated-continuation-governance/code-reviews/20260322-worker-active-reentry-for-manager-delegated-continuation-verification.md`
- completion_note: active-worker local reentry 修复、脚本级验收与 post-merge acceptance 已完成；后续 consumed-id 可见性增强应通过新 lifecycle 承接

13. `I-20260318-0930`
- title: Checkpoint commit and multi-worktree supervision governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-0735--account-aware-loop-and-checkpoint-commit-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-0735--account-aware-loop-and-checkpoint-commit-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/code-reviews/20260318-checkpoint-and-fleet-verification.md`
  - `docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/code-reviews/20260326-checkpoint-and-fleet-canonical-replay-verification.md`
- completion_note: checkpoint-guard、staged scope gate、fleet summary 与 baseline dirty-budget 暴露已经在 canonical `develop` 通过 replay；旧 dirty worktree snapshot 不再构成未完成项

14. `I-20260318-1408`
- title: Manager self-supervision and autonomous recovery
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1408--manager-self-supervision-and-autonomous-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1408--manager-self-supervision-and-autonomous-recovery/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/code-reviews/20260326-manager-self-supervision-canonical-replay-verification.md`
- completion_note: manager self-supervision alert、runtime-owned recovery、PID ownership 与 account-boundary contract 已在 canonical `develop` 通过 replay；更外层 manager ensure / watchdog 由 `I-20260318-1630` 继续承接

15. `I-20260308-0101`
- title: 状态联动、流程标识词典与 session evidence 传播治理
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/code-reviews/20260316-state-sync-verification.md`
  - `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/code-reviews/20260317-lead-agent-reentry-verification.md`
  - `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/code-reviews/20260326-state-sync-canonical-replay-verification.md`
- completion_note: 状态词典、session evidence 传播与 milestone handoff policy 已在 canonical truth 中稳定存在；旧 dirty snapshot 与当时的环境兼容性问题不再构成未完成项

16. `I-20260318-1825`
- title: Worktree hygiene supervision control plane
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/worktree-hygiene-supervision-control-plane/issues/worktree-hygiene-supervision-control-plane.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1825--autonomous-worktree-hygiene-and-checkpoint-supervision/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1825--autonomous-worktree-hygiene-and-checkpoint-supervision/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/worktree-hygiene-supervision-control-plane/code-reviews/20260326-worktree-hygiene-canonical-replay-verification.md`
- completion_note: hygiene skill、checkpoint drift escalation 与 manager hygiene alert 已在 canonical `develop` 通过 replay；若需专门 hygiene worker delegation flow，应通过新 lifecycle 承接

17. `I-20260321-0345`
- title: Manager reactivation and fleet patrol governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-reactivation-and-fleet-patrol-governance/issues/manager-reactivation-and-fleet-patrol-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-0345--manager-reactivation-and-fleet-patrol/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-0345--manager-reactivation-and-fleet-patrol/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/manager-reactivation-and-fleet-patrol-governance/code-reviews/20260321-manager-reactivation-and-fleet-patrol-verification.md`
  - `docs/epics/workspace-routing-foundation/manager-reactivation-and-fleet-patrol-governance/code-reviews/20260326-manager-reactivation-and-fleet-patrol-canonical-replay-verification.md`
- completion_note: manager reactivation 后先 patrol fleet 的协议、reference 与首跳提示已在 canonical truth 中稳定存在；真正脚本级巡检/自动派单应通过新 lifecycle 承接

18. `I-20260321-1045`
- title: Stacked worktree merge-chain governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/stacked-worktree-merge-chain-governance/issues/stacked-worktree-merge-chain-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1045--stacked-worktree-merge-chain-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1045--stacked-worktree-merge-chain-governance/candidates.md`
- evidence:
  - `docs/epics/workspace-routing-foundation/stacked-worktree-merge-chain-governance/code-reviews/20260326-stacked-merge-chain-canonical-replay-verification.md`
- completion_note: stacked merge-chain 的 skill/reference/prompt truth 已在 canonical truth 中稳定存在；CLI/脚本级自动决策属于后续增量，不再阻塞当前 issue 收口

### candidate_issues

1. `C-20260327-1115-A`
- title: Promote OAuth parallel sweep to canonical slot inventory truth
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260327-1115--oauth-api-usage-query-refactor/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260327-1115--oauth-api-usage-query-refactor/candidates.md`
- next_action: 已提升为新的 follow-on issue；后续由 `I-20260327-1115` 承接 issue-bound IBM closeout 与 dev-loop 执行

1. `C-20260323-1435-A`
- title: Interactive init bootstrap and fine-grained force/skip governance
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://interactive-init-bootstrap-and-force-governance`
- source_brainstorm: `docs/pre-brainstorms/20260323-1435--interactive-init-bootstrap-and-force-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260323-1435--interactive-init-bootstrap-and-force-governance/candidates.md`
- next_action: 继续 pre-brainstorm，先冻结 `init` 的 step graph、bootstrap commit 豁免边界，以及每个 managed item 的 skip/force contract；在这些边界稳定前，不直接往现有 `init` 继续堆局部 patch
- revisit_trigger: 当 `init` 的交互入口、repo bootstrap 语义与细粒度 skip/force 输出 contract 可以被冻结成独立 issue scope 时，重新进入 materialization 判断

2. `C-20260318-0715-A`
- title: `commit-first after checkpoint-ready` 自治治理
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260318-0715--ai-autonomy-checkpoint-commit-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-0715--ai-autonomy-checkpoint-commit-governance/candidates.md`
- next_action: 继续 pre-brainstorm，先冻结 3 个边界：`checkpoint-ready` 的结构化输出、`LAWS/runtime/checkpoint-guard/supervisor` 的职责分层、以及进入 IBM 前的 promotion gate；在这些边界稳定前不得直接写成 IBM issue 或塞回 `I-20260318-0930`
- revisit_trigger: 当 `checkpoint-ready` 的结构化输出、supervisor 职责边界与 promotion gate 可以被稳定写成最小 issue contract 时，重新进入 materialization 判断

3. `C-20260319-0402-01`
- title: 定义 Freely 的 harness engineering 分层与缺口图
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/candidates.md`
- next_action: 保持在 pre-brainstorm，先验证 Freely 是否需要一份更明确的 harness 分层与缺口图；若边界稳定，再 materialize 成 issue，而不是直接把外部文章结论塞进现有主线
- revisit_trigger: 当 harness 分层、缺口图与 Freely 自身的最小吸收面可以冻结成独立 issue contract 时，重新进入 materialization 判断

4. `C-20260319-0402-02`
- title: 把 worktree 级验证信号统一暴露成 agent 可消费接口
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/candidates.md`
- next_action: 继续 pre-brainstorm，先盘点现有 status / wt-status-all / runtime 输出，再决定要不要 materialize 成统一 machine-readable 汇总接口
- revisit_trigger: 当 worktree 级验证信号的 canonical 输入、输出与 machine-readable summary contract 可以被冻结成 issue scope 时，重新进入 materialization 判断

5. `C-20260319-0402-03`
- title: 建立文档园艺与 AI 残渣清理的周期性后台循环
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P2
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0402--openai-harness-engineering-research/candidates.md`
- next_action: 保持 `needs_research`，等前两个更基础的 harness 候选边界稳定后，再决定是否 materialize
- revisit_trigger: 当 harness 分层图与 worktree 级验证接口都已稳定，且后台园艺循环不再扩大当前 scope 时，重新进入 materialization 判断

8. `C-20260322-1615-A`
- title: Protected post-merge acceptance route and promotion guard governance
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://protected-post-merge-acceptance-route-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260322-1615--protected-post-merge-acceptance-route-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-1615--protected-post-merge-acceptance-route-governance/candidates.md`
- next_action: 继续 pre-brainstorm，但已冻结一条硬规则：历史文案中的 `pre-test-merge` 现在一律按 `test-pre-merge-*` shadow batch 解释，只做测试 merge，不直接 merge 到 `develop`。剩余要收口的是 `develop-only completion verification` 与测试批次 acceptance 的分流、raw `git add` 无法 hook 时的最小可靠兜底，以及主环境验收发现问题后的 source replay / cleanup 证据模型；在这些边界稳定前不得直接写成 issue 或只靠 skill 文案宣告完成
- revisit_trigger: 当 protected verification environment 的 replay policy、failure reroute、machine-readable evidence 与最小 guard 落点可以被冻结成独立 issue contract 时，重新进入 materialization 判断

9. `C-20260325-0525-A`
- title: Retire cooldown-driven recovery and make slot sweep canonical
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- source_brainstorm: `docs/pre-brainstorms/20260325-0525--watchdog-slot-sweep-without-cooldown-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260325-0525--watchdog-slot-sweep-without-cooldown-governance/candidates.md`
- completion_note: 当前 candidate 生命周期已通过 pre-brainstorm 收口为 same-family supporting evidence；不新开平行 issue，直接把 “cooldown 退出主恢复 contract、failure-driven full slot sweep 成为 canonical” 的边界改写回 `I-20260318-1630`

10. `C-20260322-1801-B`
- title: pre-test-merge lifecycle management capability for Freely
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://pre-test-merge-lifecycle-management-capability`
- source_brainstorm: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/candidates.md`
- next_action: 继续 pre-brainstorm，但 scope 已收窄为 `stale test-pre-merge batch governance`；历史候选名仍保留 `pre-test-merge`，语义上一律指向 `test-pre-merge-*` 前缀族。先冻结三块 machine-readable contract：`stale state truth surface`、`manager-owned lifecycle transaction`、`runtime consumption gate`；同时补齐 `replay source manifest / replay order / retire evidence`，把 `Issue + Brainstorm + PRD -> pre-tests.md` 派生链桥接成固定的 `acceptance_contract_state/source/blocker` 字段，并把 testing closeout 的集成测试 / application-native real-environment testing evidence bar 写死，在这些真源稳定前不进入实现
- revisit_trigger: 当 stale state 的 canonical 落点、manager lifecycle transaction 字段、runtime gate 消费路径、replay/retire manifest、`acceptance_contract_state/source/blocker` 桥，以及 testing closeout evidence bar 都能冻结成独立 issue contract 时，重新进入 materialization 判断

11. `C-20260322-1801-C`
- title: worker self-loop exit and scheduler closeout governance
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://worker-self-loop-exit-and-scheduler-closeout-governance`
- source_brainstorm: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/candidates.md`
- next_action: 继续 pre-brainstorm，单独冻结 `phase progress`、`loop stall`、`manager handback`、`capacity release / supersede` 规则；同时补清 lane 回交后如何识别“其实是上游 `Issue + Brainstorm + PRD -> pre-tests.md` acceptance 面不完整”以及“其实还没完成 integration / application-native real-environment testing closeout”；这里提到的 stale `pre-test-merge` gate 同样按 `test-pre-merge-*` 前缀族解释，在 machine-readable 阈值稳定前，不把两条能力线绑在一起实现
- revisit_trigger: 当 low-value self-loop 的判据、manager 回交 contract、容量释放规则，以及与 IBM/`Issue + Brainstorm + PRD -> pre-tests.md` 缺口和 testing closeout 缺口的分流条件都能冻结成独立 issue contract 时，重新进入 materialization 判断

6. `C-20260319-0500-01`
- title: 为 Freely 补一份更强的 orchestrator executable spec
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/candidates.md`
- next_action: 保持在 pre-brainstorm，先确认 Freely 是否真的缺一份更集中、可执行的 orchestrator spec；若结论稳定，再 materialize 成 issue，而不是直接把 Symphony 当成架构模板
- revisit_trigger: 当 orchestrator executable spec 的缺口、职责边界与最小验收可以冻结成独立 issue contract 时，重新进入 materialization 判断

6. `C-20260319-0500-02`
- title: 统一 issue-level continuity artifact 设计
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/candidates.md`
- next_action: 保持在 pre-brainstorm，先确认哪些 continuity 信息必须跨环持续存在、哪些仍应按 loop 分层存放；未稳定前不要 materialize
- revisit_trigger: 当 issue-level continuity artifact 的最小字段、跨环写回边界与 canonical 落点可以被冻结成 issue scope 时，重新进入 materialization 判断

7. `C-20260319-0500-03`
- title: 评估远程 worker / SSH 执行扩展对 Freely 的适用性
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P2
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0500--openai-symphony-research/candidates.md`
- next_action: 保持在 pre-brainstorm，优先只收集远程 worker 对 workspace ownership、cleanup、resume、host health 的新增要求
- revisit_trigger: 当远程 worker / SSH 扩展的 ownership、cleanup、resume 与 host health 新约束可以冻结成最小 issue contract 时，重新进入 materialization 判断

8. `C-20260310-0056-A`
- title: Evolver Sidecar for Freely Strategy Evolution
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260310-0056--evolver-autonomous-development-leverage/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260310-0056--evolver-autonomous-development-leverage/candidates.md`
- next_action: 继续 pre-brainstorm，先把本地可选 sidecar 的最小职责边界、review / validation / rollback gate 和不接管主 runtime 的约束写稳，再决定是否 materialize 成独立 issue
- revisit_trigger: 当 sidecar 的职责边界、review/validation/rollback gate 与“不接管主 runtime”约束可以被冻结成最小 issue contract 时，重新进入 materialization 判断

9. `C-20260322-0715-A`
- title: Detect and recover pre-test-merge manager acceptance stalls after delegated continuation
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://pre-test-merge-acceptance-stall-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260322-0715--pre-test-merge-post-merge-acceptance-stall/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0715--pre-test-merge-post-merge-acceptance-stall/candidates.md`
- next_action: 保持 active candidate；先依赖测试批次治理 issue 冻结 protected-env 生命周期语义。历史文案中的 `pre-test-merge` 统一按 `test-pre-merge-*` 前缀族理解，并在真实 dogfood 中跑满 watchdog 阈值；只有 delegated continuation 已进 prompt 且超过阈值仍无新 manager continuity/decision 时，才 materialize 成独立 runtime/orchestration issue
- revisit_trigger: 当治理 issue 稳定 `test-pre-merge-*` 边界后，或真实 post-merge acceptance 再次在超过 watchdog 阈值后仍复现 delegated continuation stall 时，重新进入 issue materialization 判断

10. `C-20260323-1705-A`
- title: Detect and recover manager delegated continuation stalls after prompt absorption
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://manager-delegated-continuation-stall-recovery-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260323-1705--manager-delegated-continuation-stall-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260323-1705--manager-delegated-continuation-stall-recovery/candidates.md`
- next_action: 保持 active candidate；先用 runtime 补丁和真实 dogfood 验证 prompt-absorbed delegated continuation stall 是否能被恢复，再决定是 materialize 为独立 issue，还是吸收到现有 stall/recovery issue 族
- revisit_trigger: 当再次复现 manager prompt 已吸收 continuation 但无新 continuity / handoff 的假活，或当前 runtime 补丁验证稳定后需要冻结独立 issue contract 时，重新进入 materialization 判断

11. `C-20260323-1835-A`
- title: Detect and recover active worker delegated-continuation stalls
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://worker-delegated-continuation-active-stall-recovery-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260323-1835--worker-delegated-continuation-active-stall-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260323-1835--worker-delegated-continuation-active-stall-recovery/candidates.md`
- next_action: 保持 active candidate；先让 manager watchdog 能识别并恢复 active worker delegated-continuation stall，再继续真实 dogfood 验证 retained worker 能否自动收口、cleanup 并回到 next patrol
- revisit_trigger: 当再次复现 active worker 已收到 delegated continuation 但 cycle log / closeout 长时间不推进，或当前 runtime 补丁验证稳定后需要冻结独立 issue contract 时，重新进入 materialization 判断

9. `C-20260319-1105-A`
- title: 三层循环能力映射、owner 边界与生命周期真源收敛
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260319-1105--three-loop-capability-lifecycle-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-1105--three-loop-capability-lifecycle-governance/candidates.md`
- next_action: 继续 pre-brainstorm，先验证 `docs/system/workspace/three-loop-capability-lifecycle.md` 是否足以成为唯一细节真源；若仍需更多行为约束，再 materialize 为独立 IBM issue，而不是继续把细节散落到 `CONSTITUTION`、`PROJECT_INTENT` 和多个 skills 中
- revisit_trigger: 当 lifecycle 真源之外仍出现新的行为约束必须落到独立 issue，或 manager/doc/dev-loop 继续出现无法由当前真源解释的冲突时，重新进入 materialization 判断
11. `C-20260320-0252-A`
- title: Signal restart-point routing across interruption, review, test, and recovery
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://restart-point-routing-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260320-0252--interruption-topology-and-manager-routing/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0252--interruption-topology-and-manager-routing/candidates.md`
- next_action: M1-M3 的 interruption 最小 slice 已落盘：主管 triage 已改成抽象 routing contract，且 `cleanup` followthrough 已形成第一条完整 event 链。下一步继续 pre-brainstorm，把同一 contract 扩到 review/test/runtime anomaly/worker-discovered gap 与 standing-source scan，再决定是否 materialize 为统一 routing issue
- revisit_trigger: 当 review/test/runtime anomaly/worker-discovered gap 与 standing-source scan 已共享同一 restart-point routing contract 时，重新进入 materialization 判断

12. `C-20260320-0908-A`
- title: Unresolved research candidate persistence and revisit governance
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260320-0908--research-candidate-persistence-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0908--research-candidate-persistence-governance/candidates.md`
- next_action: 继续 pre-brainstorm，先把“不能收口时必须显式保持在 candidate/blocked 队列并写清重启条件”的规则写入 lifecycle、lead prompt 与 doc-loop reference，再决定是否 materialize 为独立治理 issue
- revisit_trigger: 当后续 worktree 审查再次发现 unresolved candidate 仍会在队列层被跳过，或当前规则需要更强的 issue-bound enforcement 时，重新进入 materialization 判断
13. `C-20260320-0605-A`
- title: Agent state time-machine and shared continuity control plane
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://state-snapshot-fork-and-shared-continuity-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260320-0605--agent-state-time-machine-and-shared-continuity/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0605--agent-state-time-machine-and-shared-continuity/candidates.md`
- next_action: 继续 pre-brainstorm，先冻结四个边界：Freely 当前哪些关键状态不在 Git/worktree 治理内、哪些状态必须一起 snapshot/rollback、共享连续性与 worker 私有状态如何分层、以及最小实现是否应先从本地 snapshot index / continuity metadata 开始；在这些边界稳定前不要把 PGFS 或 PostgreSQL 直接定成默认架构
- revisit_trigger: 当 Freely 的多设备或多人协作场景需要统一共享连续性控制面，且本地 snapshot index 方案边界稳定后，再进入 IBM。
### completed_issues

1. `I-20260322-0115`
- title: CLI-first entrypoint and observability surface unification
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/issues/cli-first-entrypoint-and-observability-surface-unification.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/candidates.md`
- evidence: `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/issues/cli-first-entrypoint-and-observability-surface-unification.md`, `docs/progress/workspace-routing-foundation/p-cli-first-entrypoint-and-observability-surface-unification.md`, `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`
- cleanup_gate: `merged-pending-verify`
- branch: `feature/cli-first-observability-surfaces-20260322`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260322-feature-cli-first-observability-surfaces`
- local_branch_disposition: `retained-with-reason`
- remote_branch_disposition: `deleted`
- completion_note: issue 实现能力已被 `develop` 吸收，当前 feature branch 也已 rebase 到最新 `develop` 之上，但 branch tip 仍保留未被主线吸收的 canonical closure writeback。`2026-03-22` 的 post-merge acceptance 再次确认：milestone 队列已经保持 canonical `completed_issues`，远程同名 branch 仍不存在，但 `git rev-list --left-right --count feature/cli-first-observability-surfaces-20260322...develop` 仍为 `3 0`，因此当前 disposition 继续是 `retire-only`，cleanup gate 只能保持 `merged-pending-verify`；先把这些收口提交吸收到 canonical `develop`，再由 supervisor/runtime 在 worktree 外执行最终 branch/worktree 删除。

2. `I-20260321-1925`
- title: Manager chat reentry and cleanup misrouting governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-chat-reentry-and-cleanup-misrouting-governance/issues/manager-chat-reentry-and-cleanup-misrouting-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1925--manager-chat-reentry-and-cleanup-misrouting/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1925--manager-chat-reentry-and-cleanup-misrouting/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/interruption-manager-handler`, `docs/system/workspace/scripts/tests/test-interruption-manager-handler`, `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`, `docs/epics/workspace-routing-foundation/manager-chat-reentry-and-cleanup-misrouting-governance/code-reviews/20260321-manager-chat-reentry-and-cleanup-misrouting-verification.md`
- completion_note: broad supervisor chat signal 已不再默认误落 cleanup followthrough；纯 cleanup 请求仍保持 worker cleanup 路径，主管级广义巡检请求则回到 `handoff://continuation` 与 manager ownership

3. `I-20260322-0049`
- title: Manager continuation handoff consumption governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-continuation-handoff-consumption-governance/issues/manager-continuation-handoff-consumption-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0049--manager-continuation-handoff-consumption/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0049--manager-continuation-handoff-consumption/candidates.md`
- evidence: `docs/progress/workspace-routing-foundation/p-manager-continuation-handoff-consumption-governance.md`, `docs/epics/workspace-routing-foundation/manager-continuation-handoff-consumption-governance/code-reviews/20260322-manager-continuation-handoff-consumption-verification.md`, `docs/epics/workspace-routing-foundation/manager-continuation-handoff-consumption-governance/code-reviews/20260322-manager-continuation-handoff-consumption-cleanup-verification.md`
- completion_note: 当前 worktree 已确认 `retire-only`，历史 anomaly 仅保留追溯语义，不再 materialize 新实现 scope；milestone 队列已纠正到 `completed_issues`。fresh session after `context_compacted` 已再次复核 canonical closeout，结论未变：当前分支还保留一个已被 `feature/completed-worktree-closeout-merge-prep-20260322` 吸收的 cleanup/closure 提交且无远程同名分支；本地 branch/worktree 删除应走 closeout chain，而不是重新打开本 issue 的实现范围

4. `I-20260322-0245`
- title: Runtime worker launch linkage and stall recovery governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260322-0245--runtime-worker-launch-linkage-and-stall-recovery/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260322-0245--runtime-worker-launch-linkage-and-stall-recovery/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/runtime/manager-watchdog.sh`, `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`, `docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery`, `docs/epics/workspace-routing-foundation/runtime-worker-launch-linkage-and-stall-recovery-governance/code-reviews/20260322-runtime-worker-launch-linkage-and-stall-recovery-verification.md`
- completion_note: manager-generated worker handoff 已可直接转成 target worker continuation launch，stall recovery 也已进入 runtime-owned 控制面；当前 issue 已完成 verification closure，本轮 canonical writeback 固化后工位会恢复 clean，但本地 docs-only closure commits 仍待经 develop-facing 路径吸收，因此 cleanup gate 继续为 `retained-with-reason`

5. `I-20260321-2010`
- title: Explicit session-addressed resume governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/explicit-session-addressed-resume-governance/issues/explicit-session-addressed-resume-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-2010--explicit-session-addressed-resume-over-last-and-pty/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-2010--explicit-session-addressed-resume-over-last-and-pty/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/runtime/tool-launchers.sh`, `docs/system/workspace/scripts/monitor-ai-cli.sh`, `docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`, `docs/epics/workspace-routing-foundation/explicit-session-addressed-resume-governance/code-reviews/20260321-explicit-session-addressed-resume-verification.md`
- completion_note: 显式 session-addressed resume 已成为 Freely 的 canonical continuity model；`codex` 默认路径不再依赖 `--last`，worker-scoped target evidence 与 preemption fallback 也已闭环

6. `I-20260321-1715`
- title: Manager watchdog trigger and drift reconcile governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/issues/manager-watchdog-trigger-and-drift-reconcile-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1715--manager-patrol-trigger-and-restart-routing/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1715--manager-patrol-trigger-and-restart-routing/candidates.md`, `docs/pre-brainstorms/20260321-1430--external-drift-and-out-of-band-reconcile/candidates.md`
- evidence:
  - `docs/progress/workspace-routing-foundation/p-manager-watchdog-trigger-and-drift-reconcile-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/code-reviews/20260321-manager-watchdog-trigger-and-drift-reconcile-verification.md`
  - `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/code-reviews/20260326-manager-watchdog-trigger-and-drift-reconcile-canonical-replay-verification.md`
- completion_note: cleanup reroute contract 已在 canonical `develop` 通过 replay，cleanup-only signal 保持 `handoff://cleanup`，broad supervisor signal 保持 manager-owned continuation reentry；authoritative fleet truth 也已稳定到 4-tree / dirty=0 / all stopped。scheduler retained research owner 继续独立保留，不并入本条完成判断

4. `I-20260321-1706`
- title: Chat-triggered worker runtime reactivation governance
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/chat-triggered-worker-runtime-reactivation-governance/issues/chat-triggered-worker-runtime-reactivation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1706--chat-triggered-worker-runtime-reactivation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1706--chat-triggered-worker-runtime-reactivation/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`, `docs/epics/workspace-routing-foundation/chat-triggered-worker-runtime-reactivation-governance/code-reviews/20260321-chat-triggered-worker-runtime-reactivation-verification.md`
- completion_note: worker 工位在 `operator_stop` 后的 `freely chat` 现在会通过 delegated handoff gate 重新拉起本工位主循环；脚本级与真实狗粮验证均已通过

5. `I-20260319-1715`
- title: CLI-first human chat intake and manager delegation loop
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/human-chat-intake-and-manager-delegation/issues/human-chat-intake-and-manager-delegation.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-1715--human-chat-intake-and-manager-delegation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-1715--human-chat-intake-and-manager-delegation/candidates.md`
- evidence: `docs/epics/workspace-routing-foundation/human-chat-intake-and-manager-delegation/issues/human-chat-intake-and-manager-delegation.md`, `docs/epics/workspace-routing-foundation/human-chat-intake-and-manager-delegation/code-reviews/20260320-human-chat-intake-and-manager-delegation-verification.md`, `docs/system/workspace/scripts/tests/test-freely-human-chat-intake`
- completion_note: CLI-first human chat intake、manager queue scanning、claim/resolve/absorption writeback 与专项测试已闭环；companion canonical 分支已挂起，不再阻塞主线完成

6. `I-20260319-2315`
- title: CLI TUI interruption input box for Freely
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/cli-tui-human-interruption-input/issues/cli-tui-human-interruption-input.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-2315--cli-tui-human-interruption-input/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-2315--cli-tui-human-interruption-input/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- completion_note: `freely tui` 已收口为 interruption presentation shell，并补齐中文与多行提交回归，输入仍统一落到既有 durable intake 链路

7. `I-20260320-1405`
- title: Worktree maintenance governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/worktree-maintenance-governance/issues/worktree-maintenance-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-1410--worktree-maintenance-skill-taxonomy/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-1410--worktree-maintenance-skill-taxonomy/candidates.md`
- evidence: `docs/system/workspace/skills/worktree-maintenance-governance/SKILL.md`, `docs/system/workspace/agents/lead-agent.md`, `docs/system/workspace/agents/manager-agent.md`, `docs/system/workspace/scripts/start-lead-agent.sh`, `docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- completion_note: 已把 worktree 创建后的维护能力收敛成专门 skill，明确 `audit / merge_prep / retirement_handoff` 三种模式，并接入主管真源与首跳测试

8. `I-20260318-1222`
- title: Mem9 shared memory evaluation for Freely continuity plane
- milestone_state: completed
- phase_state: `completed`
- priority: P2
- issue_path: `docs/epics/workspace-routing-foundation/mem9-continuity-bridge/issues/mem9-continuity-bridge.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1222--mem9-shared-memory-fit-for-freely/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1222--mem9-shared-memory-fit-for-freely/candidates.md`
- completion_note: mem9 已明确收束为可选连续性增强层，不是 Freely 的治理真源；对应边界已 materialize 为 `skill:mem9-continuity-bridge`，并保持本地治理事实源优先

9. `C-20260306-1101`
- title: `lead-agent.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/lead-agent-bootstrap.md`
- evidence: `docs/system/workspace/agents/lead-agent.md`
- completion_note: 已落地首跳中枢代理职责与首跳协议

10. `C-20260306-1102`
- title: `context-source-skill.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/context-source-skill-bootstrap.md`
- evidence: `docs/system/workspace/skills/context-source-skill/SKILL.md`
- completion_note: 已落地来源判定、milestone 扫描与 usable issue 决策规则

5. `C-20260306-1103`
- title: `doc-pre-brainstorm-execution.md`
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/doc-pre-brainstorm-execution-bootstrap.md`
- evidence: `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
- completion_note: 已落地 docs 前置收敛环，负责 pre-brainstorm 产物与 milestone 原子同步

6. `C-20260306-1104`
- title: `doc-ibm-execution.md` 与 `dev-loop-execution.md` 的外循环接驳边界
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/bootstrap-routing-foundation-artifacts/issues/doc-loop-dev-loop-handoff-bootstrap.md`
- evidence: `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`, `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
- completion_note: 已收紧 issue-bound `IBM+G` 与 `DDD` 的接驳边界，状态交换统一回流给 auto-loop

7. `C-20260306-1105`
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

8. `C-20260319-0220-A`
- title: Watchdog umbrella term and sub-control-plane taxonomy
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- promoted_issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- evidence: `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`, `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`, `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`, `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- completion_note: umbrella taxonomy 已由 `watchdog-control-plane` 与现有 availability / runtime / continuity issue 主线吸收，不再单独 materialize

9. `I-20260320-0512`
- title: Milestone planning and state maintenance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/milestone-planning-and-state-maintenance/issues/milestone-planning-and-state-maintenance.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-0512--milestone-planning-and-state-maintenance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0512--milestone-planning-and-state-maintenance/candidates.md`
- completion_note: milestone planning 与 state maintenance 已作为独立治理能力物化并验证，收口为 `completed`

11. `C-20260319-0220-C`
- title: Historical watchdog productization worktree retirement handoff
- milestone_state: completed
- phase_state: `completed`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- evidence: `docs/pre-brainstorms/CONVERGENCE.md`, `docs/pre-brainstorms/20260319-0220--watchdog-control-plane-governance/brainstorms.md`
- completion_note: 旧 watchdog 产品化工位的 `materialize_then_retire` handoff、cleanup 结果与 retirement heuristic 已完成留痕；该候选归档，不新开 IBM

12. `I-20260316-1801`
- title: Auto-run session lifecycle rotation and handoff governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260303-cli-orchestration-architecture/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260303-cli-orchestration-architecture/candidates.md`
- evidence: `docs/LAWS.md`, `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/monitor-ai-cli.sh`, `docs/system/workspace/scripts/tests/test-freely-session-rotation`, `bin/test-freely-session-rotation`
- completion_note: 已把 `resume` 与 `fresh_with_handoff` 区分为显式 runtime 行为，并固定 Codex 默认模型为 `gpt-5.4`、默认 reasoning effort 为 `medium`

11. `I-20260320-0018`
- title: Default project resolution and authorized project memory for CLI-first interruption entrypoints
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/default-project-resolution-and-authorized-project-memory/issues/default-project-resolution-and-authorized-project-memory.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-0018--default-project-resolution-and-authorized-project-memory/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0018--default-project-resolution-and-authorized-project-memory/candidates.md`
- evidence: `docs/system/workspace/scripts/runtime/freely`, `docs/system/workspace/scripts/tests/test-freely-project-resolution-defaults`
- completion_note: 默认项目解析已由共享 runtime resolver 覆盖，并通过 cwd auto-resolution 与单一已授权项目回退回归锁定；后续如需多项目切换能力，应从新的 candidate materialize，不要继续扩大本条 completed issue
11. `I-20260320-0500`
- title: Candidate acceptance review governance
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/workspace-routing-foundation/candidate-acceptance-review-governance/issues/candidate-acceptance-review-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260320-0500--candidate-acceptance-review-governance/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260320-0500--candidate-acceptance-review-governance/candidates.md`
- evidence: `docs/epics/workspace-routing-foundation/candidate-acceptance-review-governance/issues/candidate-acceptance-review-governance.md`, `docs/epics/workspace-routing-foundation/candidate-acceptance-review-governance/tasks.md`, `docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`, `docs/system/workspace/scripts/quality/governance-check`
- completion_note: future candidate v2 schema、独立 acceptance review、IBM acceptance deepening 与治理门禁已稳定落盘；高风险 candidate 的双审策略保留为后续治理演进，不阻塞当前 issue 完成

12. `C-20260323-2045-A`
- title: Add capacity-aware queueing for manager worker prompt sets
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260323-2045--manager-worker-scheduler-capacity-and-queueing/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260323-2045--manager-worker-scheduler-capacity-and-queueing/candidates.md`
- evidence:
  - `AGENTS.md`
  - `docs/system/workspace/scripts/start-lead-agent.sh`
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-capacity-queue`
  - `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-busy-worker-queue`
  - `docs/epics/workspace-routing-foundation/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
  - `docs/epics/workspace-routing-foundation/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md`
  - `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- completion_note: 当前 candidate 的旧 blocker 已被 canonical `develop` 否定并吸收：dispatch metadata 已成为 runtime contract，固定 numeric launch cap 已退场，parallel-safe prompts 会直接 launch，queue 只保留给 same-lane busy、单 wave 非并行限制与 `write_scope` 冲突。后续若要继续做更强的 scheduler fairness / quota / transaction 语义，应新开 lifecycle，而不是复活这条已收口的 research。

## M-20260312-control-surface-runtime-convergence

- title: Control surface, runtime, and intervention architecture convergence
- status: active
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- intent: 把跨 pre-brainstorm / 跨 feature 分支的架构结论收敛进单一里程碑，停止悬空讨论，再按 milestone 顺序创建后续专用 worktree 落 IBM 与实现；该收敛批次以前置 issue `I-20260308-1245` 的边界复评结论为基础，不替代它。
- why_now: Freely 正在吃自己的狗粮开发自己；如果架构、控制面、standalone/OpenClaw、human intervention 等候选持续分散在多个分支和 pre-brainstorm 中，auto-loop 与人工协作都会缺少统一编排入口，同时也会与现有 frontend-probe milestone 的边界复评形成重复编排。

### committed_issues

### candidate_issues

1. `C-20260312-0011-E`
- title: AI Team Control Surface and Multi-Worktree Visibility
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 待 contract 边界初步冻结后进入 IBM，定义 day-1 control surface 的信息架构、worktree visibility 和 team timeline
- revisit_trigger: 当需要设计控制面首页、多 worktree lanes 或团队态势视图时重新唤起

2. `C-20260312-0011-G`
- title: Standalone Runtime Baseline Without OpenClaw
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 在引入任何外部 runtime profile 前，先把 Freely standalone mode 的最小组件、状态面和未闭合点写成正式 IBM 产物
- revisit_trigger: 当要证明 Freely 可以在不依赖 OpenClaw 的情况下独立运行时重新唤起

3. `C-20260312-0011-H`
- title: Human Intervention Transport Across Auto-Run CLIs
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 在当前 `SendChatIntervention` 协议语义下，先冻结 `resume_with_intervention` 的 day-1 控制链与最小依赖字段
- revisit_trigger: 当 human interruption transport 需要正式进入 IBM 或无法继续停留在临时 transport 约定时重新唤起

4. `C-20260312-0011-B`
- title: Frontend Manifest Boundary and Runtime Capability Layering
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P0
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 在 contract 与 standalone 基线明确后进入 IBM，收紧 frontend/backend/AI tool/integration 的 manifest 与真源分层
- revisit_trigger: 当 manifest 分层必须落地到可执行依赖文件时重新唤起

5. `C-20260312-0011-D`
- title: Event Log and Snapshot Reconstruction Contract
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 作为 boundary contract 的补充，单独冻结 event/snapshot 的 reconstruction 语义，服务 UI、恢复和 team visibility
- revisit_trigger: 当事件日志、快照重建或恢复语义出现实现歧义时重新唤起

6. `C-20260312-0011-F`
- title: Skill-first Capability Exposure with OpenClaw Workspace Projection
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 在 standalone baseline 清晰后再进入 IBM，定义哪些 Freely 能力先以 skill 暴露，再映射到 OpenClaw workspace/profile
- revisit_trigger: 当需要把 Freely 能力投影到 OpenClaw workspace 或 hooks 时重新唤起

7. `C-20260312-0011-C`
- title: Runtime Independence with OpenClaw Profile as Optional Adapter
- milestone_state: candidate
- phase_state: `in_pre_brainstorm`
- priority: P1
- promoted_issue_path: `pending://issue-materialization`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- next_action: 在 standalone mode 与 skill projection 明确后进入 IBM，正式定义 OpenClaw 只作为 optional adapter/profile 的边界
- revisit_trigger: 当 OpenClaw 借力边界必须被正式冻结或替换时重新唤起

### completed_issues

1. `I-20260312-0011`
- title: Backend Service Contract and Adapter Taxonomy
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/issues/backend-service-contract-and-adapter-taxonomy.md`
- source_brainstorm: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260312-0011--architecture-synthesis-and-api-boundary/candidates.md`
- evidence:
  - `docs/progress/control-surface-runtime-convergence/p-backend-service-contract-and-adapter-taxonomy.md`
  - `docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/code-reviews/20260320-backend-service-contract-and-adapter-taxonomy-ibm-completion.md`
  - `docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/code-reviews/20260326-backend-service-contract-and-adapter-taxonomy-canonical-verification.md`
- completion_note: contract layer 与 adapter layer 的冻结已经成为下游 frontend-probe architecture / boundary contract 的引用真源；因此本 issue 已从单纯 IBM 包提升为 canonical completion，后续 control surface、standalone runtime 与 intervention transport 直接复用该边界，不再阻塞在 `done_ibm`

## M-20260308-frontend-probe-dogfooding-loop

- title: Frontend probe + backend increment dogfooding loop
- status: active
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- intent: 把“backend-core-first + frontend-probe-from-day-1”收敛为 Freely 自举开发自己的正式候选批次，避免继续只有后端结论、没有产品面验证闭环
- why_now: Freely 的目标本身就是防止 AI 跑偏；如果自举开发中每个后端增量都不能立刻被前端观察、打断和回放，狗粮链路仍然不完整

## M-20260318-url-content-intake-skill-and-wechat-fetch-governance

- status: active
- linked_issue: `docs/epics/workspace-routing-foundation/url-content-intake-skill-and-wechat-fetch-governance/issues/url-content-intake-skill-and-wechat-fetch-governance.md`
- intent: 把公众号链接抓取研究转成可分享的 skill、脚本和最小测试
- why_now: 研究已经证明本地浏览器 UA 抓取可行；如果不把脚本放进 skill，分享 skill 时能力仍然是不完整的

### committed_issues

1. `I-20260318-1908`
- title: URL 内容摄取 skill 与微信公众号抓取治理
- milestone_state: committed
- phase_state: `in_dev`
- priority: P1
- issue_path: `docs/epics/workspace-routing-foundation/url-content-intake-skill-and-wechat-fetch-governance/issues/url-content-intake-skill-and-wechat-fetch-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260318-1246--iflow-wechat-webfetch-capability/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260318-1246--iflow-wechat-webfetch-capability/candidates.md`
- next_action: 把 `url-content-intake` skill、自带抓取脚本与最小测试一起落齐，再评审是否并回 `develop`

### committed_issues

3. `I-20260317-1002`
- title: Frontend Probe v0
- milestone_state: committed
- phase_state: `in_dev`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- next_action: frontend 侧 contract、transport、manifest 和错误面已基本收敛；backend bridge 缺口仍由 `I-20260317-1005` 承接。当前 Rust bridge 的本地 `cargo check` / `cargo test`、前端 `typecheck` / `build` 与公开 manifest 对齐验证都已通过；下一步等待真实 Tauri 宿主启动联调结果，再回到本 issue 收紧 frontend host integration 与 blocker 描述

6. `I-20260317-1005`
- title: Rust/Tauri Probe Bridge v1
- milestone_state: committed
- phase_state: `in_dev`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-0332--rust-tauri-probe-bridge-v1/candidates.md`
- next_action: lead-agent 首跳重入后继续命中 `milestones` 池里的当前 committed `in_dev` issue，并在同一 `codex` 会话内进入 `dev-loop-execution`。当前已补齐 `src-tauri/icons/icon.png`，`bun run rust:preflight`、`bun run cargo:check:probe` 与 `cargo test -p freely-probe-bridge` 已通过；先前的 Rust toolchain / icon blocker 和 `dead_code` warning 均已解除。下一步继续围绕真实 Tauri 宿主启动联调推进，确认前端 `Transport=tauri` 不再停在 `bridge offline`

5. `I-20260317-1004`
- title: Frontend Runtime Baseline for Probe
- milestone_state: committed
- phase_state: `done_ibm`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/issues/frontend-runtime-baseline-for-probe.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/candidates.md`
- next_action: 这条 baseline 已完成最小 IBM 收敛，但当前不在近程执行窗；先让 `I-20260317-1002` / `I-20260317-1005` 消化真实宿主与 bridge 联调成本。若当前 research/merge-prep worktree 只剩这类远期排序项，应先完成 milestone 写回并走 retirement handoff，而不是为了挂住未来 queue 长期保留 worktree。

4. `I-20260317-1003`
- title: Incremental Dogfooding Gate for Backend Increments
- milestone_state: committed
- phase_state: `done_ibm`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/incremental-dogfooding-gate-for-backend-increments/issues/incremental-dogfooding-gate-for-backend-increments.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- next_action: 这条验证门禁先保持 parked completed-IBM owner，作为后续 backend increment review gate 复用；当前不需要单独挂住 research worktree。等活跃 `in_dev` 主线逼近该成本窗口时，再决定是否补 canonical closeout 或 issue-bound continuation。

### candidate_issues

1. `C-20260317-1101`
- title: Frontend Runtime Baseline for Probe
- milestone_state: candidate
- phase_state: `todo_ibm`
- priority: P0
- promoted_issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/issues/frontend-runtime-baseline-for-probe.md`
- source_brainstorm: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260317-1101--frontend-runtime-baseline-for-probe/candidates.md`
- next_action: 已提升为独立 issue；后续由 `I-20260317-1004` 承接 issue-bound IBM 收敛

### completed_issues

1. `I-20260308-1245`
- title: Freely 内部前后端架构复评与可插拔协议边界
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/issues/internal-frontend-backend-architecture-review.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- evidence:
  - `docs/progress/frontend-probe-dogfooding-loop/p-internal-frontend-backend-architecture-review.md`
  - `docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/code-reviews/20260326-internal-frontend-backend-architecture-canonical-verification.md`
- completion_note: frontend/backend 总体边界、状态归属矩阵、协议分层、输入仲裁与 MVP autonomy milestone 已被下游 boundary contract 与 control-surface issue 直接复用，故本 issue 已完成 canonical closeout；后续 probe / bridge / runtime 实现沿该边界推进，不再回灌为总论争议

2. `I-20260317-1001`
- title: Frontend/Backend Boundary Contract v1 for Frontend Probe
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md`
- source_brainstorm: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
- evidence:
  - `docs/progress/frontend-probe-dogfooding-loop/p-frontend-backend-boundary-contract-v1-for-frontend-probe.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/code-reviews/20260326-frontend-backend-boundary-contract-v1-canonical-verification.md`
- completion_note: Probe day-1 boundary contract 已冻结到 object family、error surface、ordering 与 adapter compatibility 字段面，并被 `frontend-probe-v0` 与 `rust-tauri-probe-bridge-v1` 直接复用；因此本 issue 已完成 canonical closeout，后续真实宿主与 bridge 联调留给 active `in_dev` 主线承接

## M-20260321-ai-native-doc-loop

- title: AI-native doc-loop artifacts for Freely
- status: active
- linked_issue: `docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/issues/agent-ready-prd-for-freely-flow.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1530--agent-ready-prd-for-freely-flow/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1530--agent-ready-prd-for-freely-flow/candidates.md`
- intent: 把“AI 时代的 PRD 应该是什么”从 chat 讨论收敛为 Freely 自己可执行的 IBM 产物
- why_now: Freely 自己的 `prd.md` 还偏向人类摘要，而用户已经明确提出要在 Freely 流程里回答“AI 生成 PRD 应该长什么样”；如果不先给出 canonical 结构，后续 doc-loop 仍会沿用旧范式

### committed_issues

- none currently

### completed_issues

1. `I-20260321-1530`
- title: Agent-ready PRD architecture for Freely IBM flow
- milestone_state: completed
- phase_state: `completed`
- priority: P0
- issue_path: `docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/issues/agent-ready-prd-for-freely-flow.md`
- source_brainstorm: `docs/pre-brainstorms/20260321-1530--agent-ready-prd-for-freely-flow/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260321-1530--agent-ready-prd-for-freely-flow/candidates.md`
- evidence: `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`, `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`, `docs/system/workspace/scripts/quality/governance-check`, `docs/system/workspace/scripts/tests/test-doc-ibm-prd-quality-bar`
- completion_note: 已把 AI-ready PRD 的最小质量门槛接入 `doc-ibm-execution` 真源，并补齐 governance-check 与回归测试，确保 IBM 产物中的 `prd.md` 不再只停留在人类摘要
