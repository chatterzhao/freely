# Brainstorms - 20260402-1912--protected-branch-merge-receipt-hardening

## Context

`protected-branch-hook-bypass-breakglass-governance` 已经吸收到 canonical `develop`，并且 closeout 已合入 `33226d6`。那条 owner 解决的是：

- break-glass 白名单与禁止场景
- guarded completion / receipt 的 phase-1 contract
- protected-branch merge 的 receipt / ledger audit

但 closeout 之后，canonical `develop` 根目录还留下一组未归属的 staged 改动，暴露出“仍有人试图继续修 merge gate / merge receipt”的 residual signal。当前先要判断这组信号到底是不是还没被吸收的新问题，而不是把根目录的 staged patch 直接当答案。

## Current Repo Facts

当前可验证事实：

- canonical `develop` HEAD 是 `33226d6`
- `feature/hook-bypass-breakglass-governance-20260402-0020` 已经通过 `52f55c0` 合入 `develop`
- closeout lane `feature/hook-bypass-breakglass-closeout-20260402-0235` 已通过 `33226d6` 写回 `completed`
- 旧的 `feature/hook-bypass-break-glass-governance-20260402-1719` worktree 仍在，但只有 dirty 的 pre-brainstorm 文档，既没 materialize 到 canonical `docs/`，也没形成当前 owner 真相

当前根目录 staged 改动其实混了两类问题：

1. merge-governance residual hardening
   - `docs/system/workspace/scripts/quality/governance-merge-gate`
   - `docs/system/workspace/scripts/worktree/pr-merge-guarded`
   - `docs/system/workspace/scripts/tests/test-governance-merge-gate`
   - `docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
2. watchdog path-resolution revert
   - `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
   - `docs/system/workspace/scripts/tests/test-availability-watchdog-path-resolution`

第二类不是新的 merge-governance owner。仓库历史已经有 commit `e506982` (`Stabilize watchdog repo-root resolution`)，而且它已在 `develop` ancestry 内；根目录 staged 版本实际上是在回退这个已吸收修复，并删除对应测试。因此它不是当前要 materialize 的缺口。

## What Problem Still Remains

在把 watchdog revert 剥离后，真正还值得研究的是更窄的 merge-governance residual hardening：

- `pre-merge-commit` 的 break-glass 短路还需要继续证明只覆盖 merge completion，而不是放宽初始 clean merge
- guarded completion handshake 仍偏软，单靠环境变量约定不够稳
- `governance-check` 目前审计了 merge trailer 和 break-glass ledger 的存在，但还没有把两边字段一致性收成更硬的 canonical truth
- `governance-merge-gate` 对 staged / touched evidence 的边界已经有过一次真实误触发争议，后续 hardening 必须避免把 sibling candidate、working-tree view、staged-only owner 重新搞乱

这条问题和 `20260402-0020` 不同：

- 不是再定义“允不允许 bypass”
- 也不是再补一次 receipt 基础设施
- 而是对 phase-1 contract 的 runtime hardening 和 audit parity 做 follow-on

## Why Not Reuse 20260402-1719

旧的 `20260402-1719--hook-bypass-break-glass-governance` 候选虽然题目接近，但它的问题边界更宽：

- 还在讨论 break-glass dictionary 本身
- 还在讨论是否需要 reopen 原 owner
- 没区分 canonical absorb 的内容和 closeout 后剩余的 hardening slice

而 canonical `develop` 现在已经写明：

- `I-20260402-0020-A` 是 completed
- 若后续再出现 merge-gate false negative / stronger enforcement，需要开更窄的 follow-on owner，而不是 reopen 广义 break-glass 治理

因此继续复用 `20260402-1719` 会把已关闭的 contract 再次搅混，也会让 dirty stale worktree 伪装成 canonical owner。

## Candidate Direction

新 follow-on 应只回答四件事：

1. `merge_completion_only`
   - break-glass short-circuit 是否真的只在 merge completion 有效
2. `guarded_completion_handshake_hardening`
   - 如何减少 completion handshake 被随意伪造的空间
3. `receipt_ledger_parity_audit`
   - `governance-check` 如何校验 merge trailer 与 ledger 字段一致
4. `merge_gate_false_negative_regression_coverage`
   - 如何补强测试，防止为了 staged-view / sibling-context 争议再次把 gate 放宽到失真

明确不在这条 follow-on 范围：

- watchdog repo-root resolution
- 重开 break-glass 白名单定义
- 重做 ownership anti-stomp
- 服务端 / host-level 强制执行

## Working Conclusion

结论是：

- 现有 canonical `develop` 和其他现存 worktree 都没有正式承接这条更窄的 residual hardening
- 根目录 staged patch 不是一个可直接吸收的答案，其中还混有对已吸收 watchdog 修复的回退
- 因此应从当前 `develop` 新开 dedicated worktree，materialize 一个新的 pre-brainstorm / candidate，只承接 protected-branch merge receipt hardening
