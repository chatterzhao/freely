# Issue: governance-merge-gate-milestone-status-followthrough-governance

- issue_id: `I-20260404-0119-A`
- title: Governance merge gate milestone status followthrough governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `governance-merge-gate-milestone-status-followthrough-governance`
- issue-name: `governance-merge-gate-milestone-status-followthrough-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260404/candidates.md#c-20260404-0119-a`
- source_brainstorm: `docs/B1-docs/raw-20260404/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
- reopen_reason: `real replay surfaced a parser regression where nested milestone queue item status lines overwrite parent milestone status inside governance-merge-gate`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-governance-merge-gate-milestone-status-followthrough-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
  - `docs/system/workspace/scripts/quality/governance-merge-gate`
  - `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`governance-merge-gate` 已经负责验证 active candidate 是否绑定到 active milestone，但这轮真实 replay 暴露出一个更基础的 parser regression：`parse_milestones()` 在进入 `candidate_issues` / `committed_issues` / `completed_issues` 之后，仍会把嵌套条目的 `- status:` 当成 milestone 顶层状态来读。结果是 queue item 自己的 `needs_research` 能把本来 `active` 的 milestone 误改成 `needs_research`，并错误阻断 develop-bound merge。

这不是 runtime bootstrap owner 的 scope，也不是新的 milestone policy 设计问题，而是一条应挂在 merge-gate family 下的窄 parser followthrough。

## Scope

1. 限制 `parse_milestones()` 只读取 milestone 顶层 `- status:`。
2. 增加 focused regression，覆盖 nested candidate item `status` 不得覆盖 milestone `active` 状态。
3. 以最小 same-line lifecycle 证据完成 develop-bound replay。

## Non-Goals

1. 不修改 runtime `/bin/ps` fallback owner 的实现边界。
2. 不重写 milestone 文件格式或排程策略。
3. 不放宽 active candidate placement gate。
4. 不把其他 merge-gate residual regression 混进这条 owner。

## Acceptance

1. `parse_milestones()` 只记录 milestone 顶层 `- status:`，不会被 queue item 的 `status` 污染。
2. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate` 覆盖并锁住该回归。
3. `./bin/governance-check` 通过。
4. 该 followthrough 仍保持 narrow parser-bound scope，不吸收 broader milestone / runtime policy。

## Verification

- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `git diff --check`
- `./bin/governance-check`

## Next

- `2026-04-04` closeout: canonical `develop` already absorbed this narrow parser-bound followthrough through merge `908a6ad`.
- Keep this owner closed as the milestone-status parsing repair record; if future merge-gate regressions surface in other nested fields, reopen from current `develop` as a new owner instead of reviving `0119`.
