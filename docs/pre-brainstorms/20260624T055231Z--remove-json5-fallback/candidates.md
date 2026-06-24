# Candidates
## C-20260624T055231Z-A: 彻底移除 JSON5 回退
- candidate_format_version: v2
- title: 删除 JSON5 文件，所有消费端只读 TOML
- status: promoted
- decision_reason: #3399 重构不彻底导致 regression
- next_action: pr-create → pr-merge → wt-close
- acceptance_criteria:
  - tool-registry.json5 已删除
  - deploy-skills 检测全部已安装 tool（claude/codex/opencode）
- promotion_gate: 代码修改 + 手动测试
- promoted_issue_path: docs/issues/I-20260624T055231Z-A/issue.md
- milestone: M-20260624T055231Z-A
