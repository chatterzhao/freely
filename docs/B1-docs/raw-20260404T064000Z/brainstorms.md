# Brainstorms - 20260404-0640--protected-branch-merge-receipt-gap-followthrough

## Context

`protected-branch-merge-receipt-hardening` 已经完成了两件事：

- canonical trailer-bearing merge 的即时 receipt contract
- break-glass receipt ledger 的 parity / legacy_backfill audit

但最近对 `develop` merge 历史的人工复核暴露出一个新的 blind spot：merge commit `908a6ad` 是普通 guarded merge，却只有 subject，没有 `Freely-Merge-Path` / `Freely-Bypass-Mode` / `Freely-Source-Branch`。当前 `governance-check` 只审 HEAD protected merge 和 break-glass ledger，所以这类历史 receipt gap 可以留在 ancestry 里而不被 gate 拦住。

## Why This Is A New Follow-On

这不是 reopen `I-20260402T191200Z-A` 的理由。旧 owner 已经明确关闭，并写明：

- parity audit、guarded completion handshake、staged merge-gate boundary 已冻结
- 之后若再出现 protected-branch merge receipt gap，应新开一个更窄 follow-on

因此这条 lane 只处理一个问题：

1. 历史上已经发生、但 merge commit 本身缺 canonical trailer 的普通 protected merge，如何被显式 backfill 并持续接受审计。

## Candidate Direction

最小可行 contract：

1. 新增一个只用于“普通 protected merge receipt gap”的 backfill ledger。
2. `governance-check` 按该 ledger 的 effective date 回扫 protected branch merge history。
3. 对于 break-glass merge，继续由现有 break-glass ledger 管。
4. 对于带 canonical trailer 的普通 merge，禁止再写 backfill 条目。
5. 对于像 `908a6ad` 这样的缺 receipt 历史 merge，必须有 explicit backfill 条目、follow-on owner 和 evidence_refs，否则 `governance-check` 失败。

## Non-Goals

- 不重写 merge 历史。
- 不重新定义 `pr-merge-guarded` 正常路径的 trailer contract。
- 不扩展到 break-glass policy 本身。
- 不把 receipt gap 伪装成“允许普通 merge 没 trailer”。

## Working Conclusion

应 materialize 一个新的窄 owner：

- 名称：`protected-branch-merge-receipt-gap-followthrough`
- scope：普通 protected merge 的历史 receipt gap backfill ledger + ancestry audit
- first evidence：merge `908a6ad`
