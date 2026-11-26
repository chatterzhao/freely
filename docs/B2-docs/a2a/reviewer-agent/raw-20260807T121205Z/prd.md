# PRD: reviewer assign FAIL-CLOSED missing raw_key in SSE event

- issue_id: I-20260807T121205Z-A

## Goal

让 worker 在阶段审查点发出的 `input-required / needs-review:<phase>` 状态转换，
经由 `state_update` SSE 事件把 `raw_key` 送到 watchdog，使 reviewer 能被正确分配；
当 `raw_key` 确实无法解析时保持 fail-closed，绝不静默放行。

## 实现方案

1. 在 `docs/system/workspace/scripts/runtime/a2a_task.py` 的 a2a-exit 更新分支
   增加一个纯函数，构造 PATCH 字段：
   - 常规字段：state / summary / next / evidence / reason（行为不变）；
   - 当 `state == "input-required"` 且 `reason` 以 `needs-review:` 开头时，
     从 `--raw-key` 解析；缺省时按 `--task-id` 回读任务记录的 `raw_key`；
   - 两者都为空 → 抛出明确的 fail-closed 错误，CLI 输出 `ok:false` 且不发 PATCH。
2. `a2a_server.py` PATCH handler 会把 body 中的 `raw_key` 原样带入
   `state_update` SSE payload，因此上游补齐字段即可让下游 reviewer 路由恢复。
3. `watchdog_sse.py` 的 `FAIL-CLOSED: missing raw_key for reviewer assign` 断言
   保持不变——它是最后一道防线，不允许降级为 fail-open。

## Dev-Loop Handoff

- 唯一改动文件：`docs/system/workspace/scripts/runtime/a2a_task.py`
- 新增 AT：`docs/system/workspace/scripts/tests/test-reviewer-assign-raw-key.py`
- AT 注册：`bin/test-all` 的 CORE 与 CI_CORE 两个列表
- RED：`python3 ... test-reviewer-assign-raw-key.py --source-dir <develop root>`
- GREEN：同一命令 `--source-dir <fix worktree>`
