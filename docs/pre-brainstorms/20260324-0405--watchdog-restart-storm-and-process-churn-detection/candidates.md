# 候选：watchdog-restart-storm-and-process-churn-detection

- id: `C-20260324-0405-A`
- title: Watchdog restart-storm and process-churn signal implementation
- source_brainstorm: `docs/pre-brainstorms/20260324-0405--watchdog-restart-storm-and-process-churn-detection/brainstorms.md`
- status: `materialized`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/watchdog-restart-storm-and-process-churn-governance/issues/watchdog-restart-storm-and-process-churn-governance.md`
- legacy_id_mapping: I-20260324-0405  # 历史遗留的 issue id
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- why_now:
  - 三个 loop 的 active truth 已明确 watchdog 只能暴露 churn signal、主管负责 dead-loop / thrash 裁决
  - 真实 runtime 仍未实现短窗口 launch/restart/process-count signal，存在“盲重启掩盖死循环”的风险
- expected_outcome:
  - define the runtime-visible signal contract for restart storms and process churn
  - define the minimal manager-owned judgement handoff after signal emission
  - prepare a dedicated implementation issue instead of hiding the gap inside wording-only refactors
- current_contract:
  - raw signal truth should live in `session-state.env`
  - manager continuity should only carry the governance judgement triggered by the signal
  - `live-status` / `fleet-status` should expose the signal as derived observability, not as a separate source of truth
  - `workcell-state.env` should not mirror restart-storm/process-churn counters
  - watchdog should stop blind relaunch after signal and enter low-frequency observation while waiting for manager judgement
  - manager continuity should carry signal refs plus `ownership/restart_point/next_action`, not duplicate raw counters
  - stall detection and restart-storm detection should remain separate contracts: stall for live-but-not-advancing AI; restart storm for short-window exit/relaunch churn
  - provisional defaults: `RESTART_STORM_WINDOW_SECS=30`, `RESTART_STORM_COUNT=4`, `PROCESS_CHURN_PEAK=3`
- decision_reason:
  - 这是 runtime/watchdog 实现缺口，不是当前三个 loop 语义重构 issue 的附带 patch
  - 但它又已经被 active truth 明确依赖，不能继续只停留在口头 follow-on
- next_action:
  - 已 materialize；下一步进入 dev，实现 runtime signal、status surface 与 escalation followthrough
- promotion_gate:
  - signal truth surface frozen
  - manager escalation path frozen
  - watchdog pause/retry rule frozen
  - `live-status` / `fleet-status` exposure shape frozen
  - stall coexistence frozen
  - counter/window default contract frozen
- open_questions:
  - `live-status` / `fleet-status` 是输出原始计数，还是输出摘要+deep refs
  - runtime tests 是按 manager/worker 分别覆盖，还是先做 shared helper fixture
- revisit_trigger:
  - 需要真正修改 `runtime/freely` 与 watchdog scripts 时
  - 或再次观察到短窗口反复拉起 AI 进程却缺少 manager-level judgement
