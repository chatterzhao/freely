# Issue: structured-closeout-gate-context-and-review-evidence-governance

- issue_id: `I-20260412-0225-A`
- title: Structured closeout gate context and fresh review evidence governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `structured-closeout-gate-context-and-review-evidence-governance`
- issue-name: `structured-closeout-gate-context-and-review-evidence-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260412-0225/candidates.md#c-20260412-0225-a`
- source_brainstorm: `docs/B1-docs/raw-20260412-0225/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
  - `docs/epics/workspace-routing-foundation/implementation-decision-notes-in-issue-review-artifacts-governance/issues/implementation-decision-notes-in-issue-review-artifacts-governance.md`
  - `docs/epics/workspace-routing-foundation/pre-tests-cleanup-and-retirement-enforcement-governance/issues/pre-tests-cleanup-and-retirement-enforcement-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

当前 `develop` 门禁已经能 fail-close，但 closeout adequacy contract 仍然分散在三处：

1. runtime state 里的 `Closeout-Gate` free-text
2. owner `pre-tests.md` 中的 `premerge-integration:develop_merge` adequacy item
3. merge gate 对 fresh staged owner review artifact 的额外要求

这让 gate 经常表现为“最后一步突然拦截”，而不是从 handoff / cleanup replay 开始就可恢复地提示操作者缺哪一层 contract。

## Scope

1. 冻结 closeout contract 的结构化字段：
   - `closeout_gate_command`
   - `closeout_target_lane`
   - `closeout_promotion_gate`
   - `closeout_requires_adequacy`
   - `closeout_review_artifact_policy`
2. 让 delegated intake、worker runtime state、cleanup replay 直接消费这些字段，而不是重新解析 free-text command
3. 统一 runtime guidance 与 merge-gate diagnostics 的口径，使 develop-bound promote 能明确提示 fresh staged owner review artifact requirement
4. 保持现有 fail-closed gate 语义，不因可观察性改进而放宽门禁

## Non-Goals

1. 不重开 `verification-contract-and-premerge-adequacy-governance` 的已完成范围
2. 不重写 `implementation-decision-notes-in-issue-review-artifacts-governance` 的 review artifact 最小字段
3. 不新增 `tests.md` 或平行 closeout ledger
4. 不在本 owner 内做全仓历史 worker-state 回填

## Completion

- `docs/B1-docs/raw-20260412-0225/candidates.md`
- `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/issues/structured-closeout-gate-context-and-review-evidence-governance.md`
- `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/brainstorms/b-structured-closeout-gate-context-and-review-evidence-governance.md`
- `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/prd.md`
- `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/code-reviews/20260412-structured-closeout-gate-context-and-review-evidence-verification.md`
- `docs/progress/workspace-routing-foundation/p-structured-closeout-gate-context-and-review-evidence-governance.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/quality/pretests-gate`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/scripts/quality/pretests-retirement-gate`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-natural-language-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-partial-verification-metadata`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-projection-without-state`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
- `docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
- `docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-pretests-retain`
- `docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-retained-continuation`
- `docs/system/workspace/scripts/tests/test-pretests-gate`
- `docs/system/workspace/scripts/tests/test-governance-merge-gate`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-natural-language-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-partial-verification-metadata`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-projection-without-state`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
- `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-pretests-retain`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-retained-continuation`
- `bash docs/system/workspace/scripts/tests/test-pretests-gate`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/governance-check`
- `freely wt-create test-pre-merge-20260412-structured-closeout-gate-review-evidence-final --base develop`
- `freely pr-merge-guarded test-pre-merge-20260412-structured-closeout-gate-review-evidence-final feature/structured-closeout-gate-and-review-evidence-followon-20260412`
- `freely pr-merge-guarded develop test-pre-merge-20260412-structured-closeout-gate-review-evidence-final`

## Next

1. next_action: `completed on canonical develop via merge commit b702f966927e190e361736f75bfc965e7fb564bd; only cleanup/retirement of disposable worktrees remains.`
2. revisit_trigger: 若后续 develop-bound replay 再次不能把 blocker 收敛到 fresh staged owner review artifact，或 cleanup/retirement 重新退回到依赖 free-text closeout guidance 而不是结构化 closeout contract。
