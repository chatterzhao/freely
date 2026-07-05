# Verification: global-restart-restore-memory-governance

- issue_id: `I-20260327-2006-A-global-restart`
- verification_scope: feature-lane verification on fresh continuation before develop merge judgement
- verified_in_worktree: `feature/global-restart-restore-memory-governance-continuation-20260330-1608`
- depends_on: `I-20260327-2006-A`

## Commands

1. `bash -n docs/system/workspace/scripts/runtime/freely`
2. `bash docs/system/workspace/scripts/tests/test-freely-global-restart-restore-memory`
3. `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

## Result

- `freely restart --all-projects --project <root>` 现在是 explicit all-project restart surface，而不是 project-local restart 的隐式别名。
- global restart 会先把 restore truth 写入 `$FREELY_HOME/control-plane/restart/latest.json` 与 `history/<timestamp>[...].json`，并保留最近 20 份 history；同秒重复 restart 不会覆盖已有 history 文件。
- manifest 稳定记录 previously-running project set、operator-stopped exclusion 与 per-project `restore_selected`、`operator_stopped`、`mandatory_restore_anchors`、`auxiliary_evidence`、`continuity_anchor`。
- replay 现在按全局注册项目与当前 repo worktree 的并集选取 restore 集合，不再把其他 repo 中已注册的 Freely project 静默漏掉。
- replay 只 stop/start restart 前本来就应恢复的 projects，显式排除 operator-stopped worktree；如果某个 previously-running project 缺 mandatory anchors，则会写出 manifest 并 hard-block replay。
- `session-state.env` 等 auxiliary runtime artifacts 仍不会被升格成 mandatory restore truth。
- parent taxonomy regression `test-freely-project-command-semantics` 继续通过，说明这轮只扩了 global restart restore memory owner，没有把 `I-20260327-2006-A` 的 command semantics 打回去。

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
