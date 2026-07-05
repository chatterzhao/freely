# Issue: deep-refactor-fleet-sequencing-governance

- issue_id: `I-20260326-1915`
- title: Deep-refactor fleet sequencing governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `deep-refactor-fleet-sequencing-governance`
- issue-name: `deep-refactor-fleet-sequencing-governance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/code-reviews`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260326-1825/candidates.md#c-20260326-1825-a`
- source_brainstorm: `docs/B1-docs/raw-20260326-1825/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/issues/ibm-pretests-executable-acceptance-quality-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-owner-stance-and-source-patrol-governance/issues/manager-owner-stance-and-source-patrol-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 在准备 broad/deep refactor 时，真实 fleet 一度同时存在：

- canonical `develop` runtime 标成 `desired=running`，但实际 `stalled_without_runtime`
- develop-facing merge-prep 工位仍是 `dirty + desired=running`
- 多棵 clean/stopped 上游治理树已经形成新 contract，却还没有先后顺序

如果不先冻结“大重构前先做 fleet sequencing audit”的开发治理规则，就会把 closeout、runtime 健康判断、upstream merge、以及新的重构实现混在一起，导致 owner、依赖和 cleanup judgement 继续失真。

## Scope

1. 把 pre-refactor sequencing audit 写进开发 Freely 的入口规则：
- 运行 `git worktree list --porcelain`
- 运行 `./bin/wt-fleet-status`
- 运行 `freely live-status --project <project-root>`
- 运行 `freely fleet-status --project <project-root>`
- 把结果与 `docs/milestones.md` / 相关 `progress` 对齐

2. 明确大重构前的优先顺序：
- 优先收束 `dirty` 或仍 `desired=running` 的工位
- 优先处理仍持有 canonical closeout / merge judgement 的工位
- 在新重构实现前，先吸收会被后续工作直接消费的上游治理树

3. 这条 issue 只改开发 Freely 的治理真源：
- `AGENTS.md`
- issue-bound 生命周期文档
- `docs/milestones.md`
- `docs/progress/**`

4. 不扩大 scope：
- 不把这条规则写进 `docs/system/**`
- 不新增 runtime / watchdog / scheduler 机制
- 不把所有 clean/stopped worktree 都误判成必须先完成

## Acceptance

- `AGENTS.md` 明确要求 broad/deep refactor 前先做 fleet sequencing audit。
- 规则明确要求对齐 `milestones` / `progress`，而不是只看 worktree 数量。
- 规则明确区分必须先收束的 `dirty/running/owner` 工位与可延后的 clean/stopped 工位。
- 当前 fleet 实际验证已完成：
  - develop 与相关 worktree 的假 `desired=running` 状态已显式停机
  - develop-facing merge-prep 工位已从 dirty 变为 clean
  - upstream governance merge-prep 工位已吸收三棵上游治理树并通过治理检查
- 新 wording 不把这条 sequencing gate 误写成 Freely 运行期能力 contract。

## Completion

- `AGENTS.md`
- `docs/B1-docs/raw-20260326-1825/brainstorms.md`
- `docs/B1-docs/raw-20260326-1825/candidates.md`
- `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/issues/deep-refactor-fleet-sequencing-governance.md`
- `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/brainstorms/b-deep-refactor-fleet-sequencing-governance.md`
- `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/prd.md`
- `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-deep-refactor-fleet-sequencing-governance.md`
- `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/code-reviews/20260326-deep-refactor-fleet-sequencing-governance-verification.md`
- `docs/milestones.md`

## Verification

- `git worktree list --porcelain`
- `./bin/wt-fleet-status`
- `freely stop --project /Users/zhaoyu/Downloads/code/my-freely/freely`
- `freely stop --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-scheduler-capacity-candidate-replay`
- `freely stop --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-develop-merge-prep-fleet-closure`
- `git -C /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-develop-merge-prep-fleet-closure status --short`
- `git -C /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260327-feature-upstream-governance-merge-prep rev-list --left-right --count develop...HEAD`
- `./bin/governance-check`

## Next

- 本条治理已经把 pre-refactor sequencing gate 固定到开发 Freely 的入口层。
- 后续若要把 sequencing judgement 自动化或 runtime-visible 化，应通过新的 lifecycle 承接，而不是扩大当前 planning truth scope。
