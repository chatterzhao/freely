# Issue: manager-watchdog-trigger-and-drift-reconcile-governance

- issue_id: `I-20260321-1715`
- title: Manager watchdog trigger and drift reconcile governance
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-watchdog-trigger-and-drift-reconcile-governance`
- issue-name: `manager-watchdog-trigger-and-drift-reconcile-governance`
- source_candidate: `docs/pre-brainstorms/20260321-1715--manager-patrol-trigger-and-restart-routing/candidates.md#c-20260321-1715-a`
- source_brainstorm: `docs/pre-brainstorms/20260321-1715--manager-patrol-trigger-and-restart-routing/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/manager-reactivation-and-fleet-patrol-governance/issues/manager-reactivation-and-fleet-patrol-governance.md`, `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 当前已经分别定义了：

- `event source / standing source`
- 主管巡检与委派
- restart point routing
- `external drift / out-of-band reconcile` 的新研究结论

但这些语义还散落在多个真源里，且容易被误读成：

- `auto-loop` 只有周期巡检，没有事件触发入口
- verification / writeback / cleanup 是第四层 loop
- 主管只在最前面路由一次
- 主管既判断又亲自施工

需要一条新的治理 issue，把这些新增澄清收敛成一致的应用产物重构：

- 不回写历史 issue
- 不新造平行 skill
- 在当前新生命周期内统一重构 `three-loop` / `manager-agent` / `auto-loop-orchestrator` / patrol reference

## Absorbed Research Inputs

- `docs/pre-brainstorms/20260321-1715--manager-patrol-trigger-and-restart-routing/brainstorms.md`
- `docs/pre-brainstorms/20260321-1430--external-drift-and-out-of-band-reconcile/brainstorms.md`

## Scope

1. 在 `three-loop-capability-lifecycle.md` 中明确：
- `auto-loop` 同时包含 `patrol-driven` 与 `event-driven` 两类入口
- verification / writeback / cleanup 不构成第四层 loop
- delegated result 会重新回流到主管的 restart-point routing

2. 在 `manager-agent.md` 中明确：
- 主管对用户先输出状态解释和 ownership 判断
- 主管始终只负责判断 / 解释 / 委派 / 监督完成
- delegated owner 返回结果后，主管继续决定下一跳

3. 在 `auto-loop-orchestrator/SKILL.md` 中明确：
- 主管 watchdog 的双入口语义
- restart point 是动态决定，而不是固定从某一层重启

4. 在 patrol/reference 中明确：
- `external drift / out-of-band reconcile` 属于主管巡检面
- 发现后应按 ownership 分流到 maintenance worker / runtime owner / execution worker

## Acceptance

- `three-loop-capability-lifecycle.md` 明确 `auto-loop` 的 `patrol-driven` / `event-driven` 双入口
- `three-loop-capability-lifecycle.md` 明确 verification / writeback / cleanup 不是第四层 loop
- `manager-agent.md` 明确主管先解释状态，再委派 owner；delegated result 返回后继续由主管决定下一跳
- `auto-loop-orchestrator/SKILL.md` 明确双入口最终汇聚到统一的 manager restart-point routing
- patrol/reference 覆盖 `external drift / out-of-band reconcile`
- 不修改历史已完成 issue 的历史语义；新增澄清通过本 issue 收敛

## Completion

- `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/issues/manager-watchdog-trigger-and-drift-reconcile-governance.md`
- `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/brainstorms/b-manager-watchdog-trigger-and-drift-reconcile-governance.md`
- `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/prd.md`
- `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/tasks.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/epics/workspace-routing-foundation/manager-watchdog-trigger-and-drift-reconcile-governance/code-reviews/20260321-manager-watchdog-trigger-and-drift-reconcile-verification.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler`
- `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- review of the updated truth-source wording and cleanup restart-point routing for contradiction / overlap / residual ambiguity

## Next

- 当前最小 acceptance delta 已 materialize：新的项目级 cleanup signal 先进入 manager `notice -> claim -> restart-point routing`，产出 `handoff://cleanup`，不再被旧 `cleanup://merged-worktree-followthrough` continuity 直接吸收。
- issue 继续保持 `in_verification`；下一步做真实 manager/develop 工位回归，确认 cleanup 之外的新项目级 signal 也会先走同一 restart-point routing，再决定最终 absorption target。
- 后续若还需把 patrol cadence、event emission 或自动派单脚本化，再基于本 issue 继续进入新的 runtime/dev 增量；当前不回写历史已完成 issue。
