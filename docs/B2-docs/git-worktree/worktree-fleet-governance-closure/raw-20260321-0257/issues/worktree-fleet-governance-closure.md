# Issue: worktree-fleet-governance-closure

- issue_id: `I-20260321-0257`
- title: Worktree fleet governance closure
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `worktree-fleet-governance-closure`
- issue-name: `worktree-fleet-governance-closure`
- verification_artifact_dir: docs/B2-docs/git-worktree/worktree-fleet-governance-closure/raw-20260321-0257/code-reviews
- source_candidate: `docs/B1-docs/raw-20260321T170600Z/candidates.md#c-20260321-0257-a`
- source_brainstorm: `docs/B1-docs/raw-20260321T170600Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/B2-docs/git-worktree/worktree-maintenance-governance/issues/worktree-maintenance-governance.md`, `docs/B2-docs/ibm/stacked-worktree-merge-chain-governance/issues/stacked-worktree-merge-chain-governance.md`
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
- `docs/B2-docs/git-worktree/worktree-fleet-governance-closure/code-reviews/20260321-worktree-fleet-governance-closure-verification.md`
- `docs/B2-docs/git-worktree/worktree-fleet-governance-closure/code-reviews/20260326-worktree-fleet-governance-closure-canonical-replay-verification.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`

## Next

- 当前 `fleet_closure` 能力与 canonical inventory writeback 已完成。
- historical stable snapshot: authoritative fleet once stabilized at 4 retained worktrees with `feature/manager-scheduler-capacity-candidate-replay-20260324` as the remaining retained research owner while the candidate boundary was still unresolved.
- current canonical cleanup judgement has moved again:
  - protected/control: `develop`
  - historical retained research owner now superseded and delete-ready after canonical cleanup writeback: `feature/manager-scheduler-capacity-candidate-replay-20260324`
  - retired after absorption writeback: `feature/develop-merge-prep-fleet-closure-20260325`
- `feature/manager-scheduler-capacity-candidate-replay-20260324` should no longer be treated as active fleet truth. Its branch-local history is now only replay-owner provenance because canonical `develop` already records `C-20260323-2045-A` as absorbed supporting evidence; if future scheduler work is needed, it must open a new lifecycle instead of reviving this replay owner.
