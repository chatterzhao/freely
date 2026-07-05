# PRD: protected-branch-merge-receipt-hardening

## Goal

在不 reopen break-glass policy owner 的前提下，补齐 protected-branch merge path 的 residual hardening：completion-only boundary、receipt/ledger parity audit，以及 staged/touched regression coverage。

## Why Now

closeout 之后 root `develop` 又出现一组未归属 staged patch，说明 protected-branch merge path 仍存在 residual hardening signal；但这组 patch 同时掺入了 regression 和 unrelated watchdog revert。需要先把 follow-on owner 物化，防止再出现“根目录脏改 + 无 owner”的继续修补。

## Product Surface

- `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- `docs/system/workspace/hooks/pre-merge-commit.sh`
- `docs/system/workspace/scripts/quality/governance-check`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded*`
- `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
- `docs/system/workspace/scripts/tests/test-governance-merge-gate`

## Non-Goals

- 不改写 break-glass whitelist
- 不重做 protected branch 全部治理
- 不吸收 watchdog repo-root resolution
- 不通过删掉 staged-view / initial-receipt tests 来“修复” gate friction

## Non-Negotiables

- `merge_completion_only` 不能退化
- receipt trailer 与 ledger truth 不能继续各管各的
- staged merge gate 不能因为 false-negative 焦虑而回退成 working-tree-only
- unrelated watchdog regressions 不能搭车进这个 owner

## Context Pack

- canonical `develop` 当前已经有 guarded completion 与 break-glass receipt contract
- `test-pr-merge-guarded-hooked-initial-merge-receipt` 证明真实 pre-merge hooks 下，初始 merge 仍能保留 receipt
- `governance-merge-gate --staged` 当前有 staged-view coverage，防止 protected-branch pre-merge 只看 working tree
- root staged patch 试图回退上面两点，因此 follow-on 必须先冻结 regression boundary

## Decomposition Tree

1. classify residual patch
2. freeze completion-only and staged regression boundary
3. freeze parity audit contract
4. decide first implementation slice

## Phase-1 Follow-On Contract

### Patch classification truth

root staged patch 必须先被分类：

- `keep-as-signal`
- `already-absorbed`
- `drop-as-regression`

没有这个分类，不允许直接把 patch 继续推进成实现。

### Completion-only truth

- break-glass short-circuit 只能服务 `pr-merge-guarded complete`
- initial clean merge 仍必须走 canonical guarded merge path
- 不允许通过“更直接的 merge message 写法”绕开 current completion semantics

### Receipt parity truth

`governance-check` follow-on 需要至少比较：

- `Freely-Merge-Path`
- `Freely-Bypass-Mode`
- `Freely-Source-Branch`
- 当 `break_glass` 时：
  - `Freely-Break-Glass-Reason`
  - `Freely-Blocked-Gate`
  - `Freely-Operation-Scope`
  - `Freely-Follow-On-Issue`
  - `Freely-Evidence-Ref` set

如果 ledger 与 merge trailer 在这些字段上漂移，必须作为 audit failure surface，而不是继续只检查“有没有记录”。

历史上已经存在少量 post-hoc ledger backfill，但 merge commit 本身没有 canonical trailer。phase-1 follow-on 必须把这类 receipt 显式标成 grandfathered `legacy_backfill`，而不是让今天的 trailer-bearing break-glass merge 用同一借口逃过 parity audit。

### Staged regression boundary

- `governance-merge-gate` 仍必须支持 staged owner artifact 视图
- sibling candidate context 不能因为整文件 touched 而被误判成 directly touched candidate
- regression test 必须同时覆盖：
  - staged-only owner visibility
  - sibling-context-only candidate immunity

## Eval Plan

### Pre-merge focused regression

- environment: feature worktree
- evidence: targeted tests + issue-bound docs
- failure signal: 删除 canonical tests、回退 staged-view、或放宽 completion path 才能让变更通过

### Post-merge integration acceptance

- environment: `develop`
- evidence: protected-branch receipt audit 能报 parity drift
- failure signal: merge trailer 与 ledger 不一致时仍被当作 pass

## Execution Slices

1. IBM contract freeze
2. receipt parity audit implementation
3. staged regression guardrail tests
4. completion handshake hardening

## Slice Status

- `receipt_ledger_parity_audit`: implemented in this owner
- `guarded_completion_handshake_hardening`: implemented in this owner
- `merge_gate_false_negative_regression_coverage`: carried forward as an explicit regression boundary with canonical tests already present; no runtime change is needed in this slice

## Guarded Completion Handshake Truth

- protected-branch merge completion 不能只靠 `FREELY_*` env 自报身份
- `pr-merge-guarded` 必须在 `git merge --continue` 前写出 git-dir scoped guarded completion state
- `pre-commit` / `pre-merge-commit` 必须同时验证：
  - `FREELY_GUARDED_MERGE_COMPLETION=1`
  - active `MERGE_HEAD`
  - guarded state 中的 `target_branch` 与当前分支一致
  - guarded state 中的 `source_branch` resolve 后与 `MERGE_HEAD` 一致
- break-glass completion 还必须要求 guarded state 明确声明 `bypass_mode=break_glass`
- env-only spoof 或手工 `git commit` 不得通过 protected-branch completion hooks
