# Coordination Contract (single page)

机器可读真源：`contract.yaml`（JSON 兼容 YAML 1.2 子集，`json.loads` 可读）。
本页列出 agent 协调的合法值；新增 reason 只需改契约 + `coordination/input_required_reason.py` 一处枚举（diff ≤2 文件）。

## Task 状态机

- `submitted`
- `working`
- `input-required`
- `completed`
- `failed`
- `canceled`
- `unknown`

## Input-required reasons

- `needs-review:b1`
- `needs-review:b2`
- `needs-review:dev`
- `needs-review:red`
- `needs-review:test`
- `needs-review:gate`
- `needs-manager-decision`
- `needs-worker-retry`
- `needs-manager-scope`
- `needs-worker-task`
- `needs-human-input`
- `unknown`

## SSE topics

- `input_required`
- `task_state_update`
- `stream_task`
- `resubscribe`

## Exit contract 合法值

- `delegate_workers` — submitted worker tasks exist -> delegate before exit
- `no_recovery` — no pending work, normal exit
- `degraded_no_recovery` — degraded runtime with no self-recovery (#4157)

## 来源

- task_states: a2a_task.py normalize_state (A2A standard states)
- input_required_reasons: scripts/runtime/coordination/input_required_reason.py (moved out of agents/)
- sse_topics: watchdog_sse.py / a2a_server.py SSE event names
- exit_contracts: runtime/freely manager_exit_contract_kind() + a2a-exit exit_kind

## 边界

`scripts/runtime/coordination/` 不得反向 import `runtime/freely`；`watchdog_sse.py` 不得再把 `agents/` 注入 `sys.path`。由 `bin/check-coordination-contract` 守护。
