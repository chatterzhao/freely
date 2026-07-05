# Issue: runtime-worker-launch-linkage-and-stall-recovery-governance

- issue_id: `I-20260322-0245`
- title: Runtime worker launch linkage and stall recovery governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-worker-launch-linkage-and-stall-recovery-governance`
- issue-name: `runtime-worker-launch-linkage-and-stall-recovery-governance`
- verification_artifact_dir: `docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/code-reviews`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260322/candidates.md#c-20260322-0245-a`
- source_brainstorm: `docs/B1-docs/raw-20260322/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/runtime/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
  - `docs/B2-docs/ibm/manager-delegation-after-sufficient-patrol-evidence-governance/issues/manager-delegation-after-sufficient-patrol-evidence-governance.md`
  - `docs/B2-docs/ibm/manager-continuation-handoff-consumption-governance/issues/manager-continuation-handoff-consumption-governance.md`
- session_refs:
  - {tool: codex, session_id: "019d15e2-5874-7e73-8487-715b7aee1ce1", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/22/rollout-2026-03-22T07-10-48-019d15e2-5874-7e73-8487-715b7aee1ce1.jsonl", role: "cleanup-followthrough"}
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://current-manual-codex-thread-id-not-exposed", role: "cleanup-followthrough-verifier"}

## Why

Freely 最新 dogfood 证明：

- manager 已能 patrol 并稳定产出 `retire-only / continue-dev`
- manager 已能写出 worker launch order 与 worker prompt artifact

但 runtime 还缺少两条关键能力：

1. 没有把这些 manager-generated worker handoff 转成目标 worker worktree 的实际执行
2. 长时间无输出且有待处理 intake 的 AI 进程不会被 runtime 识别成 stall 并恢复

因此 current gap 已经不在 manager prompt 语义，而在 runtime control plane。

## Scope

1. 定义 manager-generated worker handoff 的 runtime ingestion contract。
2. 将 manager worker handoff 转成 target worker worktree 的 delegated continuation / expected-running linkage，并实际触发 worker runtime。
3. 为当前 workcell 增加最小 stalled-AI detection 与 runtime-owned graceful recovery。
4. 补最小集成测试，验证：
   - manager handoff 会真正拉起 worker
   - stalled AI + pending intake 会触发 recovery

## Acceptance

- 主管写出 stable worker handoff 后，runtime 不再只停留在 `.freely/run/worker-prompts/*.txt`。
- target worker worktree 能收到可消费的 delegated continuation，并被 runtime 拉起。
- 当前 workcell AI 长时间无输出且存在更新的待处理 intake 时，runtime 能进行 graceful recovery；必要时落 hard-kill fallback evidence。
- 至少有一条 integration-style test 证明 manager handoff 能进入 worker execution。
- 至少有一条 runtime test 证明 stalled AI recovery 会让新 intake 进入下一轮 prompt。

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/manager-watchdog.sh`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/scripts/tests/test-*` for worker launch linkage and stalled recovery

## Verification

- `./bin/governance-check`
- worker launch linkage integration test
- stalled AI recovery runtime test
- post-merge acceptance on `develop`:
  - after restarting `freely`, manager runtime consumed `manager-continuity-20260322-021727.md`
  - `manager-worker-launch-state.env` recorded all three launched worker prompt paths
  - `fleet-status` showed worker supervisors/AI running on:
    - `feature/cli-first-observability-surfaces-20260322`
    - `feature/manager-handoff-consumption-reentry-20260322`
    - `feature/three-loop-dev-loop-ai-native-definition-20260321`

## Retirement audit

- audit_date: `2026-03-22`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260322-feature-runtime-worker-launch-linkage-and-stall-recovery`
- worktree_state: `clean`
- classification: `retire-only`
- cleanup_gate: `retained-with-reason`
- why_not_verified_retirable:
  - 当前工位只剩 canonical closure writeback；固化本轮 writeback commit 后可恢复 `target clean`，但这并不等于 branch cleanup 已完成
  - `git rev-list --left-right --count develop...HEAD` 在固化本轮 writeback 后仍会保持右侧非零；本地 docs-only closure commits 仍待经 develop-facing 路径吸收，因此不能直接宣称已完成 cleanup
  - `./bin/wt-status-all` 在本工位恢复 clean 后，项目里仍有其他 dirty worktree 需按 skipped / retained 语义留痕，不能伪装成全项目 hygiene 已收口
- local_branch_disposition: `retained-with-reason`
- local_branch_reason: 当前工位只剩 canonical closure writeback，固化本轮 writeback 后仍需先让本地 docs-only closure commits 经 develop-facing 路径被吸收；在分支被主线吸收前，不执行本地 branch/worktree cleanup
- remote_branch_disposition: `deleted`
- remote_branch_reason: `origin` 未发现同名远程分支
- latest_followthrough_evidence:
  - `git log --oneline --left-right develop...HEAD` 仅显示 docs-only closure commits
  - `git diff-tree --no-commit-id --name-only -r HEAD` 仍只涉及 issue / progress / review / milestone 四个 canonical 文档
  - 当前 closure writeback commit 落盘后，`git status --short` 应恢复 clean
  - 当前 closure writeback commit 落盘后，`./bin/wt-status-all` 应恢复当前工位 `CLEAN`
- revisit_trigger:
  - 当前 canonical closure writeback 已固化，且 `develop` 吸收当前本地 docs-only closure commits 或等价的 closure evidence
  - 当前工位重新执行 cleanup followthrough
