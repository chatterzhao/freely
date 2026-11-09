---
candidate_id: C-20261104T075910Z-A
status: promoted
source_raw: raw-20261104T075910Z
created_at: 2026-11-09
milestone: M-20261104T075910Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261104T075910Z-A: DB 读写边界收口到「只读 URI + 唯一写工厂 + boundary lint」

- candidate_format_version: v2
- title: 11 处只读连接改 `mode=ro`；新增 `db_write_gate`（`BEGIN IMMEDIATE` + 锁重试）；6 处短写者显式登记并登记进 State 契约；`bin/check-db-writers` 强制边界
- status: promoted
- decision_reason: issue 报告 6 处，实测 20 处；单写者不变量已被 6 个短写者共享，而 `_generate_chat_id` 的注释仍假设「Single-writer daemon」。不设边界则后续每轮都会新增直连。
- next_action: 建 AT-001（5 静态 + 1 守卫 + 5 行为）→ 改连接 → 写 State 契约 → lint → 并发/半提交断言。
- revisit_trigger: 若把只读 CLI 也迁到 daemon RPC（方向 A），需重新评估 daemon 不可用时的降级路径。
- acceptance_criteria:
  - RED：基线有 17 处未登记写连接（含 `wt-create` / `freely` / `governance-*`，issue 未列全）。
  - RED：基线直连可写（无 `query_only`），只读约束不存在。
  - GREEN：`bin/check-db-writers` 退出 0，20 处连接全部合规。
  - GREEN：AT 内置的边界推导（不依赖 lint 脚本）同样 0 违规。
  - GREEN：`connect_reader` 拒绝写；`write_tx` 并发两个写者都落库；读者看不到未提交事务的行。
  - GREEN：State 契约登记 `agent_decisions` / `delegation_tasks` / `discussion_events` 三个 store 与迁移路径。
- promotion_gate: AT-001 RED → GREEN + 相关回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 扫出 20 处直连（issue 只列 6）；按 40 行窗口分类 11 读 / 6 写；验证 `freely`、`wt-create`、`governance-*` 的遗漏；确认与 R19 正交。
  - verdict: pass
- promoted_issue_id: I-20261104T075910Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261104T075910Z/issues/I-20261104T075910Z-A.md
- milestone: M-20261104T075910Z-A
- session_refs: []
