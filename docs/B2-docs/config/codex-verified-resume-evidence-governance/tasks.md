# Tasks: codex-verified-resume-evidence-governance

## IBM-complete decomposition

- [x] Prove the field problem is real
  - capture the invalid target chain from canonical `develop`
  - reproduce the bad target outside Freely in an isolated worktree
- [x] Bound the issue narrowly
  - keep auth/watchdog and observability surfaces out of scope
  - keep the first owner issue `codex`-scoped
- [x] Freeze the acceptance boundary
  - healthy rollout-backed `resume` must survive
  - session-id-only false positives must downgrade
- [x] Define the test-first path
  - add a focused false-positive regression before broad refactor

## Dev-loop slices

- [x] Update `docs/system/workspace/scripts/runtime/freely`
  - stop elevating session-id-only evidence into resumable truth on the proven codex path
- [x] Update focused runtime tests
  - cover invalid `session_id` with missing rollout/jsonl
  - keep valid rollout-backed `resume` green
- [x] Run governance and focused regressions
  - confirm no regression to auth/watchdog semantics

## Verification

- [x] Write feature verification artifact on the canonical merge-prep branch
- [x] Keep duplicate closeout lanes out of the active absorption path
