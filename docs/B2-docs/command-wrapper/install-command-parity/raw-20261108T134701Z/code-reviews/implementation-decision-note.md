---
issue_id: I-20261108T134701Z-A
issue_path: docs/B2-docs/command-wrapper/install-command-parity/raw-20261108T134701Z/issues/I-20261108T134701Z-A.md
phase_state: completed
---

# Implementation Decision Note — I-20261108T134701Z-A
- issue_id: I-20261108T134701Z-A
- issue_path: docs/B2-docs/command-wrapper/install-command-parity/raw-20261108T134701Z/issues/I-20261108T134701Z-A.md

- decision: 删除 `bin/freely` 中未实现的 `freely install` / 自动移除 marker 承诺；新增只读静态命令名契约检查；不新增 runtime 分派。
- why_this: `freely-package --activate` 已是唯一安装真相源（R16/#4194 的 IDN 明确排除 install 命令），runtime/freely 恰好 27166 行预算，任何新分派都会破坏 `check-runtime-size`。
- alternatives: (A) 实现 `freely install` —— 双真相源 + 撞预算，排除；(C) 只删注释 —— 同类脱线会复发，排除。
- boundary: 不改 `freely-package` 行为；不改 zshrc（个人文件，非仓库产物）；不新增平台写通道；不改 dispatcher。
- residual_risk: 用户机 `~/.zshrc` 的历史 marker 注释仍写着「安装 freely 时自动移除」，本 PR 不修改个人文件；契约检查只覆盖 `bin/freely` 注释与 `commands.md` 的 `freely <cmd>` 一级命令承诺，子命令语义由各自命令负责。
