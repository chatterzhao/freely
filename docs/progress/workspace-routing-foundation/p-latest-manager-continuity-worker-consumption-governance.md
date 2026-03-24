# Progress: latest-manager-continuity-worker-consumption-governance

- issue_id: `I-20260322-0445`
- phase_state: `in_progress`
- summary: `pre-test-merge` dogfood 继续暴露 latest continuity consumption gap：prompt target header 已修通，但 manager stop/restart 后旧的 `manager-worker-launch-state.env` 仍会把 prompt 视为已消费，导致没有活跃 worker 时也不会从同一 continuity 重新 launch。
- current_focus:
  - keep latest continuity / prompt target contract stable across both machine-readable headers and natural-language compatibility
  - make stale consumed launch-state recoverable when target worker is no longer running
  - re-run dogfood after merge to verify latest continuity can re-launch stopped worker runtimes without minting a new continuity first
