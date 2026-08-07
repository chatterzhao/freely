---
issue_id: I-20260807T071225Z-A
issue_path: docs/B2-docs/ibm/scan-frontmatter/raw-20260807T071225Z/issues/I-20260807T071225Z-A.md
phase_state: in_dev
---

- issue_id: I-20260807T071225Z-A
- issue_path: docs/B2-docs/ibm/scan-frontmatter/raw-20260807T071225Z/issues/I-20260807T071225Z-A.md

## Implementation Decision Note

- decision: parse_frontmatter 优先 yaml.safe_load，失败回退行解析 + bullet 补充
- why_this: 嵌套 YAML 正确解析；兼容 legacy bullet 混合格式
- alternatives_considered: flow 单行规避（platform_ids 变字符串，否）；仅改行解析（嵌套仍错，否）
- boundary_non_goals: 不改变 scan 其余逻辑；不迁移数据格式
- residual_risk: fallback 路径对极端混合格式仍可能误读（legacy 已稳定）
