# Tasks: runtime-human-readable-time-display-governance

- Materialize the runtime/workspace time-display owner from the absorbed pre-brainstorm.
- Add or reuse a shared display formatter for human-facing runtime status surfaces.
- Route `freely live-status`, `baseline-status`, intake status, and `develop-push status` through the formatter.
- Preserve raw stored truth while adding human-readable sibling fields where needed.
- Verify ai-cli and watchdog cooldown displays still follow the same host-local rule.
- Consolidate runtime-side "current time" call sites onto one local-display helper and one UTC machine-truth helper.
- Write back issue, progress, milestone, and verification evidence.
