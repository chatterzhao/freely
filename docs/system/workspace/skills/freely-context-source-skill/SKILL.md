---
name: freely-context-source-skill
description: >- 对当前输入做来源分层、可执行性判定、workspace 准备判断与下一跳组装。
  为 lead-agent 产出自治编排结果。

  Use when: lead-agent 需要判定输入来源和可执行性，决定下一跳。
  触发词："context source"、"来源判定"、"可执行性"、"输入分层"。
---

# skill:freely-context-source-skill

## 职责

- 把当前输入归类为 `discovery`、`milestone` 或 `continuation`。
- 在 `discovery` 里进一步区分 durable source family，至少覆盖 `human interruption` 与 `external issue`，并保持它们的消费/去重语义不混淆。
- 选择下一跳：`freely-doc-B1_IBM-execution`、`freely-doc-B2_IBM-execution`、`freely-dev-loop-execution`、`freely-worktree-maintenance-governance`、`freely-recovery-subagent-governance`，或显式返回 manager-owned 的 `completion_verification / cleanup_governance` 路由。
- 判断本轮是否需要先准备 dedicated worktree。

## 不负责

- 不直接执行 pre-brainstorm、IBM、dev-loop 主工作。
- 不替代 `freely-branch-management` 创建或清理 worktree。

## 最小输入

- `input_context`
- `manager-task-source-scan-latest.json`（若 runtime 已生成；优先把它当作结构化 patrol 输入，而不是先散读各处）
- `docs/PROJECT_INTENT.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/milestones.md`
- 按需读取相关 `B1-docs/issue/progress/recovery`

## 最小输出

- `source_class`
- `route_kind`
- `target_skill`
- `target_owner`
- `workspace_action`
- `execution_base`
- `integration_target`
- `depends_on`
- `session_evidence_refs`
- `next_prompt`

## 工作流

1. 若 runtime 已给出 `manager-task-source-scan-latest.json`，先消费其中的 `scan_reason`、`manager_context` 与 `surfaces/summary_lines/active_count`，把它当作 idle/replan patrol seed；但只把里面的状态当 advisory，后续必须回到 linked docs/evidence 做核对。
2. 再读取 [source-classification.md](references/source-classification.md) 判定输入属于哪一类来源。
3. 若命中 `discovery`，先判断它来自哪种 durable source family：
   - `human interruption`
   - `external issue`
   - 其它 discovery 信号仅作为临时分析来源，不应伪装成 durable external source lineage
4. 对 `external issue` family，必须保持这些边界：
   - raw source scan 只针对 open 且未被 canonical repo-native linkage 消费的 source issue
   - canonical linkage 比外部 labels/comments 更有决定性
   - `source issue` 是 intake lineage，不自动等于长期 public tracking surface
   - discard/accept 之后的 source closeout 由 canonical owner truth 决定，不由外部状态单独驱动
   - 若 `task-source-scan` 给出 `github_raw_issue` / `gitee_raw_issue`，默认把它当 fresh intake，下一跳优先是 `freely-doc-B1_IBM-execution`
   - 若 `task-source-scan` 给出 `github_linked_open_issue` / `gitee_linked_open_issue`，默认把它当已消费 lineage 的 drift / continuation signal；先回 canonical milestone / issue / progress truth，判断是 continuation、closeout drift，还是 publication linkage drift，而不是再新开一轮 intake
5. 若输入命中 milestone，读取 [milestone-routing.md](references/milestone-routing.md) 决定是继续 pre-brainstorm、进入 IBM、进入 dev-loop，还是仅做 completion verification。
6. 若输入来自 issue/progress/recovery 或系统监控，读取 [continuation-recovery-routing.md](references/continuation-recovery-routing.md) 判断是否必须先恢复，而不是直接继续原阶段。
7. 若 route 已经收敛为 `completion_verification` 或 `cleanup_governance`，优先返回 manager-owned route：
   - `target_owner=manager`
   - `target_skill` 可为空，或显式指向监督/维护类 skill
   - 不把这类判断伪装成新的 doc-loop / dev-loop
8. 若当前问题实质是 worktree merge / cleanup / retirement / fleet closure，优先返回 `freely-worktree-maintenance-governance`，而不是把它塞回 doc-loop / dev-loop。
9. 若本轮会写仓库，读取 [workspace-preparation.md](references/workspace-preparation.md) 产出 `workspace_action`、`execution_base`、`integration_target`、`depends_on`。
10. 返回下一跳所需的最小上下文包，不在本 skill 中直接修改长期产物。

## 完成判定

- 当前输入已被归类到正确来源层。
- 当前下一跳 skill 已明确。
- 若下一跳不是 worker 执行，而是 manager-owned verification / cleanup route，`target_owner` 已明确。
- 若本轮需要写入，worktree 准备动作与基线已明确。
- 对依赖未合并父分支的任务，已显式给出 derived worktree 判断结果。
