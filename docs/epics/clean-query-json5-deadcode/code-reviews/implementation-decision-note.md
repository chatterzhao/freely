# Implementation Decision Note: clean query tool JSON5 dead code
- issue_id: I-20260624T061532Z-A
- issue_path: docs/issues/I-20260624T061532Z-A/issue.md
- milestone: M-20260624T061532Z-A
## Implementation Decision Note
- decision: 删除 _strip_json5/_load_json5/_load_registry，_resolve_registry 直接 _load_toml
- why_this: JSON5 文件已删除，这些函数不再被调用
- alternatives_considered: 保留死代码 — 增加维护负担
- boundary_non_goals: 不修改 _resolve_registry 的 ~/.freely 覆盖逻辑
- residual_risk: 无
