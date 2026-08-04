---
candidate_id: C-20260724T024118Z-A
status: promoted
source_raw: raw-20260724T024118Z
created_at: 2026-08-04
milestone: M-20260724T024118Z-A
---

# Candidates

## C-20260724T024118Z-A: command-wrapper 元数据生命周期契约

- candidate_format_version: v2
- title: 定义并物化 command-wrapper 元数据生命周期契约
- status: promoted
- decision_reason: wrapper 与 verification 元数据无统一生命周期契约，导致 B1/B2 路由与证据歧义；Option B（契约文档 + 轻量校验测试）在防漂移与改动面间最优。
- next_action: B2 物化契约文档（`docs/system/workspace/command-wrapper-metadata-lifecycle.md`）与结构校验测试。
- revisit_trigger: 若 runtime 需要强制 wrapper 生命周期（Option C），需重开并纳入 runtime 变更范围。
- acceptance_criteria:
  - 契约文档声明五要素：owner、phase、freshness、rejection、证据绑定（B1/B2 与 RED/GREEN）
  - 契约文档位于 `docs/system/workspace/`（能力目录）
  - 校验测试断言五要素齐全且引用 wrapper 元数据字段
  - 不修改 runtime/freely 的 wrapper 行为
- promotion_gate: B2 产出契约文档草案与校验测试设计。
- open_questions: []
- acceptance_reviews:
  - reviewer: cli
  - mode: independent-readonly-review
  - summary: 边界（不碰 runtime 强制逻辑）与方案（文档 + 校验）与 raw issue 修复方案一致
  - verdict: pass
- promoted_issue_id: I-20260724T024118Z-A
- milestone: M-20260724T024118Z-A
- session_refs: []
