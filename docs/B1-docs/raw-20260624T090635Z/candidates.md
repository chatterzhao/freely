# Candidates

## C-20260624T090635Z-A: legacy issue

- candidate_format_version: v2
- title: tool-launchers.sh adapter 查询/ACP dispatch/tool family 解析注册表驱动化
- status: promoted
- decision_reason: registry 已声明全部所需字段，runtime 查询路径未打通。这是新增工具只需配 TOML 的最后障碍
- next_action: B2_IBM → dev 实现 → pr-create → pr-merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - tool_supported_adapters() 从 registry adapters.supported 读取，未注册默认 direct
  - tool_supported_launch_kinds_for_adapter() 从 registry adapters.launch_kinds 读取
  - tool_run_acp_from_prompt_file() 对已注册新工具不报错，走通用 ACP 路径
  - _resolve_tool_family() 未命中时扫描 registry aliases 做反向匹配
  - tool_supports_add_dir_boundary() 从 launch.direct.add_dir_boundary 读取
  - monitor-ai-acp.sh 不包含 claude/codex/opencode 硬编码 permission fallback
  - 现有 claude/codex/opencode 三工具行为不变
- promotion_gate: 所有函数改造完成 + 三工具回归通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - summary: 对照 registry schema 验证每个函数的查询路径
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260624T090635Z-A/issue.md
- milestone: M-20260624T090635Z-A
- session_refs: []
