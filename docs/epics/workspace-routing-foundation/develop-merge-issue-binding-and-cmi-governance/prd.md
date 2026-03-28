# PRD: develop-merge-issue-binding-and-cmi-governance

## Goal

确保 develop-bound merge 不能再靠 candidate-only evidence 或 borrowed owner issue 通过，而必须绑定到一条可审计的 owner issue 和同线 `C/M/I` 生命周期。

## Why Now

真实 dogfood replay 已经证明：

- `pre-merge-commit` 时序问题会让 gate 根本没跑
- 即使 hook 修好，`absorbed` 候选仍可能因为 owner issue 静态存在而过门禁

所以这次需要把“merge 基于具体 issue”冻结成能力真源，而不是继续停留在 supporting evidence。

## Product Surface

- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/hooks/pre-merge-commit.sh`
- `bin/governance-merge-gate`
- `bin/test-pre-merge-commit-hook`

## Non-Goals

- 一次性修复所有历史 issue id key mismatch
- 把研究型 closure 的所有例外都塞进这一批
- 引入新的数据库或 manifest

## Non-Negotiables

- develop merge 没有具体 issue/progress/review owner，不放行
- touched candidate 与 touched owner issue 不同线，不放行
- `promoted` / `absorbed` 的 owner 若未进入同次 diff，不放行

## Execution Slices

1. materialize `C-20260321-1835-A` 为独立 issue
2. 收紧 `governance-merge-gate`
3. 增补 borrowed owner regressions
4. 用真实 hook 路径复核

## Revisit Triggers

- 若未来需要把允许状态再收窄到更少的 phase / status
- 若历史 absorbed 候选需要批量迁移到更硬的 owner binding contract
