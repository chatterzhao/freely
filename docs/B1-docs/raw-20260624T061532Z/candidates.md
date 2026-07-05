# Candidates
## C-20260624T061532Z-A: legacy issue
- candidate_format_version: v2
- title: 删除 query tool 中 JSON5 兼容函数
- status: promoted
- decision_reason: JSON5 文件已删除，兼容函数变成死代码
- next_action: pr-create → pr-merge → wt-close
- acceptance_criteria:
  - _strip_json5 / _load_json5 / _load_registry 已删除
  - import re 已删除
  - _resolve_registry 直接调用 _load_toml
- promotion_gate: 代码修改 + query tool 功能验证
- promoted_issue_path: docs/issues/I-20260624T061532Z-A/issue.md
- milestone: M-20260624T061532Z-A
