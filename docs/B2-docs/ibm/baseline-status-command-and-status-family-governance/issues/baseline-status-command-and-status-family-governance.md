# Issue: baseline-status-command-and-status-family-governance

- issue_id: `I-20260320-2105`
- title: Baseline-status command and status family governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `baseline-status-command-and-status-family-governance`
- issue-name: `baseline-status-command-and-status-family-governance`
- source_candidate: `docs/B1-docs/raw-20260320/candidates.md#c-20260320-2105-a`
- source_brainstorm: `docs/B1-docs/raw-20260320/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/B2-docs/runtime/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 已经形成三块状态面：

- baseline snapshot
- live current-state
- fleet worktree state

但旧命名还让 `freely status` 承担 baseline snapshot，语义已经不准确。

## Scope

1. 正式新增 `freely baseline-status`。
2. 让 `freely status` 成为 status family 聚合入口，支持 `--view baseline|live|fleet|all`。
3. 更新当前活跃 skill、README、预研、issue 与测试，优先使用 `baseline-status`。
4. 明确 `baseline / live / fleet` 三种状态面的职责边界。

## Acceptance

- `freely baseline-status --project <path>` 可用，输出与原 baseline snapshot 一致。
- `freely status --project <path>` 默认输出聚合视图，不再伪装成 baseline alias。
- `freely status --view baseline|live|fleet|all` 可用。
- 当前活跃 skill / 文档 / 测试不再把 baseline snapshot 错称为 `status`。
- `live-status` 与 `fleet-status` 的职责边界不被回退。

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/README.md`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
- `docs/system/workspace/skills/worktree-hygiene-supervision/SKILL.md`
- `docs/system/workspace/scripts/tests/test-freely-baseline-status`
- `docs/system/workspace/scripts/tests/test-freely-status-family`
- 相关当前活跃预研 / issue / README / milestone 文档

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
- `bash docs/system/workspace/scripts/tests/test-freely-status-family`
- `bash docs/system/workspace/scripts/tests/test-freely-status-pid-ownership`
- `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-governance`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`

## Next

- 当前批次已完成并并入 `develop`。
- 后续若还要加 JSON family 输出、watch 模式或更细的过滤，再从同一 issue 继续扩，不必重新定义 taxonomy。
