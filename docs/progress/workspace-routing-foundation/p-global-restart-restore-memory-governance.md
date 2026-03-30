# Progress: global-restart-restore-memory-governance

- issue_id: `I-20260327-2006-A-global-restart`
- title: Global restart restore memory governance
- phase_state: `in_dev`
- runtime_state: `manual`
- branch: `feature/global-restart-restore-memory-governance-continuation-20260330-1608`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260330-1608-feature-global-restart-restore-memory-governance-continuation`
- issue_path: `docs/epics/workspace-routing-foundation/global-restart-restore-memory-governance/issues/global-restart-restore-memory-governance.md`
- depends_on: `I-20260327-2006-A`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "dev-loop-execution"}

## Summary

- `2026-03-30 17:10 PDT` parent `I-20260327-2006-A` 已合入 `develop`，旧 `feature/global-restart-restore-memory-governance-20260328-194636` 工位被确认是 stale runtime continuation：相对 `develop` 无独有提交、落后 37 个提交且 worktree 自身带脏改与挂起 runtime 状态，因此不再继续写入旧树。
- 新 continuation 直接从最新 `develop` 打开，并只吸收 stale 工位里仍属于本 issue 的窄实现：`$FREELY_HOME/control-plane/restart/{latest.json,history/*.json}` manifest namespace、keep-last-20 retention、previously-running selection / operator-stopped exclusion，以及 focused regression `test-freely-global-restart-restore-memory`。
- 本轮 dev-loop 目标是基于当前 `develop` 真源 materialize explicit `restart --all-projects` 行为，不重新引入 stale tree 上的额外 CLI surface 或覆盖近期已合并的 auth/watchdog/runtime 逻辑。

## Current Focus

- 让 `freely restart --all-projects --project <root>` 先写 durable manifest，再只 stop/start restart 前本来就应恢复的 projects。
- 继续保持 mandatory restore anchors 与 auxiliary evidence 的层级，不把 `session-state.env`、pid 文件等瞬态证据升级成 required restore truth。
- 所有实现和验证都留在当前 continuation，不在 stale 工位上继续 dogpile。

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-global-restart-restore-memory`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- feature verification artifact: `docs/epics/workspace-routing-foundation/global-restart-restore-memory-governance/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`

## Next Action

- 补 milestone 执行态回写，并继续判断这条 lane 是否已具备 merge-ready 条件。
