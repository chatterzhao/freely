# 候选：deep-refactor-fleet-sequencing

- id: `C-20260326-1825-A`
- title: 大重构前的 fleet sequencing audit 与 upstream merge order
- source_brainstorm: `docs/pre-brainstorms/20260326-1825--deep-refactor-fleet-sequencing/brainstorms.md`
- status: `candidate`
- adoption_type: `planning_truth`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/issues/deep-refactor-fleet-sequencing-governance.md`
- legacy_id_mapping: I-20260326-1915  # 历史遗留的 issue id
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- decision_reason:
  - 这次问题首先是开发 Freely 期间的 sequencing / planning gate，不是已经稳定到应进入 `docs/system/**` 的产品能力。
  - 当前最需要的是把大重构前的 worktree 顺序、阻塞项与 upstream merge order 写成开发期真源，避免在 fleet 状态模糊时直接开深层重构。
  - 若后续反复出现同类问题，再将其 materialize 为独立治理 issue；当前不应跳过 planning 直接改 runtime / capability 真源。
- scope:
  - 盘点所有现有 worktree、runtime 状态与 dirty owner
  - 区分必须先收口的 `dirty/running` 工位与可延后的 clean/stopped 工位
  - 明确 upstream governance merge order，避免大重构继续消费旧 contract
  - 把最小 sequencing gate 写回开发 Freely 的入口指引
- why_now:
  - canonical `develop` 当前 `activity_state=stalled_without_runtime`
  - `feature/develop-merge-prep-fleet-closure-20260325` 是唯一 `dirty + desired=running` 的 closeout owner
  - 多棵 `20260326` clean/stopped 治理树已经形成上游 contract，但尚未统一判断哪些必须先合并给后续工作消费
- sequencing_recommendation:
  1. `feature/develop-merge-prep-fleet-closure-20260325`
  2. `develop` manager runtime health / intentional freeze judgement
  3. `feature/ibm-pretests-integration-acceptance-quality-20260326`
  4. `feature/manager-owner-stance-and-source-patrol-20260326`
  5. `feature/freely-layered-architecture-and-tooling-topology-20260326` if the refactor touches root development truth
  6. dedicated deep-refactor implementation worktree
- non_blocking_trees:
  - `feature/closeout-canonical-replay-20260326`
  - clean/stopped watchdog companion worktrees already absorbed by `develop`
  - `pre-test-merge`
- acceptance_reviews:
  - reviewer: `codex`
    mode: `fresh-process candidate acceptance review`
    summary: `The sequencing gap has already produced concrete fleet drift and now has a stable smallest fix: a pre-refactor audit gate plus explicit upstream merge ordering in development governance.`
    verdict: `ready_to_materialize`
- next_action:
  - materialize 成独立治理 issue，冻结 AGENTS-level pre-refactor sequencing gate、issue-bound IBM 文档与 verification evidence
  - 保持 scope 在开发 Freely 的治理真源，不把这条 planning gate 误写进 `docs/system/**`
- revisit_trigger:
  - 当再次出现多棵 dirty/running/closeout owner 与上游治理树同时并存、且团队准备开 broad/deep refactor 时，重新检查是否需要独立治理 issue 或更高等级规则
- promoted_issue_id: `I-20260326-1915`
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
