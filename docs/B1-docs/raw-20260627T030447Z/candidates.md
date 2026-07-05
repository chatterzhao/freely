---
candidate_id: C-20260627T030447Z-A
status: promoted
source_raw: raw-20260627T030447Z
created_at: 2026-06-27
milestone: M-20260627T030447Z-A
---

## C-20260627T030447Z-A: legacy issue

- candidate_format_version: v2
- title: 移除工具适配器硬编码，改为 registry 驱动
- status: promoted
- decision_reason: tool-registry.toml 已是唯一真相来源，bash 不应维护平行硬编码列表
- next_action: B2_IBM → dev → pr-create → pr-merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `tool_supported_adapters_for_runtime()` 改为从 registry 读 `adapters.supported`
  - `tool_default_adapter()` / `tool_default_adapter_for_runtime()` 改为从 registry 读 `adapters.default`
  - `AI_TOOL_ADAPTER` 正确导出给子进程
  - direct 未实现时打印清晰错误信息
  - tool-registry.toml 添加 `[tool.adapters]` 文档注释
- promotion_gate: 代码变更完成，freely daemon 可通过 ACP 启动 claude manager
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: subagent
  - summary: 审查 4 个文件变更，确认注册表驱动逻辑正确
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260627T030447Z-A/issue.md
- milestone: M-20260627T030447Z-A
- session_refs: []
