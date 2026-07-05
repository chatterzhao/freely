# Candidates

- capability: chat entrypoint autobootstrap
- owner_loop: auto-loop runtime
- primary_surface: `freely chat`, `freely tui`
- internal_primitive: `freely intake chat`
- canonical_artifact: `docs/system/workspace/scripts/runtime/freely`
- promoted_issue_path: pending://chat-entrypoint-autobootstrap
- milestone: pending://interruption-entrypoint-ready-without-manual-start
- session_refs: []
- validation:
  - `freely chat` auto-starts dispatcher when runtime is down
  - `freely tui --once` auto-starts dispatcher when runtime is down
  - interruption item gets claimed/triaged after auto bootstrap
