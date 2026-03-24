# Progress: latest-manager-continuity-worker-consumption-governance

- issue_id: `I-20260322-0445`
- phase_state: `in_progress`
- summary: `pre-test-merge` dogfood 继续暴露 latest continuity consumption gap：旧的 consumed launch-state 已能恢复，但 delegated continuation consumed truth 仍只在 cycle completion 后落盘，导致 AI 活跃期间 `live-status` 仍把已注入当前 prompt 的 handoff 误报成 pending。
- current_focus:
  - persist delegated continuation consumed truth at prompt-build time, not only after cycle exit
  - hide prompt-consumed delegated ids from active pending views while the current AI prompt is still running
  - keep failure recovery intact by letting the same ids surface again once the active AI exits
