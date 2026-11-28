---
issue_id: I-20261128T065937Z-A
issue_path: docs/B2-docs/command-wrapper/install-command-parity/raw-20261128T065937Z/issues/I-20261128T065937Z-A.md
phase_state: completed
---

# Implementation Decision Note
- issue_id: I-20261128T065937Z-A
- issue_path: docs/B2-docs/command-wrapper/install-command-parity/raw-20261128T065937Z/issues/I-20261128T065937Z-A.md
- decision: 入口注释去非打包文档路径；测试型 checker 移到 scripts/tests/。
- why_this: commands.md 经评审不随包发布；扩 allowlist 或放宽 parity 都是设计漂移。
- alternatives_considered: 扩 allowlist（推翻既有判决）；放宽 parity（削弱 fail-closed）——均排除。
- boundary_non_goals: 不改 package-runtime-file-parity 判据；不改 allowlist；不改 dispatcher。
- residual_risk: 其他 quality 脚本若引用非打包顶层文档仍会被 parity 拦截（设计如此，需各自修正位置或引用）。
