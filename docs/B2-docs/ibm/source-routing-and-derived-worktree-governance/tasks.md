# Tasks - source-routing-and-derived-worktree-governance

## T1 路由与来源分层
- 更新 `docs/PROJECT_INTENT.md`
- 更新 `docs/LAWS.md`
- 对齐来源分类、IBM 边界、progress 边界

## T2 Skill 情景化
- 更新 `context-source-skill`
- 更新 `doc-pre-brainstorm-execution`
- 更新 `doc-ibm-execution`
- 更新 `dev-loop-execution`
- 更新 `branch-management`
- 对齐 `lead-agent` 与 `workspace/tools.md` 的同工具第二跳协议

## T3 Worktree 引导
- 新增 `freely wt-create`
- 更新 `.githooks/pre-commit`
- 更新 `.githooks/post-checkout`
- 更新 `AGENTS.md`

## T4 目录归属治理
- 明确 IBM 产物路径为 `docs/epics/{epic-name}/{story-name}/...`
- 禁止 IBM 正式产物继续落在 `docs/B1-docs/raw-`

## T5 首跳执行闭环回归
- 更新 `workspace/scripts/start-lead-agent.sh`
- 更新 `workspace/scripts/tests/test-routing-foundation-loop`
- 锁住“同工具必须继续第二跳、不能只输出 next_prompt”
