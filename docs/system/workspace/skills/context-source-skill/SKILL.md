---
name: context-source-skill
description: 对当前输入做来源分层、可执行性判定、workspace 准备判断与下一跳组装，为 lead-agent 产出自治编排结果。
---

# skill:context-source-skill

## 职责

- 把当前输入归类为 `discovery`、`milestone` 或 `continuation`。
- 选择下一跳：`doc-pre-brainstorm-execution`、`doc-ibm-execution`、`dev-loop-execution` 或 `recovery-subagent-governance`。
- 判断本轮是否需要先准备 dedicated worktree。

## 不负责

- 不直接执行 pre-brainstorm、IBM、dev-loop 主工作。
- 不替代 `branch-management` 创建或清理 worktree。

## 最小输入

- `input_context`
- `docs/PROJECT_INTENT.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/milestones.md`
- 按需读取相关 `pre-brainstorms/issue/progress/recovery`

## 最小输出

- `source_class`
- `route_kind`
- `target_skill`
- `workspace_action`
- `execution_base`
- `integration_target`
- `depends_on`
- `session_evidence_refs`
- `next_prompt`

## 工作流

1. 先读取 [source-classification.md](references/source-classification.md) 判定输入属于哪一类来源。
2. 若输入命中 milestone，读取 [milestone-routing.md](references/milestone-routing.md) 决定是继续 pre-brainstorm、进入 IBM、进入 dev-loop，还是仅做 completion verification。
3. 若输入来自 issue/progress/recovery 或系统监控，读取 [continuation-recovery-routing.md](references/continuation-recovery-routing.md) 判断是否必须先恢复，而不是直接继续原阶段。
4. 若本轮会写仓库，读取 [workspace-preparation.md](references/workspace-preparation.md) 产出 `workspace_action`、`execution_base`、`integration_target`、`depends_on`。
5. 返回下一跳所需的最小上下文包，不在本 skill 中直接修改长期产物。

## 完成判定

- 当前输入已被归类到正确来源层。
- 当前下一跳 skill 已明确。
- 若本轮需要写入，worktree 准备动作与基线已明确。
- 对依赖未合并父分支的任务，已显式给出 derived worktree 判断结果。
