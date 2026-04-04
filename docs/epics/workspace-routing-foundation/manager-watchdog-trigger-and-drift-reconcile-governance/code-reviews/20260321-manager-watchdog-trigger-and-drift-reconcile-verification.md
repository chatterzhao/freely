# Code Review: manager-watchdog-trigger-and-drift-reconcile-governance
- issue_id: `I-20260321-1715`

## Scope Reviewed

- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`

## Findings

- Fixed: runtime 不再在 `restart_point=cleanup && ownership=worker` 时直接执行 `run_cleanup_followthrough`。新的 cleanup signal 现在会先保留为 `handoff://cleanup` delegation，由后续 owner 完成真正的 cleanup followthrough 后再决定是否吸收到 `cleanup://merged-worktree-followthrough` continuity。

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler`
- `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`

## Residual Risks

- 当前修复的是 cleanup restart-point 的错误捷径；若后续出现其他 restart point 被 runtime 直接短路吸收，仍需继续补回统一 handoff contract。
- 当前还没有把 patrol cadence、event emission 或自动派单脚本化。
- 若后续 runtime 需要主动发 patrol tick 或 event bus，再应通过同一 issue 继续 materialize，而不是回写历史 issue。
