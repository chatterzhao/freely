# Issue: develop-guarded-merge-entrypoint-enforcement-governance

- issue_id: `I-20260405-0425-A`
- title: Develop guarded merge entrypoint enforcement governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `develop-guarded-merge-entrypoint-enforcement-governance`
- issue-name: `develop-guarded-merge-entrypoint-enforcement-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260405/candidates.md#c-20260405-0425-a`
- source_brainstorm: `docs/B1-docs/raw-20260405/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/develop-guarded-merge-entrypoint-enforcement-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-develop-guarded-merge-entrypoint-enforcement-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/develop-guarded-merge-entrypoint-enforcement-governance/code-reviews`
- depends_on:
  - `docs/system/workspace/hooks/pre-merge-commit.sh`
  - `docs/system/workspace/scripts/worktree/pr-merge-guarded`
  - `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
  - `docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
  - `docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经有 `freely pr-merge-guarded` 作为 merge 真源，但 `develop` 上的 `pre-merge-commit` 仍允许“没有 canonical guarded handshake 的 merge”继续走后续 gate。结果是：

1. 手工裸 `git merge` 与仓库自有 `freely pr-merge-guarded` 入口并存。
2. 只要 staged merge 内容满足 governance / promotion gate，裸 merge 仍能落地。
3. 这类误用又会在 protected branch 上制造新的治理偏差，并且让人类和 agent 在两个 merge 入口之间来回误用。

## Scope

1. 为 `develop` merge commit 增加 canonical guarded entrypoint enforcement。
2. 缺少 `pr-merge-guarded` state 或 completion marker 时，hook 直接失败并指向 `freely pr-merge-guarded`。
3. 证明 guarded handshake 存在时，原有 governance materialization gate 和 promotion ownership gate 仍然继续生效。
4. 保持 `pr-merge-guarded` 正常 merge 和 conflict completion 路径通过。

## Non-Goals

1. 不把本地 hook 讨论扩成 server-side enforcement。
2. 不重写 break-glass whitelist 或 receipt ledger。
3. 不在本条 owner 里统一改 main / `test-pre-merge-*` 的 merge 入口策略。
4. 不把这条 owner 变成“修所有 merge 治理残留”的伞形议题。

## Acceptance

1. `develop` 上的 raw `git merge` / raw `git merge --continue` 若没有 canonical guarded handshake，`pre-merge-commit` 必须直接失败，并给出 `freely pr-merge-guarded` 指引。
2. 同一 hook 在 guarded handshake 存在时，仍然会继续执行 governance materialization gate。
3. 同一 hook 在 guarded handshake 存在时，仍然会继续执行 promotion ownership gate。
4. `test-pr-merge-guarded-hooked-initial-merge-receipt` 与 `test-pr-merge-guarded-breakglass-hook-completion` 继续通过，证明 canonical merge path 没被 entrypoint enforcement 破坏。
5. issue-bound implementation decision note 必须明确：这次修的是 entrypoint contract，而不是再次定义 bypass/receipt policy。

## Current Evidence

- `docs/system/workspace/hooks/pre-merge-commit.sh`
- `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded`
- `docs/epics/workspace-routing-foundation/develop-guarded-merge-entrypoint-enforcement-governance/code-reviews/20260405-develop-guarded-merge-entrypoint-enforcement-implementation.md`
- `docs/epics/workspace-routing-foundation/develop-guarded-merge-entrypoint-enforcement-governance/code-reviews/20260405-develop-guarded-merge-entrypoint-enforcement-verification.md`
- `docs/epics/workspace-routing-foundation/develop-guarded-merge-entrypoint-enforcement-governance/code-reviews/20260405-develop-guarded-merge-entrypoint-canonical-closeout-verification.md`

## Completion Status

- canonical_merge_commit: `f1965d3`
- canonical_merge_target: `develop`
- post_merge_acceptance:
  - `git log -1 --format=%B HEAD`
  - `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
  - `./bin/governance-check`
- completion_note: canonical `develop` now rejects raw merge entry into the protected branch unless the merge came through `freely pr-merge-guarded`; later expansion beyond `develop` should reopen as a narrower follow-on rather than silently widening this owner.
