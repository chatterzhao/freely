---
issue_id: I-20261113T141456Z-A
issue_path: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141456Z/issues/I-20261113T141456Z-A.md
phase_state: in_b2_ibm
---

# Implementation Decision Note
- issue_id: I-20261113T141456Z-A
- issue_path: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141456Z/issues/I-20261113T141456Z-A.md
- decision: config 白名单单源；GATE 1 给 lane 指引；batch 显式范围。
- why_this: 双真源与不可操作诊断会把门禁冲突转嫁成语义退化。
- alternatives_considered: 保留硬编码默认；第三种 lane——均排除。
- boundary_non_goals: 不放宽实现路径跨 raw；不改 reason 前缀。
- residual_risk: 未配置 config 的项目不再有 governance-only 豁免（fail-closed，符合设计）。
