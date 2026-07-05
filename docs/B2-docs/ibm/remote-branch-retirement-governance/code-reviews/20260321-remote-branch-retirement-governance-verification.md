# Code Review: remote-branch-retirement-governance

- date: `2026-03-21`
- scope:
  - `docs/system/workspace/skills/worktree-maintenance-governance/SKILL.md`
  - `docs/system/workspace/skills/worktree-maintenance-governance/references/fleet-closure.md`
  - `docs/system/workspace/skills/worktree-maintenance-governance/references/retirement-handoff.md`
  - `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- reviewer: `codex`
- status: `in_verification`

## Focus

- cleanup followthrough 是否把 remote branch disposition 纳入标准收口
- remote branch 不能删时，是否会保留本地并写明原因
- skill / reference / runtime / test 是否对齐

## Verification Evidence

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- `freely` live smoke with interruption followthrough

## Smoke Notes

- 在当前 `feature/*` 工位直接执行 `freely start` + `freely chat` 时，运行时按既有角色设计把该工位识别为 `worker`：
  - `live-status` 显示 `role_hint: worker`
  - 插话会被 interruption dispatcher durable intake 并分类
  - 但不会在该工位直接形成主管 patrol / delegation 闭环
- 这与现有真源一致：主管监督应在 `develop` manager 工位进行，feature 工位默认承担 worker 执行职责。
- 因此本次 live smoke 的通过标准是：
  - interruption intake 正常记录
  - cleanup followthrough 行为测试通过
  - 远程 branch disposition 已进入 runtime + resolution artifact
