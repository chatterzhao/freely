---
candidate_id: C-20260701T013527Z-A
status: promoted
source_raw: raw-20260701T013527Z
created_at: 2026-07-01
milestone: M-20260701T013527Z-A
---

## C-20260701T013527Z-A: legacy issue

- candidate_format_version: v2
- title: 将 get_config 调用替换为 bash indirect variable expansion
- status: promoted
- decision_reason: load_config 已通过 toml2env 将所有 config.toml 值导出为环境变量，直接用 `${!_config_key:-}` 读取，零 IO、无新函数
- next_action: B2_IBM 设计 → dev 应用行级修复 → test 验证 daemon 启动无报错
- revisit_trigger: N/A（已 promote，简单修复无需重新审视）
- acceptance_criteria:
  - daemon 启动时不再报 `get_config: command not found`
  - ACP bridge 能从 config.toml 读取 FREELY_ACP_*_BIN 路径
  - 不影响其他功能
- promotion_gate: 修复后 daemon start 无 get_config 错误
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-sonnet-4-6
  - mode: subagent
  - summary: 确认 get_config 无其他调用者，修复方案正确
  - verdict: pass
- promoted_issue_id: I-20260701T013527Z-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260701T013527Z-A/issue.md
- milestone: M-20260701T013527Z-A
- session_refs: []
