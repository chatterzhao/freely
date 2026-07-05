# Candidates

## C-20260624T004510Z-A: legacy issue

- candidate_format_version: v2
- title: deploy-skills 默认部署到 tool-registry.json5 全部已安装 tool
- status: promoted
- decision_reason: opencode 缺通配符是 copy-paste bug；默认只部署单个 tool 导致 daemon 切换/fallback 时 skill 缺失
- next_action: pr-create → pr-review → pr-merge → wt-close
- revisit_trigger: #3399 registry 格式变更为 TOML 时同步更新 JSON5 读取逻辑
- acceptance_criteria:
  - `opencode-apikey-*` tool 名匹配 opencode* 通配符
  - 无 `--tools` 参数时自动检测 registry 中所有已安装 tool
  - `--tools` 显式指定时保持精确控制
- promotion_gate: 代码修改完成 + 手动测试通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.8
  - mode: subagent
  - summary: review deploy-skills 变更的正确性和安全性
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260624T004510Z-A/issue.md
- milestone: M-20260624T004510Z-A
- session_refs: []
