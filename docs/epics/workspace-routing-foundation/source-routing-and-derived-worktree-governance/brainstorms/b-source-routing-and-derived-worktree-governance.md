# IBM Brainstorm: source-routing-and-derived-worktree-governance

## Goal

把这轮关于来源分层、milestone-owned issue、progress 边界、derived worktree、自举 worktree 时机、IBM 正式目录归属的讨论，收敛成正式 issue-bound 产物。

## Decisions

1. 原始发现源、编排来源、延续来源必须分层。
2. candidate 先进入 milestone，再进入 IBM。
3. `IBM` 的 `I` 是 milestone-owned issue。
4. `progress` 只跟踪 dev-loop。
5. pre-brainstorm 写入应发生在合适的 dedicated worktree。
6. derived worktree 默认允许，但必须显式记录 `execution_base / integration_target / depends_on`。
7. IBM 正式产物必须落在 `docs/epics/{epic-name}/{story-name}/...`。

## Open Questions

1. 是否需要把 workspace / branch / worktree 明确升级成统一的“执行产物”类别。
2. milestone 中 `candidate_issues` 与 `committed_issues` 的升级条件是否还需进一步标准化。
3. 是否要为 derived worktree 补一份专门的恢复/续接模板。

## Current Route

- 当前 issue 已完成 candidate -> milestone 承接。
- 当前正在 IBM 环内落正式 issue-bound 产物。
- 下一步继续补齐 `prd.md`、`pre-tests.md`、`tasks.md`。
