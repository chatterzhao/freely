# PRE_TEST - source-routing-and-derived-worktree-governance

## Baseline Checks

1. 原始发现源进入 `doc-pre-brainstorm-execution` 时，必须要求 candidate + milestone 原子同步。
2. `milestone.candidate_issues` 不能被直接路由为 dev-loop。
3. `doc-ibm-execution` 在 `epic-name/story-name/issue-name` 未稳定前，不得写正式 IBM 产物。
4. `progress` 语义必须只指向 dev-loop 执行态。
5. `freely wt-create` 必须支持默认 `develop` 和显式 `--base <parent-feature>`。
6. hook 文案必须与派生 worktree 口径一致。
7. 首跳 prompt 必须显式禁止“只输出 `next_prompt` 就结束”。
8. 若 `selected_tool == AI_TOOL`，首跳协议必须要求当前会话继续执行第二跳。
