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

- 本 issue 的模式与首轮 inventory 已完成；当前 followthrough 只剩把 disposition 写回到最新 4-tree fleet truth，并继续守住 retained-vs-retired judgement。
- 当前 authoritative fleet 已收缩到 4 棵 retained worktree；本轮 writeback 提交后，`./bin/wt-status-all` 与 `./bin/wt-fleet-status` 应回到 `Summary: total=4, dirty=0` 且全部 worktree 都显式 `stopped`。
- 当前 fleet 的有效分层如下：
  - protected/control: `develop`, `pre-test-merge`
  - retained research owner: `feature/manager-scheduler-capacity-candidate-replay-20260324`
  - active develop-facing absorption owner: `feature/upstream-governance-merge-prep-20260327`
  - retired after absorption writeback: `feature/develop-merge-prep-fleet-closure-20260325`
- `feature/develop-merge-prep-fleet-closure-20260325` 已被 `feature/upstream-governance-merge-prep-20260327` 完整吸收：`git merge-base --is-ancestor feature/develop-merge-prep-fleet-closure-20260325 HEAD` 返回成功，且 `feature/develop-merge-prep-fleet-closure-20260325...HEAD = 0/26`；随后对应 worktree 与 local branch 均已删除。因此它不再属于 current fleet，只保留为 closeout provenance。
- `feature/manager-scheduler-capacity-candidate-replay-20260324` 仍保留 `needs_research / retained-with-reason`：相对当前 absorption owner 仍有未吸收的本地 commits（`feature/manager-scheduler-capacity-candidate-replay-20260324...HEAD = 24/266`），因此本轮不能把它误判成可直接退休的 superseded tree。
- 待当前 absorption owner 把 develop-facing promote / replay judgement 写回并继续守住 retained research owner 的边界后，本 issue 才能从 `in_verification` 进入最终 promote / cleanup followthrough。
