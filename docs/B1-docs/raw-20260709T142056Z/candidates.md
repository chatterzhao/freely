---
candidate_id: C-20260709T142056Z-A
status: absorbed
source_raw: raw-20260709T142056Z
absorbed_into: I-20260709T142056Z-A
created_at: 2026-07-09
milestone: M-20260709T142056Z-A
---

## C-20260709T142056Z-A: doc gate 移除 3 个非 agent 注入文件检查

- candidate_format_version: v2
- title: doc gate 移除 3 个非 agent 注入文件检查
- status: absorbed
- decision_reason: README.md/INDEX.md/CONVERGENCE.md 不是 agent 注入治理文档，不应阻塞 daemon 启动。Agent 注入链路只有 CONSTITUTION/LAWS/PROJECT_INTENT/AGENTS.md 4 个文件。
- next_action: 进入 B2 设计实现
- revisit_trigger: N/A
- acceptance_criteria:
  - `check_doc_gate_or_fail` 只检查 4 个核心治理文件
  - daemon 启动不再被 doc gate 阻塞
  - CONSTITUTION/LAWS/PROJECT_INTENT/AGENTS.md 仍然被检查
- promotion_gate: B1 完成
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260709T142056Z-A
- promoted_issue_path: docs/B2-docs/gate/doc-gate-governance/raw-20260709T142056Z/issues/I-20260709T142056Z-A.md
- milestone: M-20260709T142056Z-A
- session_refs: []

## 改动计划
修改 `freely:check_doc_gate_or_fail`，从 required 数组中删除 3 行：
- `"docs/B1-docs/README.md"`
- `"docs/B1-docs/INDEX.md"`
- `"docs/B1-docs/CONVERGENCE.md"`
