---
issue_id: I-20260717T041435Z-A
issue_path: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/issues/I-20260717T041435Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260717T041435Z-A
- issue_path: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/issues/I-20260717T041435Z-A.md

## Implementation Decision Note

- decision: pretests-gate extract 与 pr-review-guarded 取值均引号可选化（裸/单/双/反引号）
- why_this: 双向兼容全部存量格式，无文档迁移成本；解析 robustness 归工具层
- alternatives_considered: 统一强制无引号并改 review（需迁移存量，否）；连 acp_bridge glob 一并修（语义不同域，另行 B1）
- boundary_non_goals: 不改 RE 校验语义、不改格式规范、glob 问题另案
- residual_risk: 值内含引号字符的病态路径会被剥——路径规范不含引号，可接受
