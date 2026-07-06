---
candidate_id: C-20260706T023422Z-A
status: promoted
source_raw: raw-20260706T023422Z
created_at: 2026-07-06
milestone: M-20260706T023422Z-A
---

## C-20260706T023422Z-A: docs-structure-refactor 遗漏补完

- candidate_format_version: v2
- title: docs-structure-refactor 遗漏补完 — 旧路径 + 缺 raw-{key} 层
- status: promoted
- decision_reason: 原始 refactor raw-20260705T155347Z 执行有遗漏。Phase 1 修生产代码（3 文件），Phase 2 用脚本从文档字段提取 raw key 修正 51 个 I-* 文件。Workspace skills 已干净无需改。
- next_action: B2 → RED → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - 生产代码中零 `docs/pre-brainstorms/` 引用
  - 所有 I-* 文件 `verification_artifact_dir` 含 `raw-{raw_key}/` 层（4 层格式）
  - 所有 I-* 文件 `pre_tests_path` 含 `raw-{raw_key}/` 层
  - git diff 无意外修改
- promotion_gate: grep 验证旧路径清零 + verification_artifact_dir 格式统一
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: Phase 1 修复 3 文件（freely-watchdog/governance-check/checkpoint-guard），Phase 2 脚本修正 51 文件。workspace skills 已干净。方案基于原始 refactor 设计文档。
  - verdict: pass
- promoted_issue_id: I-20260706T023422Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260706T023422Z/issues/I-20260706T023422Z-A.md
- milestone: M-20260706T023422Z-A
- session_refs: []
