# Code Review: manager-watchdog-trigger-and-drift-reconcile-governance

## Scope Reviewed

- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`

## Findings

- High: 真实 `develop` 工位集成测试表明，主管虽然能被 `freely start` 拉起且能通过 `freely chat` 接住新的项目级任务，但该任务被错误吸收到旧的 `cleanup://merged-worktree-followthrough` continuity，而不是先触发新的 patrol / restart-point routing。这说明当前真源 wording 已基本收敛，但运行时主管还没有稳定兑现“新 signal 先 notice/claim/identify restart point，再决定 absorption target”的能力。

## Verification

- `./bin/governance-check`

## Residual Risks

- 当前已把语义收敛到真源，但真实集成测试表明主管仍会被旧 continuity 主导，错误吸收新的项目级监督任务。
- 当前还没有把 patrol cadence、event emission 或自动派单脚本化。
- 若后续 runtime 需要主动发 patrol tick 或 event bus，再应通过同一 issue 继续 materialize，而不是回写历史 issue。
