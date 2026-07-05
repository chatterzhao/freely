# Issue: protected-branch-merge-receipt-gap-followthrough

- issue_id: `I-20260404-0640-A`
- title: Protected-branch merge receipt gap followthrough
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `protected-branch-merge-receipt-gap-followthrough`
- issue-name: `protected-branch-merge-receipt-gap-followthrough`
- priority: P1
- source_candidate: `docs/pre-brainstorms/20260404-0640--protected-branch-merge-receipt-gap-followthrough/candidates.md#c-20260404-0640-a`
- source_brainstorm: `docs/pre-brainstorms/20260404-0640--protected-branch-merge-receipt-gap-followthrough/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-protected-branch-merge-receipt-gap-followthrough.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
  - `docs/system/workspace/scripts/worktree/pr-merge-guarded`
  - `docs/system/workspace/scripts/quality/governance-check`
  - `docs/system/workspace/hooks/protected-branch-breakglass-receipts.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经要求 protected-branch merge 写 canonical receipt trailer，也已经对 break-glass merge 建好了 ledger parity audit。但 `develop` ancestry 里仍然出现了一个普通 guarded merge `908a6ad` 没有任何 canonical trailer。当前 `governance-check` 没有对应 ancestry audit，也没有普通 merge 的 backfill 真源，因此这类 gap 只能靠人工 review 暴露。

## Scope

1. 定义普通 protected merge receipt gap 的 canonical backfill ledger。
2. 让 `governance-check` 从 ledger effective date 起回扫 protected branch merge history。
3. 要求缺 trailer 的普通 protected merge 必须有 matching backfill entry 才能通过。
4. 禁止带 canonical trailer 的普通 merge 继续声明 gap backfill。
5. 把 `908a6ad` 作为第一条 canonical backfill 落盘。

## Non-Goals

1. 不重开 break-glass whitelist 或 break-glass receipt policy。
2. 不重写现有 merge 历史。
3. 不把 backfill ledger 变成正常 merge 缺 trailer 的常规路径。
4. 不修改 `pr-merge-guarded` 的 canonical trailer 字段集。

## Acceptance

1. 普通 protected merge 的历史 receipt gap 有独立 canonical ledger，不混进 break-glass ledger。
2. `governance-check` 能从 ledger effective date 起发现普通 protected merge 的缺-trailer ancestry gap。
3. matching backfill entry 能让历史 gap 通过审计，但 trailer-bearing merge 若声明 gap backfill 必须被拒绝。
4. `908a6ad` 的 backfill 条目必须记录 source branch、canonical merge path、bypass mode、follow-on owner 和 evidence refs。
5. focused regressions 至少覆盖：no-backfill fail、matching-backfill pass、trailer-bearing merge cannot use backfill。

## Completion

- `docs/pre-brainstorms/20260404-0640--protected-branch-merge-receipt-gap-followthrough/brainstorms.md`
- `docs/pre-brainstorms/20260404-0640--protected-branch-merge-receipt-gap-followthrough/candidates.md`
- `docs/pre-brainstorms/INDEX.md`
- `docs/milestones.md`
- `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
- `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/prd.md`
- `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/pre-tests.md`
- `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/tasks.md`
- `docs/progress/workspace-routing-foundation/p-protected-branch-merge-receipt-gap-followthrough.md`
- `docs/system/workspace/hooks/protected-branch-merge-receipt-backfills.md`
- `docs/system/workspace/scripts/quality/governance-check`
- `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

## Verification

- `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
- `./bin/governance-check`

## Next

- Completed on canonical `develop` via receipt-bearing merge `0c9701f`.
- The blocker-triage continuation branch/worktree was retired after post-merge verification passed.
- Reopen only for new trailerless protected-ancestry gaps that fall outside the current subject-matched backfill contract.
