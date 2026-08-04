---
candidate_id: C-20260720T171146Z-A
status: absorbed
source_raw: raw-20260720T171146Z
created_at: 2026-08-04
milestone: M-20260720T171146Z-A
---

# Candidates

## C-20260720T171146Z-A: agent_working 单真源 fail-closed（continuation）

- candidate_format_version: v2
- title: 修复 agent_working 单真源迁移假绿与分配错绑
- status: absorbed
- decision_reason: 本 raw 是 I-20260720T120329Z 系列（agent-identity-single-truth）的 continuation，实现已在工位完成（fail-closed、next_free_and_assign、agent-id.env 停用），由父 issue I-20260720T120329Z-C 吸收。
- next_action: 无（continuation 已实现，合并后随父 issue 收口）
- revisit_trigger: 若 agent_working 再次出现假绿（测试直调 handler 而非真实 launch 链），需重开。
- acceptance_criteria:
  - DB/RPC 失败 fail-closed（不静默错绑 manager_01/worker_01）
  - 真实 launch 使用 next_free_and_assign 并按返回选择 slot
  - 生产路径零 agent-id.env 读写
  - 同 raw 重复分配幂等
- promotion_gate: 不适用（absorbed）
- open_questions: []
- absorbed_into: I-20260720T120329Z-C
- promoted_issue_path: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/issues/I-20260720T120329Z-C.md
- milestone: M-20260720T171146Z-A
- session_refs: []
