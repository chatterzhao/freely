# IBM Brainstorm: worker-active-reentry-for-manager-delegated-continuation-governance

## Decision

不新增新的 manager 逻辑分支，直接把修复落在 `launch_worker_from_manager_prompt_if_needed()`：

- 先写 delegated intake；
- 解析出 intake id；
- 若目标 worker 已有 active supervisor + AI，则触发 local continuation reentry；
- 否则继续现有 bootstrap + supervisor start。

## Why this shape

- 问题发生点就在 manager->worker launch linkage；
- `request_local_continuation_reentry` 已经存在，且语义正确；
- 这属于 runtime-owned reentry，不是 manager prompt 设计问题。
