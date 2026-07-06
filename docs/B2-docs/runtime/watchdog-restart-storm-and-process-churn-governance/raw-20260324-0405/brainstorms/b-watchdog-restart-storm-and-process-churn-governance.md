# IBM Brainstorm: watchdog-restart-storm-and-process-churn-governance

## Focus

把 pre-brainstorm 已冻结的治理边界翻译成可执行的 runtime 实现范围，避免在 dev 中重新发明真相面。

## Frozen Inputs

- 原始 signal 真相面：`session-state.env`
- `workcell-state.env` 不镜像 restart-storm / process-churn 计数
- stall 与 restart storm 各判各的
- watchdog 命中 signal 后停止 blind relaunch，进入低频观察并触发 manager escalation
- manager continuity 只写 signal ref 与 followthrough judgement
- 默认阈值：
  - `RESTART_STORM_WINDOW_SECS=30`
  - `RESTART_STORM_COUNT=4`
  - `PROCESS_CHURN_PEAK=3`

## Dev Translation

1. runtime 需要新增短窗口计数与峰值记录 helper
2. `write_session_state` 需要扩展 churn signal 字段
3. `live-status` / `fleet-status` 需要展示 churn signal 摘要
4. supervisor restart loop 需要在 signal 命中后改走 escalation，而不是继续 blind relaunch
5. 相关 tests 需要覆盖：
   - signal emission
   - no-mirror into `workcell-state.env`
   - manager escalation handoff
   - low-frequency observe instead of repeated relaunch

## Remaining IBM Notes

- `live-status` / `fleet-status` 暴露格式保留“摘要 + deep refs”方向，不在这里扩 UI/TUI/API。
- tests 先以 shared helper + manager/worker 代表性用例组合收口，不先追求全矩阵铺满。
