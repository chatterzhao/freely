# Code Review: chat-triggered-worker-runtime-reactivation-governance verification
- issue_id: `I-20260321-1706`

- date: `2026-03-21`
- reviewer: `codex`
- status: `pass`

## Verification Notes

- `freely chat` 现在在 interruption classification 之后会执行 worker-runtime reactivation preflight。
- 只有以下条件同时满足时才自动拉起：
  - 当前工位角色是 worker
  - `DESIRED_RUNTIME_STATE=stopped`
  - `LAST_EXIT_REASON=operator_stop`
  - 当前没有 active supervisor / ai
  - intake 中存在当前工位的 delegated `handoff://continuation` / `handoff://verification`
- `auth_failure` 与 active AI present 仍不会自动拉起。

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
- `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- `bash -n docs/system/workspace/scripts/runtime/freely docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
- 2026-03-21 real dogfood:
  - `freely stop --project <worker-worktree>`
  - `freely chat --project <worker-worktree> "...当前工位 continuation...请按新的 worker reactivation gate 重新拉起并继续推进"`
  - `freely live-status --project <worker-worktree>`
  - observed:
    - `chat-triggered worker runtime reactivation started`
    - `activity_state: ai_active`
    - `desired_runtime_state: running`
    - active supervisor and AI process present
