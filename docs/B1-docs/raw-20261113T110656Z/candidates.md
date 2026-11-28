---
candidate_id: C-20261113T110656Z-A
status: promoted
source_raw: raw-20261113T110656Z
created_at: 2026-11-13
milestone: M-20261113T110656Z-A
---

## C-20261113T110656Z-A: 批次① sync+skills 投影化
- candidate_format_version: v2
- title: 三条 implementation-in-bin 迁移为 workspace/scripts 真源
- status: promoted
- design_verdict: 实现未完成
- anchor_refs:
  - docs/system/workspace/scripts/README.md（bin 投影层）
  - bin/check-bin-projection（shrink 规则）
  - raw-20261113T110656Z 待迁移清单批次①
- decision_reason: 按 raw 分批复用既有可执行入口，行为不变，债务逐批收缩。
- acceptance_criteria:
  - 三个 bin 入口 ≤8 行且 exec 到新真源。
  - 真源可执行且原有测试全绿（raw-issue-pull parity、deploy-skills sha256 语义）。
  - registry 三条条目删除，check-bin-projection 全绿。
  - 剩余 10 条另立 raw，不夹带。
- promotion_gate: batch① 边界明确且门禁可测。
- next_action: B2 → RED → dev。
- revisit_trigger: 若行为回归，回退并修正真源后重跑。
- open_questions: []
- acceptance_reviews:
  - reviewer: main-agent
  - mode: B0-five-layer-audit
  - verdict: pass
- promoted_issue_id: I-20261113T110656Z-A
- promoted_issue_path: docs/B2-docs/command-wrapper/implementation-projection/raw-20261113T110656Z/issues/I-20261113T110656Z-A.md
- milestone: M-20261113T110656Z-A
- session_refs: []
