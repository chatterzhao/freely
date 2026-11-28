---
candidate_id: C-20261113T141456Z-A
status: promoted
source_raw: raw-20261113T141456Z
created_at: 2026-11-13
milestone: M-20261113T141456Z-A
---

## C-20261113T141456Z-A: governance-only lane 接线
- candidate_format_version: v2
- title: 白名单单源 + GATE 1 指引 + batch 显式范围
- status: promoted
- design_verdict: 实现偏差
- anchor_refs:
  - governance-merge-gate:359-440
  - governance-merge-gate:1286-1298
  - cmd-batch.sh:5-30
  - config.toml:59-60
- decision_reason: 设计已存在但不可执行，导致以删门禁换流程通的次生事故。
- acceptance_criteria:
  - 白名单仅来自 config；硬编码默认被移除。
  - GATE 1 mismatch 诊断含 governance-only lane 与 FREELY_SKIP_IBM_GATE 指引。
  - batch 支持 --raw-key；全量提示治理 lane。
  - AT 断言两种 lane 边界与 bin/ 始终拒绝。
- promotion_gate: 四个缺口实证。
- next_action: B2 → RED → dev。
- revisit_trigger: 若 config 可缺省，再评估最小默认白名单。
- open_questions: []
- acceptance_reviews:
  - reviewer: main-agent
  - mode: B0-five-layer-audit
  - verdict: pass
- promoted_issue_id: I-20261113T141456Z-A
- promoted_issue_path: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141456Z/issues/I-20261113T141456Z-A.md
- milestone: M-20261113T141456Z-A
- session_refs: []
