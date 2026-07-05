# Candidates

## C-20260624T013737Z-A: legacy issue

- candidate_format_version: v2
- title: tool-registry TOML 格式迁移 + config_schema 字段抽象层（Phase 1+2/10）
- status: promoted
- decision_reason: 28 处硬编码是增加新 tool 的最大障碍。TOML 格式 + config_schema 翻译层是消除硬编码的基础设施。Phase 1+2 先建立基础层，后续 PR 迁移其余。
- next_action: B2_IBM → dev-loop → pr-create → pr-merge
- revisit_trigger: 后续 PR 继续迁移 Phase 3-10 的剩余 case 分支
- acceptance_criteria:
  - tool-registry.toml 存在且包含 claude/codex/opencode 完整 schema
  - tool-registry-query.py 支持 TOML 读取 + ~/.freely 覆盖优先级
  - monitor-ai-acp.sh 用 config_schema.fields.permission_bypass 替代硬编码字段名
  - tool-launchers.sh 用 config_schema 读取权限字段
  - deploy-skills 继续正常工作（已在 #3397 改为 registry 驱动）
  - 加新 tool 只需在 TOML 中加一个 section
- promotion_gate: TOML 注册表文件创建 + query tool 更新 + 权限读取路径重构完成 + 手动测试通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.8
  - mode: subagent
  - summary: 审查 TOML schema 设计、query tool 兼容性、权限读取重构安全性
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260624T013737Z-A/issue.md
- milestone: M-20260624T013737Z-A
- session_refs: []
