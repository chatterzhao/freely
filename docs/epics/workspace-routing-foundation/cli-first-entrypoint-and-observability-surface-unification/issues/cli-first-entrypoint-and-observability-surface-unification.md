# Issue: cli-first-entrypoint-and-observability-surface-unification

- issue_id: `I-20260322-0115`
- title: CLI-first entrypoint and observability surface unification
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `cli-first-entrypoint-and-observability-surface-unification`
- issue-name: `cli-first-entrypoint-and-observability-surface-unification`
- priority: P0
- source_candidate: `docs/pre-brainstorms/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/candidates.md#c-20260322-0115-a`
- source_brainstorm: `docs/pre-brainstorms/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/default-project-resolution-and-authorized-project-memory/issues/default-project-resolution-and-authorized-project-memory.md`
  - `docs/epics/workspace-routing-foundation/chat-triggered-worker-runtime-reactivation-governance/issues/chat-triggered-worker-runtime-reactivation-governance.md`
  - `docs/epics/workspace-routing-foundation/baseline-status-command-and-status-family-governance/issues/baseline-status-command-and-status-family-governance.md`
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
- `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- `bash docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`

## Retirement Handoff

- route_kind: `completion_verification`
- maintenance_mode: `audit + retirement_handoff`
- worktree_disposition: `retire-only`
- verified_retirable: `true`
- branch: `feature/cli-first-observability-surfaces-20260322`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260322-feature-cli-first-observability-surfaces`
- local_branch_disposition: `retained-with-reason`
- local_branch_reason: 当前会话正在该 worktree 中执行 canonical writeback；本轮只补 closure evidence，不在目标 worktree 内自删 branch/worktree
- remote_branch_disposition: `deleted`
- remote_branch_evidence: `git fetch origin --prune` 后，`origin/feature/cli-first-observability-surfaces-20260322` 仍不存在
- integration_absorption_evidence:
  - `git merge-base --is-ancestor HEAD develop` -> exit `0`
  - `git rev-list --left-right --count HEAD...develop` -> `0 11`
  - `develop` tip: `e7d93d9`
  - current branch tip: `7c3ff74`
- continuity_refresh:
  - 当前轮次先吸收 `context_compacted` 轮换交接，再继续 `completion_verification`
  - 先前 handoff 中的 `behind 7` 已过时；当前实际相对本地 `develop` 为 `ahead 0 / behind 11`
- next_action: 由 supervisor/runtime 在 worktree 外执行实际 cleanup；若后续要继续 Tauri 渲染层，必须新开 lifecycle，而不是复用当前 retired worktree

## Next

- 当前批次已完成。
- 若后续要继续扩真正的 Tauri TUI/GUI 渲染层，应在同一方向下用新 lifecycle 承接，不在本 issue 上继续扩 scope。
