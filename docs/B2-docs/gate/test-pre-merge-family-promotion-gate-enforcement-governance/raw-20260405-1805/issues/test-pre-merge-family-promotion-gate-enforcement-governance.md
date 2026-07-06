# Issue: test-pre-merge-family-promotion-gate-enforcement-governance

- issue_id: `I-20260405-1805-A`
- title: Test-pre-merge family promotion gate enforcement governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `test-pre-merge-family-promotion-gate-enforcement-governance`
- issue-name: `test-pre-merge-family-promotion-gate-enforcement-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260405T230200Z/candidates.md#c-20260405-1805-a`
- source_brainstorm: `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805/verification/pre-tests.md
- progress_path: `pending://progress-created-on-dev-loop`
- verification_artifact_dir: docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805/code-reviews
- depends_on:
  - `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`
  - `docs/B2-docs/ibm/develop-guarded-merge-entrypoint-enforcement-governance/issues/develop-guarded-merge-entrypoint-enforcement-governance.md`
  - `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`I-20260405-1615-A` 已经把新的 promote model 冻结成正式 owner，但当前仓库执行的仍是旧规则：

1. `CONSTITUTION` / `LAWS` / `pre-test-merge-flow.md` 仍允许或默认 `feature/* -> develop`。
2. `pr-merge-guarded` tests 仍阻止 `test-pre-merge-* -> develop`。
3. 如果只改文档不改 gate，或者只改 gate 不改文档，就会在同一时间保留两套互相冲突的合法路径。

因此这条 owner 的职责不是重新研究 promote model，而是把新模型接到治理真源和 protected-branch gate 上，并让 regression tests 一起对齐。

## Scope

1. 同步更新新模型直接耦合的 governance truth sources：
   - `docs/CONSTITUTION.md`
   - `docs/LAWS.md`
   - `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
   - 必要的 related skills / `AGENTS.md`
2. 同步更新 protected-branch promotion gate enforcement：
   - `pr-merge-guarded`
   - 相关 hooks
   - 相关 governance gate / tests 中与 merge source 语义直接耦合的部分
3. 让 `test-pre-merge-*` family 成为 `develop` 的 canonical promote source family，并保持 `hotfix/* -> develop` 合法。
4. 阻止 `feature/* -> develop` 作为正常路径继续存在。
5. 保持 single-feature lane 与 explicit multi-bundle lane 共享同一 canonical family 前缀，而不新增第二前缀。

## Non-Goals

1. 不在本 owner 内实现 family lifecycle automation。
2. 不在本 owner 内定义或自动生成 multi-bundle manifest 的最终格式。
3. 不在本 owner 内实现 paired create / batch create UX。
4. 不在本 owner 内扩大到 runtime / fleet-status / stale visualization surfaces。
5. 不在本 owner 内重新打开 promote model 的高层产品讨论，除非当前 owner package 证明前一条 owner 不可执行。

## Acceptance

1. 新 owner 明确把 truth-source update 与 promotion gate enforcement 绑定为同一完成面，而不是拆成两个漂移 owner。
2. `CONSTITUTION` / `LAWS` / `pre-test-merge-flow.md` / relevant skills 同步表达：
   - `develop` 的正常 promote source 是 `test-pre-merge-*` family 与 `hotfix/*`
   - `feature/* -> develop` 作为正常路径被阻止
   - `test-pre-merge-*` family 覆盖 single-feature 与 explicit multi-bundle 语义
3. `pr-merge-guarded` 与直接相关 tests 同步表达相同 source-branch semantics。
4. 本 owner 不扩大到 lifecycle automation、manifest generation、paired create。
5. 文档和脚本对齐后，后续 lifecycle automation owner 不需要再回头改 promote source 的高层定义。

## IBM Handoff

- implementation_scope_summary:
  - `I-20260405-1805-A` 负责把已冻结 promote model 接到治理真源和 protected-branch gate。
  - 这条 owner 内允许同时修改 truth sources 与 gate scripts，因为两者需要同轮收敛。
  - stale automation、manifest generation、paired create、runtime surfaces 仍由后续 owner 承接。
- required_doc_refs:
  - `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`
  - `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805brainstorms/b-test-pre-merge-family-promotion-gate-enforcement-governance.md`
  - `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805prd.md`
  - `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805pre-tests.md`
  - `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805tasks.md`
  - `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`

## Verification

- `./bin/governance-check`
- review the updated `CONSTITUTION` / `LAWS` / `pre-test-merge-flow.md` together with `pr-merge-guarded`
- confirm the owner still excludes lifecycle automation

## Completion

- `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- `docs/B1-docs/raw-20260405T230200Z/candidates.md`
- `docs/B1-docs/raw-INDEX.md`
- `docs/milestones.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `AGENTS.md`
- `docs/system/workspace/hooks/README.md`
- `docs/system/workspace/hooks/pre-merge-commit.sh`
- `docs/system/workspace/scripts/quality/governance-check`
- `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
- `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
- `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- `docs/system/workspace/skills/branch-management/references/semantic-regression-checklist.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805code-reviews/20260405-test-pre-merge-family-promotion-gate-enforcement-implementation-decision.md`
- `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805code-reviews/20260405-test-pre-merge-family-promotion-gate-enforcement-verification.md`

## Next

1. `2026-04-05` closeout: governance truth sources, protected-branch gate scripts, and focused regressions now all enforce `test-pre-merge-*|hotfix/* -> develop` while blocking `feature/* -> develop` as a normal path.
2. Follow-on work should stay narrow to lifecycle automation, batch manifests, or paired create UX rather than reopening source-branch policy.
3. Any future reopen must prove a real mismatch between active truth sources and the enforced gate, not just request broader workflow automation.
