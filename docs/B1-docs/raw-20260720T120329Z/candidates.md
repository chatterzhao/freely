---
candidate_id: C-20260720T120329Z-A
status: promoted
source_raw: raw-20260720T120329Z
created_at: 2026-07-20
milestone: M-20260720T120329Z-A
---

## C-20260720T120329Z-A: DB 基础设施补齐 — review RPC + 原子分配 + Reviewer 注册修复

- candidate_format_version: v2
- title: DB 基础设施补齐 — review RPC + 原子分配 + Reviewer 注册修复
- status: promoted
- decision_reason: C-A 是 C-B 和 C-C 的阻塞依赖。先补齐 DB daemon 的 review RPC handler 缺口、切换到原子分配、修复 Reviewer 注册和 watchdog 协议，为上层消费者迁移提供稳定 DB 接口
- next_action: 进入 B2_IBM 物化 I-* issue 与设计产物
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `freely_db_manager.py`: 新增 `agent_working.record_review` RPC handler（持久化 reviewer verdict）
  - `freely_db_manager.py`: 新增 `agent_working.get_reviews` RPC handler（查询 review 记录）
  - `agent_working.py`: `agent_next_free` 改用 `next_free_and_assign` 原子 RPC（消除 TOCTOU）
  - `agent_working.py`: `acp_session_register` 对 reviewer 不再仅 UPDATE_ONLY，改为 INSERT_OR_UPDATE
  - `agent_working.py`: watchdog stale session 清理协议与 `agent_working.upsert` 参数结构对齐
  - 不改任何 shell 脚本或 scan 代码（纯 DB + Python 层）
- promotion_gate: 5 个修复点实现完成，review RPC 可写可读验证通过，原子分配并发安全
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: plan-subagent
  - summary: 审查 brainstorms 根因分析（D5/D6/D7/D8），确认 C-A scope 不越界（不改 shell/scan），DB handler 设计与 agent_working.py 调用签名对齐
  - verdict: pass
- promoted_issue_id: I-20260720T120329Z-A
- promoted_issue_path: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/issues/I-20260720T120329Z-A.md
- milestone: M-20260720T120329Z-A
- session_refs: []

---

## C-20260720T120329Z-B: 运行时 agent-id.env 退役 — 全部生产路径迁移到 agent_working

- candidate_format_version: v2
- title: 运行时 agent-id.env 退役 — 全部生产路径迁移到 agent_working
- status: blocked
- decision_reason: agent-id.env 在 9 处生产代码中仍被读写，形成双真源。C-A 补齐 DB 接口后，C-B 将所有消费者切换到 agent_working 唯一真源
- next_action: 等待 C-A merge 到 develop，然后进入 B2_IBM 物化 I-* issue
- revisit_trigger: C-A 合并后自动解锁；若 C-A 接口变更需重新对齐
- acceptance_criteria:
  - `_resolve_current_agent_id` (L340/L4323/L4832): 移除 agent-id.env fallback，agent_working 查询失败 → 显式错误退出（不默认 manager_01）
  - Worker assignment (L6014-6065): 移除 agent-id.env 双写，仅写 agent_working
  - A2A handoff (L13881): 改为查 agent_working，不读 agent-id.env
  - `_agent_working_shim` (L309-365): 移除 agent-id.env fallback
  - Discuss (L24606-24726): 改读/写 agent_working
  - Zombie cleanup (L12935-12947): 改用 agent_working 查询
  - `task-lifecycle-scan.py` (L886-910): 移除 agent-id.env fallback
  - `grep -r "agent-id\.env" docs/system/workspace/scripts/` 在生产代码中零命中（治理文档除外）
- promotion_gate: 9 处引用全部清零，`rg 'agent-id\.env'` 在生产脚本目录无输出
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260720T120329Z-B
- promoted_issue_path: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/issues/I-20260720T120329Z-B.md
- milestone: M-20260720T120329Z-A
- session_refs: []
- depends_on:
  - candidate: C-20260720T120329Z-A
  - reason: C-A 补齐的 review RPC、原子分配、Reviewer 注册修复是 C-B 消费者路径的前提

---

## C-20260720T120329Z-C: E2E 测试与回归门禁

- candidate_format_version: v2
- title: E2E 测试与回归门禁
- status: blocked
- decision_reason: C-A + C-B 完成代码迁移后，需要 E2E 测试证明真实 DB daemon 下三角色闭环可用，以及回归门禁防止 agent-id.env 重新侵入
- next_action: 等待 C-A 和 C-B merge 到 develop，然后进入 B2_IBM 物化 I-* issue
- revisit_trigger: C-A 和 C-B 合并后自动解锁
- acceptance_criteria:
  - E2E 测试: Manager 委派 Worker → Worker 注册到 agent_working → Worker 请求 Reviewer → Reviewer verdict 持久化到 agent_working → Worker retry 或 Manager 决策 → close 释放 agent_working
  - 覆盖 daemon 重启恢复（agent_working 状态持久化验证）
  - 覆盖 DB 不可用失败路径（RPC 调用失败时拒绝启动，不 fallback）
  - 回归门禁: CI 中 `rg 'agent-id\.env' docs/system/workspace/scripts/` 发现引用即失败
- promotion_gate: E2E 测试通过 + 回归门禁生效
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260720T120329Z-C
- promoted_issue_path: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/issues/I-20260720T120329Z-C.md
- milestone: M-20260720T120329Z-A
- session_refs: []
- depends_on:
  - candidate: C-20260720T120329Z-A
  - candidate: C-20260720T120329Z-B
  - reason: 需要 DB 接口完整 + agent-id.env 全部清零后才能编写真实 E2E 测试和门禁
