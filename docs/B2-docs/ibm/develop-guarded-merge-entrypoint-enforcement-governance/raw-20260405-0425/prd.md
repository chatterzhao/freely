# PRD: develop-guarded-merge-entrypoint-enforcement-governance

## Problem

`develop` 上当前同时存在两种 merge 入口：

1. canonical `freely pr-merge-guarded`
2. 裸 `git merge`

由于 `pre-merge-commit` 只检查 merge 内容的治理合法性，而不检查 merge 是否来自 canonical 入口，第二种入口仍能成功。这使得 protected merge 的操作语义继续漂移。

## Product Requirement

Freely 必须把 `develop` merge 的入口约束成单一路径：

- merge commit 进入 `pre-merge-commit` 时，必须已经携带 `pr-merge-guarded` canonical handshake
- 没有 handshake 时，hook 直接拒绝并告诉操作者改用 `freely pr-merge-guarded`
- 有 handshake 时，继续照常执行治理 gate，而不是把后续 gate 短路

## Canonical Surfaces

- `docs/system/workspace/hooks/pre-merge-commit.sh`
- `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
- `docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`

## Out Of Scope

- 将 client-side hook 升级为物理不可绕过的 server policy
- 新增 receipt ledger 语义
- 重新解释 break-glass 语义
