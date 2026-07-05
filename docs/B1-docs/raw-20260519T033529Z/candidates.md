# Candidates - 20260519T033529Z--handoff-json-corruption

### C-20260519T033529Z-A: legacy issue

- title: `Worker handoff JSON corruption — ACP stream contamination, missing handoff blocks, exit_kind alias`
- source_class: `bug_report`
- route_kind: `pre_brainstorm`
- phase_state: `done_pre_brainstorm`
- status: `dropped`
- priority: `P0`
- problem: `Worker handoff JSON 损坏（ACP stream 混入乱码）、部分 worker 不写 handoff 块、exit_kind "completed" 不被识别`
- why_now: `三项修复均已合并到 develop，issue 的实际生命周期已结束，仅需 B1 文档收口`
- decision_reason: `三项代码修复已通过独立 fix 分支合并到 develop：1) handoff.py ACP 事件剥离 + JSON 边界检测（61375ec0, fix/handoff-block-clean）；2) run-acp-prompt.py end_turn 换行修复（e0f5b8ee, fix/worker-completed-alias）；3) handoff.py completed→worker_done 别名（ff0e9441, fix/handoff-required-fields-align）。无剩余待实现项。`
- next_action: `关闭文档收口，无进一步操作`
- revisit_trigger: `N/A（已 dropped）`
- promotion_gate: `N/A（已 dropped）`
- accepted: `true`
- acceptance_criteria: []
- open_questions: []
- acceptance_reviews: []

### Closeout

- completed_at: `2026-05-19`
- closeout_evidence: `docs/B1-docs/raw-20260519T033529Z/issue.md (phase_state=dropped); 三项 fix commit 均在 develop 中可查`
- dropped_reason: `所有三项 handoff JSON 修复已通过独立 fix 分支合并到 develop，无需 I-* 跟踪`
