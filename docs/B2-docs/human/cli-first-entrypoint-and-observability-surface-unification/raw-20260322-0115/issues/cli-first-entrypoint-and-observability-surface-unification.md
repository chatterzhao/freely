# Issue: cli-first-entrypoint-and-observability-surface-unification

- issue_id: `I-20260322-0115`
- title: CLI-first entrypoint and observability surface unification
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `cli-first-entrypoint-and-observability-surface-unification`
- issue-name: `cli-first-entrypoint-and-observability-surface-unification`
- verification_artifact_dir: docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/raw-20260322-0115/code-reviews
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260322T071500Z/candidates.md#c-20260322-0115-a`
- source_brainstorm: `docs/B1-docs/raw-20260322T071500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/raw-20260322-0115/verification/pre-tests.md
- depends_on:
  - `docs/B2-docs/ibm/default-project-resolution-and-authorized-project-memory/issues/default-project-resolution-and-authorized-project-memory.md`
  - `docs/B2-docs/human/chat-triggered-worker-runtime-reactivation-governance/raw-20260321-1706issues/chat-triggered-worker-runtime-reactivation-governance.md`
  - `docs/B2-docs/ibm/baseline-status-command-and-status-family-governance/issues/baseline-status-command-and-status-family-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://current-thread", role: "author"}

## Why

Freely 已经有：

- `freely start`
- `freely chat`
- `freely tui`
- `freely live-status / baseline-status / fleet-status`

但当前仍缺少一条明确的 canonical contract：

1. 用户应只把 `freely` 当作正式前台命令，而不是在外部 AI 工具 TUI 与 Freely 之间切换。
2. `chat` 是高层 human entrypoint，但 `tui` 还没有严格复用同一条 post-submit runtime chain。
3. CLI status family 已形成 backend 可观测面，但尚未被明确为未来 TUI/GUI 的 canonical backend interface。

## Scope

1. 冻结 `freely` 作为唯一正式 front-door CLI 的语义。
2. 把 `chat` 与 `tui` 的提交后链路统一为同一个 high-level submit contract。
3. 明确 CLI status family 是未来 TUI/GUI 的 canonical backend interface。
4. 保持外部 AI 工具只作为后台 adapter，而不是人类主操作面。

## Acceptance

- `freely chat` 与 `freely tui` 通过同一个 high-level submit helper 进入 runtime
- `tui` 提交后也会执行与 `chat` 同等的：
  - interruption bootstrap
  - dispatcher ensure
  - worker runtime reactivation gate
- truth sources 明确：
  - `freely` 是唯一正式 front-door command
  - TUI/GUI 是同一 backend contract 的渲染层
- regression 覆盖 `tui` 的 worker reactivation 路径

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- `docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/progress/workspace-routing-foundation/p-cli-first-entrypoint-and-observability-surface-unification.md`
- `docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/raw-20260322-0115code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- `bash docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`

## Closure Evidence

- `develop` 已包含 `0681fba docs: close out cli-first observability unification`，当前 `git branch --contains 0681fba` 解析到 `develop`
- canonical verification artifact 已存在：`docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/raw-20260322-0115code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`
- 原始 feature branch `feature/cli-first-observability-surfaces-20260322` 已退休，本地分支不存在，远端同名分支也已删除
- 原始 feature worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260322-feature-cli-first-observability-surfaces` 已退休，不再需要额外 salvage 或 cleanup handoff

## Next

- This lifecycle is closed on canonical `develop`.
- 若后续要继续扩真正的 Tauri TUI/GUI 渲染层，应在同一方向下用新 lifecycle 承接，不在本 issue 上继续扩 scope。
