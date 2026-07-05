# Issue: checkpoint-commit-and-multi-worktree-supervision-governance

- issue_id: `I-20260318-0930`
- title: Checkpoint commit and multi-worktree supervision governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `checkpoint-commit-and-multi-worktree-supervision-governance`
- issue-name: `checkpoint-commit-and-multi-worktree-supervision-governance`
- verification_artifact_dir: `docs/B2-docs/- epic-name: `workspace-routing-foundation`/- story-name: `checkpoint-commit-and-multi-worktree-supervision-governance`/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260318/candidates.md#c-20260318-A`
- additional_source_candidates:
  - `docs/B1-docs/raw-20260318/candidates.md#c-20260318-2358-a`
  - `docs/B1-docs/raw-20260318/candidates.md#c-20260318-2358-b`
- source_brainstorm: `docs/B1-docs/raw-20260317/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/B2-docs/ibm/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
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
4. 把 checkpoint 结果接回 `freely baseline-status` 与 auto-loop prompt。
5. 增加 skill 和脚本级测试。

## Acceptance

- `./bin/checkpoint-guard` 可输出结构化 checkpoint 结论。
- `./bin/checkpoint-guard --staged-only --fail-on-required` 对混 scope staged commit 返回非零。
- `./bin/wt-fleet-status` 能列出多个 worktree，并展示 dirty / checkpoint / supervisor / ai。
- `freely baseline-status --project <worktree>` 能显示 `checkpoint_required` 与 `checkpoint_reasons`。
- `pre-commit` 对超预算 staged commit 给出阻断信息，不再只是 scope hint。

## Completion

- `docs/system/workspace/scripts/quality/checkpoint-guard`
- `docs/system/workspace/scripts/worktree/wt-fleet-status`
- `docs/system/workspace/hooks/pre-commit.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
- `docs/system/workspace/scripts/tests/test-checkpoint-guard`
- `docs/system/workspace/scripts/tests/test-wt-fleet-status`

## Verification

- 当前验证重点：
  - `checkpoint-guard` 是否对当前 worktree 和 staged scope 正确给出 checkpoint 结论
  - `wt-fleet-status` 与 `freely fleet-status` 是否能按工位展示 dirty / checkpoint / runtime 摘要
  - `freely baseline-status` / 首跳 prompt 是否已暴露 project dirty budget 与 project-level worktree summary
  - `develop/main/test-pre-merge-*` 上的主管首跳是否只做监督与委派，不直接执行第二跳实现
- 已执行 `TEST`：
  - `bash docs/system/workspace/scripts/tests/test-checkpoint-guard`
  - `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-governance`
  - `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
  - `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- 已写入 review 证据：
  - `docs/B2-docs/gate/checkpoint-commit-and-multi-worktree-supervision-governance/code-reviews/20260318-checkpoint-and-fleet-verification.md`
  - `docs/B2-docs/gate/checkpoint-commit-and-multi-worktree-supervision-governance/code-reviews/20260326-checkpoint-and-fleet-canonical-replay-verification.md`
- 当前研究阶段尚未启用正式 `docs/progress/**`，本轮 dev-loop 等价执行证据写入 `docs/B1-docs/raw-CONVERGENCE.md`。
- 本轮补充验证：
  - `./bin/checkpoint-guard` -> `checkpoint_required: no`
  - `./bin/wt-fleet-status` -> 仅当前 worktree 为 `DIRTY`
  - `./bin/governance-check` -> `passed with 10 warning(s)`（均为 legacy pre-brainstorm naming 提示，非阻断）
  - `start-lead-agent.sh --project <develop>` -> `MANAGER_MODE=true`，且提示主管工位不得直接修改受版本管理产物

## Verification Summary

- canonical `develop` 仍保留 `checkpoint-guard`、`wt-fleet-status`、`freely baseline-status` dirty-budget 暴露，以及 `pre-commit` 的 staged scope gate，focused replay 全部通过。
- 早先阻塞 closeout 的 `dirty=1` / promote-cleanup 叙述属于当时 verification worktree 的现场快照，不再能代表当前 canonical truth；继续把该 issue 留在 active queue 只会制造假待办。
- `commit-first after checkpoint-ready` 已按边界外候选回流到 `C-20260318-0715-A`，不再阻止当前 issue 收口。
- 当前批次据此把本 issue 视为 completed；后续若继续扩自治 commit/promotion contract，应通过新 lifecycle 承接。
