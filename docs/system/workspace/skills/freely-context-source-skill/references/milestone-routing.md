# Milestone Routing

## Candidate issues

- 边界仍不稳、仍需研究：`freely-doc-B1_IBM-execution`
- candidate 已清晰且可 materialize：`freely-doc-B2_IBM-execution`

## Committed issues

- 缺 `b-issue/prd/pre-tests/tasks`：`freely-doc-B2_IBM-execution`
- docs 足够且 `phase_state` 为 `done_b2_ibm` 或 `in_dev`：`freely-dev-loop-execution`
- 若处于 `in_verification`：只做校验和回写，不重开实现

## Completed issues

- 不重复执行
- 仅做 completion verification、追溯或重新发现

## Required checks

- 不再只看泛化 `status`
- 必须结合 `phase_state` 判断是否期待 `progress`
- `milestone_state` 只表达队列归属，不替代执行阶段
