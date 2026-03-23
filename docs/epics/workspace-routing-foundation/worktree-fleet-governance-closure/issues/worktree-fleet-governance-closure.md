# Issue: worktree-fleet-governance-closure

- issue_id: `I-20260321-0257`
- title: Worktree fleet governance closure
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `worktree-fleet-governance-closure`
- issue-name: `worktree-fleet-governance-closure`
- source_candidate: `docs/pre-brainstorms/20260321-0257--worktree-fleet-governance-closure/candidates.md#c-20260321-0257-a`
- source_brainstorm: `docs/pre-brainstorms/20260321-0257--worktree-fleet-governance-closure/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/worktree-maintenance-governance/issues/worktree-maintenance-governance.md`, `docs/epics/workspace-routing-foundation/stacked-worktree-merge-chain-governance/issues/stacked-worktree-merge-chain-governance.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 已经具备单树 worktree audit、merge-prep、stacked merge-chain 和 retirement handoff，但还缺一层“项目级 fleet closure”。

这会让主管在面对大量 active worktree 时只能临时拼：

- `git worktree list`
- `wt-status-all`
- pre-brainstorm / candidate / milestone / issue
- review / tests / implementation reality
- 是否已 merge / 是否该 cleanup

结果是：

- 有些树其实只该继续开发，不该强行关闭
- 有些树已可向上 merge，却没人把它纳入统一 closure plan
- 有些树已经 merge 但未 cleanup，治理未真正结束
- 有些树 candidate / issue 生命周期未闭环，却容易被误判为“完成”

## Scope

1. 扩展 `skill:worktree-maintenance-governance`，新增 `fleet_closure` 模式。
2. 定义项目级 fleet closure 的最小核查面：
   - git ancestry / clean / dirty
   - pre-brainstorm / candidate / milestone / issue lifecycle
   - review / tests / implementation reality
   - merge / cleanup readiness
3. 更新主管真源与首跳提示，让主管在“检查所有 worktree”场景优先走 `fleet_closure`。
4. 增加脚本级回归，锁住 `fleet_closure` 提示接线。
5. 产出一份当前仓库的 first-pass fleet inventory，证明该模式不是抽象设计。

## Acceptance

- `skill:worktree-maintenance-governance` 明确包含 `fleet_closure`
- `lead-agent`、`manager-agent`、`start-lead-agent.sh` 明确在“检查所有 worktree”场景使用该模式
- skill 明确“不是所有树都要同一轮关闭，但每棵树都要有 disposition / next_action / cleanup gate”
- `test-routing-foundation-loop` 锁定 `fleet_closure` 提示
- 当前仓库的 fleet inventory 至少完成首轮分类，并可支撑后续 merge / cleanup

## Completion

- `docs/system/workspace/skills/worktree-maintenance-governance/SKILL.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/references/fleet-closure.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/references/audit.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/references/retirement-handoff.md`
- `docs/system/workspace/agents/lead-agent.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `docs/epics/workspace-routing-foundation/worktree-fleet-governance-closure/code-reviews/20260321-worktree-fleet-governance-closure-verification.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`

## Next

- 本 issue 的模式与首轮 inventory 已完成，但最终 review 仍需跟上当前真实 fleet，而不是停留在旧的 `current sweep` 快照。
- `cli-first`、`manager-handoff` 已完成 closeout 且 worktree clean，当前是 `ready for manager merge`，但在被上游吸收前仍不能 cleanup。
- `manager-watchdog-trigger` worktree 也已 clean，并进入单独的 manager disposition；`runtime-worker-launch-linkage` 仍保持 `in_verification`。
- 本轮新增的 `protected-post-merge-acceptance-route-governance` 已正确回流到 pre-brainstorm，说明 `fleet_closure` 已把“当前 issue 之外的新治理缺口”重新路由，而不是硬塞回原 issue。
- 待 manager 完成剩余 worktree 的 merge / verification / cleanup 判断后，本 issue 才能从 `in_verification` 进入最终 promote / cleanup followthrough。
