# Issue: structured-closeout-gate-context-and-review-evidence-governance

- issue_id: `I-20260412-0225-A`
- title: Structured closeout gate context and fresh review evidence governance
- phase_state: `in_dev`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `structured-closeout-gate-context-and-review-evidence-governance`
- issue-name: `structured-closeout-gate-context-and-review-evidence-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260412-0225--structured-closeout-gate-and-fresh-review-evidence/candidates.md#c-20260412-0225-a`
- source_brainstorm: `docs/pre-brainstorms/20260412-0225--structured-closeout-gate-and-fresh-review-evidence/brainstorms.md`
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

## Next

1. next_action: `finish the remaining develop-bound verification slice by updating owner pre-tests/progress truth and replaying a disposable test-pre-merge -> develop chain until the only remaining blocker is the expected fresh staged owner review artifact requirement.`
2. revisit_trigger: 若 guarded replay 在 owner 已进 execution phase 且已回填完成项后，仍然先被其他 lifecycle drift 拦住，而不是收敛到 fresh staged owner review artifact 诊断。
