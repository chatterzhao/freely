# Source Classification

## Rules

- `source_class=discovery`
  - `PROJECT_INTENT`
  - chat / session evidence
  - test
  - code-review
  - github-issue
  - 治理漂移
  - 新运行时异常
- `source_class=milestone`
  - `docs/milestones.md` 中的 `candidate_issues` / `committed_issues` / `completed_issues`
- `source_class=continuation`
  - issue
  - `docs/progress/**`
  - `docs/recovery/**`
  - 系统监控命中的活跃执行上下文

## Output hints

- `discovery` 通常先去 `doc-pre-brainstorm-execution`
- `milestone` 需要再看队列和 `phase_state`
- `continuation` 需要再看 docs 完整度、`phase_state`、`runtime_state` 与恢复证据
