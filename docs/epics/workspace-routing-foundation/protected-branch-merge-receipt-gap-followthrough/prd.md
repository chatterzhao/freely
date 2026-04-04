# PRD

## Goal

让 Freely 对普通 protected-branch merge 的历史 receipt gap 也保持可审计：merge commit 若已经缺失 canonical trailer，必须有显式 backfill ledger 和 owner，而不是永远依赖人工发现。

## Requirements

1. 定义一个独立于 break-glass ledger 的普通 merge receipt-gap backfill 真源。
2. `governance-check` 必须按 effective date 回扫 protected branch merge history。
3. 缺 trailer 的普通 protected merge 必须有 matching backfill entry 才能通过。
4. trailer-bearing merge 不得继续声明普通 gap backfill。
5. `908a6ad` 作为第一条真实 gap 必须被 ledger 吸收。

## Non-Goals

- 不改变 break-glass ledger contract
- 不允许未来正常 merge 用 backfill 代替 canonical trailer
- 不重写现有 git 历史
