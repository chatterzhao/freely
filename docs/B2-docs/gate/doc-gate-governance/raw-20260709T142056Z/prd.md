---
issue_id: I-20260709T142056Z-A
phase_state: done_b2_ibm
source_candidate: docs/B1-docs/raw-20260709T142056Z/candidates.md#C-20260709T142056Z-A
---

# PRD: doc gate 移除 3 个非 agent 注入文件检查
- issue_id: I-20260709T142056Z-A

## Goal
精简 `check_doc_gate_or_fail` 为只检查 agent 注入的 4 个核心治理文件。

## 实现
`freely:check_doc_gate_or_fail` — 从 required 数组删除 3 行 + 删除 pre-brainstorms 目录检查。
