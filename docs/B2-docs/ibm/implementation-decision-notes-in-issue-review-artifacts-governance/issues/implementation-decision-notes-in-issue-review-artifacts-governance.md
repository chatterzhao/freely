# Issue: implementation-decision-notes-in-issue-review-artifacts-governance

- issue_id: `I-20260401-2354-A`
- title: Implementation decision notes in issue-bound review artifacts
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `implementation-decision-notes-in-issue-review-artifacts-governance`
- issue-name: `implementation-decision-notes-in-issue-review-artifacts-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260401/candidates.md#c-20260401-2354-a`
- source_brainstorm: `docs/B1-docs/raw-20260401/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/implementation-decision-notes-in-issue-review-artifacts-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-implementation-decision-notes-in-issue-review-artifacts-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/implementation-decision-notes-in-issue-review-artifacts-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/ibm/candidate-acceptance-review-governance/issues/candidate-acceptance-review-governance.md`
  - `docs/B2-docs/ibm/pre-tests-evidence-binding-and-completion-gate-governance/issues/pre-tests-evidence-binding-and-completion-gate-governance.md`
  - `docs/system/workspace/scripts/quality/governance-merge-gate`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经在 pre-brainstorm 和 IBM 层解决了“为什么值得做”和“issue 边界如何冻结”的 thoughtfulness，但在 dev-loop 的实现层还缺一块稳定真源：

- 这次实现到底选择了什么
- 为什么现在选这个
- 放弃了哪些可行替代
- 哪些边界保持不动
- 残余风险和 follow-on 是什么

如果这层只散落在会话或自由 prose 里，未来 worker / reviewer 虽然能看到代码 diff，却不一定能快速恢复“为什么不是另一种做法”。这会让 Freely 的 thoughtfulness 在 candidate/PRD 很强、到实现 closeout 却变弱。

## Scope

1. 冻结 implementation decision note 的 canonical landing surface：
   - issue-bound `code-reviews/` / verification artifact
   - 不新建平行 `decision-summary` 目录
2. 冻结最小字段：
   - `decision`
   - `why_this`
   - `alternatives_considered`
   - `boundary_non_goals`
   - `residual_risk`
3. 冻结何时强制：
   - develop-bound implementation-bearing diff 默认必须带 decision note
   - research-only / IBM-only / milestone reshuffle 不强制
4. 冻结 owner association：
   - gate 从当前 issue 的 `verification_artifact_dir` 找 review artifact
   - 不扫描全仓，不依赖自由命名
5. 实现最小 gate 与回归测试：
   - 缺 review artifact 时拒绝
   - review artifact 缺 decision note 最小字段时拒绝
   - 具备完整 note 时通过

## Non-Goals

1. 不把 candidate / PRD 的上游 thoughtfulness 再复制到 dev-loop。
2. 不尝试自动评判 prose 质量或“思考深度”。
3. 不为每个纯机械改动强制长文说明。
4. 不引入独立 JSON manifest 或新 artifact family。

## Acceptance

1. `LAWS` 明确：develop-bound implementation-bearing work 默认必须在 issue-bound review artifact 中留下 implementation decision note。
2. `dev-loop-execution` 与相关 IBM checklist 明确 canonical landing surface 与最小字段。
3. `governance-merge-gate` 能通过 owner issue 的 `verification_artifact_dir` 要求同批 staged review artifact。
4. `governance-merge-gate` 能要求 staged review artifact 至少包含：
   - `decision`
   - `why_this`
   - `alternatives_considered`
   - `boundary_non_goals`
   - `residual_risk`
5. 回归测试覆盖：
   - 有 implementation-bearing diff 但没有 staged review artifact -> fail
   - 有 staged review artifact 但缺 decision note -> fail
   - staged review artifact decision note 完整 -> pass

## Completion

- `docs/B1-docs/raw-20260401/brainstorms.md`
- `docs/B1-docs/raw-20260401/candidates.md`
- `docs/B2-docs/ibm/implementation-decision-notes-in-issue-review-artifacts-governance/issues/implementation-decision-notes-in-issue-review-artifacts-governance.md`
- `docs/B2-docs/ibm/implementation-decision-notes-in-issue-review-artifacts-governance/brainstorms/b-implementation-decision-notes-in-issue-review-artifacts-governance.md`
- `docs/B2-docs/ibm/implementation-decision-notes-in-issue-review-artifacts-governance/prd.md`
- `docs/B2-docs/ibm/implementation-decision-notes-in-issue-review-artifacts-governance/pre-tests.md`
- `docs/B2-docs/ibm/implementation-decision-notes-in-issue-review-artifacts-governance/tasks.md`
- `docs/B2-docs/ibm/implementation-decision-notes-in-issue-review-artifacts-governance/code-reviews/20260401-implementation-decision-notes-in-review-artifacts-verification.md`
- `docs/progress/workspace-routing-foundation/p-implementation-decision-notes-in-issue-review-artifacts-governance.md`
- `docs/LAWS.md`
- `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
- `docs/system/workspace/skills/dev-loop-execution/references/implementation-decision-note.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `docs/milestones.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`

## Implementation Status

- `2026-04-01`: canonical landing surface, laws / skill / IBM checklist updates, merge-gate enforcement, and merge-gate regression coverage all landed in this lane.

## Next

- Observe whether the initial implementation-bearing path detection is too broad or too narrow; if so, reopen as a narrower follow-on without changing the canonical landing surface.

## Closeout

- canonical_merge_target: `develop`
- gate_commit: `cdb8278`
- proof_owner: `I-20260402-0540-A`
- proof_artifact: `docs/B2-docs/runtime/runtime-loop-log-timezone-label-followthrough-governance/code-reviews/20260402-runtime-loop-log-timezone-label-followthrough-verification.md`
- post_gate_proof: The `runtime-loop-log-timezone-label-followthrough` owner merged to `develop` after `cdb8278` and its staged review artifact carries a complete `Implementation Decision Note` with all required minimum fields.
- closeout_note: The canonical gate is no longer waiting on hypothetical future usage; a real post-gate develop-bound owner has already exercised the required note path end to end.
