# Code Review: cli-first-entrypoint-and-observability-surface-unification

## Scope

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- `docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`

## Findings

- `chat` 与 `tui` 现在通过同一个 high-level submit helper 进入 runtime，避免了两套 post-submit 语义漂移。
- `tui` 现在也能触发与 `chat` 相同的 worker continuation reactivation gate。
- 三层 loop 与 auto-loop 真源已经明确：
  - `freely` 是唯一 front-door command
  - CLI status family 是 canonical backend interface
  - TUI/GUI 只应复用，不另造业务语义

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- `bash docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
- `./bin/governance-check`

## Result

- pass
