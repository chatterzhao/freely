---
candidate_id: C-20260626T150328Z-A
status: promoted
source_raw: raw-20260626T150328Z28Z
created_at: 2026-06-26
milestone: M-20260626T150328Z-A
---

## C-20260626T150328Z-A: legacy issue

- candidate_format_version: v2
- title: TOML array comma-join + feedback validation + bash 3.2 guard
- status: promoted
- decision_reason: Root cause is Python/bash format contract mismatch. Fixing both sides (Python comma-join + bash alias loop) is the correct long-term fix. Adding feedback validation prevents future malformed issues. Guarding empty array iteration fixes bash 3.2 compat.
- next_action: B2_IBM → pr-create-guarded → pr-merge-guarded → wt-close
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - tool-registry-query.py adapters.supported 返回逗号分隔的 "direct,acp"
  - _resolve_tool_by_binary aliases 循环正确处理逗号分隔
  - cmd_feedback 拒绝无前缀、过长标题、过短body、无 ## section 的输入
  - _ensure_acp_bridge_running 在 kiro-cli (未注册 base_tool) 场景不崩溃
- promotion_gate: 三个文件修改已完成且通过基本验证测试
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - summary: 验证 comma-join 输出格式、feedback 校验拦截、bash 3.2 空数组保护
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260626T150328Z-A/issue.md
- milestone: M-20260626T150328Z-A
- session_refs: []
