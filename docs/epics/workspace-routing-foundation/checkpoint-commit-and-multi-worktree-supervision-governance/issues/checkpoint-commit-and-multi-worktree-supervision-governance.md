# Issue: checkpoint-commit-and-multi-worktree-supervision-governance

- issue_id: `I-20260318-0930`
- title: Checkpoint commit and multi-worktree supervision governance
- phase_state: `in_dev`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `checkpoint-commit-and-multi-worktree-supervision-governance`
- issue-name: `checkpoint-commit-and-multi-worktree-supervision-governance`
- source_candidate: `docs/pre-brainstorms/20260317-0735--account-aware-loop-and-checkpoint-commit-governance/candidates.md#c-20260317-0735-b`
- source_brainstorm: `docs/pre-brainstorms/20260317-0735--account-aware-loop-and-checkpoint-commit-governance/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 当前已经会 worktree 隔离、session handoff、rate-limit account switch，但仍不会像项目负责人一样管理多个工位：

- 不能可靠判断什么时候必须先 checkpoint，而不是继续堆脏树
- 不能阻止一个 commit 同时混入 control-plane 与 product-plane
- 缺少一个 CLI-first 的工位总览，无法统一安排继续开发、冻结等待、集成批次与合并顺序

## Scope

1. 提供 `checkpoint-guard` CLI，面向当前 worktree 和 staged commit 输出 checkpoint budget 结果。
2. 在 `pre-commit` 上接 staged scope gate，阻止明显跨 issue 的混提。
3. 提供 `wt-fleet-status` CLI，以项目级视图展示所有 worktree 的 branch、dirty、checkpoint 与 runtime 状态。
4. 把 checkpoint 结果接回 `freely status` 与 auto-loop prompt。
5. 增加 skill 和脚本级测试。

## Acceptance

- `./bin/checkpoint-guard` 可输出结构化 checkpoint 结论。
- `./bin/checkpoint-guard --staged-only --fail-on-required` 对混 scope staged commit 返回非零。
- `./bin/wt-fleet-status` 能列出多个 worktree，并展示 dirty / checkpoint / supervisor / ai。
- `./bin/freely status --project <worktree>` 能显示 `checkpoint_required` 与 `checkpoint_reasons`。
- `pre-commit` 对超预算 staged commit 给出阻断信息，不再只是 scope hint。

## Completion

- `docs/system/workspace/scripts/quality/checkpoint-guard`
- `docs/system/workspace/scripts/worktree/wt-fleet-status`
- `docs/system/workspace/hooks/pre-commit.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
- `docs/system/workspace/scripts/tests/test-checkpoint-guard`
- `docs/system/workspace/scripts/tests/test-wt-fleet-status`
