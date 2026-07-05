# Issue: remote-branch-retirement-governance

- issue_id: `I-20260321-1515`
- title: Remote branch retirement governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `remote-branch-retirement-governance`
- issue-name: `remote-branch-retirement-governance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260321/candidates.md#c-20260321-1515-a`
- source_brainstorm: `docs/B1-docs/raw-20260321/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/worktree-maintenance-governance/issues/worktree-maintenance-governance.md`, `docs/epics/workspace-routing-foundation/worktree-fleet-governance-closure/issues/worktree-fleet-governance-closure.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 当前已经能：

- merge up 到 `develop`
- 删除本地 worktree
- 删除本地 feature branch

但 worktree 治理真正完成时，远程同名 branch 也必须进入明确 disposition：

- deleted
- retained with reason

否则治理闭环会停在“本地看起来已经退休”，而远程协作面仍保留历史 feature branch。

## Scope

1. 扩展 `worktree-maintenance-governance`，把 remote branch disposition 纳入 fleet closure / retirement handoff 的必查面。
2. 扩展 `branch-management` 的 cleanup lifecycle，明确 remote exists / merged / delete-failed 的规则。
3. 扩展 runtime `cleanup-followthrough`，让它在删除本地 worktree / branch 前先判断并处理 remote branch。
4. 增加 script 级回归，锁定：
   - merged remote branch 会被删除
   - dirty worktree 保留
   - resolution artifact 记录 remote disposition

## Acceptance

- `worktree-maintenance-governance` 明确要求 cleanup 结论必须包含本地/远程分支 disposition
- `branch-management` cleanup reference 明确记录 remote deletion 或 retained reason
- `cleanup-followthrough` 不再只删本地；当 remote branch 已 merged 时会尝试删除 remote
- 若 remote branch 未 merged 或删除失败，会保留本地并写明原因
- `test-freely-interruption-direct-answer` 覆盖 remote retirement 行为

## Completion

- `docs/B1-docs/raw-20260321/brainstorms.md`
- `docs/B1-docs/raw-20260321/candidates.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/SKILL.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/references/fleet-closure.md`
- `docs/system/workspace/skills/worktree-maintenance-governance/references/retirement-handoff.md`
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- `docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/code-reviews/20260321-remote-branch-retirement-governance-verification.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- `docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/code-reviews/20260326-remote-branch-retirement-canonical-replay-verification.md`

## Next

- remote branch retirement check 已成为 worktree cleanup 的标准一部分，本 issue 正式完成。
- 后续若要扩成独立 `fleet-status` / `live-status` 可见字段，再基于同一主题继续，不在本 issue 内平行新增 skill。
