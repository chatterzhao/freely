# Issue: worktree-hygiene-supervision-control-plane

- issue_id: `I-20260318-1825`
- title: Worktree hygiene supervision control plane
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `worktree-hygiene-supervision-control-plane`
- issue-name: `worktree-hygiene-supervision-control-plane`
- source_candidate: `docs/pre-brainstorms/20260318-1825--autonomous-worktree-hygiene-and-checkpoint-supervision/candidates.md#candidate-a`
- source_brainstorm: `docs/pre-brainstorms/20260318-1825--autonomous-worktree-hygiene-and-checkpoint-supervision/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 已有 checkpoint-guard、fleet-status 与 manager/worker 角色边界，但还缺一条更主动的自治控制面：

- worker 连续多轮 dirty/checkpoint 漂移时，runtime 只会提醒，不会升级为明确的 hygiene intervention
- manager 能看到 dirty/checkpoint 数字，但缺少可直接委派的 hygiene alert
- 缺少一个统一的 hygiene skill，把 manager 的委派和 worker 的收口步骤收成同源能力

## Scope

1. 新增 `skill:worktree-hygiene-supervision`，统一 manager/worker 的 hygiene 收口步骤。
2. 在 runtime 里记录 `checkpoint_drift_streak`，连续多轮漂移时升级为 hygiene intervention。
3. 在 manager prompt 中增加 `Worktree hygiene alert`，对进入 drift 的 worker 输出结构化委派信号。
4. 在 `freely status` 中暴露 `checkpoint_drift_streak`。
5. 增加脚本级测试，锁住 worker escalation 与 manager alert 行为。

## Acceptance

- `docs/system/workspace/skills/worktree-hygiene-supervision/SKILL.md` 存在并被技能目录索引。
- worker 在 `checkpoint_drift_streak >= threshold` 时，prompt 中出现 `Worktree hygiene intervention`。
- manager 在存在 drift worker 时，prompt 中出现 `Worktree hygiene alert` 和 `next_action=delegate_hygiene_worker`。
- `./bin/freely status --project <worktree>` 能显示 `checkpoint_drift_streak`。
- 新旧 checkpoint / supervision 相关测试同时通过。

## Completion

- `docs/system/workspace/skills/worktree-hygiene-supervision/SKILL.md`
- `docs/system/workspace/skills/README.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-worktree-hygiene-alert`
- `docs/system/workspace/scripts/tests/test-freely-checkpoint-drift-escalation`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-governance`
- `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-drift-escalation`
- `bash docs/system/workspace/scripts/tests/test-freely-worktree-hygiene-alert`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert`
- `./bin/governance-check`

## Next

- 先保持 `in_verification`，等待 review 与 promote 判断。
- 若后续仍发现仅靠 intervention 提示不足，再从同一问题线 materialize `dedicated hygiene worker delegation flow`，不要在当前 issue 中提前扩 scope。
