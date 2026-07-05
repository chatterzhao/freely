# Pre-Tests: application-native-runtime-observation-contract-and-observability-planes

1. 只读 issue / PRD / IBM brainstorm 时，能明确看出：
   - artifact plane 是 `acceptance evidence` 的 canonical truth surface
   - current-state / fleet / API 只镜像最小摘要与 `acceptance_ref`
   - `progress signal`、`stall signal`、`acceptance evidence` 三类 schema 职责分离
2. 只读 `three-loop-capability-lifecycle`、`multi-worktree-supervision`、`watchdog-control-plane` 真源时，能明确看出：
   - `auto-loop` 负责基于 evidence 做完成/cleanup judgement
   - progress/stall 观察面只提供信号，不直接自裁决完成
3. contract review 需要覆盖：
   - CLI / TUI / GUI / API 共享同一组最小 `deep ref groups`
   - richer surface 只能扩展不能替换
4. Freely self-host concrete profile 需要覆盖：
   - `live-status`
   - `fleet-status`
   - session jsonl / cycle log
   - continuity / prompt / verification artifacts
5. 后续 dev 必须验证：
   - machine-readable minimum fields 已写入 active truth / runtime-facing contract
   - issue completion judgement 与 delete gate 不再靠分散口头规则
