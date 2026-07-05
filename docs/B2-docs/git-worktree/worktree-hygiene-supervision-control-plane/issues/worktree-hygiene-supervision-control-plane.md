# Issue: worktree-hygiene-supervision-control-plane

- issue_id: `I-20260318-1825`
- title: Worktree hygiene supervision control plane
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `worktree-hygiene-supervision-control-plane`
- issue-name: `worktree-hygiene-supervision-control-plane`
- verification_artifact_dir: `docs/B2-docs/git-worktree/worktree-hygiene-supervision-control-plane/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260318T163000Z/candidates.md#C-20260318-1825-A`
- source_brainstorm: `docs/B1-docs/raw-20260318T163000Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/B2-docs/gate/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md`
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
4. 在 `freely baseline-status` 中暴露 `checkpoint_drift_streak`。
5. 增加脚本级测试，锁住 worker escalation 与 manager alert 行为。

## Acceptance

- `docs/system/workspace/skills/worktree-hygiene-supervision/SKILL.md` 存在并被技能目录索引。
- worker 在 `checkpoint_drift_streak >= threshold` 时，prompt 中出现 `Worktree hygiene intervention`。
- manager 在存在 drift worker 时，prompt 中出现 `Worktree hygiene alert` 和 `next_action=delegate_hygiene_worker`。
- `freely baseline-status --project <worktree>` 能显示 `checkpoint_drift_streak`。
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
- `docs/B2-docs/git-worktree/worktree-hygiene-supervision-control-plane/code-reviews/20260326-worktree-hygiene-canonical-replay-verification.md`

## Verification Summary

- canonical replay 继续证明：`checkpoint_drift_streak` 会升级成 hygiene intervention，manager prompt 会把 drift worker 暴露成可委派的 hygiene alert，`baseline-status` 也仍保留相关可见性。
- 当前阻塞只剩历史上的 review / promote 表述，没有新的实现缺口；继续保留 `in_verification` 会把已落盘能力误当成待开发。
- 若后续仍发现 intervention 提示不足，再从同一问题线 materialize `dedicated hygiene worker delegation flow`，不要回退到当前 issue 再重复实现。
- 当前批次据此把本 issue 关闭为 `completed`。
