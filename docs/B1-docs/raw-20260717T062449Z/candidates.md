---
candidate_id: C-20260717T062449Z-A
status: promoted
source_raw: raw-20260717T062449Z
created_at: 2026-07-17
milestone: M-20260717T062449Z-A
---

# Candidates

## C-20260717T062449Z-A: trace 打点拆相与 launch_observed 前移

- candidate_format_version: v2
- title: L041 前移 + L042 分支出口 OUT + cleanup 链出口声明
- status: promoted
- decision_reason: API 支持 in/out 拆相；三缺口均可在不动业务逻辑前提下闭合。见 brainstorms Option B
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - AC1: 真实 auto 周期中 launch_observed 与 launch_begin 时差 ≤10s（现状 94s 级）
  - AC2: 真实周期后最新 L042 OUT 的 to 为单值检查点（无候选集竖线）
  - AC3: 真实 stop 场景 cleanup 链 L090/L092 OUT ok=1 且 to 单值
  - AC4: 契约 §12 三条目更新为 resolved（含 L042 接力语义修订）
- promotion_gate: 三发射点与出口分支 file:line 勘察完毕；纯打点改动零业务逻辑
- open_questions: []
- acceptance_reviews:
  - reviewer: inline-code-verification
  - mode: inline
  - summary: in/out API 与六出口分支逐一核对
  - verdict: pass
- promoted_issue_id: I-20260717T062449Z-A
- promoted_issue_path: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T062449Z/issues/I-20260717T062449Z-A.md
- milestone: M-20260717T062449Z-A
- session_refs: []
