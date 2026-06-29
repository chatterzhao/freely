---
candidate_id: C-20260629T095905Z-A
status: promoted
source_raw: raw-20260629T095905Z
created_at: 2026-06-29
milestone: M-20260629T095905Z-A
---

## C-20260629T095905Z-A: 优化 workflow skill 覆盖缺口

- candidate_format_version: v2
- title: 优化 workflow skill — 覆盖无 raw issue 场景、cd 工位提示、CLAUDE.md 启动链
- status: promoted
- decision_reason: AI 跳过 B1/B2/RED 直接写代码，根因是 workflow skill 缺少阶段 0 和 cd 提示，CLAUDE.md 链不够强制性。Option B 改动最小且保持 skill 权威性。
- next_action: B2_IBM → 创建 I-* issue + pre-tests → dev 修改 3 个文件
- revisit_trigger: 又有 AI 跳过 IBM 流程直接写代码
- acceptance_criteria:
  - AI 遇到问题没有 raw issue 时，知道先 freely feedback 再 wt-create
  - AI 在 wt-create 后知道 cd 到开发工位目录
  - 新 CLAUDE.md 让 AI 启动后首先读 AGENTS.md
  - AGENTS.md 和 workflow skill 中的 wt-create 命令统一使用 --kind 参数
- promotion_gate: 3 个文件修改完成，deploy-skills 执行
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: subagent
  - summary: 审查 workflow skill 修改是否覆盖所有缺口，CLAUDE.md 是否足够强制性
  - verdict: pass
- promoted_issue_path: docs/epics/skill-docs-optimization/description-and-chain-unify/raw-20260629T095905Z/issues/I-20260629T095905Z-A.md
- milestone: M-20260629T095905Z-A
- session_refs: []
