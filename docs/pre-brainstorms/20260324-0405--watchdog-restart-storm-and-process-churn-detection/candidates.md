# 候选：watchdog-restart-storm-and-process-churn-detection

- id: `C-20260324-0405-A`
- title: Watchdog restart-storm and process-churn signal implementation
- source_brainstorm: `docs/pre-brainstorms/20260324-0405--watchdog-restart-storm-and-process-churn-detection/brainstorms.md`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://watchdog-restart-storm-and-process-churn-signal-materialization`
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
- decision_reason:
  - 这是 runtime/watchdog 实现缺口，不是当前三个 loop 语义重构 issue 的附带 patch
  - 但它又已经被 active truth 明确依赖，不能继续只停留在口头 follow-on
- next_action:
  - 继续 pre-brainstorm，先冻结 signal truth surface、window/counter shape、watchdog pause rule 与 manager escalation path，再决定是否 materialize 为独立 issue
- revisit_trigger:
  - 需要真正修改 `runtime/freely` 与 watchdog scripts 时
  - 或再次观察到短窗口反复拉起 AI 进程却缺少 manager-level judgement
