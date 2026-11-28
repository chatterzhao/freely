---
issue_id: I-20261113T110656Z-A
issue_path: docs/B2-docs/command-wrapper/implementation-projection/raw-20261113T110656Z/issues/I-20261113T110656Z-A.md
phase_state: completed
---

# Implementation Decision Note
- issue_id: I-20261113T110656Z-A
- issue_path: docs/B2-docs/command-wrapper/implementation-projection/raw-20261113T110656Z/issues/I-20261113T110656Z-A.md
- decision: 批次① 三条实现迁 scripts 真源，bin 入口改薄投影，registry 删条目。
- why_this: scripts/README.md 的 bin 投影层契约与 check-bin-projection 的 shrink 规则。
- alternatives_considered: 永久豁免；单 PR 迁全部 13 条——均排除。
- boundary_non_goals: 不动其余 10 条；不放宽门禁；不改 dispatcher。
- residual_risk: 真源路径变化需刷新 projection.lock；原 bin 头部长注释丢失，属投影层允许范围。
