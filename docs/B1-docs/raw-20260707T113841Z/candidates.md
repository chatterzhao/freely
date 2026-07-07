---
candidate_id: C-20260707T113841Z-A
status: absorbed
source_raw: raw-20260707T113841Z
milestone: M-20260707T113841Z-A
---

## C-20260707T113841Z-A: 多阶段强制 Review 门禁

- candidate_format_version: v2
- title: feat — 三层审查保障：阶段指南 + 命令门禁 + 自动委派
- status: absorbed
- decision_reason: 在现有 A2A/SSE/ACP 架构上补三层：提示词层（phase-definitions）→ 指南层（review-guidelines）→ 命令层（pr-create-guarded + 签名检查 + 自动委派）
- next_action: B2_IBM 物化 I-* issue → 实现 review-guidelines + phase-definitions + agent_working 改造 + pr-create-guarded gate 增强
- revisit_trigger: 新增 workflow phase 时需要同步新增对应的 review-guidelines 和 phase-definitions
- acceptance_criteria:
  - 5 个阶段的审查指南文件存在且内容完整 (review-guidelines/)
  - 5 个阶段的完成定义文件存在且内容完整 (phase-definitions/)
  - agent_working 表增加 review_verdict/review_stage/reviewed_by/reviewed_at/review_findings 字段
  - pr-create-guarded gate chain 检查所有已完成 phase 的 review signature
  - review 缺失时 gate 阻塞并输出具体缺失的 phase 列表
  - ACP 可用时自动委派 Reviewer（注入对应阶段指南）
  - ACP 不可用时降级为人工审查提示（不静默跳过）
  - freely-review 的 ACP 不可用场景从 exit 0 改为明确的阻塞或降级
  - 跨模型检查：同一 tool slot 时输出 warning
- promotion_gate: agent_working schema 变更无破坏 + gate chain 逻辑正确 + 指南文件覆盖所有 phase
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260707T113841Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260707T113841Z/issues/I-20260707T113841Z-A.md
- milestone: M-20260707T113841Z-A
- session_refs: []
