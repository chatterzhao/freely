---
candidate_id: C-20260719T192542Z-A / status: promoted / source_raw: raw-20260719T192542Z
created_at: '2026-07-19' / milestone: M-20260719T192542Z-A
---
## C-20260719T192542Z-A: 三agent prompt强化角色边界与协作
- candidate_format_version: v2 / title: Manager/Worker/Reviewer prompt模板强化
- status: promoted / decision_reason: 当前三个agent的prompt模板缺数据注入和边界约束。需重新设计
- acceptance_criteria: Manager看得到agent_working + 不写代码 + 委派完整workflow; Worker走完整B1→review循环; Reviewer有独立prompt
- promotion_gate: 三个prompt模板改好
- promoted_issue_id: I-20260719T192542Z-A
