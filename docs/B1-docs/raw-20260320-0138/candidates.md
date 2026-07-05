# Candidates

- capability: interruption entrypoint runtime preflight
- owner_loop: auto-loop runtime
- primary_surface: `freely chat`, `freely tui`
- non_goal_surface: `freely intake chat`
- canonical_artifact: `docs/system/workspace/scripts/runtime/freely`
- promoted_issue_path: pending://runtime-entrypoint-preflight
- milestone: pending://interruption-entrypoint-runtime-ready
- session_refs: []
- validation:
  - `freely chat` fails when neither supervisor nor dispatcher is running
  - `freely tui` fails when neither supervisor nor dispatcher is running
  - `freely intake chat` still succeeds offline
  - `freely chat` / `freely tui` succeed when dispatcher is ready
