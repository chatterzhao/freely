# Progress: watchdog-restart-storm-and-process-churn-governance

- issue: `I-20260324-0405`
- title: Watchdog restart-storm and process-churn governance
- phase_state: `done_ibm`
- summary: 已把 watchdog restart-storm / process-churn 缺口从 pre-brainstorm materialize 成正式 issue，冻结了 signal 真相面、manager escalation 边界、stall 分离语义与默认阈值；下一步进入 dev，实现 runtime signal 与 status surface 暴露。
- completed:
  - freeze raw signal truth in `session-state.env`
  - freeze no-mirror rule for `workcell-state.env`
  - freeze manager-owned judgement contract
  - freeze default thresholds
- next:
  - implement runtime helpers and session-state fields
  - expose signal in `live-status` / `fleet-status`
  - add tests for signal emission and escalation
