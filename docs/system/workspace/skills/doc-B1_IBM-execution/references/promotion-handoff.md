# Promotion Handoff

## Promotion checks

- candidate 已具备进入 issue-bound IBM 的条件
- `milestone` 不再是 `pending://milestone-binding`
- 当前 `C-{issue-id}` 已经先在 milestone 中取得 `M-{issue-id}` 候选位
- 若 issue 归属已明确，回填 `promoted_issue_path`
- handoff 必须保留同一个 `{issue-id}`，供 IBM 物化成一个或多个 `I-{issue-id}*`

## Output

- `status=completed`
- `next_recommended_route=doc-B2_IBM-execution`
- 最小 issue 上下文摘要

## Anti-patterns

- 不要把 `promoted` 长期留在 `pending://issue-materialization`
- 不要让 `C-{issue-id}` 跳过 milestone 候选位，直接伪装成正式 IBM issue
- 不要在 pre-brainstorm 中直接写正式 IBM 产物
