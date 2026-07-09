---
issue_id: I-20260709T142056Z-A
issue_path: docs/B2-docs/gate/doc-gate-governance/raw-20260709T142056Z/issues/I-20260709T142056Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260709T142056Z-A
- issue_path: docs/B2-docs/gate/doc-gate-governance/raw-20260709T142056Z/issues/I-20260709T142056Z-A.md

## Implementation Decision Note

- decision: 从 `check_doc_gate_or_fail` 的 required 数组删除 3 个 B1-docs 文件引用 + 删除 `docs/pre-brainstorms` 目录检查
- why_this: 这 3 个文件不是 agent 注入治理文档。Agent 注入链路是 CLAUDE.md → AGENTS.md → CONSTITUTION/LAWS/PROJECT_INTENT。过程文档不应阻塞 daemon 启动。pre-brainstorms 是已废弃架构的空目录。
- alternatives_considered: 创建占位文件绕过检查 — 不解决架构混淆根本问题
- boundary_non_goals: 不清理 `pre_brainstorm_patrol_seed_snapshot_for_project` 死代码（独立 issue）
- residual_risk: 零
