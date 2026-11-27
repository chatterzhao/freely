---
candidate_id: C-20261126T120834Z-A
status: promoted
source_raw: raw-20261126T120834Z
created_at: 2026-11-26
milestone: M-20261126T120834Z-A
---

# Candidates

## C-20261126T120834Z-A: 退役门禁删除失效的 freshness check

- candidate_format_version: v2
- title: 删除 pretests-retirement-gate 自造 HEAD 相等判据
- status: promoted
- design_verdict: 实现偏差
- anchor_refs:
  - `quality/test-evidence.py:174`「Carry test evidence forward across metadata-equivalent commits」
  - `pretests-retirement-gate`「[pretests_stale] 测试工位有新提交但未重新跑测试」
- decision_reason: #4703 已建立三态判据，退役门禁是遗漏的消费者；复用它可避免无谓重跑且不降低强度。
- next_action: B2 物化 I-20261126T120834Z-A → RED → dev → GREEN → PR
- revisit_trigger: 若 #4703 的 validate 三态被收回，恢复独立判据并重新评审
- acceptance_criteria:
  - equivalent（元数据提交 + attest-meta）→ 退役门禁 rc=0
  - stale（真代码变更未重跑）→ rc=1，不放宽
  - not_tested → rc=1
  - 不修改 `test-evidence.py` 的判据与 HARD_EXCLUDED
- promotion_gate: B1 §0 判定为「实现偏差」，且证据显示 pr-create 与 wt-close 判定不一致
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus
  - mode: main-agent
  - summary: 评审确认退役门禁是 #4703 的遗漏消费者，删除自造判据不引入第二真源。
  - verdict: pass
- promoted_issue_id: I-20261126T120834Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/wt-close/raw-20261126T120834Z/issues/I-20261126T120834Z-A.md
- milestone: M-20261126T120834Z-A
- session_refs: []
