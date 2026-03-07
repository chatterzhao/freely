# Issue: source-routing-and-derived-worktree-governance

- issue_id: `I-20260307-1201`
- title: 源分类、milestone-owned issue 与派生 worktree 路由治理
- status: in_progress
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `source-routing-and-derived-worktree-governance`
- issue-name: `source-routing-and-derived-worktree-governance`
- source_candidate: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/candidates.md#c-20260307-1201`
- source_brainstorm: `docs/pre-brainstorms/20260307-0930--source-routing-and-derived-worktree-governance/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `none`

## Why

收紧 Freely 自举时的整体路由逻辑，确保：
- 问题来源分层清晰
- candidate 必须进入 milestone 后再进入 IBM
- `IBM` 只处理 milestone-owned issue
- `progress` 只跟踪 dev-loop 执行态
- 依赖未合并父分支的子任务可以使用 derived worktree
- skill 以情景步骤而不是抽象约束来指导 AI 执行

## Scope

1. 更新路由与边界治理文档。
2. 更新 `context-source-skill`、`doc-pre-brainstorm-execution`、`doc-ibm-execution`、`dev-loop-execution`、`branch-management`。
3. 增加标准 worktree 创建入口 `./bin/wt-create`。
4. 更新 hook / AGENTS 提示，使其支持 derived worktree 语义。
5. 明确 IBM 正式产物目录必须在 `docs/epics/{epic-name}/{story-name}/...`。

## Acceptance

- `LAWS` 和 `PROJECT_INTENT` 对来源分层、IBM 边界、progress 边界、derived worktree 口径一致。
- 核心 skills 以“情景 -> 动作 -> 产物 -> 下一跳”表达。
- `doc-pre-brainstorm-execution` 明确 pre-brainstorm 应在合适 worktree 中写入。
- `doc-ibm-execution` 明确先确定 `epic-name/story-name/issue-name`，再写正式 IBM 产物。
- `./bin/wt-create` 可支持默认基线和 `--base` 派生基线。

## Next

- 继续收敛 `prd.md`、`pre-tests.md`、`tasks.md`，使该 issue ready for后续治理/实现工作。
