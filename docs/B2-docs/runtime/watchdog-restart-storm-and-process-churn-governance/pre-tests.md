# Pre-Tests: watchdog-restart-storm-and-process-churn-governance

1. 只读 issue / PRD / IBM brainstorm 时，能明确看出：
   - 原始 signal 真相面是 `session-state.env`
   - `workcell-state.env` 不镜像 churn 计数
   - stall 与 restart storm 是分开的判定面
2. 只读 `watchdog-control-plane/SKILL.md` 与 `auto-loop-orchestrator/SKILL.md` 时，能看出：
   - watchdog 只暴露 signal
   - dead-loop / thrash 裁决仍归 manager `auto-loop`
3. runtime 测试需要覆盖：
   - signal emission into `session-state.env`
   - no mirror into `workcell-state.env`
   - low-frequency observe after signal
   - manager escalation handoff after signal
4. `live-status` / `fleet-status` 验证需要覆盖：
   - signal 可见
   - 输出不要求原样展开全部计数文件，但必须能给出摘要与 deep refs
