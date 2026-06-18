# Candidates

## C-20260618T040226Z-A: pr-review-guarded — 独立 PR review 门禁

- candidate_format_version: v2
- title: pr-review-guarded command + review document + full workflow integration
- status: promoted
- decision_reason: ef251886/15fa666c receipt 丢失暴露了 pr-create 和 pr-merge 之间的 review gap。行业标准要求独立 review 作为 merge 前置步骤。Freely 需要 machine-readable review verdict 落盘。
- next_action: B2_IBM → dev 实现 → 18+ 文件修改
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `bin/pr-review-guarded` 命令可用，6 个 review 维度检查
  - review 文档格式标准化（`pr-review-{PR#}.md`）
  - pr-merge-guarded 检查 review verdict=pass 才能合并
  - 全链路 8 个 skill 文件更新为 `pr-create → pr-review → pr-merge`
  - wt-create 下一步提示更新
  - pr-create-guarded 成功提示更新
  - AGENTS.md 核心开发流程更新
  - IBM framework 文档更新
  - governance-merge-gate 增加 review 文档检查
  - pre-push hook 提示更新
  - `deploy-skills` 部署后生效
- promotion_gate: 所有文件修改完成，review 文档格式正确，门禁集成可用
- open_questions:
  - Phase 2: GitHub PR review API 同步是否必要？（当前可先手动 gh pr review）
  - review 维度是否应该可扩展？（通过配置文件或 skill 扩展）
- acceptance_reviews:
  - reviewer: claude
  - mode: fresh
  - summary: 审查 6 个 review 维度的完整性和 feasibility
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260618T040226Z-A/issue.md
- milestone: M-20260618T040226Z-A
- session_refs: []
