# Progress: project-command-semantics-and-restore-work-governance

- issue_id: `I-20260327-2006-A`
- title: Project command semantics and explicit restore-work governance
- phase_state: `in_dev`
- runtime_state: `restart_required`
- branch: `feature/start-restart-control-plane-semantics-20260327-200651`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260327-200651-feature-start-restart-control-plane-semantics`
- issue_path: `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/issues/project-command-semantics-and-restore-work-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "dev-loop-initial-slice"}

## Summary

- 2026-03-28 这条 lane 已从 `done_ibm` 正式切到 `in_dev`，因为 runtime 真源已经开始 materialize project command family。
- 当前已落下的实现切片：
  - usage surface 增加 `freely start --force`、`freely restart`、`freely restore-work`
  - `cmd_stop()` 的 project-local kill / cleanup 逻辑被提取成 `stop_project_runtime()`
  - `start --force` 走 project-local stop reason `start_force`
  - `restart` 走 project-local stop reason `operator_restart`，默认不做 implicit work restore
  - `restore-work` 只接受 project-scoped continuity anchors；`session-state.env` 与 `session-handoff.txt` 明确保持 auxiliary-only
- 本轮又补齐了缺口：
  - runtime main dispatch 现在真正接入 `restart` 与 `restore-work`
  - focused regression `test-freely-project-command-semantics` 覆盖 `restart`、`start --force` 与 `restore-work` anchor gate

## Current Focus

- 继续把 project-local repair ordering 收到稳定实现，而不是让 `start --force` 退化成 generic cleanup
- 保持 explicit `restore-work` 只消费 mandatory anchors，不把 transient pid/run-state 升格成 required truth
- 为后续 `I-20260327-2006-B` 保留清晰的 downstream 依赖，不在当前 issue 提前混入 global restart manifest owner

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

## Next Action

- 继续实现 project-local repair ordering 与 safe repair set 的其余 runtime/test slices
- 当前 issue 保持 `in_dev`，直到 focused regressions 与 command blast radius evidence 足以进入 verification
