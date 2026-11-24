---
candidate_id: C-20261124T054241Z-A
status: promoted
source_raw: raw-20261124T054241Z
created_at: 2026-11-24
milestone: M-20261124T054241Z-A
---

## C-20261124T054241Z-A: session restore 退出码
- candidate_format_version: v2
- title: 恢复失败时非零退出 + 结构化汇总
- status: promoted
- design_verdict: 实现缺陷
- anchor_refs:
  - `agent_session_restore.py:73-80` 恒 return 0
  - 项目 fail-closed 原则
- decision_reason: Option B 保留汇总信息且如实反映失败。
- next_action: B2 物化；改 main()；AT 覆盖。
- revisit_trigger: 若外部调用者改为解析 JSON 而非退出码，重新评估。
- acceptance_criteria:
  - failed>0 → 非零退出
  - 汇总打印 resumed/failed/slot_unavailable 计数 + health
  - 全 resumed → 退出码 0、行为兼容
  - resume_persisted_sessions 返回结构不变
- promotion_gate: 改动面有 RED 设计；不改返回结构。
- open_questions: []
- acceptance_reviews:
  - reviewer: self-b1-audit
  - mode: structured-check
  - summary: B0 判定、三方案对比与锚点一致。
  - verdict: pass
- promoted_issue_id: I-20261124T054241Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261124T054241Z/issues/I-20261124T054241Z-A.md
- milestone: M-20261124T054241Z-A
- session_refs:
  - tool: codebuddy-agent
  - session_id: unavailable://current-session
  - jsonl_path: unavailable://current-session
  - role: worker
