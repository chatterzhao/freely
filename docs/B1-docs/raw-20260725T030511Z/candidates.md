---
candidate_id: C-20260725T030511Z-A
status: promoted
source_raw: raw-20260725T030511Z
created_at: 2026-07-25
milestone: M-20260725T030511Z-A
---

# Candidates

## C-20260725T030511Z-A: 配置平台 raw 副本一致性门禁

- candidate_format_version: v2
- title: 配置平台 raw 副本发现、对账与生命周期门禁
- status: promoted
- decision_reason: 当前 adapter 的大小写比较与空匹配契约已经阻断合法 `wt-create`，且 discovery、物化和 lifecycle 规则分散，必须先建立统一的配置驱动 reconciliation 边界。
- next_action: 在 B2 中物化 `I-20260725T030511Z-A`，先完成 receipt/gate 的 RED 测试，再实现 adapter discovery、reconciliation 与 lifecycle 接入。
- revisit_trigger: 平台 transport 无法提供完整且带命名空间的副本元数据，或现有 raw metadata contract 无法存储经确认的副本基线。
- acceptance_criteria:
  - 全部 active configured platform 可返回带 `platform`、remote ID、标题、正文、状态、标签、评论、更新时间和版本的 raw 副本记录。
  - 对空配置、不可达平台、分页不完整、缺副本、重复匹配、内容或状态差异生成确定的 fail-closed receipt，不能降级为空清单。
  - `wt-create`、PR create/review/merge、`wt-close` 复用同一个只读 gate，且 gate 不隐式写平台或本地元数据。
  - resolution 与 gate 分离；resolution 后重新实时读取并确认一致。
  - 现有 raw materialization 与 lifecycle 测试覆盖大小写 raw-key、empty result、单/多平台、缺副本、差异和零副作用。
- promotion_gate: B2 明确 projection、receipt、gate、resolution 的职责边界和测试矩阵，并将 I-* issue 写入 committed_issues。
- open_questions: []
- acceptance_reviews:
  - reviewer: lifecycle-entrypoint-review
  - mode: independent-readonly-review
  - summary: 确认 lifecycle 入口应复用共享 gate，`pr-merge-guarded` 仍有 GitHub 单平台关闭 PR 的残留边界。
  - verdict: pass
  - reviewer: adapter-contract-review
  - mode: independent-readonly-review
  - summary: 确认 adapter 保持 transport/registry，projection 与 reconciliation receipt 应作为纯模块拆出，避免继续扩大单体 adapter。
  - verdict: pass
- promoted_issue_id: I-20260725T030511Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20260725T030511Z/issues/I-20260725T030511Z-A.md
- milestone: M-20260725T030511Z-A
- session_refs: []
