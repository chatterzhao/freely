---
issue_id: I-20260720T120329Z-A
issue_path: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/issues/I-20260720T120329Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260720T120329Z-A
- issue_path: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/issues/I-20260720T120329Z-A.md

## Implementation Decision Note

- decision: 在 freely_db_manager.py 中新增 reviews 表（UNIQUE on raw_key+review_stage）+ record_review/get_reviews 两个 RPC handler；在 agent_working.py 中 agent_next_free 新增 raw_key 可选参数并切换到 next_free_and_assign 原子 RPC；移除 agent_assign 的 update_only/upsert_only 路径。总计 ~70 行改动，2 文件，零 shell 改动。

- why_this:
  1. reviews 表独立于 agent_working 表 — 两者生命周期解耦（agent_working 行可被 wt-close 删除，review 记录应持久保留用于审计和恢复）
  2. UNIQUE(raw_key, review_stage) 保证每个阶段只有一条 verdict，与 agent_working.py REVIEW_PHASES 的 5 阶段模型一致
  3. next_free_and_assign 已在 DB daemon 实现（L1489），只需在 agent_working.py 中切换调用
  4. 移除 upsert_only 消除 Reviewer 静默失败路径 — INSERT_OR_UPDATE 语义在行不存在时自动创建，更安全

- alternatives_considered:
  - 将 review 信息直接存入 agent_working 表新列 → 拒绝：agent_working 生命周期与 raw_key 绑定，wt-close 删除行时会丢失 review 记录；reviews 表独立持久化更合理
  - 在 agent_working.py 层面实现重试 + 原子分配 → 拒绝：Python 层面无法实现 DB 内原子性，必须用 DB 的 next_free_and_assign
  - Reviewer 保持 UPDATE_ONLY 但加阻塞等待 → 拒绝：增加复杂度（需重试/超时），INSERT_OR_UPDATE 语义更简洁

- boundary_non_goals:
  - 不改 agent_working 表的现有 schema
  - 不改 a2a_tasks 表
  - 不改 freely shell 脚本（C-B 负责）
  - 不加 reviewer 分配队列（C-C 负责）
  - 不实现 review 记录的定期清理

- residual_risk:
  - reviews 表无外键约束到 agent_working.raw_key — orphan review 可能残留（但使用 UNIQUE 约束避免了重复，孤立记录无害）
  - next_free_and_assign 的 raw_key 参数为空时 fallback 到旧的非原子路径 — 需调用方确保传入 raw_key
  - 移除 upsert_only 后 Reviewer 可能在未分配的 raw_key 上注册 → 创建含 reviewer_id 的行（其他列为空），与 Worker 后创建的完整行不冲突（UPSERT 合并）
