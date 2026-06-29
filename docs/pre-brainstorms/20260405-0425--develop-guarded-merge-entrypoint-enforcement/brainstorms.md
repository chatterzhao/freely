# Brainstorms - 20260405-0425--develop-guarded-merge-entrypoint-enforcement

## Context

Freely 已经有 `freely pr-merge-guarded` 作为 protected-branch merge 的 canonical 入口，也已经为 break-glass completion 和 receipt 审计建好了 contract。但这轮狗粮里仍然再次发生了一个更窄的问题：

- 操作者直接在 `develop` 上执行了裸 `git merge`
- merge 本身因为 staged evidence 看起来合法而通过
- 结果又制造出一条新的“不是仓库自有入口发起的 protected merge”

这说明当前门禁只在“merge 内容是否合法”上工作，却没有把“merge 必须从哪个入口发起”收成 canonical gate。

## Why This Is A New Follow-On

这不是 reopen 旧 owner 的理由。已完成的 merge governance owners 分别冻结了：

- break-glass completion contract
- merge receipt parity / historical backfill audit

但它们都没有把“裸 `git merge` 在 `develop` 上本身就应被挡住”写成 hook 级 entrypoint enforcement。因此这次问题应 materialize 为新的窄 follow-on，而不是回写已完成 owner。

## Candidate Direction

最小可行 contract：

1. `develop` 上只允许带 canonical guarded handshake 的 merge commit 继续进入 `pre-merge-commit` 后续 gate。
2. 裸 `git merge` / `git merge --continue` 若没有 `pr-merge-guarded` 写入的 state 和 completion marker，hook 直接拒绝，并明确提示改用 `freely pr-merge-guarded`。
3. 一旦 guarded handshake 存在，原有 governance materialization gate 与 promotion ownership gate 仍然照常执行，避免“入口 enforcement 把下游 gate 短路掉”。
4. `pr-merge-guarded` 正常初始 merge 与 `pr-merge-guarded complete` 冲突 completion 路径必须继续通过。

## Non-Goals

- 不尝试把本地 Git client-side hook 变成物理上不可绕过的 server-side enforcement。
- 不重写 break-glass whitelist。
- 不扩张到新的 receipt ledger 语义。
- 不在这条 owner 里顺手改 main / `test-pre-merge-*` 的所有 merge policy；先把实际复现的 `develop` 入口误用收住。

## Working Conclusion

应 materialize 一个新的窄 owner：

- 名称：`develop-guarded-merge-entrypoint-enforcement-governance`
- scope：`develop` merge 进入 `pre-merge-commit` 前必须已经具备 `pr-merge-guarded` canonical handshake
- first evidence：本轮在 `develop` 上再次发生的手工裸 `git merge` 误用
